from typing import Dict, List, Optional
from ..models.api_category import BaseResource


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

    # Integration OAuth2 Methods

    def get_oauth2_config(self) -> Dict:
        """
        Retrieve OAuth2 configuration for integrations.

        :return: A dictionary containing OAuth2 configuration.
        """
        response = self._client.make_request("GET", "integrations/oauth2")
        return response.json()

    def create_oauth2_config(self, oauth2_data: Dict) -> Dict:
        """
        Create or update OAuth2 configuration for integrations.

        :param oauth2_data: A dictionary containing OAuth2 configuration data.
        :return: A dictionary representing the created/updated OAuth2 configuration.
        """
        response = self._client.make_request("POST", "integrations/oauth2", json=oauth2_data)
        return response.json()

    # Integration Validation Methods

    def validate_integration(self, operation_type: str, validation_data: Dict) -> Dict:
        """
        Validate an integration operation.

        :param operation_type: The type of operation to validate (e.g., 'create', 'update').
        :param validation_data: A dictionary containing data to validate.
        :return: A dictionary representing the validation result.
        """
        response = self._client.make_request("POST", f"integrations/validate/{operation_type}", json=validation_data)
        return response.json()

    # Integration Kinds Methods

    def get_integration_kinds(self, integration_id: str) -> List[Dict]:
        """
        Retrieve all kinds for a specific integration.

        :param integration_id: The identifier of the integration.
        :return: A list of kind dictionaries.
        """
        response = self._client.make_request("GET", f"integrations/{integration_id}/kinds")
        return response.json().get("kinds", [])

    def get_integration_kind(self, integration_id: str, kind: str) -> Dict:
        """
        Retrieve details for a specific integration kind.

        :param integration_id: The identifier of the integration.
        :param kind: The identifier of the kind.
        :return: A dictionary representing the integration kind.
        """
        response = self._client.make_request("GET", f"integrations/{integration_id}/kinds/{kind}")
        return response.json().get("kind", {})

    def update_integration_kind(self, integration_id: str, kind: str, kind_data: Dict) -> Dict:
        """
        Update an existing integration kind.

        :param integration_id: The identifier of the integration.
        :param kind: The identifier of the kind to update.
        :param kind_data: A dictionary containing the updated data.
        :return: A dictionary representing the updated integration kind.
        """
        response = self._client.make_request("PUT", f"integrations/{integration_id}/kinds/{kind}", json=kind_data)
        return response.json()

    def delete_integration_kind(self, integration_id: str, kind: str) -> bool:
        """
        Delete an integration kind.

        :param integration_id: The identifier of the integration.
        :param kind: The identifier of the kind to delete.
        :return: True if deletion was successful (HTTP 204), otherwise False.
        """
        response = self._client.make_request("DELETE", f"integrations/{integration_id}/kinds/{kind}")
        return response.status_code == 204

    # Integration Kind Examples Methods

    def get_integration_kind_examples(self, integration_id: str, kind: str) -> List[Dict]:
        """
        Retrieve all examples for a specific integration kind.

        :param integration_id: The identifier of the integration.
        :param kind: The identifier of the kind.
        :return: A list of example dictionaries.
        """
        response = self._client.make_request("GET", f"integrations/{integration_id}/kinds/{kind}/examples")
        return response.json().get("examples", [])

    def create_integration_kind_example(self, integration_id: str, kind: str, example_data: Dict) -> Dict:
        """
        Create a new example for a specific integration kind.

        :param integration_id: The identifier of the integration.
        :param kind: The identifier of the kind.
        :param example_data: A dictionary containing example data.
        :return: A dictionary representing the newly created example.
        """
        response = self._client.make_request("POST", f"integrations/{integration_id}/kinds/{kind}/examples", json=example_data)
        return response.json()

    def get_integration_kind_example(self, integration_id: str, kind: str, example_id: str) -> Dict:
        """
        Retrieve details for a specific integration kind example.

        :param integration_id: The identifier of the integration.
        :param kind: The identifier of the kind.
        :param example_id: The identifier of the example.
        :return: A dictionary representing the integration kind example.
        """
        response = self._client.make_request("GET", f"integrations/{integration_id}/kinds/{kind}/examples/{example_id}")
        return response.json().get("example", {})

    def update_integration_kind_example(self, integration_id: str, kind: str, example_id: str, example_data: Dict) -> Dict:
        """
        Update an existing integration kind example.

        :param integration_id: The identifier of the integration.
        :param kind: The identifier of the kind.
        :param example_id: The identifier of the example to update.
        :param example_data: A dictionary containing the updated data.
        :return: A dictionary representing the updated integration kind example.
        """
        response = self._client.make_request("PUT", f"integrations/{integration_id}/kinds/{kind}/examples/{example_id}", json=example_data)
        return response.json()

    def delete_integration_kind_example(self, integration_id: str, kind: str, example_id: str) -> bool:
        """
        Delete an integration kind example.

        :param integration_id: The identifier of the integration.
        :param kind: The identifier of the kind.
        :param example_id: The identifier of the example to delete.
        :return: True if deletion was successful (HTTP 204), otherwise False.
        """
        response = self._client.make_request("DELETE", f"integrations/{integration_id}/kinds/{kind}/examples/{example_id}")
        return response.status_code == 204

    # Integration Logs Methods

    def get_integration_logs(self, integration_id: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve logs for a specific integration.

        :param integration_id: The identifier of the integration.
        :param params: Optional query parameters for filtering logs.
        :return: A list of log dictionaries.
        """
        response = self._client.make_request("GET", f"integrations/{integration_id}/logs", params=params)
        return response.json().get("logs", [])

    # Integration Config Methods

    def get_integration_config(self, integration_id: str) -> Dict:
        """
        Retrieve configuration for a specific integration.

        :param integration_id: The identifier of the integration.
        :return: A dictionary representing the integration configuration.
        """
        response = self._client.make_request("GET", f"integrations/{integration_id}/config")
        return response.json().get("config", {})

    def update_integration_config(self, integration_id: str, config_data: Dict) -> Dict:
        """
        Update configuration for a specific integration.

        :param integration_id: The identifier of the integration.
        :param config_data: A dictionary containing the updated configuration data.
        :return: A dictionary representing the updated integration configuration.
        """
        response = self._client.make_request("PUT", f"integrations/{integration_id}/config", json=config_data)
        return response.json()

    def check_provision_enabled(self) -> Dict:
        """
        Check if provisioning is enabled for integrations.

        :return: A dictionary containing provisioning status information.
        """
        response = self._client.make_request("GET", "integrations/provision-enabled")
        return response.json()
