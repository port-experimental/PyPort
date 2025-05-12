from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class Migrations(BaseAPIService):
    """Migrations API category for managing migrations.

    This class provides methods for interacting with the Migrations API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all migrations
        >>> migrations = client.migrations.get_migrations()
        >>> # Get a specific migration
        >>> migration = client.migrations.get_migration("migration-id")
    """

    def __init__(self, client):
        """Initialize the Migrations API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="migrations", response_key="migration")

    def get_migrations(self, page: Optional[int] = None, per_page: Optional[int] = None,
                       params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all migrations.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of migration dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        return self.get_all(page=page, per_page=per_page, params=params)

    def get_migration(self, migration_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific migration.

        Args:
            migration_id: The identifier of the migration.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the migration.

        Raises:
            PortResourceNotFoundError: If the migration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.get_by_id(migration_id, params=params)

    def create_migration(self, migration_data: Dict[str, Any],
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new migration.

        Args:
            migration_data: A dictionary containing migration data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created migration.

        Raises:
            PortValidationError: If the migration data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("POST", "migrations", json=migration_data)
        return response.json()

    def update_migration(self, migration_id: str, migration_data: Dict[str, Any],
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing migration.

        Args:
            migration_id: The identifier of the migration to update.
            migration_data: A dictionary with updated migration data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated migration.

        Raises:
            PortResourceNotFoundError: If the migration does not exist.
            PortValidationError: If the migration data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("PUT", f"migrations/{migration_id}", json=migration_data)
        return response.json()

    def delete_migration(self, migration_id: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a migration.

        Args:
            migration_id: The identifier of the migration to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the migration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.delete_resource(migration_id, params=params)

    def cancel_migration(self, migration_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Cancel an in-progress migration.

        Args:
            migration_id: The identifier of the migration to cancel.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the result of the cancellation.

        Raises:
            PortResourceNotFoundError: If the migration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("migrations", migration_id, "cancel")

        # Make the request
        response = self._make_request_with_params('POST', endpoint, params=params)
        return response
