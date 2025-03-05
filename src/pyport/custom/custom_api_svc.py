from typing import Dict, Optional, Any, Union

from pyport.models.api_category import BaseResource


class Custom(BaseResource):
    """Custom API category for sending custom requests to the Port API."""

    def send_request(
        self,
        relative_path: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """
        Send a custom request to the Port API.

        :param relative_path: The relative URL/path to the API endpoint.
        :param method: HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        :param headers: Optional dictionary of HTTP headers to send.
        :param params: Optional dictionary of query string parameters.
        :param data: Optional data to send in the request body (form data or string).
        :param json_data: Optional JSON data to send in the request body.
        :return: The JSON response from the API.
        """
        # Ensure method is uppercase
        method = method.upper()
        
        # Prepare kwargs for the request
        kwargs = {}
        if headers:
            kwargs['headers'] = headers
        if params:
            kwargs['params'] = params
        if data:
            kwargs['data'] = data
        if json_data:
            kwargs['json'] = json_data
            
        # Make the request
        response = self._client.make_request(method, relative_path, **kwargs)
        
        # Return the JSON response if the response has content
        if response.content:
            return response.json()
        # Return an empty dict for responses with no content (e.g., 204 No Content)
        return {}
