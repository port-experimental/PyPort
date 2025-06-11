from typing import Dict, List, Any, Optional
from ..services.base_api_service import BaseAPIService


class Organizations(BaseAPIService):
    """Organizations API category for managing organizations.

    This class provides methods for interacting with the Organizations API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all organizations
        >>> organizations = client.organizations.get_organizations()
        >>> # Get a specific organization
        >>> organization = client.organizations.get_organization("org-id")
    """

    def __init__(self, client):
        """Initialize the Organizations API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="organizations", response_key="organization")

    def get_organizations(
        self, page: Optional[int] = None, per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all organizations.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of organizations per page (default: None).
            params: Optional query parameters for the request.

        Returns:
            A list of organization dictionaries, each containing:
            - id: The unique identifier of the organization
            - name: The name of the organization
            - description: The description of the organization (if any)
            - createdAt: The creation timestamp
            - updatedAt: The last update timestamp

        Examples:
            >>> organizations = client.organizations.get_organizations()
            >>> for org in organizations:
            ...     print(f"{org['name']} ({org['id']})")
        """
        # Use the base class get_all method which handles pagination
        return self.get_all(page=page, per_page=per_page, params=params, **kwargs)

    def get_organization(
        self, organization_id: str, params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Retrieve details for a specific organization.

        Args:
            organization_id: The identifier of the organization.
            params: Optional query parameters for the request.

        Returns:
            A dictionary containing the organization details:
            - id: The unique identifier of the organization
            - name: The name of the organization
            - description: The description of the organization (if any)
            - createdAt: The creation timestamp
            - updatedAt: The last update timestamp

        Examples:
            >>> organization = client.organizations.get_organization("org-id")
            >>> print(f"Organization: {organization['name']}")
        """
        # Use the base class get_by_id method which handles response extraction
        return self.get_by_id(organization_id, params=params, **kwargs)

    def create_organization(self, organization_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new organization.

        Args:
            organization_data: A dictionary containing the data for the new organization.
                Must include at minimum:
                - name: The name of the organization (string)

                May also include:
                - description: A description of the organization (string)

        Returns:
            A dictionary representing the created organization.

        Examples:
            >>> new_org = client.organizations.create_organization({
            ...     "name": "Engineering Org",
            ...     "description": "Engineering organization"
            ... })
        """
        # Use the base class create_resource method which handles response extraction
        return self.create_resource(organization_data)

    def update_organization(self, organization_id: str, organization_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing organization.

        Args:
            organization_id: The identifier of the organization to update.
            organization_data: A dictionary with updated organization data.
                May include any of the fields mentioned in create_organization.

        Returns:
            A dictionary representing the updated organization.

        Examples:
            >>> updated_org = client.organizations.update_organization(
            ...     "org-id",
            ...     {"name": "Engineering Organization"}
            ... )
        """
        # Use the base class update_resource method which handles response extraction
        return self.update_resource(organization_id, organization_data)

    def delete_organization(self, organization_id: str) -> bool:
        """
        Delete an organization.

        Args:
            organization_id: The identifier of the organization to delete.

        Returns:
            True if deletion was successful, otherwise False.

        Examples:
            >>> success = client.organizations.delete_organization("org-id")
            >>> if success:
            ...     print("Organization deleted successfully")
        """
        # Use the base class delete_resource method
        return self.delete_resource(organization_id)

    # Organization Details Methods

    def get_organization_details(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve organization details.

        Args:
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing organization data.

        Raises:
            PortApiError: If the API request fails.
        """
        response = self._make_request_with_params('GET', "organization", params=params)
        return response

    # Organization Secrets Methods

    def get_organization_secrets(self, page: Optional[int] = None, per_page: Optional[int] = None,
                                 params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve all organization secrets.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing organization secrets data.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Make the request
        endpoint = self._build_endpoint("organization", "secrets")
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response

    def get_organization_secret(self, secret_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific organization secret.

        Args:
            secret_name: The name of the secret.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the secret.

        Raises:
            PortResourceNotFoundError: If the secret does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("organization", "secrets", secret_name)
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

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
