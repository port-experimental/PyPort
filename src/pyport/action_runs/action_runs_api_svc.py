from typing import Dict, List
from pyport.models.api_category import BaseResource


class ActionRuns(BaseResource):
    """Action Runs API category for managing action execution runs."""

    def execute_self_service(self, action_id: str) -> List[Dict]:
        """
        Retrieve all runs for a given action.

        :param action_id: The identifier of the action.
        :return: A list of run dictionaries.
        """
        response = self._client.make_request("GET", f"actions/{action_id}/runs")
        return response.json().get("runs", [])

    def get_action_run(self, action_id: str, run_id: str) -> Dict:
        """
        Retrieve details of a specific action run.

        :param action_id: The identifier of the action.
        :param run_id: The identifier of the run.
        :return: A dictionary representing the action run.
        """
        response = self._client.make_request("GET", f"actions/{action_id}/runs/{run_id}")
        return response.json().get("run", {})
