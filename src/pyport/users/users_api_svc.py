from typing import Dict, List
from pyport.models.api_category import BaseResource


class Users(BaseResource):
    """Users API category for managing users."""

    def get_users(self) -> List[Dict]:
        """
        Retrieve all users.

        :return: A list of user dictionaries.
        """
        response = self._client.make_request("GET", "users")
        return response.json().get("users", [])

    def get_user(self, user_id: str) -> Dict:
        """
        Retrieve details for a specific user.

        :param user_id: The identifier of the user.
        :return: A dictionary representing the user.
        """
        response = self._client.make_request("GET", f"users/{user_id}")
        return response.json().get("user", {})

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
