from typing import Dict, List, Any, Optional, cast

from .types import User

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

    def get_users(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> List[User]:
        """
        Retrieve all users.

        This method retrieves a list of all users in the organization.

        Args:
            params: Optional query parameters for the request.

        Returns:
            A list of user dictionaries, each containing:
            - id: The unique identifier of the user
            - email: The email address of the user
            - firstName: The first name of the user
            - lastName: The last name of the user
            - status: The status of the user (e.g., "active")
            - role: The role of the user
            - createdAt: The creation timestamp
            - updatedAt: The last update timestamp

        Examples:
            >>> users = client.users.get_users()
            >>> for user in users:
            ...     print(f"{user['firstName']} {user['lastName']} ({user['email']})")
        """
        # For backward compatibility, ignore kwargs
        # Use the base class list method
        users = self.list(params=params)
        return cast(List[User], users)

    def get_user(self, user_id: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> User:
        """
        Retrieve details for a specific user.

        This method retrieves detailed information about a specific user.

        Args:
            user_id: The unique identifier of the user to retrieve.
            params: Optional query parameters for the request.

        Returns:
            A dictionary containing the user details:
            - id: The unique identifier of the user
            - email: The email address of the user
            - firstName: The first name of the user
            - lastName: The last name of the user
            - status: The status of the user (e.g., "active")
            - role: The role of the user
            - createdAt: The creation timestamp
            - updatedAt: The last update timestamp

        Examples:
            >>> user = client.users.get_user("user-id")
            >>> print(f"User: {user['firstName']} {user['lastName']}")
            >>> print(f"Email: {user['email']}")
        """
        # For backward compatibility, ignore kwargs
        # Use the base class get method
        response = self.get(user_id, params=params)
        return cast(User, response.get("user", {}))

    def create_user(self, user_data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            user_data: A dictionary containing user data.
            params: Optional query parameters for the request.

        Returns:
            A dictionary representing the newly created user.

        Raises:
            PortValidationError: If the user data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("POST", "users", json=user_data)
        return response.json()

    def update_user(self, user_id: str, user_data: Dict[str, Any],
                    params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing user.

        Args:
            user_id: The identifier of the user to update.
            user_data: A dictionary with updated user data.
            params: Optional query parameters for the request.

        Returns:
            A dictionary representing the updated user.

        Raises:
            PortResourceNotFoundError: If the user does not exist.
            PortValidationError: If the user data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("PUT", f"users/{user_id}", json=user_data)
        return response.json()

    def delete_user(self, user_id: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a user.

        Args:
            user_id: The identifier of the user to delete.
            params: Optional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the user does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.delete_resource(user_id, params=params)

    def invite_user(self, invitation_data: Dict[str, Any],
                    params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Invite a new user to the organization.

        Args:
            invitation_data: A dictionary containing invitation data (email, role, etc.).
            params: Optional query parameters for the request.

        Returns:
            A dictionary representing the invitation result.

        Raises:
            PortValidationError: If the invitation data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("users", "invite")
        response = self._make_request_with_params('POST', endpoint, json=invitation_data, params=params)
        return response

    def get_user_profile(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve the profile of the currently authenticated user.

        Args:
            params: Optional query parameters for the request.

        Returns:
            A dictionary representing the user profile.

        Raises:
            PortApiError: If the API request fails.
        """
        endpoint = "profile"
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("profile", {})

    def rotate_user_credentials(self, user_email: str,
                                params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Rotate credentials for a specific user.

        Args:
            user_email: The email of the user whose credentials should be rotated.
            params: Optional query parameters for the request.

        Returns:
            A dictionary containing the new credentials.

        Raises:
            PortResourceNotFoundError: If the user does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("rotate-credentials", user_email)
        response = self._make_request_with_params('POST', endpoint, params=params)
        return response
