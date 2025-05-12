"""
Property-based tests for the PyPort client library.

This module uses property-based testing to verify that the client behaves
correctly under a wide range of inputs.

Note: This requires the `hypothesis` library to be installed.
"""

import unittest
from unittest.mock import patch, MagicMock

try:
    from hypothesis import given, strategies as st
    from hypothesis.strategies import text, dictionaries, lists, integers, booleans, none
    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False
    # Create dummy decorators for when hypothesis is not available
    def given(*args, **kwargs):
        def decorator(f):
            return f
        return decorator
    
    class st:
        @staticmethod
        def text(*args, **kwargs):
            return None
        
        @staticmethod
        def dictionaries(*args, **kwargs):
            return None
        
        @staticmethod
        def lists(*args, **kwargs):
            return None
        
        @staticmethod
        def integers(*args, **kwargs):
            return None
        
        @staticmethod
        def booleans(*args, **kwargs):
            return None
        
        @staticmethod
        def none(*args, **kwargs):
            return None

from pyport import PortClient
from pyport.exceptions import PortApiError
from tests.mock_server import MockServer, MockResponse


@unittest.skipIf(not HYPOTHESIS_AVAILABLE, "Hypothesis library not available")
class TestPropertyBased(unittest.TestCase):
    """Property-based test cases for the PyPort client library."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock server
        self.server = MockServer()
        
        # Register a route that echoes the request data
        def echo_response(endpoint, **kwargs):
            json_data = kwargs.get("json", {})
            params = kwargs.get("params", {})
            headers = kwargs.get("headers", {})
            
            return MockResponse(
                status_code=200,
                json_data={
                    "method": kwargs.get("method", "GET"),
                    "endpoint": endpoint,
                    "json": json_data,
                    "params": params,
                    "headers": headers
                }
            )
        
        self.server.register_route("GET", r".*", echo_response)
        self.server.register_route("POST", r".*", echo_response)
        self.server.register_route("PUT", r".*", echo_response)
        self.server.register_route("DELETE", r".*", echo_response)
        
        # Create a client with authentication disabled
        self.client = PortClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            skip_auth=True
        )
        
        # Mock the client's make_request method to use the mock server
        self.mock_make_request = self.server.mock_client_request(self.client)
    
    @given(
        endpoint=text(min_size=1, max_size=100).filter(lambda s: "/" not in s),
        params=dictionaries(
            keys=text(min_size=1, max_size=20),
            values=text(min_size=0, max_size=50)
        )
    )
    def test_get_request_params(self, endpoint, params):
        """Test that GET requests correctly handle query parameters."""
        response = self.client.make_request("GET", endpoint, params=params)
        data = response.json()
        
        self.assertEqual(data["method"], "GET")
        self.assertEqual(data["endpoint"], endpoint)
        self.assertEqual(data["params"], params)
    
    @given(
        endpoint=text(min_size=1, max_size=100).filter(lambda s: "/" not in s),
        json_data=dictionaries(
            keys=text(min_size=1, max_size=20),
            values=st.one_of(
                text(min_size=0, max_size=50),
                integers(-1000, 1000),
                booleans(),
                none()
            )
        )
    )
    def test_post_request_json(self, endpoint, json_data):
        """Test that POST requests correctly handle JSON data."""
        response = self.client.make_request("POST", endpoint, json=json_data)
        data = response.json()
        
        self.assertEqual(data["method"], "POST")
        self.assertEqual(data["endpoint"], endpoint)
        self.assertEqual(data["json"], json_data)
    
    @given(
        endpoint=text(min_size=1, max_size=100).filter(lambda s: "/" not in s),
        json_data=dictionaries(
            keys=text(min_size=1, max_size=20),
            values=st.one_of(
                text(min_size=0, max_size=50),
                integers(-1000, 1000),
                booleans(),
                none()
            )
        )
    )
    def test_put_request_json(self, endpoint, json_data):
        """Test that PUT requests correctly handle JSON data."""
        response = self.client.make_request("PUT", endpoint, json=json_data)
        data = response.json()
        
        self.assertEqual(data["method"], "PUT")
        self.assertEqual(data["endpoint"], endpoint)
        self.assertEqual(data["json"], json_data)
    
    @given(
        endpoint=text(min_size=1, max_size=100).filter(lambda s: "/" not in s),
        params=dictionaries(
            keys=text(min_size=1, max_size=20),
            values=text(min_size=0, max_size=50)
        )
    )
    def test_delete_request_params(self, endpoint, params):
        """Test that DELETE requests correctly handle query parameters."""
        response = self.client.make_request("DELETE", endpoint, params=params)
        data = response.json()
        
        self.assertEqual(data["method"], "DELETE")
        self.assertEqual(data["endpoint"], endpoint)
        self.assertEqual(data["params"], params)
    
    @given(
        endpoint=text(min_size=1, max_size=100).filter(lambda s: "/" not in s),
        headers=dictionaries(
            keys=text(min_size=1, max_size=20),
            values=text(min_size=0, max_size=50)
        )
    )
    def test_request_headers(self, endpoint, headers):
        """Test that requests correctly handle custom headers."""
        response = self.client.make_request("GET", endpoint, headers=headers)
        data = response.json()
        
        self.assertEqual(data["method"], "GET")
        self.assertEqual(data["endpoint"], endpoint)
        
        # The client adds some default headers, so we just check that our custom headers are included
        for key, value in headers.items():
            self.assertEqual(data["headers"].get(key), value)
    
    @given(
        blueprint_id=text(min_size=1, max_size=50).filter(lambda s: "/" not in s),
        entity_data=dictionaries(
            keys=text(min_size=1, max_size=20),
            values=st.one_of(
                text(min_size=0, max_size=50),
                integers(-1000, 1000),
                booleans(),
                none(),
                dictionaries(
                    keys=text(min_size=1, max_size=10),
                    values=st.one_of(
                        text(min_size=0, max_size=20),
                        integers(-100, 100),
                        booleans(),
                        none()
                    )
                )
            )
        )
    )
    def test_create_entity_property(self, blueprint_id, entity_data):
        """
        Test the property that creating an entity with the client correctly
        passes the entity data to the API.
        """
        # Mock the entities service to use our mock server
        with patch('pyport.entities.entities_api_svc.Entities._make_request_with_params') as mock_request:
            # Set up the mock to return a successful response
            mock_response = MagicMock()
            mock_response.json.return_value = {"entity": entity_data}
            mock_request.return_value = mock_response
            
            # Create an entity
            entity = self.client.entities.create_entity(blueprint_id, entity_data)
            
            # Verify that the entity data was passed correctly
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            self.assertEqual(args[0], "POST")
            self.assertEqual(kwargs["json"], entity_data)
            
            # Verify that the response was processed correctly
            self.assertEqual(entity, entity_data)
    
    @given(
        blueprint_id=text(min_size=1, max_size=50).filter(lambda s: "/" not in s),
        entity_id=text(min_size=1, max_size=50).filter(lambda s: "/" not in s),
        entity_data=dictionaries(
            keys=text(min_size=1, max_size=20),
            values=st.one_of(
                text(min_size=0, max_size=50),
                integers(-1000, 1000),
                booleans(),
                none()
            )
        )
    )
    def test_update_entity_property(self, blueprint_id, entity_id, entity_data):
        """
        Test the property that updating an entity with the client correctly
        passes the entity data to the API.
        """
        # Mock the entities service to use our mock server
        with patch('pyport.entities.entities_api_svc.Entities._make_request_with_params') as mock_request:
            # Set up the mock to return a successful response
            mock_response = MagicMock()
            mock_response.json.return_value = {"entity": entity_data}
            mock_request.return_value = mock_response
            
            # Update an entity
            entity = self.client.entities.update_entity(blueprint_id, entity_id, entity_data)
            
            # Verify that the entity data was passed correctly
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            self.assertEqual(args[0], "PUT")
            self.assertEqual(kwargs["json"], entity_data)
            
            # Verify that the response was processed correctly
            self.assertEqual(entity, entity_data)
    
    @given(
        page=st.integers(min_value=1, max_value=100),
        per_page=st.integers(min_value=1, max_value=100)
    )
    def test_pagination_property(self, page, per_page):
        """
        Test the property that pagination parameters are correctly passed to the API.
        """
        # Mock the blueprints service to use our mock server
        with patch('pyport.blueprints.blueprint_api_svc.Blueprints._make_request_with_params') as mock_request:
            # Set up the mock to return a successful response
            mock_response = MagicMock()
            mock_response.json.return_value = {"blueprints": []}
            mock_request.return_value = mock_response
            
            # Get blueprints with pagination
            self.client.blueprints.get_blueprints(page=page, per_page=per_page)
            
            # Verify that the pagination parameters were passed correctly
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            self.assertEqual(args[0], "GET")
            self.assertEqual(kwargs["params"]["page"], page)
            self.assertEqual(kwargs["params"]["per_page"], per_page)


if __name__ == "__main__":
    unittest.main()
