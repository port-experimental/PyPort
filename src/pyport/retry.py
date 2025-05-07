"""
Retry utilities for the PyPort client library.

This module provides utilities for retrying failed API requests with
various backoff strategies and circuit breaker patterns.

Features:
- Multiple retry strategies (constant, linear, exponential, fibonacci)
- Configurable retry conditions based on exception types or status codes
- Automatic jitter to prevent thundering herd problems
- Circuit breaker pattern to prevent cascading failures
- Detailed retry statistics for monitoring and debugging
- Support for idempotent vs. non-idempotent HTTP methods
- Respect for Retry-After headers in rate limit responses

Example usage:

```python
# Basic usage with the PortClient
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    max_retries=5,
    retry_strategy="exponential",
    retry_jitter=True
)

# Custom retry configuration for a specific function
from src.pyport.retry import RetryConfig, RetryStrategy, with_retry

config = RetryConfig(
    max_retries=3,
    retry_delay=1.0,
    strategy=RetryStrategy.EXPONENTIAL,
    jitter=True
)

@with_retry(config=config)
def fetch_data(url, method="GET"):
    # Function that might fail and should be retried
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```
"""
import logging
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional, Set, Type, TypeVar, Union

from src.pyport.exceptions import PortApiError, PortRateLimitError

logger = logging.getLogger("pyport")

# Type for the function to retry
T = TypeVar('T')
RetryableFunc = Callable[..., T]
RetryCondition = Callable[[Exception], bool]


class RetryStrategy(Enum):
    """Enumeration of retry strategies."""
    CONSTANT = "constant"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    FIBONACCI = "fibonacci"


@dataclass
class RetryStats:
    """Statistics about retry attempts."""
    attempts: int = 0
    successes: int = 0
    failures: int = 0
    total_retry_time: float = 0.0
    last_error: Optional[Exception] = None
    errors: List[Exception] = field(default_factory=list)
    retry_times: List[float] = field(default_factory=list)

    def record_attempt(self, success: bool, error: Optional[Exception] = None, retry_time: float = 0.0) -> None:
        """Record an attempt."""
        self.attempts += 1
        if success:
            self.successes += 1
        else:
            self.failures += 1
            if error:
                self.last_error = error
                self.errors.append(error)
        self.total_retry_time += retry_time
        self.retry_times.append(retry_time)

    def reset(self) -> None:
        """Reset all statistics."""
        self.attempts = 0
        self.successes = 0
        self.failures = 0
        self.total_retry_time = 0.0
        self.last_error = None
        self.errors = []
        self.retry_times = []

    def __str__(self) -> str:
        """Return a string representation of the statistics."""
        return (
            f"RetryStats(attempts={self.attempts}, successes={self.successes}, "
            f"failures={self.failures}, total_retry_time={self.total_retry_time:.2f}s)"
        )


@dataclass
class CircuitBreakerState:
    """State of a circuit breaker."""
    # Configuration
    failure_threshold: int = 5       # Number of consecutive failures before opening the circuit
    reset_timeout: float = 60.0      # Time in seconds before the circuit resets (1 minute)
    half_open_timeout: float = 30.0  # Time in seconds before allowing a test request (30 seconds)

    # State
    failures: int = 0
    last_failure_time: float = 0.0
    is_open: bool = False

    def record_failure(self) -> None:
        """Record a failure and potentially open the circuit."""
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.is_open = True
            logger.warning(
                f"Circuit breaker opened after {self.failures} consecutive failures. "
                f"Will reset after {self.reset_timeout} seconds."
            )

    def record_success(self) -> None:
        """Record a success and reset the failure count."""
        self.failures = 0
        self.is_open = False

    def can_attempt(self) -> bool:
        """Check if a request can be attempted."""
        if not self.is_open:
            return True

        # Check if the reset timeout has elapsed
        elapsed = time.time() - self.last_failure_time
        if elapsed >= self.reset_timeout:
            logger.info(
                f"Circuit breaker reset after {elapsed:.2f} seconds. "
                f"Allowing new requests."
            )
            self.is_open = False
            self.failures = 0
            return True

        # Check if we should allow a half-open test
        if elapsed >= self.half_open_timeout:
            logger.info(
                f"Circuit breaker in half-open state after {elapsed:.2f} seconds. "
                f"Allowing a test request."
            )
            return True

        return False

    def __str__(self) -> str:
        """Return a string representation of the circuit breaker state."""
        state = "OPEN" if self.is_open else "CLOSED"
        return (
            f"CircuitBreaker({state}, failures={self.failures}, "
            f"threshold={self.failure_threshold})"
        )


