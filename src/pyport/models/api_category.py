from abc import ABC
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union, cast, Protocol, runtime_checkable

# Define type variables for generic types
T = TypeVar('T')  # Generic type for resource items
R = TypeVar('R')  # Generic type for response objects


@runtime_checkable
class ApiClient(Protocol):
    """Protocol defining the interface for an API client."""

    def make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make a request to the API."""
        ...


class BaseResource(ABC):
    """Base class for all API resource categories.

    This class provides common functionality for API resource categories,
    such as making requests to the API and handling responses.

    It implements common CRUD operations (list, get, create, update, delete)
    that can be used by subclasses to reduce code duplication.
    """

    def __init__(self, client: ApiClient, resource_name: Optional[str] = None):
        """
        Initialize a BaseResource.

        Args:
            client: The API client to use for requests.
            resource_name: The name of the resource in the API (e.g., "blueprints").
                If None, the resource name must be provided in each method call.
        """
        self._client = client
        self._resource_name = resource_name

    def _get_resource_path(self, resource_id: Optional[str] = None, subresource: Optional[str] = None) -> str:
        """
        Get the resource path for the API request.

        Args:
            resource_id: The ID of the resource, if accessing a specific resource.
            subresource: The name of a subresource, if accessing a subresource.

        Returns:
            The resource path for the API request.

        Raises:
            ValueError: If resource_name is not set and not provided.
        """
        if not self._resource_name:
            raise ValueError("Resource name not set. Either set it in the constructor or provide it in the method call.")

        path = self._resource_name

        if resource_id:
            path = f"{path}/{resource_id}"

        if subresource:
            path = f"{path}/{subresource}"

        return path

    def list(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> List[Dict[str, Any]]:
        """
        List resources.

        This method retrieves a list of resources from the API.

        Args:
            params: Query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            A list of resources as dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        response = self._client.make_request("GET", self._get_resource_path(), params=params, **kwargs)
        return response.json().get(self._resource_name, [])

    def get(self, resource_id: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Get a specific resource.

        This method retrieves a specific resource from the API by its ID.

        Args:
            resource_id: The ID of the resource to get.
            params: Query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            The resource as a dictionary.

        Raises:
            PortResourceNotFoundError: If the resource does not exist.
            PortApiError: If the API request fails for another reason.
        """
        response = self._client.make_request("GET", self._get_resource_path(resource_id), params=params, **kwargs)
        return response.json()

    def create(self, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a new resource.

        This method creates a new resource in the API with the provided data.

        Args:
            data: The data for the new resource.
            params: Query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            The created resource as a dictionary.

        Raises:
            PortValidationError: If the data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        response = self._client.make_request("POST", self._get_resource_path(), json=data, params=params, **kwargs)
        return response.json()

    def update(self, resource_id: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Update a resource.

        This method updates an existing resource in the API with the provided data.

        Args:
            resource_id: The ID of the resource to update.
            data: The updated data for the resource.
            params: Query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            The updated resource as a dictionary.

        Raises:
            PortResourceNotFoundError: If the resource does not exist.
            PortValidationError: If the data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        response = self._client.make_request("PUT", self._get_resource_path(resource_id), json=data, params=params, **kwargs)
        return response.json()

    def patch(self, resource_id: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Partially update a resource.

        This method partially updates an existing resource in the API with the provided data.
        Unlike update(), which replaces the entire resource, patch() only updates the specified fields.

        Args:
            resource_id: The ID of the resource to update.
            data: The updated data for the resource (only the fields to update).
            params: Query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            The updated resource as a dictionary.

        Raises:
            PortResourceNotFoundError: If the resource does not exist.
            PortValidationError: If the data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        response = self._client.make_request("PATCH", self._get_resource_path(resource_id), json=data, params=params, **kwargs)
        return response.json()

    def delete(self, resource_id: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> bool:
        """
        Delete a resource.

        This method deletes an existing resource from the API.

        Args:
            resource_id: The ID of the resource to delete.
            params: Query parameters for the request.
            **kwargs: Additional parameters for the request.

        Returns:
            True if the resource was deleted successfully (status code 204), False otherwise.

        Raises:
            PortResourceNotFoundError: If the resource does not exist.
            PortApiError: If the API request fails for another reason.
        """
        response = self._client.make_request("DELETE", self._get_resource_path(resource_id), params=params, **kwargs)
        return response.status_code == 204
