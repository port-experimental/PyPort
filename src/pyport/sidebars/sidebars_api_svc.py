from typing import Dict, List
from pyport.models.api_category import BaseResource


class Sidebars(BaseResource):
    """Sidebars API category for managing sidebar configurations."""

    def get_sidebars(self) -> List[Dict]:
        """
        Retrieve all sidebars.

        :return: A list of sidebar dictionaries.
        """
        response = self._client.make_request("GET", "sidebars")
        return response.json().get("sidebars", [])

    def get_sidebar(self, sidebar_id: str) -> Dict:
        """
        Retrieve details for a specific sidebar.

        :param sidebar_id: The identifier of the sidebar.
        :return: A dictionary representing the sidebar.
        """
        response = self._client.make_request("GET", f"sidebars/{sidebar_id}")
        return response.json().get("sidebar", {})

    def create_sidebar(self, sidebar_data: Dict) -> Dict:
        """
        Create a new sidebar.

        :param sidebar_data: A dictionary containing sidebar data.
        :return: A dictionary representing the newly created sidebar.
        """
        response = self._client.make_request("POST", "sidebars", json=sidebar_data)
        return response.json()

    def update_sidebar(self, sidebar_id: str, sidebar_data: Dict) -> Dict:
        """
        Update an existing sidebar.

        :param sidebar_id: The identifier of the sidebar to update.
        :param sidebar_data: A dictionary with updated sidebar data.
        :return: A dictionary representing the updated sidebar.
        """
        response = self._client.make_request("PUT", f"sidebars/{sidebar_id}", json=sidebar_data)
        return response.json()

    def delete_sidebar(self, sidebar_id: str) -> bool:
        """
        Delete a sidebar.

        :param sidebar_id: The identifier of the sidebar to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"sidebars/{sidebar_id}")
        return response.status_code == 204
