"""
Blueprint utility functions.

This module provides high-level utility functions for working with blueprints.
"""
from typing import Dict, Any

from ..client.client import PortClient


def clear_blueprint(client: PortClient, blueprint_id: str) -> Dict[str, Any]:
    """
    Delete all entities in a blueprint using the Port API's bulk delete endpoint.

    This function wraps the existing delete_all_blueprint_entities API method
    to provide a convenient utility interface.

    Args:
        client: PortClient instance
        blueprint_id: ID of the blueprint to clear

    Returns:
        dict: Summary of the operation from the Port API

    Raises:
        PortResourceNotFoundError: If the blueprint does not exist
        PortApiError: If the API request fails

    Example:
        >>> result = clear_blueprint(client, "service")
        >>> print(f"Cleared blueprint: {result}")
    """
    # Use the existing API method to delete all entities
    return client.blueprints.delete_all_blueprint_entities(blueprint_id)
