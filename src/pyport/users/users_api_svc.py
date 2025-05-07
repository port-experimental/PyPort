from typing import Dict, List, Any, Optional, cast

from src.pyport.types import User, UsersResponse, UserResponse

from src.pyport.models.api_category import BaseResource
from src.pyport.models.response import PortListResponse, PortItemResponse


class Users(BaseResource):
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
        super().__init__(client, resource_name="users")

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

    def create_user(self, user_data: Dict) -> Dict:
        """
        Create a new user.

        :param user_data: A dictionary containing user data.
        :return: A dictionary representing the newly created user.
        """
        response = self._client.make_request("POST", "users", json=user_data)
        return response.json()

    def update_user(self, user_id: str, user_data: Dict) -> Dict:
        """
        Update an existing user.

        :param user_id: The identifier of the user to update.
        :param user_data: A dictionary with updated user data.
        :return: A dictionary representing the updated user.
        """
        response = self._client.make_request("PUT", f"users/{user_id}", json=user_data)
        return response.json()

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.

        :param user_id: The identifier of the user to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"users/{user_id}")
        return response.status_code == 204

    def invite_user(self, invitation_data: Dict) -> Dict:
        """
        Invite a new user to the organization.

        :param invitation_data: A dictionary containing invitation data (email, role, etc.).
        :return: A dictionary representing the invitation result.
        """
        response = self._client.make_request("POST", "users/invite", json=invitation_data)
        return response.json()

    def get_user_profile(self) -> Dict:
        """
        Retrieve the profile of the currently authenticated user.

        :return: A dictionary representing the user profile.
        """
        response = self._client.make_request("GET", "profile")
        return response.json().get("profile", {})

    def rotate_user_credentials(self, user_email: str) -> Dict:
        """
        Rotate credentials for a specific user.

        :param user_email: The email of the user whose credentials should be rotated.
        :return: A dictionary containing the new credentials.
        """
        response = self._client.make_request("POST", f"rotate-credentials/{user_email}")
        return response.json()
