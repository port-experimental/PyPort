"""
Response models for the PyPort client library.
"""
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union

import requests

T = TypeVar('T')


class PortResponse(Generic[T]):
    """
    A wrapper for API responses that provides a consistent interface.
    
    This class allows accessing the response data in different ways:
    - As a raw response object
    - As parsed JSON
    - As extracted data from a specific key in the JSON
    
    It also provides access to metadata like status code and headers.
    """
    
    def __init__(
        self, 
        response: requests.Response,
        data_key: Optional[str] = None,
        default_value: Optional[T] = None
    ):
        """
        Initialize a PortResponse.
        
        :param response: The HTTP response from the API.
        :param data_key: Optional key to extract from the JSON response.
        :param default_value: Default value to return if data_key is not found.
        """
        self._response = response
        self._data_key = data_key
        self._default_value = default_value
        self._parsed_json: Optional[Dict[str, Any]] = None
    
    @property
    def raw(self) -> requests.Response:
        """Get the raw response object."""
        return self._response
    
    @property
    def status_code(self) -> int:
        """Get the HTTP status code."""
        return self._response.status_code
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get the response headers."""
        return dict(self._response.headers)
    
    @property
    def json(self) -> Dict[str, Any]:
        """Get the parsed JSON response."""
        if self._parsed_json is None:
            self._parsed_json = self._response.json()
        return self._parsed_json
    
    @property
    def data(self) -> T:
        """
        Get the data from the response.
        
        If data_key was provided, returns the value for that key.
        Otherwise, returns the full JSON response.
        """
        if self._data_key is not None:
            return self.json.get(self._data_key, self._default_value)  # type: ignore
        return self.json  # type: ignore
    
    def __bool__(self) -> bool:
        """
        Return True if the request was successful (2xx status code).
        
        This allows using the response in boolean contexts:
        ```
        if response:
            # Request was successful
        ```
        """
        return 200 <= self.status_code < 300


class PortListResponse(PortResponse[List[Dict[str, Any]]]):
    """
    A specialized response wrapper for list endpoints.
    
    This class provides additional methods for working with paginated lists.
    """
    
    def __init__(
        self, 
        response: requests.Response,
        data_key: str,
    ):
        """
        Initialize a PortListResponse.
        
        :param response: The HTTP response from the API.
        :param data_key: The key in the JSON response that contains the list of items.
        """
        super().__init__(response, data_key, default_value=[])
    
    def __iter__(self):
        """
        Iterate over the items in the list.
        
        This allows using the response in for loops:
        ```
        for item in response:
            # Process item
        ```
        """
        return iter(self.data)
    
    def __len__(self) -> int:
        """
        Return the number of items in the list.
        
        This allows using the len() function on the response:
        ```
        count = len(response)
        ```
        """
        return len(self.data)
    
    def __getitem__(self, index):
        """
        Get an item from the list by index.
        
        This allows using square bracket notation on the response:
        ```
        first_item = response[0]
        ```
        """
        return self.data[index]


class PortItemResponse(PortResponse[Dict[str, Any]]):
    """
    A specialized response wrapper for single item endpoints.
    
    This class provides additional methods for working with individual items.
    """
    
    def __init__(
        self, 
        response: requests.Response,
        data_key: Optional[str] = None,
    ):
        """
        Initialize a PortItemResponse.
        
        :param response: The HTTP response from the API.
        :param data_key: Optional key in the JSON response that contains the item.
        """
        super().__init__(response, data_key, default_value={})
    
    def __getitem__(self, key):
        """
        Get a value from the item by key.
        
        This allows using square bracket notation on the response:
        ```
        name = response['name']
        ```
        """
        return self.data[key]
    
    def get(self, key, default=None):
        """
        Get a value from the item by key, with a default if the key is not found.
        
        This mimics the dict.get() method:
        ```
        name = response.get('name', 'Unknown')
        ```
        """
        return self.data.get(key, default)


class PortDeleteResponse(PortResponse[bool]):
    """
    A specialized response wrapper for delete endpoints.
    
    This class provides a boolean result indicating whether the deletion was successful.
    """
    
    def __init__(self, response: requests.Response):
        """
        Initialize a PortDeleteResponse.
        
        :param response: The HTTP response from the API.
        """
        super().__init__(response)
    
    @property
    def data(self) -> bool:
        """
        Get the result of the deletion.
        
        Returns True if the deletion was successful (status code 204).
        """
        return self.status_code == 204
