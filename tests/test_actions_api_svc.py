import unittest
from unittest.mock import MagicMock

from pyport.actions.actions_api_svc import Actions


class TestActions(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.actions = Actions(self.mock_client)

    def test_get_actions(self):
        # Setup
        expected_actions = [{"id": "action1"}, {"id": "action2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"actions": expected_actions}
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.actions.get_actions()

        # Assert
        self.mock_client.make_request.assert_called_once_with("GET", "actions")
        self.assertEqual(result, expected_actions)

    def test_get_action(self):
        # Setup
        action_id = "action123"
        expected_action = {"id": action_id, "name": "Test Action"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"action": expected_action}
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.actions.get_action(action_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with("GET", f"actions/{action_id}")
        self.assertEqual(result, expected_action)

    def test_create_action(self):
        # Setup
        action_data = {"identifier": "action123", "title": "Test Action"}
        expected_result = {"id": "action123", "name": "Test Action"}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.actions.create_action(action_data)

        # Assert
        self.mock_client.make_request.assert_called_once_with("POST", "actions", json=action_data)
        self.assertEqual(result, expected_result)

    def test_delete_action(self):
        # Setup
        action_id = "action123"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.actions.delete_action(action_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with("DELETE", f"actions/{action_id}")
        self.assertTrue(result)

        # Test with non-204 status code
        mock_response.status_code = 200
        result = self.actions.delete_action(action_id)
        self.assertFalse(result)

    def test_get_action_permissions(self):
        # Setup
        action_id = "action123"
        expected_status = {"allowed": True}
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": expected_status}
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.actions.get_action_permissions(action_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with("GET", f"actions/{action_id}/permissions")
        self.assertEqual(result, expected_status)

    def test_update_action_permissions(self):
        # Setup
        action_id = "action123"
        mock_response = MagicMock()
        mock_response.status_code = 200
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.actions.update_action_permissions(action_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with("PATCH", f"actions/{action_id}/permissions")
        self.assertTrue(result)

        # Test with non-200 status code
        mock_response.status_code = 400
        result = self.actions.update_action_permissions(action_id)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
