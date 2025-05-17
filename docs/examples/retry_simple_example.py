"""
Simplified Retry Logic Example

This example demonstrates the key features of the enhanced retry logic in the PyPort client.
"""
import logging
import os
import sys
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pyport.api_client import PortClient
from src.pyport.exceptions import PortApiError
from src.pyport.retry import RetryStrategy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    Demonstrate the key retry features of the PyPort client.
    """
    # Get client credentials from environment variables
    client_id = os.environ.get("PORT_CLIENT_ID")
    client_secret = os.environ.get("PORT_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        logger.error("PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables must be set.")
        return
    
    # Example 1: Client with default retry configuration
    logger.info("=== Example 1: Default Retry Configuration ===")
    client = PortClient(
        client_id=client_id,
        client_secret=client_secret
    )
    logger.info("Default client created with exponential backoff strategy")
    
    # Example 2: Client with custom retry configuration
    logger.info("\n=== Example 2: Custom Retry Configuration ===")
    custom_client = PortClient(
        client_id=client_id,
        client_secret=client_secret,
        # Custom retry configuration
        max_retries=5,                        # Retry up to 5 times
        retry_delay=0.5,                      # Start with a 0.5 second delay
        max_delay=30.0,                       # Maximum delay of 30 seconds
        retry_strategy=RetryStrategy.LINEAR,  # Linear backoff strategy
        retry_jitter=True                     # Add jitter to prevent thundering herd
    )
    logger.info("Custom client created with linear backoff strategy")
    
    # Example 3: Request with custom retry parameters
    logger.info("\n=== Example 3: Request with Custom Retry Parameters ===")
    try:
        # Make a request with custom retry parameters just for this request
        blueprints = client.blueprints.get_blueprints(
            retries=2,                # Only retry twice
            retry_delay=0.5           # Start with a 0.5 second delay
        )
        logger.info(f"Successfully retrieved {len(blueprints)} blueprints")
    except PortApiError as e:
        logger.error(f"Failed to retrieve blueprints: {e}")
    
    # Example 4: Checking retry statistics
    logger.info("\n=== Example 4: Retry Statistics ===")
    logger.info(f"Retry statistics: {client.retry_config.stats}")
    
    logger.info("\nRetry examples completed successfully")


if __name__ == "__main__":
    main()
