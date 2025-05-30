"""
Example demonstrating the improved type hints and documentation in the PyPort client library.

This example shows how to use the PyPort client library with the improved type hints,
documentation, and error handling.
"""
import os
import sys
import logging
from typing import List, Dict, Any

from pyport import PortClient
from pyport.exceptions import (
    PortApiError,
    PortResourceNotFoundError,
    PortValidationError,
    PortAuthenticationError
)
from pyport.types import Blueprint, Entity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("pyport-example")


def get_all_blueprints(client: PortClient) -> List[Blueprint]:
    """
    Get all blueprints with pagination.
    
    This function demonstrates:
    - Pagination support
    - Type hints for parameters and return values
    - Error handling with specific exception types
    
    Args:
        client: The Port client.
        
    Returns:
        A list of blueprints.
    """
    logger.info("Getting all blueprints...")
    
    all_blueprints = []
    page = 1
    per_page = 50
    
    try:
        # Get blueprints with pagination
        while True:
            logger.info(f"Getting page {page} (items per page: {per_page})...")
            blueprints = client.blueprints.get_blueprints(page=page, per_page=per_page)
            
            if not blueprints:
                break
                
            all_blueprints.extend(blueprints)
            logger.info(f"Retrieved {len(blueprints)} blueprints on page {page}")
            
            # If we got fewer blueprints than requested, we've reached the end
            if len(blueprints) < per_page:
                break
                
            page += 1
            
        logger.info(f"Retrieved a total of {len(all_blueprints)} blueprints")
        return all_blueprints
        
    except PortResourceNotFoundError as e:
        logger.error(f"Resource not found: {e}")
        return []
    except PortApiError as e:
        logger.error(f"API error: {e}")
        # Check if it's a transient error that can be retried
        if e.is_transient():
            logger.info("This error is transient and can be retried.")
        return []


def get_blueprint_details(client: PortClient, blueprint_id: str) -> Blueprint:
    """
    Get details for a specific blueprint.
    
    This function demonstrates:
    - Specific exception handling
    - Accessing blueprint properties
    - Type hints for parameters and return values
    
    Args:
        client: The Port client.
        blueprint_id: The identifier of the blueprint.
        
    Returns:
        The blueprint details or an empty dictionary if not found.
    """
    logger.info(f"Getting details for blueprint '{blueprint_id}'...")
    
    try:
        # Get the blueprint
        blueprint = client.blueprints.get_blueprint(blueprint_id)
        
        # Print blueprint details
        logger.info(f"Blueprint: {blueprint.get('title')} ({blueprint.get('identifier')})")
        
        # Print blueprint properties
        properties = blueprint.get("properties", {})
        if properties:
            logger.info("Properties:")
            for prop_name, prop_details in properties.items():
                prop_type = prop_details.get("type", "unknown")
                prop_title = prop_details.get("title", prop_name)
                logger.info(f"  - {prop_name}: {prop_title} ({prop_type})")
        else:
            logger.info("No properties defined for this blueprint.")
            
        return blueprint
        
    except PortResourceNotFoundError as e:
        logger.error(f"Blueprint not found: {e}")
        return {}
    except PortApiError as e:
        logger.error(f"API error: {e}")
        return {}


def create_blueprint(client: PortClient, blueprint_data: Dict[str, Any]) -> Blueprint:
    """
    Create a new blueprint.
    
    This function demonstrates:
    - Creating a blueprint with the improved API
    - Handling validation errors
    - Type hints for complex parameters
    
    Args:
        client: The Port client.
        blueprint_data: The data for the new blueprint.
        
    Returns:
        The created blueprint or an empty dictionary if creation failed.
    """
    logger.info(f"Creating blueprint '{blueprint_data.get('identifier')}'...")
    
    try:
        # Create the blueprint
        blueprint = client.blueprints.create_blueprint(blueprint_data)
        
        logger.info(f"Blueprint created: {blueprint.get('title')} ({blueprint.get('identifier')})")
        return blueprint
        
    except PortValidationError as e:
        logger.error(f"Validation error: {e}")
        return {}
    except PortApiError as e:
        logger.error(f"API error: {e}")
        return {}


def main():
    """Main function demonstrating the improved PyPort client library."""
    # Get credentials from environment variables
    client_id = os.getenv("PORT_CLIENT_ID")
    client_secret = os.getenv("PORT_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        logger.error("Missing environment variables: PORT_CLIENT_ID or PORT_CLIENT_SECRET")
        logger.info("Please set these environment variables and try again.")
        return
    
    try:
        # Initialize the client
        client = PortClient(client_id=client_id, client_secret=client_secret)
        
        # Example 1: Get all blueprints
        blueprints = get_all_blueprints(client)
        
        # Example 2: Get details for a specific blueprint
        if blueprints:
            # Use the first blueprint from the list
            first_blueprint_id = blueprints[0].get("identifier")
            get_blueprint_details(client, first_blueprint_id)
        else:
            # If no blueprints were found, try to create one
            logger.info("No blueprints found. Creating a sample blueprint...")
            
            # Example 3: Create a new blueprint
            sample_blueprint = {
                "identifier": "sample-service",
                "title": "Sample Service",
                "icon": "Service",
                "properties": {
                    "language": {
                        "type": "string",
                        "title": "Language",
                        "enum": ["Python", "JavaScript", "Java", "Go"]
                    },
                    "url": {
                        "type": "string",
                        "title": "URL",
                        "format": "url"
                    }
                }
            }
            
            created_blueprint = create_blueprint(client, sample_blueprint)
            
            if created_blueprint:
                # Get details for the created blueprint
                get_blueprint_details(client, created_blueprint.get("identifier"))
        
    except PortAuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        logger.info("Please check your credentials and try again.")
    except PortApiError as e:
        logger.error(f"API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
