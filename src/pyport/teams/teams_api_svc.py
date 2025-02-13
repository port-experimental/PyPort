from typing import Dict, List
from pyport.models.api_category import BaseResource


class Teams(BaseResource):
    """Teams API category for managing teams."""

    def get_teams(self) -> List[Dict]:
        """
        Retrieve all teams.

        :return: A list of team dictionaries.
        """
        response = self._client.make_request("GET", "teams")
        return response.json().get("teams", [])

    def get_team(self, team_id: str) -> Dict:
        """
        Retrieve details for a specific team.

        :param team_id: The identifier of the team.
        :return: A dictionary representing the team.
        """
        response = self._client.make_request("GET", f"teams/{team_id}")
        return response.json().get("team", {})

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
