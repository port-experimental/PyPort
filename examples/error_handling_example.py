"""
Example script demonstrating the error handling capabilities of the PyPort client.
"""
import logging
import sys
from typing import Dict, Any

from pyport.api_client import PortClient
from pyport.exceptions import (
    PortApiError,
    PortAuthenticationError,
    PortPermissionError,
    PortResourceNotFoundError,
    PortValidationError,
    PortRateLimitError,
    PortServerError,
    PortTimeoutError,
    PortConnectionError,
    PortConfigurationError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("pyport-example")


def handle_port_error(e: PortApiError) -> None:
    """
    Handle Port API errors in a consistent way.

    :param e: The Port API error.
    """
    logger.error(f"Error: {str(e)}")

    # Log additional details for debugging
    if hasattr(e, 'status_code') and e.status_code:
        logger.debug(f"Status Code: {e.status_code}")
    if hasattr(e, 'endpoint') and e.endpoint:
        logger.debug(f"Endpoint: {e.endpoint}")
    if hasattr(e, 'method') and e.method:
        logger.debug(f"Method: {e.method}")
    if hasattr(e, 'response_body') and e.response_body:
        logger.debug(f"Response Body: {e.response_body}")

    # Handle specific error types
    if isinstance(e, PortAuthenticationError):
        logger.error("Authentication failed. Please check your credentials.")
    elif isinstance(e, PortPermissionError):
        logger.error("Permission denied. You don't have access to this resource.")
    elif isinstance(e, PortResourceNotFoundError):
        logger.error("Resource not found. Please check the identifier.")
    elif isinstance(e, PortValidationError):
        logger.error("Validation error. Please check your request data.")
    elif isinstance(e, PortRateLimitError):
        retry_after = e.retry_after or 60
        logger.warning(f"Rate limit exceeded. Please retry after {retry_after} seconds.")
    elif isinstance(e, PortServerError):
        logger.error("Server error. Please try again later or contact support.")
    elif isinstance(e, PortTimeoutError):
        logger.error("Request timed out. Please check your network connection or try again later.")
    elif isinstance(e, PortConnectionError):
        logger.error("Connection error. Please check your network connection.")
    elif isinstance(e, PortConfigurationError):
        logger.error("Configuration error. Please check your client configuration.")


def get_blueprint_safely(client: PortClient, blueprint_id: str) -> Dict[str, Any]:
    """
    Get a blueprint with proper error handling.

    :param client: The Port client.
    :param blueprint_id: The blueprint identifier.
    :return: The blueprint data.
    """
    try:
        return client.blueprints.get_blueprint(blueprint_id)
    except PortApiError as e:
        handle_port_error(e)
        return {}


def example_with_error_handling_helper():
    """Example using the with_error_handling helper method."""
    try:
        # Create a client with invalid credentials
        client = PortClient(
            client_id="invalid_client_id",
            client_secret="invalid_client_secret"
        )

        # Define custom error handlers
        def on_error(e):
            logger.error(f"Custom error handler: {e}")
            return {"error": str(e)}

        def on_not_found():
            logger.warning("Resource not found, returning default value")
            return {"default": "blueprint"}

        # Use the with_error_handling helper
        result = client.with_error_handling(
            client.blueprints.get_blueprint,
            "example-blueprint",
            on_error=on_error,
            on_not_found=on_not_found
        )

        logger.info(f"Result: {result}")

    except PortConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


def main():
    """Main function demonstrating error handling."""
    logger.info("=== Example 1: Basic Error Handling ===")
    try:
        # Create a client with invalid credentials to demonstrate authentication error
        client = PortClient(
            client_id="invalid_client_id",
            client_secret="invalid_client_secret"
        )

        # Try to get a blueprint (this will fail with authentication error)
        blueprint = get_blueprint_safely(client, "example-blueprint")

        if blueprint:
            logger.info(f"Blueprint: {blueprint}")
        else:
            logger.warning("Failed to get blueprint.")

    except PortConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

    logger.info("\n=== Example 2: Using with_error_handling Helper ===")
    example_with_error_handling_helper()


if __name__ == "__main__":
    main()
