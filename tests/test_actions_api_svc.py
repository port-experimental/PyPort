import unittest
from unittest.mock import MagicMock, patch
from src.pyport.actions.actions_api_svc import Actions
from src.pyport.api_client import PortClient

class TestActionsService(unittest.TestCase):
    def setUp(self):
        # Patch _get_local_env_cred and _get_access_token to avoid environment dependency.
        patcher_env = patch('src.pyport.api_client.PortClient._get_local_env_cred', return_value=('dummy_id', 'dummy_secret'))
        self.addCleanup(patcher_env.stop)
        self.mock_get_local_env_cred = patcher_env.start()

        patcher_token = patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
        self.addCleanup(patcher_token.stop)
        self.mock_get_access_token = patcher_token.start()

        # Initialize a dummy PortClient and override its make_request method.
        self.client = PortClient(auto_refresh=False)
        self.client.make_request = MagicMock()
        self.actions = Actions(self.client)
        self.blueprint_id = "bp_123"
        self.action_id = "act_456"

    def test_get_actions(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"actions": [{"id": self.action_id}]}
        self.client.make_request.return_value = dummy_response

        result = self.actions.get_actions(self.blueprint_id)
        self.client.make_request.assert_called_once_with('GET', f"blueprints/{self.blueprint_id}/actions")
        self.assertEqual(result, [{"id": self.action_id}])

    def test_get_action(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"action": {"id": self.action_id}}
        self.client.make_request.return_value = dummy_response

        result = self.actions.get_action(self.blueprint_id, self.action_id)
        self.client.make_request.assert_called_once_with('GET', f"blueprints/{self.blueprint_id}/actions/{self.action_id}")
        self.assertEqual(result, {"id": self.action_id})

    def test_execute_action(self):
        payload = {"param": "value"}
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"result": "executed"}
        self.client.make_request.return_value = dummy_response

        result = self.actions.execute_action(self.blueprint_id, self.action_id, payload)
        self.client.make_request.assert_called_once_with(
            'POST', f"blueprints/{self.blueprint_id}/actions/{self.action_id}/execute", json=payload
        )
        self.assertEqual(result, {"result": "executed"})

    def test_delete_action(self):
        dummy_response = MagicMock()
        dummy_response.status_code = 204
        self.client.make_request.return_value = dummy_response

        result = self.actions.delete_action(self.blueprint_id, self.action_id)
        self.client.make_request.assert_called_once_with('DELETE', f"blueprints/{self.blueprint_id}/actions/{self.action_id}")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
