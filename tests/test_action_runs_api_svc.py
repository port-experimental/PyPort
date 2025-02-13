import unittest
from unittest.mock import MagicMock
from src.pyport.action_runs.action_runs_api_svc import ActionRuns

class TestActionRuns(unittest.TestCase):
    def setUp(self):
        # Create a dummy client with a mocked make_request method.
        self.mock_client = MagicMock()
        self.action_runs = ActionRuns(self.mock_client)

    def test_get_action_runs(self):
        action_id = "action1"
        fake_runs = [{"id": "run1"}, {"id": "run2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"runs": fake_runs}
        self.mock_client.make_request.return_value = mock_response

        result = self.action_runs.get_action_runs(action_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"actions/{action_id}/runs")
        self.assertEqual(result, fake_runs)

    def test_get_action_run(self):
        action_id = "action1"
        run_id = "run1"
        fake_run = {"id": run_id, "status": "completed"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"run": fake_run}
        self.mock_client.make_request.return_value = mock_response

        result = self.action_runs.get_action_run(action_id, run_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"actions/{action_id}/runs/{run_id}")
        self.assertEqual(result, fake_run)

    def test_create_action_run(self):
        action_id = "action1"
        run_data = {"param": "value"}
        fake_response_data = {"id": "run_new", "status": "pending"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.action_runs.create_action_run(action_id, run_data)
        self.mock_client.make_request.assert_called_once_with("POST", f"actions/{action_id}/runs", json=run_data)
        self.assertEqual(result, fake_response_data)

    def test_cancel_action_run(self):
        action_id = "action1"
        run_id = "run1"
        mock_response = MagicMock()
        mock_response.status_code = 200
        self.mock_client.make_request.return_value = mock_response

        result = self.action_runs.cancel_action_run(action_id, run_id)
        self.mock_client.make_request.assert_called_once_with("POST", f"actions/{action_id}/runs/{run_id}/cancel")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
