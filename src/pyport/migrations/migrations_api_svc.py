from typing import Dict, List
from pyport.models.api_category import BaseResource


class Migrations(BaseResource):
    """Migrations API category for managing migrations."""

    def get_migrations(self) -> List[Dict]:
        """
        Retrieve all migrations.

        :return: A list of migration dictionaries.
        """
        response = self._client.make_request("GET", "migrations")
        return response.json().get("migrations", [])

    def get_migration(self, migration_id: str) -> Dict:
        """
        Retrieve details for a specific migration.

        :param migration_id: The identifier of the migration.
        :return: A dictionary representing the migration.
        """
        response = self._client.make_request("GET", f"migrations/{migration_id}")
        return response.json().get("migration", {})

    def create_migration(self, migration_data: Dict) -> Dict:
        """
        Create a new migration.

        :param migration_data: A dictionary containing migration data.
        :return: A dictionary representing the newly created migration.
        """
        response = self._client.make_request("POST", "migrations", json=migration_data)
        return response.json()

    def update_migration(self, migration_id: str, migration_data: Dict) -> Dict:
        """
        Update an existing migration.

        :param migration_id: The identifier of the migration to update.
        :param migration_data: A dictionary with updated migration data.
        :return: A dictionary representing the updated migration.
        """
        response = self._client.make_request("PUT", f"migrations/{migration_id}", json=migration_data)
        return response.json()

    def delete_migration(self, migration_id: str) -> bool:
        """
        Delete a migration.

        :param migration_id: The identifier of the migration to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"migrations/{migration_id}")
        return response.status_code == 204
