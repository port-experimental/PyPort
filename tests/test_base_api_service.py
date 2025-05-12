"""
Tests for the BaseAPIService class.
"""

import unittest
from unittest.mock import MagicMock, patch

from pyport.services.base_api_service import BaseAPIService


class TestBaseAPIService(unittest.TestCase):
    """Test cases for the BaseAPIService class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = MagicMock()
        self.service = BaseAPIService(self.mock_client, resource_name="test_resource", response_key="test")

    def test_init(self):
        """Test initialization of BaseAPIService."""
        self.assertEqual(self.service._client, self.mock_client)
        self.assertEqual(self.service._resource_name, "test_resource")
        self.assertEqual(self.service._response_key, "test")

    def test_extract_response_data_dict(self):
        """Test extracting data from a dictionary response."""
        response = {"test": {"id": "123", "name": "Test"}}
        result = self.service._extract_response_data(response)
        self.assertEqual(result, {"id": "123", "name": "Test"})

    def test_extract_response_data_list(self):
        """Test extracting data from a list response."""
        response = {"test": [{"id": "123"}, {"id": "456"}]}
        result = self.service._extract_response_data(response)
        self.assertEqual(result, [{"id": "123"}, {"id": "456"}])

    def test_extract_response_data_missing_key(self):
        """Test extracting data when the key is missing."""
        response = {"other_key": {"id": "123"}}
        result = self.service._extract_response_data(response)
        self.assertEqual(result, {})

    def test_handle_pagination_params(self):
        """Test handling pagination parameters."""
        # Test with both parameters
        params = self.service._handle_pagination_params(page=2, per_page=50)
        self.assertEqual(params, {"page": 2, "per_page": 50})

        # Test with only page
        params = self.service._handle_pagination_params(page=2)
        self.assertEqual(params, {"page": 2})

        # Test with only per_page
        params = self.service._handle_pagination_params(per_page=50)
        self.assertEqual(params, {"per_page": 50})

        # Test with no parameters
        params = self.service._handle_pagination_params()
        self.assertEqual(params, {})

    def test_build_endpoint(self):
        """Test building an endpoint from parts."""
        # Test with multiple parts
        endpoint = self.service._build_endpoint("part1", "part2", "part3")
        self.assertEqual(endpoint, "part1/part2/part3")

        # Test with empty parts
        endpoint = self.service._build_endpoint("part1", "", "part3")
        self.assertEqual(endpoint, "part1/part3")

    def test_make_request_with_params(self):
        """Test making a request with parameters."""
        # Set up mock response
        mock_response = MagicMock()
        self.mock_client.make_request.return_value = mock_response

        # Test with parameters
        self.service._make_request_with_params("GET", "test_endpoint", params={"param": "value"})
        self.mock_client.make_request.assert_called_with("GET", "test_endpoint", params={"param": "value"})

        # Test without parameters
        self.service._make_request_with_params("GET", "test_endpoint")
        self.mock_client.make_request.assert_called_with("GET", "test_endpoint")

    def test_get_all(self):
        """Test getting all resources."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test_resource": [{"id": "123"}, {"id": "456"}]}
        self.mock_client.make_request.return_value = mock_response

        # Test with pagination
        result = self.service.get_all(page=2, per_page=50)
        self.mock_client.make_request.assert_called_with(
            "GET", "test_resource", params={"page": 2, "per_page": 50}
        )
        self.assertEqual(result, [{"id": "123"}, {"id": "456"}])

    def test_get_by_id(self):
        """Test getting a resource by ID."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": {"id": "123", "name": "Test"}}
        self.mock_client.make_request.return_value = mock_response

        # Test with default response key
        result = self.service.get_by_id("123")
        self.mock_client.make_request.assert_called_with("GET", "test_resource/123")
        self.assertEqual(result, {"id": "123", "name": "Test"})

        # Test with custom response key
        result = self.service.get_by_id("123", response_key="custom")
        self.assertEqual(result, {})  # Empty because the response doesn't have "custom" key

    def test_create_resource(self):
        """Test creating a resource."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": {"id": "123", "name": "Test"}}
        self.mock_client.make_request.return_value = mock_response

        # Test with default response key
        data = {"name": "Test"}
        result = self.service.create_resource(data)
        self.mock_client.make_request.assert_called_with("POST", "test_resource", json=data)
        self.assertEqual(result, {"id": "123", "name": "Test"})

    def test_update_resource(self):
        """Test updating a resource."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": {"id": "123", "name": "Updated"}}
        self.mock_client.make_request.return_value = mock_response

        # Test with default response key
        data = {"name": "Updated"}
        result = self.service.update_resource("123", data)
        self.mock_client.make_request.assert_called_with("PUT", "test_resource/123", json=data)
        self.assertEqual(result, {"id": "123", "name": "Updated"})

    def test_delete_resource(self):
        """Test deleting a resource."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        # Test successful deletion
        result = self.service.delete_resource("123")
        self.mock_client.make_request.assert_called_with("DELETE", "test_resource/123")
        self.assertTrue(result)

        # Test unsuccessful deletion
        mock_response.status_code = 404
        result = self.service.delete_resource("456")
        self.assertFalse(result)

    def test_get_all_with_custom_params(self):
        """Test getting all resources with custom parameters."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test_resource": [{"id": "123"}, {"id": "456"}]}
        self.mock_client.make_request.return_value = mock_response

        # Test with custom parameters
        result = self.service.get_all(params={"filter": "value"})
        self.mock_client.make_request.assert_called_with(
            "GET", "test_resource", params={"filter": "value"}
        )
        self.assertEqual(result, [{"id": "123"}, {"id": "456"}])

        # Test with both pagination and custom parameters
        result = self.service.get_all(page=2, per_page=50, params={"filter": "value"})
        self.mock_client.make_request.assert_called_with(
            "GET", "test_resource", params={"page": 2, "per_page": 50, "filter": "value"}
        )
        self.assertEqual(result, [{"id": "123"}, {"id": "456"}])

    def test_create_resource_with_params(self):
        """Test creating a resource with query parameters."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": {"id": "123", "name": "Test"}}
        self.mock_client.make_request.return_value = mock_response

        # Test with query parameters
        data = {"name": "Test"}
        params = {"dryRun": "true"}
        result = self.service.create_resource(data, params=params)
        self.mock_client.make_request.assert_called_with(
            "POST", "test_resource", json=data, params=params
        )
        self.assertEqual(result, {"id": "123", "name": "Test"})

    def test_update_resource_with_params(self):
        """Test updating a resource with query parameters."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": {"id": "123", "name": "Updated"}}
        self.mock_client.make_request.return_value = mock_response

        # Test with query parameters
        data = {"name": "Updated"}
        params = {"dryRun": "true"}
        result = self.service.update_resource("123", data, params=params)
        self.mock_client.make_request.assert_called_with(
            "PUT", "test_resource/123", json=data, params=params
        )
        self.assertEqual(result, {"id": "123", "name": "Updated"})

    def test_delete_resource_with_params(self):
        """Test deleting a resource with query parameters."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        # Test with query parameters
        params = {"force": "true"}
        result = self.service.delete_resource("123", params=params)
        self.mock_client.make_request.assert_called_with(
            "DELETE", "test_resource/123", params=params
        )
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
