"""
Retry Logic Example

This example demonstrates how to use the enhanced retry logic in the PyPort client.
"""
import logging
import os
import sys
import time
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pyport.api_client import PortClient
from src.pyport.exceptions import PortApiError, PortServerError
from src.pyport.retry import RetryConfig, RetryStrategy, with_retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_client() -> PortClient:
    """
    Create a Port client using environment variables.

    Returns:
        A configured Port client.
    """
    client_id = os.environ.get("PORT_CLIENT_ID")
    client_secret = os.environ.get("PORT_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError(
            "PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables must be set."
        )

    # Create a client with custom retry configuration
    return PortClient(
        client_id=client_id,
        client_secret=client_secret,
        # Retry configuration
        max_retries=5,
        retry_delay=1.0,
        max_delay=10.0,
        retry_strategy=RetryStrategy.EXPONENTIAL,
        retry_jitter=True
    )


def example_default_retry():
    """
    Example of using the default retry configuration.
    """
    logger.info("=== Default Retry Configuration Example ===")
    client = get_client()

    try:
        # This will use the client's default retry configuration
        blueprints = client.blueprints.get_blueprints()
        logger.info(f"Successfully retrieved {len(blueprints)} blueprints")
    except PortApiError as e:
        logger.error(f"Failed to retrieve blueprints: {e}")


def example_custom_retry_per_request():
    """
    Example of using a custom retry configuration for a specific request.
    """
    logger.info("=== Custom Retry Per Request Example ===")
    client = get_client()

    try:
        # This will use a custom retry configuration for this specific request
        # We're specifying custom retry parameters just for this request
        blueprints = client.blueprints.get_blueprints(
            # Override the retry settings just for this request
            retries=2,                # Only retry twice
            retry_delay=0.5           # Start with a shorter delay (0.5 seconds)
        )
        logger.info(f"Successfully retrieved {len(blueprints)} blueprints with custom retry configuration")

        # Check the retry statistics
        logger.info(f"Retry statistics: {client.retry_config.stats}")
    except PortApiError as e:
        logger.error(f"Failed to retrieve blueprints: {e}")


def example_retry_with_custom_function():
    """
    Example of using the retry decorator with a custom function.
    """
    logger.info("=== Custom Function with Retry Example ===")

    # Create a custom retry configuration
    retry_config = RetryConfig(
        max_retries=3,
        retry_delay=0.5,
        strategy=RetryStrategy.LINEAR,
        jitter=True
    )

    # Define a function that might fail
    @with_retry(config=retry_config)
    def fetch_data(url: str, method: str = "GET") -> Dict[str, Any]:
        """
        Fetch data from a URL with retry logic.

        Args:
            url: The URL to fetch data from.
            method: The HTTP method to use.

        Returns:
            The fetched data.

        Raises:
            PortApiError: If the request fails after all retries.
        """
        logger.info(f"Fetching data from {url}...")

        # Simulate a failure on the first attempt
        if getattr(fetch_data, "_attempts", 0) < 1:
            setattr(fetch_data, "_attempts", getattr(fetch_data, "_attempts", 0) + 1)
            raise PortServerError("Simulated server error", status_code=500)

        # Return simulated data on subsequent attempts
        return {"data": "Simulated data", "url": url}

    try:
        # Call the function with retry logic
        data = fetch_data("https://api.example.com/data", method="GET")
        logger.info(f"Successfully fetched data: {data}")

        # Check the retry statistics
        logger.info(f"Retry statistics: {retry_config.stats}")
    except PortApiError as e:
        logger.error(f"Failed to fetch data: {e}")


def example_circuit_breaker():
    """
    Example of using the circuit breaker pattern.
    """
    logger.info("=== Circuit Breaker Example ===")

    # Create a custom retry configuration with a circuit breaker
    retry_config = RetryConfig(
        max_retries=3,
        retry_delay=0.5,
        strategy=RetryStrategy.EXPONENTIAL,
        jitter=False
    )

    # Set a low failure threshold for the circuit breaker
    retry_config.circuit_breaker.failure_threshold = 2
    retry_config.circuit_breaker.reset_timeout = 5.0

    # Define a function that always fails
    @with_retry(config=retry_config)
    def always_fails(method: str = "GET") -> None:
        """
        A function that always fails.

        Args:
            method: The HTTP method to use.

        Raises:
            PortServerError: Always raised.
        """
        logger.info("Attempting operation that will fail...")
        raise PortServerError("Simulated server error", status_code=500)

    # Try calling the function multiple times
    for i in range(5):
        try:
            always_fails(method="GET")
        except PortApiError as e:
            logger.warning(f"Attempt {i+1} failed: {e}")

            # Check the circuit breaker state
            logger.info(f"Circuit breaker state: {retry_config.circuit_breaker}")

            # If the circuit is open, wait for it to reset
            if retry_config.circuit_breaker.is_open:
                logger.info("Circuit is open. Waiting for reset timeout...")
                time.sleep(retry_config.circuit_breaker.reset_timeout)
                logger.info("Reset timeout elapsed. Trying again...")


def example_different_retry_strategies():
    """
    Example of using different retry strategies.
    """
    logger.info("=== Different Retry Strategies Example ===")

    strategies = [
        RetryStrategy.CONSTANT,
        RetryStrategy.LINEAR,
        RetryStrategy.EXPONENTIAL,
        RetryStrategy.FIBONACCI
    ]

    for strategy in strategies:
        logger.info(f"Testing {strategy.value} retry strategy")

        # Create a custom retry configuration with the current strategy
        retry_config = RetryConfig(
            max_retries=3,
            retry_delay=1.0,
            strategy=strategy,
            jitter=False
        )

        # Define a function that fails a few times
        @with_retry(config=retry_config)
        def fails_then_succeeds(method: str = "GET") -> str:
            """
            A function that fails a few times then succeeds.

            Args:
                method: The HTTP method to use.

            Returns:
                A success message.

            Raises:
                PortServerError: Raised for the first few attempts.
            """
            attempts = getattr(fails_then_succeeds, "_attempts", 0)
            setattr(fails_then_succeeds, "_attempts", attempts + 1)

            if attempts < 2:
                logger.info(f"Attempt {attempts+1} will fail...")
                raise PortServerError("Simulated server error", status_code=500)

            logger.info(f"Attempt {attempts+1} will succeed!")
            return "Success!"

        try:
            # Reset the attempt counter
            setattr(fails_then_succeeds, "_attempts", 0)

            # Call the function with retry logic
            result = fails_then_succeeds(method="GET")
            logger.info(f"Result: {result}")

            # Check the retry statistics
            logger.info(f"Retry times: {retry_config.stats.retry_times}")
        except PortApiError as e:
            logger.error(f"Failed with {strategy.value} strategy: {e}")


def main():
    """
    Run all retry examples.
    """
    try:
        example_default_retry()
        print("\n")

        example_custom_retry_per_request()
        print("\n")

        example_retry_with_custom_function()
        print("\n")

        example_circuit_breaker()
        print("\n")

        example_different_retry_strategies()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()
