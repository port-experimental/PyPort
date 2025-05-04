from typing import Dict, List
from pyport.models.api_category import BaseResource


class DataSources(BaseResource):
    """Data Sources API category for managing data sources."""

    def get_data_sources(self) -> List[Dict]:
        """
        Retrieve all data sources.

        :return: A list of data source dictionaries.
        """
        response = self._client.make_request("GET", "data-sources")
        return response.json().get("dataSources", [])
