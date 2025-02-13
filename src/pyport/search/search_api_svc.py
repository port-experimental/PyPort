from typing import Dict, List
from pyport.models.api_category import BaseResource


class Search(BaseResource):
    """Search API category for querying resources."""

    def search_entities(self, query_params: Dict) -> List[Dict]:
        """
        Search for entities based on query parameters.

        :param query_params: A dictionary of query parameters.
        :return: A list of matching entity dictionaries.
        """
        response = self._client.make_request("GET", "search/entities", params=query_params)
        return response.json().get("results", [])

    def search_blueprints(self, query_params: Dict) -> List[Dict]:
        """
        Search for blueprints based on query parameters.

        :param query_params: A dictionary of query parameters.
        :return: A list of matching blueprint dictionaries.
        """
        response = self._client.make_request("GET", "search/blueprints", params=query_params)
        return response.json().get("results", [])
