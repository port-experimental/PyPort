"""
Example demonstrating the improved logging capabilities in the PyPort client library.

This example shows how to configure logging and how to use the correlation IDs
to track requests across systems.
"""
import logging
import sys
import json
from typing import Dict, Any

from pyport import PortClient
from pyport.exceptions import PortApiError
from pyport.logging import configure_logging

# Configure a custom logger for this example
logger = logging.getLogger("pyport-example")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))
logger.addHandler(handler)


def custom_log_handler(level: int, message: str) -> None:
    """
    A custom log handler that could send logs to a centralized logging system.
    
    In a real application, this could send logs to Elasticsearch, Splunk, etc.
    
    Args:
        level: The logging level.
        message: The log message.
    """
    # Parse the message to extract the correlation ID
    try:
        if message.startswith("Request:") or message.startswith("Response:") or message.startswith("Error:"):
            data = json.loads(message.split(":", 1)[1].strip())
            correlation_id = data.get("correlation_id", "unknown")
            
            # In a real application, you would send this to your logging system
            logger.info(f"[{correlation_id}] Would send to centralized logging: {message}")
    except Exception as e:
        logger.error(f"Error in custom log handler: {e}")


class CustomLogHandler(logging.Handler):
    """A custom logging handler that sends logs to a centralized logging system."""
    
    def emit(self, record: logging.LogRecord) -> None:
        """Process a log record."""
        custom_log_handler(record.levelno, record.getMessage())


def configure_custom_logging() -> None:
    """Configure custom logging for the PyPort client library."""
    # Create a custom handler
    handler = CustomLogHandler()
    handler.setLevel(logging.DEBUG)
    
    # Configure the PyPort logger to use our custom handler
    configure_logging(level=logging.DEBUG, handler=handler)


def make_requests_with_correlation_id(client: PortClient) -> None:
    """
    Make requests with a correlation ID to demonstrate request tracking.
    
    Args:
        client: The Port client.
    """
    logger.info("Making requests with correlation ID...")
    
    try:
        # Make a request with a specific correlation ID
        correlation_id = "example-correlation-id-123"
        blueprints = client.blueprints.get_blueprints(page=1, per_page=5)
        
        logger.info(f"Retrieved {len(blueprints)} blueprints")
        
        # Make another request with the same correlation ID
        if blueprints:
            blueprint_id = blueprints[0].get("identifier")
            client.blueprints.get_blueprint(blueprint_id)
            logger.info(f"Retrieved blueprint: {blueprint_id}")
        
    except PortApiError as e:
        logger.error(f"API error: {e}")


def main() -> None:
    """Main function demonstrating the improved logging capabilities."""
    # Get credentials from environment variables
    import os
    client_id = os.getenv("PORT_CLIENT_ID")
    client_secret = os.getenv("PORT_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        logger.error("Missing environment variables: PORT_CLIENT_ID or PORT_CLIENT_SECRET")
        logger.info("Please set these environment variables and try again.")
        return
    
    # Configure custom logging
    configure_custom_logging()
    
    try:
        # Initialize the client with DEBUG logging
        client = PortClient(
            client_id=client_id,
            client_secret=client_secret,
            log_level=logging.DEBUG
        )
        
        # Make requests with correlation ID
        make_requests_with_correlation_id(client)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
