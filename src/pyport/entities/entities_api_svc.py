from typing import Dict, List

from pyport.models.api_category import BaseResource


class Entities(BaseResource):
    """Entities API category for interacting with entity endpoints."""

    def get_entities(self, blueprint_identifier: str) -> List[Dict]:
        """
        Retrieve a list of all entities for the specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: A list of entity dictionaries.
        """
        response = self._client.make_request('GET', f"blueprints/{blueprint_identifier}/entities")
        # Assuming the JSON response looks like: {"status": "success", "entities": [...] }
        return response.json().get("entities", [])

    def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> Dict:
        """
        Retrieve a specific entity by its identifier.

        :param blueprint_identifier: The identifier of the blueprint.
        :param entity_identifier: The identifier of the entity.
        :return: A dictionary representing the entity.
        """
        response = self._client.make_request(
            'GET', f"blueprints/{blueprint_identifier}/entities/{entity_identifier}"
        )
        # Adjust key ("entity") as needed based on your API's response format
        return response.json().get("entity", {})

    def create_entity(self, blueprint_identifier: str, entity_data: Dict) -> Dict:
        """
        Create a new entity under the specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param entity_data: A dictionary containing the data for the new entity.
        :return: A dictionary representing the created entity.
        """
        response = self._client.make_request(
            'POST', f"blueprints/{blueprint_identifier}/entities", json=entity_data
        )
        return response.json()

    def update_entity(self, blueprint_identifier: str, entity_identifier: str, entity_data: Dict) -> Dict:
        """
        Update an existing entity.

        :param blueprint_identifier: The identifier of the blueprint.
        :param entity_identifier: The identifier of the entity to update.
        :param entity_data: A dictionary containing the updated data for the entity.
        :return: A dictionary representing the updated entity.
        """
        response = self._client.make_request(
            'PUT', f"blueprints/{blueprint_identifier}/entities/{entity_identifier}", json=entity_data
        )
        return response.json()

    def delete_entity(self, blueprint_identifier: str, entity_identifier: str) -> bool:
        """
        Delete an entity from the specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param entity_identifier: The identifier of the entity to delete.
        :return: True if deletion was successful (e.g., status code 204), otherwise False.
        """
        response = self._client.make_request(
            'DELETE', f"blueprints/{blueprint_identifier}/entities/{entity_identifier}"
        )
        # Assuming a successful deletion returns HTTP status 204 No Content
        return response.status_code == 204
