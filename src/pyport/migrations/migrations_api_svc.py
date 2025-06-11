from typing import Dict, Optional, Any

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
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve all migrations.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing migrations data.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Make the request
        response = self._make_request_with_params('GET', "migrations", params=all_params)
        return response

    def get_migration(self, migration_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve a specific migration by its identifier.

        Args:
            migration_id: The identifier of the migration.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the migration.

        Raises:
            PortResourceNotFoundError: If the migration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("migrations", migration_id)
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

    def cancel_migration(self, migration_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Cancel a migration.

        Args:
            migration_id: The identifier of the migration to cancel.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the cancellation result.

        Raises:
            PortResourceNotFoundError: If the migration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("migrations", migration_id, "cancel")
        response = self._make_request_with_params('POST', endpoint, params=params)
        return response
