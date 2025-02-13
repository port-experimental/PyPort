from typing import Dict, List
from pyport.models.api_category import BaseResource


class Apps(BaseResource):
    """Apps API category for managing applications."""

    def get_apps(self) -> List[Dict]:
        """
        Retrieve all apps.

        :return: A list of app dictionaries.
        """
        response = self._client.make_request("GET", "apps")
        return response.json().get("apps", [])

    def get_app(self, app_id: str) -> Dict:
        """
        Retrieve details for a specific app.

        :param app_id: The identifier of the app.
        :return: A dictionary representing the app.
        """
        response = self._client.make_request("GET", f"apps/{app_id}")
        return response.json().get("app", {})

    def create_app(self, app_data: Dict) -> Dict:
        """
        Create a new app.

        :param app_data: A dictionary containing app data.
        :return: A dictionary representing the newly created app.
        """
        response = self._client.make_request("POST", "apps", json=app_data)
        return response.json()

    def update_app(self, app_id: str, app_data: Dict) -> Dict:
        """
        Update an existing app.

        :param app_id: The identifier of the app to update.
        :param app_data: A dictionary with updated app data.
        :return: A dictionary representing the updated app.
        """
        response = self._client.make_request("PUT", f"apps/{app_id}", json=app_data)
        return response.json()

    def delete_app(self, app_id: str) -> bool:
        """
        Delete an app.

        :param app_id: The identifier of the app to delete.
        :return: True if deletion was successful (HTTP 204), else False.
        """
        response = self._client.make_request("DELETE", f"apps/{app_id}")
        return response.status_code == 204
