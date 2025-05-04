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

    # Blueprint Permissions Methods

    def get_blueprint_permissions(self, blueprint_identifier: str) -> Dict:
        """
        Retrieve permissions for a specific blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: A dictionary representing the blueprint permissions.
        """
        response = self._client.make_request('GET', f"blueprints/{blueprint_identifier}/permissions")
        return response.json().get("permissions", {})

    def update_blueprint_permissions(self, blueprint_identifier: str, permissions_data: Dict) -> Dict:
        """
        Update permissions for a specific blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param permissions_data: A dictionary containing updated permissions data.
        :return: A dictionary representing the updated blueprint permissions.
        """
        response = self._client.make_request('PUT', f"blueprints/{blueprint_identifier}/permissions", json=permissions_data)
        return response.json()

    # Blueprint Property Operations Methods

    def rename_blueprint_property(self, blueprint_identifier: str, property_name: str, rename_data: Dict) -> Dict:
        """
        Rename a property in a blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param property_name: The name of the property to rename.
        :param rename_data: A dictionary containing the new name for the property.
        :return: A dictionary representing the result of the rename operation.
        """
        response = self._client.make_request('POST', f"blueprints/{blueprint_identifier}/properties/{property_name}/rename", json=rename_data)
        return response.json()

    def rename_blueprint_mirror(self, blueprint_identifier: str, mirror_name: str, rename_data: Dict) -> Dict:
        """
        Rename a mirror in a blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param mirror_name: The name of the mirror to rename.
        :param rename_data: A dictionary containing the new name for the mirror.
        :return: A dictionary representing the result of the rename operation.
        """
        response = self._client.make_request('POST', f"blueprints/{blueprint_identifier}/mirror/{mirror_name}/rename", json=rename_data)
        return response.json()

    def rename_blueprint_relation(self, blueprint_identifier: str, relation_identifier: str, rename_data: Dict) -> Dict:
        """
        Rename a relation in a blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :param relation_identifier: The identifier of the relation to rename.
        :param rename_data: A dictionary containing the new name for the relation.
        :return: A dictionary representing the result of the rename operation.
        """
        response = self._client.make_request('POST', f"blueprints/{blueprint_identifier}/relations/{relation_identifier}/rename", json=rename_data)
        return response.json()

    def get_blueprint_system_structure(self, blueprint_identifier: str) -> Dict:
        """
        Retrieve the system structure for a specific blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: A dictionary representing the blueprint system structure.
        """
        response = self._client.make_request('GET', f"blueprints/system/{blueprint_identifier}/structure")
        return response.json().get("structure", {})
