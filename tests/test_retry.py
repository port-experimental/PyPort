"""
Tests for the retry module.
"""
import time
import unittest
from unittest.mock import MagicMock, patch

import requests

from pyport.exceptions import (
    PortApiError,
    PortRateLimitError,
    PortServerError,
    PortTimeoutError
)
from pyport.retry import (
    CircuitBreakerState,
    RetryConfig,
    RetryStats,
    RetryStrategy,
    create_retry_condition,
    is_idempotent_method,
    with_retry
)


class TestRetryConfig(unittest.TestCase):
    """Tests for the RetryConfig class."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        config = RetryConfig()
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.retry_delay, 1.0)
        self.assertEqual(config.max_delay, 60.0)
        self.assertEqual(config.strategy, RetryStrategy.EXPONENTIAL)
        self.assertTrue(config.jitter)
        self.assertEqual(config.jitter_factor, 0.1)
        self.assertIsNone(config.retry_on)
        self.assertEqual(config.retry_status_codes, {429, 500, 502, 503, 504})
        self.assertEqual(config.idempotent_methods, {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"})
        self.assertIsNotNone(config.circuit_breaker)
        self.assertIsNone(config.retry_hook)
        self.assertIsInstance(config.stats, RetryStats)

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        retry_hook = MagicMock()
        config = RetryConfig(
            max_retries=5,
            retry_delay=2.0,
            max_delay=30.0,
            strategy=RetryStrategy.LINEAR,
            jitter=False,
            jitter_factor=0.2,
            retry_on=PortApiError,
            retry_status_codes={500, 502},
            idempotent_methods={"GET", "HEAD"},
            circuit_breaker=CircuitBreakerState(failure_threshold=10),
            retry_hook=retry_hook
        )
        self.assertEqual(config.max_retries, 5)
        self.assertEqual(config.retry_delay, 2.0)
        self.assertEqual(config.max_delay, 30.0)
        self.assertEqual(config.strategy, RetryStrategy.LINEAR)
        self.assertFalse(config.jitter)
        self.assertEqual(config.jitter_factor, 0.2)
        self.assertEqual(config.retry_on, PortApiError)
        self.assertEqual(config.retry_status_codes, {500, 502})
        self.assertEqual(config.idempotent_methods, {"GET", "HEAD"})
        self.assertEqual(config.circuit_breaker.failure_threshold, 10)
        self.assertEqual(config.retry_hook, retry_hook)

    def test_should_retry_with_transient_error(self):
        """Test should_retry with a transient error."""
        config = RetryConfig()
        error = PortServerError("Server error", status_code=500)
        self.assertTrue(config.should_retry(error, "GET"))

    def test_should_retry_with_non_transient_error(self):
        """Test should_retry with a non-transient error."""
        config = RetryConfig()
        error = PortApiError("API error", status_code=400)
        self.assertFalse(config.should_retry(error, "GET"))

    def test_should_retry_with_non_idempotent_method(self):
        """Test should_retry with a non-idempotent method."""
        config = RetryConfig()
        error = PortServerError("Server error", status_code=500)
        self.assertFalse(config.should_retry(error, "POST"))

    def test_should_retry_with_custom_retry_on(self):
        """Test should_retry with a custom retry_on condition."""
        # Create a custom retry condition function
        def is_timeout_error(error):
            return isinstance(error, PortTimeoutError)

        config = RetryConfig(retry_on=is_timeout_error)
        timeout_error = PortTimeoutError("Timeout")
        server_error = PortServerError("Server error", status_code=500)
        self.assertTrue(config.should_retry(timeout_error, "GET"))
        self.assertFalse(config.should_retry(server_error, "GET"))

    def test_should_retry_with_custom_retry_on_set(self):
        """Test should_retry with a custom retry_on set of exceptions."""
        config = RetryConfig(retry_on={PortTimeoutError, PortRateLimitError})
        timeout_error = PortTimeoutError("Timeout")
        rate_limit_error = PortRateLimitError("Rate limit", status_code=429)
        server_error = PortServerError("Server error", status_code=500)
        self.assertTrue(config.should_retry(timeout_error, "GET"))
        self.assertTrue(config.should_retry(rate_limit_error, "GET"))
        self.assertFalse(config.should_retry(server_error, "GET"))

    def test_should_retry_with_custom_retry_on_function(self):
        """Test should_retry with a custom retry_on function."""
        def custom_condition(error):
            return isinstance(error, PortApiError) and error.status_code == 418

        config = RetryConfig(retry_on=custom_condition)
        teapot_error = PortApiError("I'm a teapot", status_code=418)
        server_error = PortServerError("Server error", status_code=500)
        self.assertTrue(config.should_retry(teapot_error, "GET"))
        self.assertFalse(config.should_retry(server_error, "GET"))

    def test_should_retry_with_circuit_breaker_open(self):
        """Test should_retry with an open circuit breaker."""
        circuit_breaker = CircuitBreakerState(failure_threshold=1)
        circuit_breaker.record_failure()  # Open the circuit
        config = RetryConfig(circuit_breaker=circuit_breaker)
        error = PortServerError("Server error", status_code=500)
        self.assertFalse(config.should_retry(error, "GET"))

    def test_get_retry_delay_with_rate_limit(self):
        """Test get_retry_delay with a rate limit error."""
        config = RetryConfig()
        error = PortRateLimitError("Rate limit", status_code=429, retry_after=10)
        delay = config.get_retry_delay(0, error)
        self.assertEqual(delay, 10)

    def test_get_retry_delay_with_constant_strategy(self):
        """Test get_retry_delay with constant strategy."""
        config = RetryConfig(strategy=RetryStrategy.CONSTANT, retry_delay=2.0, jitter=False)
        error = PortServerError("Server error", status_code=500)
        delay = config.get_retry_delay(0, error)
        self.assertEqual(delay, 2.0)
        delay = config.get_retry_delay(1, error)
        self.assertEqual(delay, 2.0)
        delay = config.get_retry_delay(2, error)
        self.assertEqual(delay, 2.0)

    def test_get_retry_delay_with_linear_strategy(self):
        """Test get_retry_delay with linear strategy."""
        config = RetryConfig(strategy=RetryStrategy.LINEAR, retry_delay=2.0, jitter=False)
        error = PortServerError("Server error", status_code=500)
        delay = config.get_retry_delay(0, error)
        self.assertEqual(delay, 2.0)
        delay = config.get_retry_delay(1, error)
        self.assertEqual(delay, 4.0)
        delay = config.get_retry_delay(2, error)
        self.assertEqual(delay, 6.0)

    def test_get_retry_delay_with_exponential_strategy(self):
        """Test get_retry_delay with exponential strategy."""
        config = RetryConfig(strategy=RetryStrategy.EXPONENTIAL, retry_delay=2.0, jitter=False)
        error = PortServerError("Server error", status_code=500)
        delay = config.get_retry_delay(0, error)
        self.assertEqual(delay, 2.0)
        delay = config.get_retry_delay(1, error)
        self.assertEqual(delay, 4.0)
        delay = config.get_retry_delay(2, error)
        self.assertEqual(delay, 8.0)

    def test_get_retry_delay_with_fibonacci_strategy(self):
        """Test get_retry_delay with fibonacci strategy."""
        config = RetryConfig(strategy=RetryStrategy.FIBONACCI, retry_delay=1.0, jitter=False)
        error = PortServerError("Server error", status_code=500)
        delay = config.get_retry_delay(0, error)
        self.assertEqual(delay, 1.0)
        delay = config.get_retry_delay(1, error)
        self.assertEqual(delay, 1.0)
        delay = config.get_retry_delay(2, error)
        self.assertEqual(delay, 2.0)
        delay = config.get_retry_delay(3, error)
        self.assertEqual(delay, 3.0)
        delay = config.get_retry_delay(4, error)
        self.assertEqual(delay, 5.0)

    def test_get_retry_delay_with_max_delay(self):
        """Test get_retry_delay with max_delay."""
        config = RetryConfig(
            strategy=RetryStrategy.EXPONENTIAL,
            retry_delay=2.0,
            max_delay=10.0,
            jitter=False
        )
        error = PortServerError("Server error", status_code=500)
        delay = config.get_retry_delay(0, error)
        self.assertEqual(delay, 2.0)
        delay = config.get_retry_delay(1, error)
        self.assertEqual(delay, 4.0)
        delay = config.get_retry_delay(2, error)
        self.assertEqual(delay, 8.0)
        delay = config.get_retry_delay(3, error)
        self.assertEqual(delay, 10.0)  # Capped at max_delay

    def test_get_retry_delay_with_jitter(self):
        """Test get_retry_delay with jitter."""
        config = RetryConfig(
            strategy=RetryStrategy.CONSTANT,
            retry_delay=10.0,
            jitter=True,
            jitter_factor=0.5
        )
        error = PortServerError("Server error", status_code=500)
        delay = config.get_retry_delay(0, error)
        # With jitter_factor=0.5, delay should be between 5.0 and 15.0
        self.assertGreaterEqual(delay, 5.0)
        self.assertLessEqual(delay, 15.0)


class TestCircuitBreaker(unittest.TestCase):
    """Tests for the CircuitBreakerState class."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        cb = CircuitBreakerState()
        self.assertEqual(cb.failure_threshold, 5)
        self.assertEqual(cb.reset_timeout, 60.0)
        self.assertEqual(cb.half_open_timeout, 30.0)
        self.assertEqual(cb.failures, 0)
        self.assertEqual(cb.last_failure_time, 0.0)
        self.assertFalse(cb.is_open)

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        cb = CircuitBreakerState(
            failure_threshold=10,
            reset_timeout=120.0,
            half_open_timeout=60.0
        )
        self.assertEqual(cb.failure_threshold, 10)
        self.assertEqual(cb.reset_timeout, 120.0)
        self.assertEqual(cb.half_open_timeout, 60.0)

    def test_record_failure(self):
        """Test record_failure method."""
        cb = CircuitBreakerState(failure_threshold=2)
        self.assertEqual(cb.failures, 0)
        self.assertFalse(cb.is_open)

        cb.record_failure()
        self.assertEqual(cb.failures, 1)
        self.assertFalse(cb.is_open)

        cb.record_failure()
        self.assertEqual(cb.failures, 2)
        self.assertTrue(cb.is_open)

    def test_record_success(self):
        """Test record_success method."""
        cb = CircuitBreakerState(failure_threshold=2)
        cb.record_failure()
        cb.record_failure()
        self.assertEqual(cb.failures, 2)
        self.assertTrue(cb.is_open)

        cb.record_success()
        self.assertEqual(cb.failures, 0)
        self.assertFalse(cb.is_open)

    def test_can_attempt_with_closed_circuit(self):
        """Test can_attempt with a closed circuit."""
        cb = CircuitBreakerState()
        self.assertTrue(cb.can_attempt())

    def test_can_attempt_with_open_circuit(self):
        """Test can_attempt with an open circuit."""
        cb = CircuitBreakerState(failure_threshold=1, reset_timeout=0.1)
        cb.record_failure()
        self.assertFalse(cb.can_attempt())

        # Wait for reset timeout
        time.sleep(0.2)
        self.assertTrue(cb.can_attempt())

    def test_can_attempt_with_half_open_circuit(self):
        """Test can_attempt with a half-open circuit."""
        cb = CircuitBreakerState(
            failure_threshold=1,
            reset_timeout=1.0,
            half_open_timeout=0.1
        )
        cb.record_failure()
        self.assertFalse(cb.can_attempt())

        # Wait for half-open timeout
        time.sleep(0.2)
        self.assertTrue(cb.can_attempt())


