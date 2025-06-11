from typing import Dict, Optional, Any

from ..services.base_api_service import BaseAPIService


class ActionRuns(BaseAPIService):
    """Action Runs API category for managing action execution runs.

    This class provides methods for interacting with the Action Runs API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all action runs
        >>> runs = client.action_runs.get_action_runs()
        >>> # Get a specific action run
        >>> run = client.action_runs.get_action_run("run-id")
    """

    def __init__(self, client):
        """Initialize the Action Runs API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="actions/runs", response_key="run")

    def get_action_runs(self, page: Optional[int] = None, per_page: Optional[int] = None,
                        params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve all action runs.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing action runs data.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Make the request
        endpoint = self._build_endpoint("actions", "runs")
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response

    def get_action_run(self, run_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve a specific action run by its identifier.

        Args:
            run_id: The identifier of the action run.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the action run.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id)
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

    def update_action_run(self, run_id: str, run_data: Dict[str, Any],
                          params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an action run.

        Args:
            run_id: The identifier of the action run to update.
            run_data: A dictionary containing updated data for the action run.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated action run.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortValidationError: If the run data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id)
        response = self._make_request_with_params('PATCH', endpoint, json=run_data, params=params)
        return response

    def approve_action_run(self, run_id: str, approval_data: Optional[Dict[str, Any]] = None,
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Approve an action run.

        Args:
            run_id: The identifier of the action run to approve.
            approval_data: A dictionary containing approval data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the approval result.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "approval")
        response = self._make_request_with_params('PATCH', endpoint, json=approval_data or {}, params=params)
        return response

    def add_action_run_log(self, run_id: str, log_data: Dict[str, Any],
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a log entry to an action run.

        Args:
            run_id: The identifier of the action run.
            log_data: A dictionary containing log data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the log creation result.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortValidationError: If the log data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "logs")
        response = self._make_request_with_params('POST', endpoint, json=log_data, params=params)
        return response

    def get_action_run_logs(self, run_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve logs for a specific action run.

        Args:
            run_id: The identifier of the action run.
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing the action run logs.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "logs")
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

    def get_action_run_approvers(self, run_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve approvers for a specific action run.

        Args:
            run_id: The identifier of the action run.
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing the action run approvers.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "approvers")
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response
