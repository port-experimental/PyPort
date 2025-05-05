from typing import Dict, List
from pyport.models.api_category import BaseResource


class Webhooks(BaseResource):
    """Webhooks API category for managing webhooks."""

    def get_webhooks(self) -> List[Dict]:
        """
        Retrieve all webhooks.

        :return: A list of webhook dictionaries.
        """
        response = self._client.make_request("GET", "webhooks")
        return response.json().get("webhooks", [])

    def get_webhook(self, webhook_id: str) -> Dict:
        """
        Retrieve details for a specific webhook.

        :param webhook_id: The identifier of the webhook.
        :return: A dictionary representing the webhook.
        """
        response = self._client.make_request("GET", f"webhooks/{webhook_id}")
        return response.json().get("webhook", {})

    def create_webhook(self, webhook_data: Dict) -> Dict:
        """
        Create a new webhook.

        :param webhook_data: A dictionary containing webhook data.
        :return: A dictionary representing the newly created webhook.
        """
        response = self._client.make_request("POST", "webhooks", json=webhook_data)
        return response.json()

    def update_webhook(self, webhook_id: str, webhook_data: Dict) -> Dict:
        """
        Update an existing webhook.

        :param webhook_id: The identifier of the webhook to update.
        :param webhook_data: A dictionary with updated webhook data.
        :return: A dictionary representing the updated webhook.
        """
        response = self._client.make_request("PUT", f"webhooks/{webhook_id}", json=webhook_data)
        return response.json()

    def delete_webhook(self, webhook_id: str) -> bool:
        """
        Delete a webhook.

        :param webhook_id: The identifier of the webhook to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"webhooks/{webhook_id}")
        return response.status_code == 204
