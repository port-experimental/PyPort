"""Webhooks API service for managing Port webhooks.

This module provides methods for creating, retrieving, updating, and deleting
webhook configurations in Port."""

from typing import Dict, Optional, Any

from ..services.base_api_service import BaseAPIService


class Webhooks(BaseAPIService):
    """Webhooks API category for managing webhooks.

    This class provides methods for interacting with the Webhooks API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all webhooks
        >>> webhooks = client.webhooks.get_webhooks()
        >>> # Get a specific webhook
        >>> webhook = client.webhooks.get_webhook("webhook-id")
    """

    def __init__(self, client):
        """Initialize the Webhooks API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="webhooks", response_key="webhook")

    def get_webhooks(self, page: Optional[int] = None, per_page: Optional[int] = None,
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve all webhooks.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing webhooks data.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Make the request
        response = self._make_request_with_params('GET', "webhooks", params=all_params)
        return response

    def get_webhook(self, webhook_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific webhook.

        Args:
            webhook_id: The identifier of the webhook.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the webhook.

        Raises:
            PortResourceNotFoundError: If the webhook does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("webhooks", webhook_id)
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

    def create_webhook(self, webhook_data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new webhook.

        Args:
            webhook_data: A dictionary containing webhook data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created webhook.

        Raises:
            PortValidationError: If the webhook data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        response = self._make_request_with_params('POST', "webhooks", json=webhook_data, params=params)
        return response

    def update_webhook(self, webhook_id: str, webhook_data: Dict[str, Any],
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing webhook (PATCH method).

        Args:
            webhook_id: The identifier of the webhook to update.
            webhook_data: A dictionary with updated webhook data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated webhook.

        Raises:
            PortResourceNotFoundError: If the webhook does not exist.
            PortValidationError: If the webhook data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("webhooks", webhook_id)
        response = self._make_request_with_params('PATCH', endpoint, json=webhook_data, params=params)
        return response

    def delete_webhook(self, webhook_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Delete a webhook.

        Args:
            webhook_id: The identifier of the webhook to delete.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the deletion result.

        Raises:
            PortResourceNotFoundError: If the webhook does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("webhooks", webhook_id)
        response = self._make_request_with_params('DELETE', endpoint, params=params)
        return response
