"""Sidebars API service for managing Port sidebar configurations.

This module provides methods for creating, retrieving, updating, and deleting
sidebar configurations in Port."""

from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class Sidebars(BaseAPIService):
    """Sidebars API category for managing sidebar configurations.

    This class provides methods for interacting with the Sidebars API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all sidebars
        >>> sidebars = client.sidebars.get_sidebars()
        >>> # Get a specific sidebar
        >>> sidebar = client.sidebars.get_sidebar("sidebar-id")
    """

    def __init__(self, client):
        """Initialize the Sidebars API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="sidebars", response_key="sidebar")

    def get_sidebars(self, page: Optional[int] = None, per_page: Optional[int] = None,
                     params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all sidebars.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of sidebar dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        return self.get_all(page=page, per_page=per_page, params=params)

    def get_sidebar(self, sidebar_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific sidebar.

        Args:
            sidebar_id: The identifier of the sidebar.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the sidebar.

        Raises:
            PortResourceNotFoundError: If the sidebar does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.get_by_id(sidebar_id, params=params)

    def create_sidebar(self, sidebar_data: Dict[str, Any],
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new sidebar.

        Args:
            sidebar_data: A dictionary containing sidebar data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created sidebar.

        Raises:
            PortValidationError: If the sidebar data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("POST", "sidebars", json=sidebar_data)
        return response.json()

    def update_sidebar(self, sidebar_id: str, sidebar_data: Dict[str, Any],
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing sidebar.

        Args:
            sidebar_id: The identifier of the sidebar to update.
            sidebar_data: A dictionary with updated sidebar data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated sidebar.

        Raises:
            PortResourceNotFoundError: If the sidebar does not exist.
            PortValidationError: If the sidebar data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("PUT", f"sidebars/{sidebar_id}", json=sidebar_data)
        return response.json()

    def delete_sidebar(self, sidebar_id: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a sidebar.

        Args:
            sidebar_id: The identifier of the sidebar to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the sidebar does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.delete_resource(sidebar_id, params=params)

    # Sidebar Folders Methods

    def get_sidebar_folders(self, sidebar_id: str, page: Optional[int] = None,
                            per_page: Optional[int] = None,
                            params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all folders for a specific sidebar.

        Args:
            sidebar_id: The identifier of the sidebar.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of folder dictionaries.

        Raises:
            PortResourceNotFoundError: If the sidebar does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = self._build_endpoint("sidebars", sidebar_id, "folders")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("folders", [])

    def create_sidebar_folder(self, sidebar_id: str, folder_data: Dict[str, Any],
                              params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new folder for a specific sidebar.

        Args:
            sidebar_id: The identifier of the sidebar.
            folder_data: A dictionary containing folder data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created folder.

        Raises:
            PortResourceNotFoundError: If the sidebar does not exist.
            PortValidationError: If the folder data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("sidebars", sidebar_id, "folders")

        # Make the request
        response = self._make_request_with_params('POST', endpoint, json=folder_data, params=params)
        return response

    def get_sidebar_folder(self, sidebar_id: str, folder_id: str,
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific sidebar folder.

        Args:
            sidebar_id: The identifier of the sidebar.
            folder_id: The identifier of the folder.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the sidebar folder.

        Raises:
            PortResourceNotFoundError: If the sidebar or folder does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("sidebars", sidebar_id, "folders", folder_id)

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("folder", {})

    def update_sidebar_folder(self, sidebar_id: str, folder_id: str,
                              folder_data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing sidebar folder.

        Args:
            sidebar_id: The identifier of the sidebar.
            folder_id: The identifier of the folder to update.
            folder_data: A dictionary with updated folder data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated sidebar folder.

        Raises:
            PortResourceNotFoundError: If the sidebar or folder does not exist.
            PortValidationError: If the folder data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("sidebars", sidebar_id, "folders", folder_id)

        # Make the request
        response = self._make_request_with_params('PUT', endpoint, json=folder_data, params=params)
        return response

    def delete_sidebar_folder(self, sidebar_id: str, folder_id: str,
                              params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a sidebar folder.

        Args:
            sidebar_id: The identifier of the sidebar.
            folder_id: The identifier of the folder to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the sidebar or folder does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("sidebars", sidebar_id, "folders", folder_id)

        # Make the request
        response = self._client.make_request("DELETE", endpoint)
        return response.status_code == 204
