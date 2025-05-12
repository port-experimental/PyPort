from typing import Dict, List, Optional, Any

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

    def get_action_run(self, run_id: str, action_id: Optional[str] = None,
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details of a specific action run.

        Args:
            run_id: The identifier of the run.
            action_id: The identifier of the action (optional).
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the action run.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint based on whether an action ID is provided
        if action_id:
            endpoint = self._build_endpoint("actions", action_id, "runs", run_id)
        else:
            endpoint = self._build_endpoint("actions", "runs", run_id)

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

    def get_action_runs(self, action_id: Optional[str] = None,
                        page: Optional[int] = None, per_page: Optional[int] = None,
                        params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all action runs, optionally filtered by action ID.

        Args:
            action_id: Optional identifier of the action to filter runs.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of action run dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint based on whether an action ID is provided
        if action_id:
            endpoint = self._build_endpoint("actions", action_id, "runs")
        else:
            endpoint = self._build_endpoint("actions", "runs")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("runs", [])

    def create_action_run(self, run_data: Dict[str, Any],
                          params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new action run.

        Args:
            run_data: A dictionary containing the action run data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the created action run.

        Raises:
            PortValidationError: If the run data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs")
        response = self._make_request_with_params('POST', endpoint, json=run_data, params=params)
        return response

    def cancel_action_run(self, run_id: str,
                          params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Cancel an in-progress action run.

        Args:
            run_id: The identifier of the run to cancel.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the result of the cancellation.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "approval")
        response = self._make_request_with_params('POST', endpoint, json={"status": "CANCELED"}, params=params)
        return response

    def approve_action_run(self, run_id: str,
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Approve an action run that requires approval.

        Args:
            run_id: The identifier of the run to approve.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the result of the approval.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "approval")
        response = self._make_request_with_params('POST', endpoint, json={"status": "APPROVED"}, params=params)
        return response

    def reject_action_run(self, run_id: str,
                          params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Reject an action run that requires approval.

        Args:
            run_id: The identifier of the run to reject.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the result of the rejection.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "approval")
        response = self._make_request_with_params('POST', endpoint, json={"status": "REJECTED"}, params=params)
        return response

    def execute_self_service(self, action_id: str, payload: Optional[Dict[str, Any]] = None,
                             params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a self-service action.

        Args:
            action_id: The identifier of the action to execute.
            payload: Optional payload for the action.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the result of the execution.

        Raises:
            PortResourceNotFoundError: If the action does not exist.
            PortValidationError: If the payload is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        if payload:
            response = self._client.make_request("POST", f"actions/{action_id}/runs", json=payload)
        else:
            response = self._client.make_request("POST", f"actions/{action_id}/runs")
        return response.json()

    def get_action_run_logs(self, run_id: str,
                            params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get logs for an action run.

        Args:
            run_id: The identifier of the run.
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing the logs.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "logs")
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response

    def get_action_run_approvers(self, run_id: str,
                                 params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get approvers for an action run.

        Args:
            run_id: The identifier of the run.
            params: Additional query parameters for the request.

        Returns:
            A list of approver dictionaries.

        Raises:
            PortResourceNotFoundError: If the action run does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("actions", "runs", run_id, "approvers")
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("approvers", [])
