from typing import Dict, List, Any, Optional, cast

from src.pyport.types import Role

from src.pyport.models.api_category import BaseResource


class Roles(BaseResource):
    """Roles API category for managing roles.

    This class provides methods for interacting with the Roles API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all roles
        >>> roles = client.roles.get_roles()
        >>> # Get a specific role
        >>> role = client.roles.get_role("role-id")
    """

    def __init__(self, client):
        """Initialize the Roles API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="roles")

    def get_roles(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> List[Role]:
        """
        Retrieve all roles.

        This method retrieves a list of all roles in the organization.

        Args:
            params: Optional query parameters for the request.

        Returns:
            A list of role dictionaries, each containing:
            - id: The unique identifier of the role
            - name: The name of the role
            - description: The description of the role (if any)
            - permissions: A list of permission strings
            - createdAt: The creation timestamp
            - updatedAt: The last update timestamp

        Examples:
            >>> roles = client.roles.get_roles()
            >>> for role in roles:
            ...     print(f"{role['name']} ({role['id']})")
        """
        # For backward compatibility, ignore kwargs
        # Use the base class list method
        roles = self.list(params=params)
        return cast(List[Role], roles)

    def get_role(self, role_id: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Role:
        """
        Retrieve details for a specific role.

        This method retrieves detailed information about a specific role.

        Args:
            role_id: The unique identifier of the role to retrieve.
            params: Optional query parameters for the request.

        Returns:
            A dictionary containing the role details:
            - id: The unique identifier of the role
            - name: The name of the role
            - description: The description of the role (if any)
            - permissions: A list of permission strings
            - createdAt: The creation timestamp
            - updatedAt: The last update timestamp

        Examples:
            >>> role = client.roles.get_role("role-id")
            >>> print(f"Role: {role['name']}")
            >>> print(f"Permissions: {', '.join(role['permissions'])}")
        """
        # For backward compatibility, ignore kwargs
        # Use the base class get method
        response = self.get(role_id, params=params)
        return cast(Role, response.get("role", {}))

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
