from typing import Dict, List
from pyport.models.api_category import BaseResource


class Pages(BaseResource):
    """Pages API category"""

    def get_pages(self, blueprint_identifier: str) -> List[Dict]:
        """
        Retrieve all pages for a specified blueprint.

        :param blueprint_identifier: The identifier of the blueprint.
        :return: A list of page dictionaries.
        """
        response = self._client.make_request('GET', f"blueprints/{blueprint_identifier}/pages")
        return response.json().get("pages", [])

    def get_page(self, blueprint_identifier: str, page_identifier: str) -> Dict:
        """
        Retrieve a single page by its identifier.

        :param blueprint_identifier: The blueprint identifier.
        :param page_identifier: The identifier of the page.
        :return: A dictionary representing the page.
        """
        response = self._client.make_request('GET', f"blueprints/{blueprint_identifier}/pages/{page_identifier}")
        return response.json().get("page", {})

    def create_page(self, blueprint_identifier: str, page_data: Dict) -> Dict:
        """
        Create a new page under the specified blueprint.

        :param blueprint_identifier: The blueprint identifier.
        :param page_data: A dictionary containing data for the new page.
        :return: A dictionary representing the created page.
        """
        response = self._client.make_request('POST', f"blueprints/{blueprint_identifier}/pages", json=page_data)
        return response.json()

    def update_page(self, blueprint_identifier: str, page_identifier: str, page_data: Dict) -> Dict:
        """
        Update an existing page.

        :param blueprint_identifier: The blueprint identifier.
        :param page_identifier: The identifier of the page to update.
        :param page_data: A dictionary containing updated data for the page.
        :return: A dictionary representing the updated page.
        """
        response = self._client.make_request('PUT', f"blueprints/{blueprint_identifier}/pages/{page_identifier}",
                                             json=page_data)
        return response.json()

    def delete_page(self, blueprint_identifier: str, page_identifier: str) -> bool:
        """
        Delete a page.

        :param blueprint_identifier: The blueprint identifier.
        :param page_identifier: The identifier of the page to delete.
        :return: True if deletion was successful (e.g., status code 204), else False.
        """
        response = self._client.make_request('DELETE', f"blueprints/{blueprint_identifier}/pages/{page_identifier}")
        return response.status_code == 204

    # Page Widgets Methods

    def get_page_widgets(self, page_identifier: str) -> List[Dict]:
        """
        Retrieve all widgets for a specific page.

        :param page_identifier: The identifier of the page.
        :return: A list of widget dictionaries.
        """
        response = self._client.make_request('GET', f"pages/{page_identifier}/widgets")
        return response.json().get("widgets", [])

    def create_page_widget(self, page_identifier: str, widget_data: Dict) -> Dict:
        """
        Create a new widget for a specific page.

        :param page_identifier: The identifier of the page.
        :param widget_data: A dictionary containing widget data.
        :return: A dictionary representing the newly created widget.
        """
        response = self._client.make_request('POST', f"pages/{page_identifier}/widgets", json=widget_data)
        return response.json()

    def get_page_widget(self, page_identifier: str, widget_id: str) -> Dict:
        """
        Retrieve details for a specific page widget.

        :param page_identifier: The identifier of the page.
        :param widget_id: The identifier of the widget.
        :return: A dictionary representing the page widget.
        """
        response = self._client.make_request('GET', f"pages/{page_identifier}/widgets/{widget_id}")
        return response.json().get("widget", {})

    def update_page_widget(self, page_identifier: str, widget_id: str, widget_data: Dict) -> Dict:
        """
        Update an existing page widget.

        :param page_identifier: The identifier of the page.
        :param widget_id: The identifier of the widget to update.
        :param widget_data: A dictionary with updated widget data.
        :return: A dictionary representing the updated page widget.
        """
        response = self._client.make_request('PUT', f"pages/{page_identifier}/widgets/{widget_id}", json=widget_data)
        return response.json()

    def delete_page_widget(self, page_identifier: str, widget_id: str) -> bool:
        """
        Delete a page widget.

        :param page_identifier: The identifier of the page.
        :param widget_id: The identifier of the widget to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request('DELETE', f"pages/{page_identifier}/widgets/{widget_id}")
        return response.status_code == 204

    # Page Permissions Methods

    def get_page_permissions(self, page_identifier: str) -> Dict:
        """
        Retrieve permissions for a specific page.

        :param page_identifier: The identifier of the page.
        :return: A dictionary representing the page permissions.
        """
        response = self._client.make_request('GET', f"pages/{page_identifier}/permissions")
        return response.json().get("permissions", {})

    def update_page_permissions(self, page_identifier: str, permissions_data: Dict) -> Dict:
        """
        Update permissions for a specific page.

        :param page_identifier: The identifier of the page.
        :param permissions_data: A dictionary containing updated permissions data.
        :return: A dictionary representing the updated page permissions.
        """
        response = self._client.make_request('PUT', f"pages/{page_identifier}/permissions", json=permissions_data)
        return response.json()
