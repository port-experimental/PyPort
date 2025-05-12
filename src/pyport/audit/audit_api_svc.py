from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class Audit(BaseAPIService):
    """Audit API category for retrieving audit logs.

    This class provides methods for interacting with the Audit API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all audit logs
        >>> audit_logs = client.audit.get_audit_logs()
        >>> # Get a specific audit log
        >>> audit_log = client.audit.get_audit_log("audit-id")
    """

    def __init__(self, client):
        """Initialize the Audit API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="audit", response_key="audit")

    def get_audit_logs(self, page: Optional[int] = None, per_page: Optional[int] = None,
                       params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all audit logs.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of audit log dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = "audit"

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("audits", [])

    def get_audit_log(self, audit_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific audit log.

        Args:
            audit_id: The identifier of the audit log.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the audit log.

        Raises:
            PortResourceNotFoundError: If the audit log does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.get_by_id(audit_id, params=params)