class TestRetryStats(unittest.TestCase):
    """Tests for the RetryStats class."""

    def test_init(self):
        """Test initialization."""
        stats = RetryStats()
        self.assertEqual(stats.attempts, 0)
        self.assertEqual(stats.successes, 0)
        self.assertEqual(stats.failures, 0)
        self.assertEqual(stats.total_retry_time, 0.0)
        self.assertIsNone(stats.last_error)
        self.assertEqual(stats.errors, [])
        self.assertEqual(stats.retry_times, [])

    def test_record_attempt_success(self):
        """Test record_attempt with a successful attempt."""
        stats = RetryStats()
        stats.record_attempt(success=True, retry_time=1.0)
        self.assertEqual(stats.attempts, 1)
        self.assertEqual(stats.successes, 1)
        self.assertEqual(stats.failures, 0)
        self.assertEqual(stats.total_retry_time, 1.0)
        self.assertEqual(stats.retry_times, [1.0])

    def test_record_attempt_failure(self):
        """Test record_attempt with a failed attempt."""
        stats = RetryStats()
        error = Exception("Test error")
        stats.record_attempt(success=False, error=error, retry_time=2.0)
        self.assertEqual(stats.attempts, 1)
        self.assertEqual(stats.successes, 0)
        self.assertEqual(stats.failures, 1)
        self.assertEqual(stats.total_retry_time, 2.0)
        self.assertEqual(stats.last_error, error)
        self.assertEqual(stats.errors, [error])
        self.assertEqual(stats.retry_times, [2.0])

    def test_reset(self):
        """Test reset method."""
        stats = RetryStats()
        error = Exception("Test error")
        stats.record_attempt(success=False, error=error, retry_time=2.0)
        stats.reset()
        self.assertEqual(stats.attempts, 0)
        self.assertEqual(stats.successes, 0)
        self.assertEqual(stats.failures, 0)
        self.assertEqual(stats.total_retry_time, 0.0)
        self.assertIsNone(stats.last_error)
        self.assertEqual(stats.errors, [])
        self.assertEqual(stats.retry_times, [])


