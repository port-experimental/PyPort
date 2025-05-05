from typing import Dict, List
from pyport.models.api_category import BaseResource


class ActionRuns(BaseResource):
    """Action Runs API category for managing action execution runs."""

    def execute_self_service(self, action_id: str) -> Dict:
        """
        Execute a self-service action.

        :param action_id: The identifier of the action to execute.
        :return: A dictionary containing the execution result.
        """
        response = self._client.make_request("POST", f"actions/{action_id}/runs")
        return response.json()

    def get_action_run(self, action_id: str, run_id: str) -> Dict:
        """
        Retrieve details of a specific action run.

        :param action_id: The identifier of the action.
        :param run_id: The identifier of the run.
        :return: A dictionary representing the action run.
        """
        response = self._client.make_request("GET", f"actions/runs/{run_id}")
        return response.json()

    def get_action_runs(self, action_id: str = None) -> List[Dict]:
        """
        Retrieve all action runs, optionally filtered by action ID.

        :param action_id: Optional identifier of the action to filter runs.
        :return: A list of action run dictionaries.
        """
        endpoint = "actions/runs"
        if action_id:
            endpoint = f"actions/{action_id}/runs"
        response = self._client.make_request("GET", endpoint)
        return response.json().get("runs", [])

    def create_action_run(self, run_data: Dict) -> Dict:
        """
        Create a new action run.

        :param run_data: A dictionary containing the action run data.
        :return: A dictionary representing the created action run.
        """
        response = self._client.make_request("POST", "actions/runs", json=run_data)
        return response.json()

    def cancel_action_run(self, run_id: str) -> Dict:
        """
        Cancel an in-progress action run.

        :param run_id: The identifier of the run to cancel.
        :return: A dictionary representing the result of the cancellation.
        """
        response = self._client.make_request("POST", f"actions/runs/{run_id}/approval", json={"status": "CANCELED"})
        return response.json()

    def approve_action_run(self, run_id: str) -> Dict:
        """
        Approve an action run that requires approval.

        :param run_id: The identifier of the run to approve.
        :return: A dictionary representing the result of the approval.
        """
        response = self._client.make_request("POST", f"actions/runs/{run_id}/approval", json={"status": "APPROVED"})
        return response.json()

    def reject_action_run(self, run_id: str) -> Dict:
        """
        Reject an action run that requires approval.

        :param run_id: The identifier of the run to reject.
        :return: A dictionary representing the result of the rejection.
        """
        response = self._client.make_request("POST", f"actions/runs/{run_id}/approval", json={"status": "REJECTED"})
        return response.json()

    def get_action_run_logs(self, run_id: str) -> Dict:
        """
        Retrieve logs for a specific action run.

        :param run_id: The identifier of the run.
        :return: A dictionary containing the logs of the action run.
        """
        response = self._client.make_request("GET", f"actions/runs/{run_id}/logs")
        return response.json()

    def get_action_run_approvers(self, run_id: str) -> List[Dict]:
        """
        Retrieve approvers for a specific action run.

        :param run_id: The identifier of the run.
        :return: A list of approver dictionaries.
        """
        response = self._client.make_request("GET", f"actions/runs/{run_id}/approvers")
        return response.json().get("approvers", [])
