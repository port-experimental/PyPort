from typing import Dict, List
from pyport.models.api_category import BaseResource


class Integrations(BaseResource):
    """Integrations API category for managing third-party integrations."""

    def get_integrations(self) -> List[Dict]:
        """
        Retrieve all integrations.

        :return: A list of integration dictionaries.
        """
        response = self._client.make_request("GET", "integrations")
        return response.json().get("integrations", [])

    def get_integration(self, integration_id: str) -> Dict:
        """
        Retrieve details for a specific integration.

        :param integration_id: The identifier of the integration.
        :return: A dictionary representing the integration.
        """
        response = self._client.make_request("GET", f"integrations/{integration_id}")
        return response.json().get("integration", {})

    def create_integration(self, integration_data: Dict) -> Dict:
        """
        Create a new integration.

        :param integration_data: A dictionary containing integration data.
        :return: A dictionary representing the newly created integration.
        """
        response = self._client.make_request("POST", "integrations", json=integration_data)
        return response.json()

    def update_integration(self, integration_id: str, integration_data: Dict) -> Dict:
        """
        Update an existing integration.

        :param integration_id: The identifier of the integration to update.
        :param integration_data: A dictionary containing the updated data.
        :return: A dictionary representing the updated integration.
        """
        response = self._client.make_request("PUT", f"integrations/{integration_id}", json=integration_data)
        return response.json()

    def delete_integration(self, integration_id: str) -> bool:
        """
        Delete an integration.

        :param integration_id: The identifier of the integration to delete.
        :return: True if deletion was successful (HTTP 204), otherwise False.
        """
        response = self._client.make_request("DELETE", f"integrations/{integration_id}")
        return response.status_code == 204