class RetryConfig:
    """
    Configuration for retry behavior.

    This class encapsulates all the configuration options for retry behavior,
    including retry strategies, conditions, circuit breaker, and statistics.

    Attributes:
        max_retries: Maximum number of retry attempts.
        retry_delay: Initial delay between retries in seconds.
        max_delay: Maximum delay between retries in seconds.
        strategy: Retry strategy to use (CONSTANT, LINEAR, EXPONENTIAL, FIBONACCI).
        jitter: Whether to add random jitter to retry delays.
        jitter_factor: Factor to use for jitter (0.0-1.0).
        retry_on: Exception types or function that determines if an exception should be retried.
        retry_status_codes: HTTP status codes that should trigger retries.
        idempotent_methods: HTTP methods that are safe to retry.
        circuit_breaker: Circuit breaker state to prevent cascading failures.
        retry_hook: Function to call before each retry attempt.
        stats: Statistics about retry attempts.

    Examples:
        >>> # Basic configuration with exponential backoff
        >>> config = RetryConfig(
        ...     max_retries=3,
        ...     retry_delay=1.0,
        ...     strategy=RetryStrategy.EXPONENTIAL
        ... )
        >>>
        >>> # Configuration with custom retry conditions
        >>> config = RetryConfig(
        ...     max_retries=5,
        ...     retry_status_codes={429, 500, 503},
        ...     retry_on=PortTimeoutError
        ... )
        >>>
        >>> # Configuration with a retry hook for logging
        >>> def log_retry(error, attempt, delay):
        ...     print(f"Retry {attempt} after {error} with delay {delay}s")
        >>>
        >>> config = RetryConfig(
        ...     max_retries=3,
        ...     retry_hook=log_retry
        ... )
    """

    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        max_delay: float = 60.0,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        jitter: bool = True,
        jitter_factor: float = 0.1,
        retry_on: Optional[Union[Type[Exception], Set[Type[Exception]], RetryCondition]] = None,
        retry_status_codes: Optional[Set[int]] = None,
        idempotent_methods: Optional[Set[str]] = None,
        circuit_breaker: Optional[CircuitBreakerState] = None,
        retry_hook: Optional[Callable[[Exception, int, float], None]] = None
    ):
        """
        Initialize retry configuration.

        Args:
            max_retries: Maximum number of retry attempts.
            retry_delay: Initial delay between retries in seconds (e.g., 1.0 = 1 second).
            max_delay: Maximum delay between retries in seconds (e.g., 60.0 = 1 minute).
            strategy: Retry strategy to use.
            jitter: Whether to add jitter to retry delays.
            jitter_factor: Factor to use for jitter (0.0-1.0).
            retry_on: Exception types or a function that returns True if the exception should be retried.
            retry_status_codes: HTTP status codes that should be retried.
            idempotent_methods: HTTP methods that are idempotent and safe to retry.
            circuit_breaker: Circuit breaker state to use.
            retry_hook: Function to call before each retry.
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_delay = max_delay
        self.strategy = strategy
        self.jitter = jitter
        self.jitter_factor = jitter_factor

        # Set up retry conditions
        self.retry_on = retry_on
        self.retry_status_codes = retry_status_codes or {429, 500, 502, 503, 504}
        self.idempotent_methods = idempotent_methods or {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}

        # Set up circuit breaker
        self.circuit_breaker = circuit_breaker or CircuitBreakerState()

        # Set up hooks
        self.retry_hook = retry_hook

        # Statistics
        self.stats = RetryStats()

    def should_retry(self, exception: Exception, method: str) -> bool:
        """
        Determine if a request should be retried based on the exception and method.

        Args:
            exception: The exception that occurred.
            method: The HTTP method used for the request.

        Returns:
            True if the request should be retried, False otherwise.
        """
        # Check if the method is idempotent
        if method.upper() not in self.idempotent_methods:
            logger.warning(f"Method {method} is not idempotent. Not retrying.")
            return False

        # Check if the circuit breaker allows attempts
        if not self.circuit_breaker.can_attempt():
            logger.warning("Circuit breaker is open. Not retrying.")
            return False

        # Check if the exception is retryable based on custom condition
        if self.retry_on is not None:
            if callable(self.retry_on):
                return self.retry_on(exception)
            elif isinstance(self.retry_on, set):
                return any(isinstance(exception, exc_type) for exc_type in self.retry_on)
            else:
                return isinstance(exception, self.retry_on)

        # Check if the exception is a PortApiError with a status code
        if isinstance(exception, PortApiError) and exception.status_code:
            return exception.status_code in self.retry_status_codes

        # Default to checking if the exception is transient
        if isinstance(exception, PortApiError):
            return exception.is_transient()

        return False

    def get_retry_delay(self, attempt: int, exception: Exception) -> float:
        """
        Calculate the delay before the next retry attempt.

        Args:
            attempt: The current attempt number (0-based).
            exception: The exception that occurred.

        Returns:
            The delay in seconds before the next retry.
        """
        # Check for rate limit with Retry-After header
        if isinstance(exception, PortRateLimitError) and exception.retry_after:
            delay = exception.retry_after
            logger.info(f"Using Retry-After header: {delay} seconds")
            return delay

        # Calculate delay based on strategy
        if self.strategy == RetryStrategy.CONSTANT:
            delay = self.retry_delay
        elif self.strategy == RetryStrategy.LINEAR:
            delay = self.retry_delay * (attempt + 1)
        elif self.strategy == RetryStrategy.EXPONENTIAL:
            delay = self.retry_delay * (2 ** attempt)
        elif self.strategy == RetryStrategy.FIBONACCI:
            # Calculate Fibonacci number (1, 1, 2, 3, 5, 8, ...)
            a, b = 1, 1
            for _ in range(attempt):
                a, b = b, a + b
            delay = self.retry_delay * a
        else:
            delay = self.retry_delay

        # Apply maximum delay
        delay = min(delay, self.max_delay)

        # Add jitter if enabled
        if self.jitter:
            jitter_amount = delay * self.jitter_factor
            delay += random.uniform(-jitter_amount, jitter_amount)
            delay = max(0.1, delay)  # Ensure delay is at least 0.1 seconds

        return delay


def with_retry(
    func: RetryableFunc[T],
    config: Optional[RetryConfig] = None,
    **retry_kwargs
) -> RetryableFunc[T]:
    """
    Decorator to add retry logic to a function.

    This decorator wraps a function with retry logic based on the provided
    configuration. When the wrapped function raises an exception that matches
    the retry conditions, it will be called again after a delay determined by
    the retry strategy.

    The decorator can be used in two ways:

    1. As a simple decorator with default settings:
       ```python
       @with_retry
       def my_function():
           # Function that might fail
           pass
       ```

    2. With a custom configuration:
       ```python
       @with_retry(config=RetryConfig(max_retries=5))
       def my_function():
           # Function that might fail
           pass
       ```

    3. With custom configuration parameters:
       ```python
       @with_retry(max_retries=5, retry_delay=0.5)
       def my_function():
           # Function that might fail
           pass
       ```

    For HTTP requests, the function should accept a 'method' parameter that
    indicates the HTTP method being used. This is used to determine if the
    request is idempotent and safe to retry.

    Args:
        func: The function to retry. This function will be called repeatedly
            until it succeeds or the retry conditions are exhausted.
        config: Retry configuration to use. If None, a new configuration will
            be created using the retry_kwargs.
        **retry_kwargs: Additional keyword arguments to pass to RetryConfig
            if config is None. These can include max_retries, retry_delay,
            strategy, etc.

    Returns:
        A wrapped function that will retry on failure according to the
        specified configuration.

    Examples:
        >>> # Basic usage
        >>> @with_retry
        ... def fetch_data(url, method="GET"):
        ...     response = requests.get(url)
        ...     response.raise_for_status()
        ...     return response.json()
        >>>
        >>> # With custom configuration
        >>> @with_retry(max_retries=5, retry_delay=0.5)
        ... def fetch_data(url, method="GET"):
        ...     response = requests.get(url)
        ...     response.raise_for_status()
        ...     return response.json()
        >>>
        >>> # Using the decorator programmatically
        >>> def fetch_data(url):
        ...     response = requests.get(url)
        ...     response.raise_for_status()
        ...     return response.json()
        >>>
        >>> retry_fetch = with_retry(fetch_data, max_retries=3)
        >>> data = retry_fetch("https://api.example.com/data", method="GET")
    """
    # Create a retry configuration if one wasn't provided
    if config is None:
        config = RetryConfig(**retry_kwargs)

    def wrapper(*args, **kwargs) -> T:
        method = kwargs.get('method', 'GET')  # Default to GET if not specified

        # Check if the circuit breaker is open before making any attempts
        if not config.circuit_breaker.can_attempt():
            logger.warning("Circuit breaker is open. Not attempting the request.")
            # Create a dummy exception to raise
            if 'exception' in kwargs:
                # If an exception was provided in kwargs, use it
                exception = kwargs['exception']
            else:
                # Otherwise create a generic PortApiError
                exception = PortApiError("Request not attempted due to open circuit breaker")
            raise exception

        for attempt in range(config.max_retries + 1):
            try:
                # Attempt the function call
                result = func(*args, **kwargs)

                # Record success in circuit breaker and stats
                config.circuit_breaker.record_success()
                config.stats.record_attempt(success=True)

                return result

            except Exception as e:
                # Record the attempt in stats
                config.stats.record_attempt(success=False, error=e)

                # Check if we should retry
                if attempt < config.max_retries and config.should_retry(e, method):
                    # Calculate delay
                    delay = config.get_retry_delay(attempt, e)

                    # Call retry hook if provided
                    if config.retry_hook:
                        config.retry_hook(e, attempt, delay)

                    # Log the retry
                    logger.warning(
                        f"Attempt {attempt + 1}/{config.max_retries} failed with {e.__class__.__name__}. "
                        f"Retrying in {delay:.2f} seconds."
                    )

                    # Wait before retrying
                    time.sleep(delay)

                    # Record the retry time in stats
                    config.stats.retry_times[-1] = delay
                else:
                    # Record failure in circuit breaker
                    config.circuit_breaker.record_failure()

                    # If we're out of retries or shouldn't retry, re-raise the exception
                    logger.error(
                        f"All {attempt + 1} attempts failed. Last error: {e}"
                    )
                    raise

    return wrapper


def is_idempotent_method(method: str) -> bool:
    """
    Check if an HTTP method is idempotent.

    Args:
        method: The HTTP method to check.

    Returns:
        True if the method is idempotent, False otherwise.
    """
    return method.upper() in {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}


def create_retry_condition(
    exception_types: Optional[Union[Type[Exception], List[Type[Exception]]]] = None,
    status_codes: Optional[List[int]] = None,
    transient_only: bool = True
) -> RetryCondition:
    """
    Create a retry condition function.

    Args:
        exception_types: Exception types to retry.
        status_codes: HTTP status codes to retry.
        transient_only: Whether to only retry transient errors.

    Returns:
        A function that returns True if the exception should be retried.
    """
    def condition(exception: Exception) -> bool:
        # If exception_types is specified, check if the exception is of one of those types
        if exception_types:
            if not isinstance(exception_types, list):
                types_list = [exception_types]
            else:
                types_list = exception_types

            if not any(isinstance(exception, exc_type) for exc_type in types_list):
                return False

        # If status_codes is specified, check if the exception has one of those status codes
        if status_codes and isinstance(exception, PortApiError) and exception.status_code:
            return exception.status_code in status_codes

        # If transient_only is True, check if the exception is transient
        if transient_only and isinstance(exception, PortApiError):
            return exception.is_transient()

        # If we've made it this far with exception_types specified, return True
        if exception_types:
            return True

        # Default case
        return False

    return condition
