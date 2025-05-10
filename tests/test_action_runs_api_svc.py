import unittest
from unittest.mock import MagicMock

from pyport.action_runs.action_runs_api_svc import ActionRuns


class TestActionRuns(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.action_runs = ActionRuns(self.mock_client)

    def test_execute_self_service(self):
        # Setup
        action_id = "action123"
        expected_result = {"id": "run123", "status": "RUNNING"}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.execute_self_service(action_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "POST", f"actions/{action_id}/runs"
        )
        self.assertEqual(result, expected_result)

    def test_get_action_run(self):
        # Setup
        action_id = "action123"
        run_id = "run123"
        expected_result = {"id": run_id, "status": "COMPLETED"}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.get_action_run(action_id, run_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "GET", f"actions/runs/{run_id}"
        )
        self.assertEqual(result, expected_result)

    def test_get_action_runs_without_action_id(self):
        # Setup
        expected_result = {"runs": [{"id": "run1"}, {"id": "run2"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.get_action_runs()

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "GET", "actions/runs"
        )
        self.assertEqual(result, expected_result["runs"])

    def test_get_action_runs_with_action_id(self):
        # Setup
        action_id = "action123"
        expected_result = {"runs": [{"id": "run1"}, {"id": "run2"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.get_action_runs(action_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "GET", f"actions/{action_id}/runs"
        )
        self.assertEqual(result, expected_result["runs"])

    def test_create_action_run(self):
        # Setup
        run_data = {"action": "action123", "inputs": {"key": "value"}}
        expected_result = {"id": "run123", "status": "CREATED"}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.create_action_run(run_data)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "POST", "actions/runs", json=run_data
        )
        self.assertEqual(result, expected_result)

    def test_cancel_action_run(self):
        # Setup
        run_id = "run123"
        expected_result = {"id": run_id, "status": "CANCELED"}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.cancel_action_run(run_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "POST", f"actions/runs/{run_id}/approval", json={"status": "CANCELED"}
        )
        self.assertEqual(result, expected_result)

    def test_approve_action_run(self):
        # Setup
        run_id = "run123"
        expected_result = {"id": run_id, "status": "APPROVED"}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.approve_action_run(run_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "POST", f"actions/runs/{run_id}/approval", json={"status": "APPROVED"}
        )
        self.assertEqual(result, expected_result)

    def test_reject_action_run(self):
        # Setup
        run_id = "run123"
        expected_result = {"id": run_id, "status": "REJECTED"}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.reject_action_run(run_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "POST", f"actions/runs/{run_id}/approval", json={"status": "REJECTED"}
        )
        self.assertEqual(result, expected_result)

    def test_get_action_run_logs(self):
        # Setup
        run_id = "run123"
        expected_result = {"logs": ["log1", "log2"]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.get_action_run_logs(run_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "GET", f"actions/runs/{run_id}/logs"
        )
        self.assertEqual(result, expected_result)

    def test_get_action_run_approvers(self):
        # Setup
        run_id = "run123"
        expected_result = {"approvers": [{"id": "user1"}, {"id": "user2"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.action_runs.get_action_run_approvers(run_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "GET", f"actions/runs/{run_id}/approvers"
        )
        self.assertEqual(result, expected_result["approvers"])


if __name__ == "__main__":
    unittest.main()
