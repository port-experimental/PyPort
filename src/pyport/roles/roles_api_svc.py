from typing import Dict, List, Any, Optional, cast

from .types import Role

from ..services.base_api_service import BaseAPIService


class Roles(BaseAPIService):
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
        super().__init__(client, resource_name="roles", response_key="role")

    def get_roles(
        self, page: Optional[int] = None, per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> List[Role]:
        """
        Retrieve all roles.

        This method retrieves a list of all roles in the organization.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of roles per page (default: None).
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
        # Use the base class get_all method which handles pagination
        roles = self.get_all(page=page, per_page=per_page, params=params, **kwargs)
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
        # Use the base class get_by_id method which handles response extraction
        return cast(Role, self.get_by_id(role_id, params=params, **kwargs))

    def create_role(self, role_data: Dict[str, Any]) -> Role:
        """
        Create a new role.

        Args:
            role_data: A dictionary containing the data for the new role.
                Must include at minimum:
                - name: The name of the role (string)

                May also include:
                - description: A description of the role (string)
                - permissions: A list of permission strings (list of strings)

        Returns:
            A dictionary representing the created role.

        Examples:
            >>> new_role = client.roles.create_role({
            ...     "name": "Developer",
            ...     "description": "Developer role",
            ...     "permissions": ["read:blueprints", "write:entities"]
            ... })
        """
        # Use the base class create_resource method which handles response extraction
        return cast(Role, self.create_resource(role_data))

    def update_role(self, role_id: str, role_data: Dict[str, Any]) -> Role:
        """
        Update an existing role.

        Args:
            role_id: The identifier of the role to update.
            role_data: A dictionary with updated role data.
                May include any of the fields mentioned in create_role.

        Returns:
            A dictionary representing the updated role.

        Examples:
            >>> updated_role = client.roles.update_role(
            ...     "role-id",
            ...     {"name": "Senior Developer"}
            ... )
        """
        # Use the base class update_resource method which handles response extraction
        return cast(Role, self.update_resource(role_id, role_data))

    def delete_role(self, role_id: str) -> bool:
        """
        Delete a role.

        Args:
            role_id: The identifier of the role to delete.

        Returns:
            True if deletion was successful, otherwise False.

        Examples:
            >>> success = client.roles.delete_role("role-id")
            >>> if success:
            ...     print("Role deleted successfully")
        """
        # Use the base class delete_resource method
        return self.delete_resource(role_id)
