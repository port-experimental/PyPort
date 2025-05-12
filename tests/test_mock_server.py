"""
Tests for the mock server.

This module tests the mock server functionality and demonstrates how to use it for testing.
"""

import unittest
from unittest.mock import patch

from pyport import PortClient
from pyport.exceptions import PortResourceNotFoundError
from tests.mock_server import create_mock_server, MockServer, MockResponse


class TestMockServer(unittest.TestCase):
    """Test cases for the mock server."""

    def setUp(self):
        """Set up test fixtures."""
        self.server = create_mock_server()

        # Create a client with authentication disabled
        self.client = PortClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            skip_auth=True
        )

        # Mock the client's make_request method to use the mock server
        self.mock_make_request = self.server.mock_client_request(self.client)

    def test_get_blueprints(self):
        """Test getting all blueprints."""
        blueprints = self.client.blueprints.get_blueprints()

        # Verify the mock was called with the correct arguments
        self.mock_make_request.assert_called_once_with(
            "GET", "blueprints"
        )

        # Verify the response
        self.assertEqual(len(blueprints), 2)
        self.assertEqual(blueprints[0]["identifier"], "service")
        self.assertEqual(blueprints[1]["identifier"], "microservice")

    def test_get_blueprint(self):
        """Test getting a specific blueprint."""
        blueprint = self.client.blueprints.get_blueprint("service")

        # Verify the mock was called with the correct arguments
        self.mock_make_request.assert_called_once_with(
            "GET", "blueprints/service"
        )

        # Verify the response
        self.assertEqual(blueprint["identifier"], "service")
        self.assertEqual(blueprint["title"], "Service")
        self.assertIn("language", blueprint["properties"])

    def test_create_blueprint(self):
        """Test creating a blueprint."""
        blueprint_data = {
            "identifier": "new-blueprint",
            "title": "New Blueprint"
        }

        blueprint = self.client.blueprints.create_blueprint(blueprint_data)

        # Verify the mock was called with the correct arguments
        self.mock_make_request.assert_called_once_with(
            "POST", "blueprints", json=blueprint_data
        )

        # Verify the response
        self.assertEqual(blueprint["identifier"], "new-blueprint")
        self.assertEqual(blueprint["title"], "New Blueprint")

    def test_get_nonexistent_blueprint(self):
        """Test getting a non-existent blueprint."""
        from pyport.exceptions import PortApiError
        with self.assertRaises(PortApiError):
            self.client.blueprints.get_blueprint("non-existent")

        # Verify the mock was called with the correct arguments
        self.mock_make_request.assert_called_once_with(
            "GET", "blueprints/non-existent"
        )

    def test_custom_mock_server(self):
        """Test creating a custom mock server."""
        # Create a new mock server
        server = MockServer()

        # Register a custom route
        server.register_json_response(
            "GET",
            r"^custom/endpoint$",
            {"message": "Custom response"}
        )

        # Create a new client
        client = PortClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            skip_auth=True
        )

        # Mock the client's make_request method
        mock_make_request = server.mock_client_request(client)

        # Make a request to the custom endpoint
        response = client.make_request("GET", "custom/endpoint")

        # Verify the mock was called with the correct arguments
        mock_make_request.assert_called_once_with(
            "GET", "custom/endpoint"
        )

        # Verify the response
        self.assertEqual(response.json(), {"message": "Custom response"})

    def test_mock_response(self):
        """Test creating a mock response directly."""
        # Create a mock response
        response = MockResponse(
            status_code=200,
            json_data={"message": "Test response"}
        )

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Test response"})
        self.assertEqual(response.text, '{"message": "Test response"}')

    def test_mock_error_response(self):
        """Test creating a mock error response."""
        # Create a mock error response
        response = MockResponse(
            status_code=400,
            json_data={"error": "Bad request"},
            reason="Bad Request"
        )

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Bad request"})
        self.assertEqual(response.reason, "Bad Request")

        # Verify that raise_for_status raises an exception
        with self.assertRaises(Exception):
            response.raise_for_status()


if __name__ == "__main__":
    unittest.main()
