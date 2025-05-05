from typing import Dict, List
from pyport.models.api_category import BaseResource


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

    # Organization Secrets Methods

    def get_organization_secrets(self) -> List[Dict]:
        """
        Retrieve all organization secrets.

        :return: A list of secret dictionaries.
        """
        response = self._client.make_request("GET", "organization/secrets")
        return response.json().get("secrets", [])

    def get_organization_secret(self, secret_name: str) -> Dict:
        """
        Retrieve details for a specific organization secret.

        :param secret_name: The name of the secret.
        :return: A dictionary representing the secret.
        """
        response = self._client.make_request("GET", f"organization/secrets/{secret_name}")
        return response.json().get("secret", {})

    def create_organization_secret(self, secret_data: Dict) -> Dict:
        """
        Create a new organization secret.

        :param secret_data: A dictionary containing secret data (name and value).
        :return: A dictionary representing the newly created secret.
        """
        response = self._client.make_request("POST", "organization/secrets", json=secret_data)
        return response.json()

    def update_organization_secret(self, secret_name: str, secret_data: Dict) -> Dict:
        """
        Update an existing organization secret.

        :param secret_name: The name of the secret to update.
        :param secret_data: A dictionary with updated secret data.
        :return: A dictionary representing the updated secret.
        """
        response = self._client.make_request("PUT", f"organization/secrets/{secret_name}", json=secret_data)
        return response.json()

    def delete_organization_secret(self, secret_name: str) -> bool:
        """
        Delete an organization secret.

        :param secret_name: The name of the secret to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"organization/secrets/{secret_name}")
        return response.status_code == 204
