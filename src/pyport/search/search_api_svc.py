"""Search API service for Port search functionality.

This module provides methods for searching entities and other resources
within Port using various search criteria."""

from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class Search(BaseAPIService):
    """Search API category for querying resources.

    This class provides methods for searching entities and blueprints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Search for entities
        >>> entities = client.search.search_entities({"query": "my-entity"})
        >>> # Search for blueprints
        >>> blueprints = client.search.search_blueprints({"query": "my-blueprint"})
    """

    def __init__(self, client):
        """Initialize the Search API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="search", response_key=None)

    def search_entities(self, query_params: Dict[str, Any],
                        additional_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for entities based on query parameters.

        Args:
            query_params: A dictionary of query parameters for the search.
            additional_params: Additional query parameters for the request.

        Returns:
            A list of matching entity dictionaries.

        Raises:
            PortValidationError: If the query parameters are invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Combine query parameters
        all_params = query_params.copy()
        if additional_params:
            all_params.update(additional_params)

        # Build the endpoint
        endpoint = self._build_endpoint("search", "entities")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("results", [])

    def search_blueprints(self, query_params: Dict[str, Any],
                          additional_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for blueprints based on query parameters.

        Args:
            query_params: A dictionary of query parameters for the search.
            additional_params: Additional query parameters for the request.

        Returns:
            A list of matching blueprint dictionaries.

        Raises:
            PortValidationError: If the query parameters are invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Combine query parameters
        all_params = query_params.copy()
        if additional_params:
            all_params.update(additional_params)

        # Build the endpoint
        endpoint = self._build_endpoint("search", "blueprints")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("results", [])
