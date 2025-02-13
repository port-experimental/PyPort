from typing import Dict, List
from pyport.models.api_category import BaseResource


class Checklist(BaseResource):
    """Checklist API category for managing checklists."""

    def get_checklists(self) -> List[Dict]:
        """
        Retrieve all checklists.

        :return: A list of checklist dictionaries.
        """
        response = self._client.make_request("GET", "checklists")
        return response.json().get("checklists", [])

    def get_checklist(self, checklist_id: str) -> Dict:
        """
        Retrieve details for a specific checklist.

        :param checklist_id: The identifier of the checklist.
        :return: A dictionary representing the checklist.
        """
        response = self._client.make_request("GET", f"checklists/{checklist_id}")
        return response.json().get("checklist", {})

    def create_checklist(self, checklist_data: Dict) -> Dict:
        """
        Create a new checklist.

        :param checklist_data: A dictionary containing checklist data.
        :return: A dictionary representing the newly created checklist.
        """
        response = self._client.make_request("POST", "checklists", json=checklist_data)
        return response.json()

    def update_checklist(self, checklist_id: str, checklist_data: Dict) -> Dict:
        """
        Update an existing checklist.

        :param checklist_id: The identifier of the checklist to update.
        :param checklist_data: A dictionary with updated checklist data.
        :return: A dictionary representing the updated checklist.
        """
        response = self._client.make_request("PUT", f"checklists/{checklist_id}", json=checklist_data)
        return response.json()

    def delete_checklist(self, checklist_id: str) -> bool:
        """
        Delete a checklist.

        :param checklist_id: The identifier of the checklist to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"checklists/{checklist_id}")
        return response.status_code == 204
