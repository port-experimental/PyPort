from typing import Dict, List

from pyport.models.api_category import BaseResource


class Blueprints(BaseResource):
    """Blueprints API category"""

    def get_blueprints(self) -> List[Dict]:
        """Get all blueprints"""
        response = self._client.make_request('GET', 'blueprints')
        # Corrected to call .json() only once.
        return response.json().get("blueprints", [])

    def get_blueprint(self, blueprint_identifier: str) -> Dict:
        """
        Get a specific blueprint by its identifier.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: A dictionary representing the blueprint.
        """
        response = self._client.make_request('GET', f"blueprints/{blueprint_identifier}")
        # Adjust the key "blueprint" if your API structure differs.
        return response.json().get("blueprint", {})

    def create_blueprint(self, blueprint_data: Dict) -> Dict:
        """
        Create a new blueprint.

        :param blueprint_data: A dictionary containing the data for the new blueprint.
        :return: A dictionary representing the created blueprint.
        """
        response = self._client.make_request('POST', 'blueprints', json=blueprint_data)
        return response.json()

    def update_blueprint(self, blueprint_identifier: str, blueprint_data: Dict) -> Dict:
        """
        Update an existing blueprint.

        :param blueprint_identifier: The identifier of the blueprint to update.
        :param blueprint_data: A dictionary containing the updated data for the blueprint.
        :return: A dictionary representing the updated blueprint.
        """
        response = self._client.make_request('PUT', f"blueprints/{blueprint_identifier}", json=blueprint_data)
        return response.json()

    def delete_blueprint(self, blueprint_identifier: str) -> bool:
        """
        Delete a blueprint.

        :param blueprint_identifier: The identifier of the blueprint to delete.
        :return: True if deletion was successful (e.g., status code 204), otherwise False.
        """
        response = self._client.make_request('DELETE', f"blueprints/{blueprint_identifier}")
        return response.status_code == 204
