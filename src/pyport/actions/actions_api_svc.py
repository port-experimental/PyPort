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
        response = self._client.make_request('GET', "/v1/actions")
        return response.json().get("actions", [])

    def get_action(self, action_identifier: str) -> Dict:
        """
        Retrieve a single action by its identifier.

        :param action_identifier: The identifier of the action.
        :return: A dictionary representing the action.
        """
        response = self._client.make_request('GET', f"/v1/actions/{action_identifier}")
        return response.json().get("action", {})

    def create_action(self, action_data: Dict) -> Dict:
        """
        Create a new action under the specified blueprint.

        :param blueprint_identifier: The blueprint identifier.
        :param action_data: A dictionary containing data for the new action.
        :return: A dictionary representing the created action.
        """
        response = self._client.make_request('POST', f"/v1/actions", json=action_data)
        return response.json()

    def update_action(self, blueprint_identifier: str, action_identifier: str, action_data: Dict) -> Dict:
        """
        Update an existing action.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action to update.
        :param action_data: A dictionary containing updated data for the action.
        :return: A dictionary representing the updated action.
        """
        response = self._client.make_request('PUT', f"/v1/actions/{action_identifier}",
                                             json=action_data)
        return response.json()

    def delete_action(self, blueprint_identifier: str, action_identifier: str) -> bool:
        """
        Delete an action.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action to delete.
        :return: True if deletion was successful (e.g., status code 204), else False.
        """
        response = self._client.make_request('DELETE', f"/v1/actions/{action_identifier}")
        return response.status_code == 204

    def get_action_permissions(self, blueprint_identifier: str, action_identifier: str) -> Dict:
        """
        Retrieve the status of a specific action.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action.
        :return: A dictionary representing the action's status.
        """
        response = self._client.make_request(
            'GET', f"/v1/actions/{action_identifier}/permissions"
        )
        return response.json().get("status", {})

    def update_action_permissions(self, blueprint_identifier: str, action_identifier: str) -> bool:
        """
        Cancel an in-progress action.

        :param blueprint_identifier: The blueprint identifier.
        :param action_identifier: The identifier of the action.
        :return: True if cancellation was successful (e.g., status code 200), else False.
        """
        response = self._client.make_request(
            'POST', f"/v1/actions/{action_identifier}/permissions"
        )
        return response.status_code == 200
