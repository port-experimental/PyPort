import unittest
from unittest.mock import MagicMock
from src.pyport.migrations.migrations_api_svc import Migrations

class TestMigrations(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.migrations = Migrations(self.mock_client)

    def test_get_migrations(self):
        fake_migrations = [{"id": "mig1"}, {"id": "mig2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"migrations": fake_migrations}
        self.mock_client.make_request.return_value = mock_response

        result = self.migrations.get_migrations()
        self.mock_client.make_request.assert_called_once_with("GET", "migrations")
        self.assertEqual(result, fake_migrations)

    def test_get_migration(self):
        migration_id = "mig1"
        fake_migration = {"id": migration_id, "status": "completed"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"migration": fake_migration}
        self.mock_client.make_request.return_value = mock_response

        result = self.migrations.get_migration(migration_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"migrations/{migration_id}")
        self.assertEqual(result, fake_migration)

    def test_create_migration(self):
        migration_data = {"name": "New Migration"}
        fake_response_data = {"id": "mig_new", "name": "New Migration"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.migrations.create_migration(migration_data)
        self.mock_client.make_request.assert_called_once_with("POST", "migrations", json=migration_data)
        self.assertEqual(result, fake_response_data)

    def test_update_migration(self):
        migration_id = "mig1"
        migration_data = {"name": "Updated Migration"}
        fake_response_data = {"id": migration_id, "name": "Updated Migration"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.migrations.update_migration(migration_id, migration_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"migrations/{migration_id}", json=migration_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_migration(self):
        migration_id = "mig1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.migrations.delete_migration(migration_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"migrations/{migration_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
