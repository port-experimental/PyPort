import unittest
from unittest.mock import MagicMock
from pyport.migrations.migrations_api_svc import Migrations

class TestMigrations(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.migrations = Migrations(self.mock_client)

    def test_get_migrations(self):
        expected_result = {"migrations": [{"id": "mig1"}, {"id": "mig2"}]}
        self.migrations._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.migrations.get_migrations()
        self.migrations._make_request_with_params.assert_called_once_with('GET', 'migrations', params={})
        self.assertEqual(result, expected_result)

    def test_get_migration(self):
        migration_id = "mig1"
        expected_result = {"migration": {"id": migration_id, "status": "completed"}}
        self.migrations._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.migrations.get_migration(migration_id)
        self.migrations._make_request_with_params.assert_called_once_with('GET', f'migrations/{migration_id}', params=None)
        self.assertEqual(result, expected_result)

    def test_cancel_migration(self):
        migration_id = "mig123"
        expected_result = {"id": migration_id, "status": "cancelled"}
        self.migrations._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.migrations.cancel_migration(migration_id)
        self.migrations._make_request_with_params.assert_called_once_with('POST', f'migrations/{migration_id}/cancel', params=None)
        self.assertEqual(result, expected_result)



if __name__ == "__main__":
    unittest.main()
