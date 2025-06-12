import unittest
from unittest.mock import MagicMock

from pyport.action_runs.action_runs_api_svc import ActionRuns


class TestActionRuns(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.action_runs = ActionRuns(self.mock_client)

    def test_get_action_runs_basic(self):
        # Setup
        expected_result = {"runs": [{"id": "run1"}, {"id": "run2"}]}
        self.action_runs._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.action_runs.get_action_runs()

        # Assert
        self.action_runs._make_request_with_params.assert_called_once_with(
            'GET', 'actions/runs', params={}
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
        result = self.action_runs.get_action_run(run_id=run_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with(
            "GET", f"actions/runs/{run_id}"
        )
        self.assertEqual(result, expected_result)

    def test_get_action_runs_with_pagination(self):
        # Setup
        expected_result = {"runs": [{"id": "run1"}, {"id": "run2"}]}
        self.action_runs._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.action_runs.get_action_runs(page=1, per_page=10)

        # Assert
        self.action_runs._make_request_with_params.assert_called_once_with(
            'GET', 'actions/runs', params={'page': 1, 'per_page': 10}
        )
        self.assertEqual(result, expected_result)

    def test_get_action_run(self):
        # Setup
        run_id = "run123"
        expected_result = {"id": run_id, "status": "COMPLETED"}
        self.action_runs._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.action_runs.get_action_run(run_id)

        # Assert
        self.action_runs._make_request_with_params.assert_called_once_with(
            'GET', f'actions/runs/{run_id}', params=None
        )
        self.assertEqual(result, expected_result)

    def test_update_action_run(self):
        # Setup
        run_id = "run123"
        run_data = {"status": "COMPLETED"}
        expected_result = {"id": run_id, "status": "COMPLETED"}
        self.action_runs._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.action_runs.update_action_run(run_id, run_data)

        # Assert
        self.action_runs._make_request_with_params.assert_called_once_with(
            'PATCH', f'actions/runs/{run_id}', json=run_data, params=None
        )
        self.assertEqual(result, expected_result)

    def test_approve_action_run(self):
        # Setup
        run_id = "run123"
        expected_result = {"id": run_id, "status": "APPROVED"}
        self.action_runs._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.action_runs.approve_action_run(run_id)

        # Assert
        self.action_runs._make_request_with_params.assert_called_once_with(
            'PATCH', f'actions/runs/{run_id}/approval', json={}, params=None
        )
        self.assertEqual(result, expected_result)

    def test_add_action_run_log(self):
        # Setup
        run_id = "run123"
        log_data = {"message": "Test log", "level": "INFO"}
        expected_result = {"success": True}
        self.action_runs._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.action_runs.add_action_run_log(run_id, log_data)

        # Assert
        self.action_runs._make_request_with_params.assert_called_once_with(
            'POST', f'actions/runs/{run_id}/logs', json=log_data, params=None
        )
        self.assertEqual(result, expected_result)

    def test_get_action_run_logs(self):
        # Setup
        run_id = "run123"
        expected_result = {"logs": ["log1", "log2"]}
        self.action_runs._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.action_runs.get_action_run_logs(run_id)

        # Assert
        self.action_runs._make_request_with_params.assert_called_once_with(
            'GET', f'actions/runs/{run_id}/logs', params=None
        )
        self.assertEqual(result, expected_result)

    def test_get_action_run_approvers(self):
        # Setup
        run_id = "run123"
        expected_result = {"approvers": [{"id": "user1"}, {"id": "user2"}]}
        self.action_runs._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.action_runs.get_action_run_approvers(run_id)

        # Assert
        self.action_runs._make_request_with_params.assert_called_once_with(
            'GET', f'actions/runs/{run_id}/approvers', params=None
        )
        self.assertEqual(result, expected_result)




if __name__ == "__main__":
    unittest.main()
