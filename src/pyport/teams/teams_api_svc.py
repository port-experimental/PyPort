from typing import Dict, List, Any, Optional, cast

from .types import Team

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

    def get_teams(
        self, page: Optional[int] = None, per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> List[Team]:
        """
        Retrieve all teams.

        This method retrieves a list of all teams in the organization.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of teams per page (default: None).
            params: Optional query parameters for the request.

        Returns:
            A list of team dictionaries, each containing:
            - id: The unique identifier of the team
            - name: The name of the team
            - description: The description of the team (if any)
            - members: A list of member IDs
            - createdAt: The creation timestamp
            - updatedAt: The last update timestamp

        Examples:
            >>> teams = client.teams.get_teams()
            >>> for team in teams:
            ...     print(f"{team['name']} ({team['id']})")
        """
        # Use the base class get_all method which handles pagination
        teams = self.get_all(page=page, per_page=per_page, params=params, **kwargs)
        return cast(List[Team], teams)

    def get_team(self, team_id: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Team:
        """
        Retrieve details for a specific team.

        This method retrieves detailed information about a specific team.

        Args:
            team_id: The unique identifier of the team to retrieve.
            params: Optional query parameters for the request.

        Returns:
            A dictionary containing the team details:
            - id: The unique identifier of the team
            - name: The name of the team
            - description: The description of the team (if any)
            - members: A list of member IDs
            - createdAt: The creation timestamp
            - updatedAt: The last update timestamp

        Examples:
            >>> team = client.teams.get_team("team-id")
            >>> print(f"Team: {team['name']}")
            >>> print(f"Members: {len(team['members'])}")
        """
        # Use the base class get_by_id method which handles response extraction
        return cast(Team, self.get_by_id(team_id, params=params, **kwargs))

    def create_team(self, team_data: Dict[str, Any]) -> Team:
        """
        Create a new team.

        Args:
            team_data: A dictionary containing the data for the new team.
                Must include at minimum:
                - name: The name of the team (string)

                May also include:
                - description: A description of the team (string)
                - members: A list of member IDs (list of strings)

        Returns:
            A dictionary representing the created team.

        Examples:
            >>> new_team = client.teams.create_team({
            ...     "name": "Engineering",
            ...     "description": "Engineering team",
            ...     "members": ["user-1", "user-2"]
            ... })
        """
        # Use the base class create_resource method which handles response extraction
        return cast(Team, self.create_resource(team_data))

    def update_team(self, team_id: str, team_data: Dict[str, Any]) -> Team:
        """
        Update an existing team.

        Args:
            team_id: The identifier of the team to update.
            team_data: A dictionary with updated team data.
                May include any of the fields mentioned in create_team.

        Returns:
            A dictionary representing the updated team.

        Examples:
            >>> updated_team = client.teams.update_team(
            ...     "team-id",
            ...     {"name": "Engineering Team"}
            ... )
        """
        # Use the base class update_resource method which handles response extraction
        return cast(Team, self.update_resource(team_id, team_data))

    def delete_team(self, team_id: str) -> bool:
        """
        Delete a team.

        Args:
            team_id: The identifier of the team to delete.

        Returns:
            True if deletion was successful, otherwise False.

        Examples:
            >>> success = client.teams.delete_team("team-id")
            >>> if success:
            ...     print("Team deleted successfully")
        """
        # Use the base class delete_resource method
        return self.delete_resource(team_id)
