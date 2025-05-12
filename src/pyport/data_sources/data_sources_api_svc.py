from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class DataSources(BaseAPIService):
    """Data Sources API category for managing data sources.

    This class provides methods for interacting with the Data Sources API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all data sources
        >>> data_sources = client.data_sources.get_data_sources()
    """

    def __init__(self, client):
        """Initialize the Data Sources API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="data-sources", response_key="dataSource")

    def get_data_sources(self, page: Optional[int] = None, per_page: Optional[int] = None,
                         params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all data sources.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of data source dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = "data-sources"

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("dataSources", [])
