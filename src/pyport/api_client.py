"""
Port API Client for Python.

This module provides the main client for interacting with the Port API. It handles:

1. Authentication and token management
2. Request handling with retry logic
3. Error handling and response processing
4. Access to all API resources through specialized service classes

The PortClient class is the main entry point for the library and provides
access to all API resources through properties like `blueprints`, `entities`, etc.

Example:
    ```python
    from pyport import PortClient

    # Create a client
    client = PortClient(
        client_id="your-client-id",
        client_secret="your-client-secret"
    )

    # Get all blueprints
    blueprints = client.blueprints.get_blueprints()

    # Create a new entity
    entity = client.entities.create_entity(
        "service",  # Blueprint identifier
        {
            "identifier": "my-service",
            "title": "My Service",
            "properties": {
                "language": "Python"
            }
        }
    )
    ```

Note: The implementation has been refactored into the `client` package for better
organization, but this module is maintained for backward compatibility.
"""

# Import from the refactored implementation
from src.pyport.client.client import PortClient

# Re-export for backward compatibility
__all__ = ['PortClient']

# No need to import requests as it's not used directly
