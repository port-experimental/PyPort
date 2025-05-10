from typing import Dict, List
from ..models.api_category import BaseResource


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

    # Checklist Items Methods

    def get_checklist_items(self, checklist_id: str) -> List[Dict]:
        """
        Retrieve all items for a specific checklist.

        :param checklist_id: The identifier of the checklist.
        :return: A list of checklist item dictionaries.
        """
        response = self._client.make_request("GET", f"checklists/{checklist_id}/items")
        return response.json().get("items", [])

    def create_checklist_item(self, checklist_id: str, item_data: Dict) -> Dict:
        """
        Create a new item for a specific checklist.

        :param checklist_id: The identifier of the checklist.
        :param item_data: A dictionary containing item data.
        :return: A dictionary representing the newly created checklist item.
        """
        response = self._client.make_request("POST", f"checklists/{checklist_id}/items", json=item_data)
        return response.json()

    def update_checklist_item(self, checklist_id: str, item_id: str, item_data: Dict) -> Dict:
        """
        Update an existing checklist item.

        :param checklist_id: The identifier of the checklist.
        :param item_id: The identifier of the item to update.
        :param item_data: A dictionary with updated item data.
        :return: A dictionary representing the updated checklist item.
        """
        response = self._client.make_request("PUT", f"checklists/{checklist_id}/items/{item_id}", json=item_data)
        return response.json()

    def delete_checklist_item(self, checklist_id: str, item_id: str) -> bool:
        """
        Delete a checklist item.

        :param checklist_id: The identifier of the checklist.
        :param item_id: The identifier of the item to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"checklists/{checklist_id}/items/{item_id}")
        return response.status_code == 204
