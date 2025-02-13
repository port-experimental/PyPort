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
