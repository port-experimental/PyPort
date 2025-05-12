from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class Integrations(BaseAPIService):
    """Integrations API category for managing third-party integrations.

    This class provides methods for interacting with the Integrations API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all integrations
        >>> integrations = client.integrations.get_integrations()
        >>> # Get a specific integration
        >>> integration = client.integrations.get_integration("integration-id")
    """

    def __init__(self, client):
        """Initialize the Integrations API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="integrations", response_key="integration")

    def get_integrations(self, page: Optional[int] = None, per_page: Optional[int] = None,
                         params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all integrations.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of integration dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        return self.get_all(page=page, per_page=per_page, params=params)

    def get_integration(self, integration_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific integration.

        Args:
            integration_id: The identifier of the integration.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the integration.

        Raises:
            PortResourceNotFoundError: If the integration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.get_by_id(integration_id, params=params)

    def create_integration(self, integration_data: Dict[str, Any],
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new integration.

        Args:
            integration_data: A dictionary containing integration data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created integration.

        Raises:
            PortValidationError: If the integration data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("POST", "integrations", json=integration_data)
        return response.json()

    def update_integration(self, integration_id: str, integration_data: Dict[str, Any],
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing integration.

        Args:
            integration_id: The identifier of the integration to update.
            integration_data: A dictionary containing the updated data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated integration.

        Raises:
            PortResourceNotFoundError: If the integration does not exist.
            PortValidationError: If the integration data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("PUT", f"integrations/{integration_id}", json=integration_data)
        return response.json()

    def delete_integration(self, integration_id: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete an integration.

        Args:
            integration_id: The identifier of the integration to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the integration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.delete_resource(integration_id, params=params)

    # Integration OAuth2 Methods

    def get_oauth2_config(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve OAuth2 configuration for integrations.

        Args:
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing OAuth2 configuration.

        Raises:
            PortApiError: If the API request fails.
        """
        endpoint = self._build_endpoint("integrations", "oauth2")
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

    def create_oauth2_config(self, oauth2_data: Dict[str, Any],
                             params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create or update OAuth2 configuration for integrations.

        Args:
            oauth2_data: A dictionary containing OAuth2 configuration data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the created/updated OAuth2 configuration.

        Raises:
            PortValidationError: If the OAuth2 data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("integrations", "oauth2")
        response = self._make_request_with_params('POST', endpoint, json=oauth2_data, params=params)
        return response

    # Integration Validation Methods

    def validate_integration(self, operation_type: str, validation_data: Dict[str, Any],
                             params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate an integration operation.

        Args:
            operation_type: The type of operation to validate (e.g., 'create', 'update').
            validation_data: A dictionary containing data to validate.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the validation result.

        Raises:
            PortValidationError: If the validation data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("integrations", "validate", operation_type)
        response = self._make_request_with_params('POST', endpoint, json=validation_data, params=params)
        return response

    # Integration Kinds Methods

    def get_integration_kinds(self, integration_id: str, page: Optional[int] = None,
                              per_page: Optional[int] = None,
                              params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all kinds for a specific integration.

        Args:
            integration_id: The identifier of the integration.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of kind dictionaries.

        Raises:
            PortResourceNotFoundError: If the integration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("kinds", [])

    def get_integration_kind(self, integration_id: str, kind: str,
                             params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific integration kind.

        Args:
            integration_id: The identifier of the integration.
            kind: The identifier of the kind.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the integration kind.

        Raises:
            PortResourceNotFoundError: If the integration or kind does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds", kind)

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("kind", {})

    def update_integration_kind(self, integration_id: str, kind: str,
                                kind_data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing integration kind.

        Args:
            integration_id: The identifier of the integration.
            kind: The identifier of the kind to update.
            kind_data: A dictionary containing the updated data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated integration kind.

        Raises:
            PortResourceNotFoundError: If the integration or kind does not exist.
            PortValidationError: If the kind data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds", kind)

        # Make the request
        response = self._make_request_with_params('PUT', endpoint, json=kind_data, params=params)
        return response

    def delete_integration_kind(self, integration_id: str, kind: str,
                                params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete an integration kind.

        Args:
            integration_id: The identifier of the integration.
            kind: The identifier of the kind to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the integration or kind does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds", kind)

        # Make the request
        response = self._client.make_request("DELETE", endpoint)
        return response.status_code == 204

    # Integration Kind Examples Methods

    def get_integration_kind_examples(self, integration_id: str, kind: str,
                                      page: Optional[int] = None, per_page: Optional[int] = None,
                                      params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all examples for a specific integration kind.

        Args:
            integration_id: The identifier of the integration.
            kind: The identifier of the kind.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of example dictionaries.

        Raises:
            PortResourceNotFoundError: If the integration or kind does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds", kind, "examples")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("examples", [])

    def create_integration_kind_example(
        self, integration_id: str, kind: str, example_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new example for a specific integration kind.

        Args:
            integration_id: The identifier of the integration.
            kind: The identifier of the kind.
            example_data: A dictionary containing example data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created example.

        Raises:
            PortResourceNotFoundError: If the integration or kind does not exist.
            PortValidationError: If the example data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds", kind, "examples")

        # Make the request
        response = self._make_request_with_params('POST', endpoint, json=example_data, params=params)
        return response

    def get_integration_kind_example(self, integration_id: str, kind: str, example_id: str,
                                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific integration kind example.

        Args:
            integration_id: The identifier of the integration.
            kind: The identifier of the kind.
            example_id: The identifier of the example.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the integration kind example.

        Raises:
            PortResourceNotFoundError: If the integration, kind, or example does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds", kind, "examples", example_id)

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("example", {})

    def update_integration_kind_example(
        self, integration_id: str, kind: str, example_id: str, example_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing integration kind example.

        Args:
            integration_id: The identifier of the integration.
            kind: The identifier of the kind.
            example_id: The identifier of the example to update.
            example_data: A dictionary containing the updated data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated integration kind example.

        Raises:
            PortResourceNotFoundError: If the integration, kind, or example does not exist.
            PortValidationError: If the example data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds", kind, "examples", example_id)

        # Make the request
        response = self._make_request_with_params('PUT', endpoint, json=example_data, params=params)
        return response

    def delete_integration_kind_example(self, integration_id: str, kind: str, example_id: str,
                                        params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete an integration kind example.

        Args:
            integration_id: The identifier of the integration.
            kind: The identifier of the kind.
            example_id: The identifier of the example to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the integration, kind, or example does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "kinds", kind, "examples", example_id)

        # Make the request
        response = self._client.make_request("DELETE", endpoint)
        return response.status_code == 204

    # Integration Logs Methods

    def get_integration_logs(self, integration_id: str, page: Optional[int] = None,
                             per_page: Optional[int] = None,
                             params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve logs for a specific integration.

        Args:
            integration_id: The identifier of the integration.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for filtering logs.

        Returns:
            A list of log dictionaries.

        Raises:
            PortResourceNotFoundError: If the integration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "logs")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("logs", [])

    # Integration Config Methods

    def get_integration_config(self, integration_id: str,
                               params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve configuration for a specific integration.

        Args:
            integration_id: The identifier of the integration.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the integration configuration.

        Raises:
            PortResourceNotFoundError: If the integration does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "config")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("config", {})

    def update_integration_config(self, integration_id: str, config_data: Dict[str, Any],
                                  params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update configuration for a specific integration.

        Args:
            integration_id: The identifier of the integration.
            config_data: A dictionary containing the updated configuration data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated integration configuration.

        Raises:
            PortResourceNotFoundError: If the integration does not exist.
            PortValidationError: If the configuration data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", integration_id, "config")

        # Make the request
        response = self._make_request_with_params('PUT', endpoint, json=config_data, params=params)
        return response

    def check_provision_enabled(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Check if provisioning is enabled for integrations.

        Args:
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing provisioning status information.

        Raises:
            PortApiError: If the API request fails.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("integrations", "provision-enabled")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response
