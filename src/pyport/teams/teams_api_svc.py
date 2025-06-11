from typing import Dict, Any, Optional

from ..services.base_api_service import BaseAPIService


class Teams(BaseAPIService):
    """Teams API category for managing teams.

    This class provides methods for interacting with the Teams API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all teams
        >>> teams = client.teams.get_teams()
        >>> # Get a specific team
        >>> team = client.teams.get_team("team-id")
    """

    def __init__(self, client):
        """Initialize the Teams API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="teams", response_key="team")

    def get_teams(self, page: Optional[int] = None, per_page: Optional[int] = None,
                  params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve all teams in the organization.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing teams data.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Make the request
        response = self._make_request_with_params('GET', "teams", params=all_params)
        return response

    def get_team(self, team_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve a specific team by name.

        Args:
            team_name: The name of the team.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the team.

        Raises:
            PortResourceNotFoundError: If the team does not exist.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("teams", team_name)
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response
