from typing import Dict, List
from pyport.models.api_category import BaseResource


class Scorecards(BaseResource):
    """Scorecards API category for managing scorecards."""

    def get_scorecards(self) -> List[Dict]:
        """
        Retrieve all scorecards.

        :return: A list of scorecard dictionaries.
        """
        response = self._client.make_request("GET", "scorecards")
        return response.json().get("scorecards", [])

    def get_scorecard(self, scorecard_id: str) -> Dict:
        """
        Retrieve details for a specific scorecard.

        :param scorecard_id: The identifier of the scorecard.
        :return: A dictionary representing the scorecard.
        """
        response = self._client.make_request("GET", f"scorecards/{scorecard_id}")
        return response.json().get("scorecard", {})

    def create_scorecard(self, scorecard_data: Dict) -> Dict:
        """
        Create a new scorecard.

        :param scorecard_data: A dictionary containing scorecard data.
        :return: A dictionary representing the newly created scorecard.
        """
        response = self._client.make_request("POST", "scorecards", json=scorecard_data)
        return response.json()

    def update_scorecard(self, scorecard_id: str, scorecard_data: Dict) -> Dict:
        """
        Update an existing scorecard.

        :param scorecard_id: The identifier of the scorecard to update.
        :param scorecard_data: A dictionary with updated scorecard data.
        :return: A dictionary representing the updated scorecard.
        """
        response = self._client.make_request("PUT", f"scorecards/{scorecard_id}", json=scorecard_data)
        return response.json()

    def delete_scorecard(self, scorecard_id: str) -> bool:
        """
        Delete a scorecard.

        :param scorecard_id: The identifier of the scorecard to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"scorecards/{scorecard_id}")
        return response.status_code == 204
