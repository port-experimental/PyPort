from typing import Dict, List
from pyport.models.api_category import BaseResource


class Roles(BaseResource):
    """Roles API category for managing roles."""

    def get_roles(self) -> List[Dict]:
        """
        Retrieve all roles.

        :return: A list of role dictionaries.
        """
        response = self._client.make_request("GET", "roles")
        return response.json().get("roles", [])

    def get_role(self, role_id: str) -> Dict:
        """
        Retrieve details for a specific role.

        :param role_id: The identifier of the role.
        :return: A dictionary representing the role.
        """
        response = self._client.make_request("GET", f"roles/{role_id}")
        return response.json().get("role", {})

    def create_role(self, role_data: Dict) -> Dict:
        """
        Create a new role.

        :param role_data: A dictionary containing role data.
        :return: A dictionary representing the newly created role.
        """
        response = self._client.make_request("POST", "roles", json=role_data)
        return response.json()

    def update_role(self, role_id: str, role_data: Dict) -> Dict:
        """
        Update an existing role.

        :param role_id: The identifier of the role to update.
        :param role_data: A dictionary with updated role data.
        :return: A dictionary representing the updated role.
        """
        response = self._client.make_request("PUT", f"roles/{role_id}", json=role_data)
        return response.json()

    def delete_role(self, role_id: str) -> bool:
        """
        Delete a role.

        :param role_id: The identifier of the role to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"roles/{role_id}")
        return response.status_code == 204
