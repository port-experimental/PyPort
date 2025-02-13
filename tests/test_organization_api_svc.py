from typing import Dict, List
from src.pyport.models.api_category import BaseResource


class Organizations(BaseResource):
    """Organizations API category for managing organizations."""

    def get_organizations(self) -> List[Dict]:
        """
        Retrieve all organizations.

        :return: A list of organization dictionaries.
        """
        response = self._client.make_request("GET", "organizations")
        return response.json().get("organizations", [])

    def get_organization(self, organization_id: str) -> Dict:
        """
        Retrieve details for a specific organization.

        :param organization_id: The identifier of the organization.
        :return: A dictionary representing the organization.
        """
        response = self._client.make_request("GET", f"organizations/{organization_id}")
        return response.json().get("organization", {})

    def create_organization(self, organization_data: Dict) -> Dict:
        """
        Create a new organization.

        :param organization_data: A dictionary containing organization data.
        :return: A dictionary representing the newly created organization.
        """
        response = self._client.make_request("POST", "organizations", json=organization_data)
        return response.json()

    def update_organization(self, organization_id: str, organization_data: Dict) -> Dict:
        """
        Update an existing organization.

        :param organization_id: The identifier of the organization to update.
        :param organization_data: A dictionary with updated organization data.
        :return: A dictionary representing the updated organization.
        """
        response = self._client.make_request("PUT", f"organizations/{organization_id}", json=organization_data)
        return response.json()

    def delete_organization(self, organization_id: str) -> bool:
        """
        Delete an organization.

        :param organization_id: The identifier of the organization to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"organizations/{organization_id}")
        return response.status_code == 204
