from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class Apps(BaseAPIService):
    """Apps API category for managing applications.

    This class provides methods for interacting with the Apps API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all apps
        >>> apps = client.apps.get_apps()
        >>> # Get a specific app
        >>> app = client.apps.get_app("app-id")
    """

    def __init__(self, client):
        """Initialize the Apps API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="apps", response_key="app")

    def get_apps(self, page: Optional[int] = None, per_page: Optional[int] = None,
                 params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all apps.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of app dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        return self.get_all(page=page, per_page=per_page, params=params)

    def get_app(self, app_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific app.

        Args:
            app_id: The identifier of the app.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the app.

        Raises:
            PortResourceNotFoundError: If the app does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.get_by_id(app_id, params=params)

    def create_app(self, app_data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new app.

        Args:
            app_data: A dictionary containing app data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created app.

        Raises:
            PortValidationError: If the app data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("POST", "apps", json=app_data)
        return response.json()

    def update_app(self, app_id: str, app_data: Dict[str, Any],
                   params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing app.

        Args:
            app_id: The identifier of the app to update.
            app_data: A dictionary with updated app data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated app.

        Raises:
            PortResourceNotFoundError: If the app does not exist.
            PortValidationError: If the app data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("PUT", f"apps/{app_id}", json=app_data)
        return response.json()

    def delete_app(self, app_id: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete an app.

        Args:
            app_id: The identifier of the app to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the app does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.delete_resource(app_id, params=params)

    def rotate_app_secret(self, app_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Rotate the secret for a specific app.

        Args:
            app_id: The identifier of the app whose secret should be rotated.
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing the new secret.

        Raises:
            PortResourceNotFoundError: If the app does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("apps", app_id, "rotate-secret")
        response = self._make_request_with_params('POST', endpoint, params=params)
        return response
