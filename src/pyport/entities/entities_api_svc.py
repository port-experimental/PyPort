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

    def create_entity(self, blueprint_identifier: str, entity_data: Dict,
                      upsert: bool = False,
                      validation_only: bool = False,
                      create_missing_related_entities: bool = False,
                      merge: bool = False) -> Dict:
        """
        Create a new entity under the specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param entity_data: A dictionary containing the data for the new entity.
        :return: A dictionary representing the created entity.
        """
        url = (f"blueprints/{blueprint_identifier}/entities?"
               f"upsert={upsert}&"
               f"validation_only={validation_only}&"
               f"create_missing_related_entities={create_missing_related_entities}&"
               f"merge={merge}")
        response = self._client.make_request('POST', url.lower(), json=entity_data)
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

    def create_entities_bulk(self, blueprint_identifier: str, entities_data: List[Dict]) -> Dict:
        """
        Create multiple entities in bulk for the specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param entities_data: A list of dictionaries, each containing data for a new entity.
        :return: A dictionary representing the result of the bulk creation.
        """
        response = self._client.make_request(
            'POST', f"blueprints/{blueprint_identifier}/entities/bulk", json={"entities": entities_data}
        )
        return response.json()

    def get_entities_count(self, blueprint_identifier: str) -> int:
        """
        Get the count of entities for the specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: The count of entities.
        """
        response = self._client.make_request(
            'GET', f"blueprints/{blueprint_identifier}/entities-count"
        )
        return response.json().get("count", 0)

    def get_all_entities(self, blueprint_identifier: str) -> List[Dict]:
        """
        Retrieve all entities for the specified blueprint, including related entities.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: A list of entity dictionaries.
        """
        response = self._client.make_request(
            'GET', f"blueprints/{blueprint_identifier}/all-entities"
        )
        return response.json().get("entities", [])

    # Entity Search and Aggregation Methods

    def search_entities(self, search_data: Dict) -> List[Dict]:
        """
        Search for entities across all blueprints.

        :param search_data: A dictionary containing search criteria.
        :return: A list of matching entity dictionaries.
        """
        response = self._client.make_request('POST', "entities/search", json=search_data)
        return response.json().get("entities", [])

    def search_blueprint_entities(self, blueprint_identifier: str, search_data: Dict) -> List[Dict]:
        """
        Search for entities within a specific blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param search_data: A dictionary containing search criteria.
        :return: A list of matching entity dictionaries.
        """
        response = self._client.make_request(
            'POST', f"blueprints/{blueprint_identifier}/entities/search", json=search_data
        )
        return response.json().get("entities", [])

    def aggregate_entities(self, aggregation_data: Dict) -> Dict:
        """
        Aggregate entities based on specified criteria.

        :param aggregation_data: A dictionary containing aggregation criteria.
        :return: A dictionary containing the aggregation results.
        """
        response = self._client.make_request('POST', "entities/aggregate", json=aggregation_data)
        return response.json()

    def aggregate_entities_over_time(self, aggregation_data: Dict) -> Dict:
        """
        Aggregate entities over time based on specified criteria.

        :param aggregation_data: A dictionary containing aggregation criteria.
        :return: A dictionary containing the time-based aggregation results.
        """
        response = self._client.make_request('POST', "entities/aggregate-over-time", json=aggregation_data)
        return response.json()

    def get_entity_properties_history(self, history_data: Dict) -> Dict:
        """
        Retrieve the history of entity properties.

        :param history_data: A dictionary containing criteria for retrieving property history.
        :return: A dictionary containing the property history.
        """
        response = self._client.make_request('POST', "entities/properties-history", json=history_data)
        return response.json()
