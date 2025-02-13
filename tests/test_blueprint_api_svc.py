import unittest
from unittest.mock import MagicMock, patch
from src.pyport.blueprints.blueprint_api_svc import Blueprints
from src.pyport.api_client import PortClient

class TestBlueprintsService(unittest.TestCase):
    def setUp(self):
        patcher_env = patch('src.pyport.api_client.PortClient._get_local_env_cred', return_value=('dummy_id', 'dummy_secret'))
        self.addCleanup(patcher_env.stop)
        self.mock_get_local_env_cred = patcher_env.start()

        patcher_token = patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
        self.addCleanup(patcher_token.stop)
        self.mock_get_access_token = patcher_token.start()

        self.client = PortClient(auto_refresh=False)
        self.client.make_request = MagicMock()
        self.blueprints = Blueprints(self.client)
        self.blueprint_id = "bp_123"

    def test_get_blueprints(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"blueprints": [{"id": self.blueprint_id}]}
        self.client.make_request.return_value = dummy_response

        result = self.blueprints.get_blueprints()
        self.client.make_request.assert_called_once_with('GET', 'blueprints')
        self.assertEqual(result, [{"id": self.blueprint_id}])

    def test_get_blueprint(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"blueprint": {"id": self.blueprint_id}}
        self.client.make_request.return_value = dummy_response

        result = self.blueprints.get_blueprint(self.blueprint_id)
        self.client.make_request.assert_called_once_with('GET', f"blueprints/{self.blueprint_id}")
        self.assertEqual(result, {"id": self.blueprint_id})

    def test_create_blueprint(self):
        blueprint_data = {"name": "Test Blueprint"}
        dummy_response = MagicMock()
        dummy_response.json.return_value = blueprint_data
        self.client.make_request.return_value = dummy_response

        result = self.blueprints.create_blueprint(blueprint_data)
        self.client.make_request.assert_called_once_with('POST', 'blueprints', json=blueprint_data)
        self.assertEqual(result, blueprint_data)

    def test_delete_blueprint(self):
        dummy_response = MagicMock()
        dummy_response.status_code = 204
        self.client.make_request.return_value = dummy_response

        result = self.blueprints.delete_blueprint(self.blueprint_id)
        self.client.make_request.assert_called_once_with('DELETE', f"blueprints/{self.blueprint_id}")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
