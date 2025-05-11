from typing import Dict, List
from ..models.api_category import BaseResource


class Actions(BaseResource):
    """Actions API category"""

    def get_actions(self, blueprint_identifier: str = None) -> List[Dict]:
        """
        Retrieve all actions for a specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: A list of action dictionaries.
        """
        endpoint = "actions"
        if blueprint_identifier:
            endpoint = f"blueprints/{blueprint_identifier}/actions"
        response = self._client.make_request('GET', endpoint)
        return response.json().get("actions", [])

    def get_action(self, action_id: str) -> Dict:
        """
        Retrieve a single action by its identifier.

        :param action_id: The identifier of the action.
        :return: A dictionary representing the action.
        """
        response = self._client.make_request('GET', f"actions/{action_id}")
        return response.json().get("action", {})

    def create_action(self, action_data: Dict) -> Dict:
        """
        Create a new action.

        :param action_data: A dictionary containing data for the new action.
        :return: A dictionary representing the created action.
        """
        response = self._client.make_request('POST', "actions", json=action_data)
        return response.json()

    def update_action(self, action_identifier: str, action_data: Dict) -> Dict:
        """
        Update an existing action.

        :param action_identifier: The identifier of the action to update.
        :param action_data: A dictionary containing updated data for the action.
        :return: A dictionary representing the updated action.
        """
        response = self._client.make_request('PUT', f"actions/{action_identifier}",
                                             json=action_data)
        return response.json()

    def delete_action(self, action_id: str) -> bool:
        """
        Delete an action.

        :param action_id: The identifier of the action to delete.
        :return: True if deletion was successful (e.g., status code 204), else False.
        """
        response = self._client.make_request('DELETE', f"actions/{action_id}")
        return response.status_code == 204

    def get_action_permissions(self, action_identifier: str) -> Dict:
        """
        Retrieve the permissions of a specific action.

        :param action_identifier: The identifier of the action.
        :return: A dictionary representing the action's permissions.
        """
        response = self._client.make_request(
            'GET', f"actions/{action_identifier}/permissions"
        )
        return response.json().get("status", {})

    def update_action_permissions(self, action_identifier: str) -> bool:
        """
        Update the permissions of a specific action.

        :param action_identifier: The identifier of the action.
        :return: True if the update was successful (e.g., status code 200), else False.
        """
        response = self._client.make_request(
            'PATCH', f"actions/{action_identifier}/permissions"
        )
        return response.status_code == 200
