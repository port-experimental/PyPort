"""
Base API Service module.

This module provides a base class for all API service classes in the PyPort library.
It implements common functionality and patterns used across all API services.
"""

from typing import Any, Dict, List, Optional, cast, Union

from ..models.api_category import BaseResource as BaseResourceModel, ApiClient
from ..types import JsonDict

# Import specific types for better type hints
from ..types import PaginationParams


class BaseAPIService(BaseResourceModel):
    """Base class for all API service classes.

    This class extends BaseResource to provide additional common functionality
    for API service classes, such as standardized method signatures, common
    response handling patterns, and utility methods.

    All API service classes should inherit from this class instead of directly
    from BaseResource to ensure consistent behavior and reduce code duplication.
    """

    def __init__(self, client: ApiClient, resource_name: Optional[str] = None,
                 response_key: Optional[str] = None):
        """
        Initialize a BaseAPIService.

        Args:
            client: The API client to use for requests.
            resource_name: The name of the resource in the API (e.g., "blueprints").
                If None, the resource name must be provided in each method call.
            response_key: The key to use when extracting data from API responses.
                If None, defaults to resource_name.
        """
        super().__init__(client, resource_name)
        self._response_key = response_key or resource_name

    def _extract_response_data(self, response: JsonDict, key: Optional[str] = None) -> Union[JsonDict, List[JsonDict]]:
        """
        Extract data from an API response using the specified key.

        This method handles the common pattern of extracting data from API responses
        where the data is nested under a specific key.

        Args:
            response: The API response as a dictionary.
            key: The key to extract data from. If None, uses the service's response_key.

        Returns:
            The extracted data, or an empty dict/list if the key is not found.
        """
        extract_key = key or self._response_key
        if not extract_key:
            return response

        # Handle both list and dictionary responses
        if isinstance(response.get(extract_key), list):
            return response.get(extract_key, [])
        return response.get(extract_key, {})

    def _handle_pagination_params(self, page: Optional[int] = None,
                                  per_page: Optional[int] = None) -> PaginationParams:
        """
        Create a parameters dictionary for pagination.

        This method handles the common pattern of creating pagination parameters
        for API requests.

        Args:
            page: The page number to retrieve.
            per_page: The number of items per page.

        Returns:
            A dictionary of pagination parameters, or an empty dict if no pagination is needed.
        """
        params: PaginationParams = {}
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = per_page
        return params

    def _build_endpoint(self, *parts: str) -> str:
        """
        Build an API endpoint from the given parts.

        This method handles the common pattern of building API endpoints
        by joining path parts with slashes.

        Args:
            *parts: The parts of the endpoint to join.

        Returns:
            The complete endpoint as a string.
        """
        return '/'.join(part for part in parts if part)

    def _make_request_with_params(self, method: str, endpoint: str,
                                  params: Optional[Dict[str, Any]] = None,
                                  **kwargs) -> JsonDict:
        """
        Make a request with optional parameters.

        This method handles the common pattern of making requests with optional
        parameters, only including them if they are not None and not empty.

        Args:
            method: The HTTP method to use.
            endpoint: The API endpoint to request.
            params: Query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            The API response as a JSON dictionary.
        """
        # For backward compatibility, only include params if it's not None and not empty
        if params is not None and params:
            response = self._client.make_request(method, endpoint, params=params, **kwargs)
        else:
            response = self._client.make_request(method, endpoint, **kwargs)

        # Return the JSON response
        return response.json()

    def get_all(self, page: Optional[int] = None, per_page: Optional[int] = None,
                params: Optional[Dict[str, Any]] = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Get all resources with pagination support.

        This method retrieves a list of all resources, with optional pagination.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            A list of resource dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        # Combine pagination parameters with any additional parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Use the base class list method
        return cast(List[Dict[str, Any]], self.list(params=all_params, **kwargs))

    def get_by_id(self, resource_id: str, params: Optional[Dict[str, Any]] = None,
                  response_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Get a specific resource by its ID.

        This method retrieves a specific resource and extracts it from the response
        using the specified response key.

        Args:
            resource_id: The ID of the resource to get.
            params: Query parameters for the request.
            response_key: The key to extract the resource from in the response.
                If None, uses the service's response_key.
            **kwargs: Additional parameters for the request.

        Returns:
            The resource as a dictionary.

        Raises:
            PortResourceNotFoundError: If the resource does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Use the base class get method
        response = self.get(resource_id, params=params, **kwargs)
        return cast(Dict[str, Any], self._extract_response_data(response, response_key))

    def create_resource(self, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None,
                        response_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a new resource.

        This method creates a new resource and extracts it from the response
        using the specified response key.

        Args:
            data: The data for the new resource.
            params: Query parameters for the request.
            response_key: The key to extract the resource from in the response.
                If None, uses the service's response_key.
            **kwargs: Additional parameters for the request.

        Returns:
            The created resource as a dictionary.

        Raises:
            PortValidationError: If the data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Use the base class create method
        response = self.create(data, params=params, **kwargs)
        return cast(Dict[str, Any], self._extract_response_data(response, response_key))

    def update_resource(self, resource_id: str, data: Dict[str, Any],
                        params: Optional[Dict[str, Any]] = None,
                        response_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Update an existing resource.

        This method updates an existing resource and extracts it from the response
        using the specified response key.

        Args:
            resource_id: The ID of the resource to update.
            data: The updated data for the resource.
            params: Query parameters for the request.
            response_key: The key to extract the resource from in the response.
                If None, uses the service's response_key.
            **kwargs: Additional parameters for the request.

        Returns:
            The updated resource as a dictionary.

        Raises:
            PortResourceNotFoundError: If the resource does not exist.
            PortValidationError: If the data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Use the base class update method
        response = self.update(resource_id, data, params=params, **kwargs)
        return cast(Dict[str, Any], self._extract_response_data(response, response_key))

    def delete_resource(self, resource_id: str, params: Optional[Dict[str, Any]] = None,
                        **kwargs) -> bool:
        """
        Delete a resource.

        This method deletes an existing resource.

        Args:
            resource_id: The ID of the resource to delete.
            params: Query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            True if the resource was deleted successfully, False otherwise.

        Raises:
            PortResourceNotFoundError: If the resource does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Use the base class delete method
        return self.delete(resource_id, params=params, **kwargs)
