from typing import Dict, List
from pyport.models.api_category import BaseResource


class Actions(BaseResource):
    """Actions API category"""

    def get_actions(self, blueprint_identifier: str) -> List[Dict]:
        """
        Retrieve all actions for a specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: A list of action dictionaries.
        """
        response = self._client.make_request('GET', f"blueprints/{blueprint_identifier}/actions")
        return response.json().get("actions", [])

    def get_action(self, blueprint_identifier: str, action_identifier: str) -> Dict:
        """
        Retrieve a single action by its identifier.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action.
        :return: A dictionary representing the action.
        """
        response = self._client.make_request('GET', f"blueprints/{blueprint_identifier}/actions/{action_identifier}")
        return response.json().get("action", {})

    def create_action(self, blueprint_identifier: str, action_data: Dict) -> Dict:
        """
        Create a new action under the specified blueprint.

        :param blueprint_identifier: The blueprint identifier.
        :param action_data: A dictionary containing data for the new action.
        :return: A dictionary representing the created action.
        """
        response = self._client.make_request('POST', f"blueprints/{blueprint_identifier}/actions", json=action_data)
        return response.json()

    def update_action(self, blueprint_identifier: str, action_identifier: str, action_data: Dict) -> Dict:
        """
        Update an existing action.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action to update.
        :param action_data: A dictionary containing updated data for the action.
        :return: A dictionary representing the updated action.
        """
        response = self._client.make_request('PUT', f"blueprints/{blueprint_identifier}/actions/{action_identifier}",
                                             json=action_data)
        return response.json()

    def delete_action(self, blueprint_identifier: str, action_identifier: str) -> bool:
        """
        Delete an action.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action to delete.
        :return: True if deletion was successful (e.g., status code 204), else False.
        """
        response = self._client.make_request('DELETE', f"blueprints/{blueprint_identifier}/actions/{action_identifier}")
        return response.status_code == 204

    def execute_action(self, blueprint_identifier: str, action_identifier: str, payload: Dict) -> Dict:
        """
        Execute a specific action by triggering its execution endpoint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param action_identifier: The identifier of the action to execute.
        :param payload: A dictionary containing additional parameters for executing the action.
        :return: A dictionary representing the execution result.
        """
        response = self._client.make_request(
            'POST', f"blueprints/{blueprint_identifier}/actions/{action_identifier}/execute", json=payload
        )
        return response.json()

    def get_action_status(self, blueprint_identifier: str, action_identifier: str) -> Dict:
        """
        Retrieve the status of a specific action.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action.
        :return: A dictionary representing the action's status.
        """
        response = self._client.make_request(
            'GET', f"blueprints/{blueprint_identifier}/actions/{action_identifier}/status"
        )
        return response.json().get("status", {})

    def cancel_action(self, blueprint_identifier: str, action_identifier: str) -> bool:
        """
        Cancel an in-progress action.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action.
        :return: True if cancellation was successful (e.g., status code 200), else False.
        """
        response = self._client.make_request(
            'POST', f"blueprints/{blueprint_identifier}/actions/{action_identifier}/cancel"
        )
        return response.status_code == 200
