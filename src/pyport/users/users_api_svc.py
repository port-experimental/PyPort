from typing import Dict, Any, Optional

from ..services.base_api_service import BaseAPIService


class Users(BaseAPIService):
    """Users API category for managing users.

    This class provides methods for interacting with the Users API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all users
        >>> users = client.users.get_users()
        >>> # Get a specific user
        >>> user = client.users.get_user("user-id")
    """

    def __init__(self, client):
        """Initialize the Users API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="users", response_key="user")

    def get_users(self, page: Optional[int] = None, per_page: Optional[int] = None,
                  params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve all users in the organization.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing users data.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Make the request
        response = self._make_request_with_params('GET', "users", params=all_params)
        return response

    def get_user(self, user_email: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve a specific user by email.

        Args:
            user_email: The email address of the user.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the user.

        Raises:
            PortResourceNotFoundError: If the user does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("users", user_email)
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

    def invite_user(self, invitation_data: Dict[str, Any],
                    params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Invite a user to the organization.

        Args:
            invitation_data: A dictionary containing invitation data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the invitation result.

        Raises:
            PortValidationError: If the invitation data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("users", "invite")
        response = self._make_request_with_params('POST', endpoint, json=invitation_data, params=params)
        return response