class TestWithRetry(unittest.TestCase):
    """Tests for the with_retry decorator."""

    def test_with_retry_success_first_attempt(self):
        """Test with_retry with a successful first attempt."""
        mock_func = MagicMock(return_value="success")
        decorated_func = with_retry(mock_func)
        result = decorated_func()
        self.assertEqual(result, "success")
        mock_func.assert_called_once()

    def test_with_retry_success_after_retry(self):
        """Test with_retry with a successful retry."""
        mock_func = MagicMock(side_effect=[PortServerError("Server error", status_code=500), "success"])
        config = RetryConfig(retry_delay=0.1, jitter=False)
        decorated_func = with_retry(mock_func, config=config)
        result = decorated_func(method="GET")
        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 2)
        self.assertEqual(config.stats.attempts, 2)
        self.assertEqual(config.stats.successes, 1)
        self.assertEqual(config.stats.failures, 1)

    def test_with_retry_max_retries_exceeded(self):
        """Test with_retry with max retries exceeded."""
        error = PortServerError("Server error", status_code=500)
        mock_func = MagicMock(side_effect=[error, error, error, error])
        config = RetryConfig(max_retries=3, retry_delay=0.1, jitter=False)
        decorated_func = with_retry(mock_func, config=config)
        with self.assertRaises(PortServerError):
            decorated_func(method="GET")
        self.assertEqual(mock_func.call_count, 4)  # Initial attempt + 3 retries
        self.assertEqual(config.stats.attempts, 4)
        self.assertEqual(config.stats.successes, 0)
        self.assertEqual(config.stats.failures, 4)

    def test_with_retry_non_retryable_error(self):
        """Test with_retry with a non-retryable error."""
        error = PortApiError("API error", status_code=400)
        mock_func = MagicMock(side_effect=error)
        config = RetryConfig(retry_delay=0.1, jitter=False)
        decorated_func = with_retry(mock_func, config=config)
        with self.assertRaises(PortApiError):
            decorated_func(method="GET")
        mock_func.assert_called_once()
        self.assertEqual(config.stats.attempts, 1)
        self.assertEqual(config.stats.successes, 0)
        self.assertEqual(config.stats.failures, 1)

    def test_with_retry_non_idempotent_method(self):
        """Test with_retry with a non-idempotent method."""
        error = PortServerError("Server error", status_code=500)
        mock_func = MagicMock(side_effect=error)
        config = RetryConfig(retry_delay=0.1, jitter=False)
        decorated_func = with_retry(mock_func, config=config)
        with self.assertRaises(PortServerError):
            decorated_func(method="POST")
        mock_func.assert_called_once()
        self.assertEqual(config.stats.attempts, 1)
        self.assertEqual(config.stats.successes, 0)
        self.assertEqual(config.stats.failures, 1)

    def test_with_retry_circuit_breaker(self):
        """Test with_retry with a circuit breaker."""
        # Create a mock function that always raises an error
        error = PortServerError("Server error", status_code=500)
        mock_func = MagicMock(side_effect=error)

        # Create a circuit breaker that opens after the first failure
        circuit_breaker = CircuitBreakerState(failure_threshold=1)

        # Manually open the circuit breaker before the test
        circuit_breaker.record_failure()
        self.assertTrue(circuit_breaker.is_open)

        # Create a retry config with the open circuit breaker
        config = RetryConfig(
            max_retries=3,
            retry_delay=0.1,
            jitter=False,
            circuit_breaker=circuit_breaker
        )

        # Create the decorated function
        decorated_func = with_retry(mock_func, config=config)

        # Call should fail immediately because the circuit is already open
        with self.assertRaises(PortServerError):
            decorated_func(method="GET", exception=error)

        # The function should not be called at all because the circuit is open
        mock_func.assert_not_called()

    def test_with_retry_hook(self):
        """Test with_retry with a retry hook."""
        error = PortServerError("Server error", status_code=500)
        mock_func = MagicMock(side_effect=[error, "success"])
        mock_hook = MagicMock()
        config = RetryConfig(
            retry_delay=0.1,
            jitter=False,
            retry_hook=mock_hook
        )
        decorated_func = with_retry(mock_func, config=config)
        result = decorated_func(method="GET")
        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 2)
        mock_hook.assert_called_once_with(error, 0, 0.1)


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""

    def test_is_idempotent_method(self):
        """Test is_idempotent_method function."""
        self.assertTrue(is_idempotent_method("GET"))
        self.assertTrue(is_idempotent_method("get"))
        self.assertTrue(is_idempotent_method("HEAD"))
        self.assertTrue(is_idempotent_method("PUT"))
        self.assertTrue(is_idempotent_method("DELETE"))
        self.assertTrue(is_idempotent_method("OPTIONS"))
        self.assertFalse(is_idempotent_method("POST"))
        self.assertFalse(is_idempotent_method("PATCH"))

    def test_create_retry_condition(self):
        """Test create_retry_condition function."""
        # Test with exception types
        condition = create_retry_condition(exception_types=PortTimeoutError)
        self.assertTrue(condition(PortTimeoutError("Timeout")))
        self.assertFalse(condition(PortApiError("API error")))

        # Test with multiple exception types
        condition = create_retry_condition(exception_types=[PortTimeoutError, PortRateLimitError])
        self.assertTrue(condition(PortTimeoutError("Timeout")))
        self.assertTrue(condition(PortRateLimitError("Rate limit", status_code=429)))
        self.assertFalse(condition(PortApiError("API error")))

        # Test with status codes
        condition = create_retry_condition(status_codes=[429, 503], transient_only=False)
        self.assertTrue(condition(PortApiError("API error", status_code=429)))
        self.assertTrue(condition(PortApiError("API error", status_code=503)))
        self.assertFalse(condition(PortApiError("API error", status_code=400)))

        # Test with transient_only
        condition = create_retry_condition(transient_only=True)
        self.assertTrue(condition(PortServerError("Server error", status_code=500)))
        self.assertFalse(condition(PortApiError("API error", status_code=400)))

        # Test with all parameters
        condition = create_retry_condition(
            exception_types=[PortTimeoutError, PortRateLimitError],
            status_codes=[429, 503],
            transient_only=False
        )
        self.assertTrue(condition(PortTimeoutError("Timeout")))
        self.assertTrue(condition(PortRateLimitError("Rate limit", status_code=429)))
        self.assertFalse(condition(PortApiError("API error", status_code=400)))
        self.assertFalse(condition(PortApiError("API error", status_code=500)))  # Not in exception_types


if __name__ == "__main__":
    unittest.main()
