from typing import Dict, List, Any, Optional, cast

from src.pyport.types import Team

from src.pyport.models.api_category import BaseResource


class Teams(BaseResource):
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
        super().__init__(client, resource_name="teams")

    def get_teams(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> List[Team]:
        """
        Retrieve all teams.

        This method retrieves a list of all teams in the organization.

        Args:
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
        # For backward compatibility, ignore kwargs
        # Use the base class list method
        teams = self.list(params=params)
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
        # For backward compatibility, ignore kwargs
        # Use the base class get method
        response = self.get(team_id, params=params)
        return cast(Team, response.get("team", {}))

    def create_team(self, team_data: Dict) -> Dict:
        """
        Create a new team.

        :param team_data: A dictionary containing team data.
        :return: A dictionary representing the newly created team.
        """
        response = self._client.make_request("POST", "teams", json=team_data)
        return response.json()

    def update_team(self, team_id: str, team_data: Dict) -> Dict:
        """
        Update an existing team.

        :param team_id: The identifier of the team to update.
        :param team_data: A dictionary with updated team data.
        :return: A dictionary representing the updated team.
        """
        response = self._client.make_request("PUT", f"teams/{team_id}", json=team_data)
        return response.json()

    def delete_team(self, team_id: str) -> bool:
        """
        Delete a team.

        :param team_id: The identifier of the team to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"teams/{team_id}")
        return response.status_code == 204
