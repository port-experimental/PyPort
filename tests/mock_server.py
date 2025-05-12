"""
Mock server for testing the PyPort client library.

This module provides a mock server that simulates the Port API for testing purposes.
It allows testing the client library without making actual API requests.
"""

import json
import re
from typing import Dict, List, Any, Optional, Callable, Tuple, Pattern
from unittest.mock import MagicMock


class MockResponse:
    """Mock response object that simulates a requests.Response object."""

    def __init__(
        self,
        status_code: int = 200,
        content: Optional[bytes] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        reason: str = "OK"
    ):
        """
        Initialize a mock response.

        Args:
            status_code: HTTP status code for the response.
            content: Response content as bytes.
            json_data: Response data as a dictionary (will be converted to JSON).
            headers: Response headers.
            reason: HTTP reason phrase.
        """
        self.status_code = status_code
        self._content = content or b""
        self._json_data = json_data or {}
        self.headers = headers or {}
        self.reason = reason
        self.request = MagicMock()
        self.url = "https://api.getport.io/v1/"
        self.text = json.dumps(self._json_data) if json_data else ""

    def json(self) -> Dict[str, Any]:
        """Return the response data as a dictionary."""
        return self._json_data

    @property
    def content(self) -> bytes:
        """Return the response content as bytes."""
        return self._content

    def raise_for_status(self) -> None:
        """Raise an exception if the status code indicates an error."""
        if 400 <= self.status_code < 600:
            from requests.exceptions import HTTPError
            raise HTTPError(f"HTTP Error: {self.status_code} {self.reason}")


class MockServer:
    """
    Mock server that simulates the Port API for testing purposes.

    This class provides methods for registering mock responses for different API endpoints
    and HTTP methods. It can be used to test the client library without making actual API requests.
    """

    def __init__(self):
        """Initialize the mock server."""
        self.routes: Dict[Tuple[str, Pattern[str]], Callable] = {}
        self.default_response = MockResponse(
            status_code=404,
            json_data={"error": "Not Found"},
            reason="Not Found"
        )

    def register_route(
        self,
        method: str,
        endpoint_pattern: str,
        response_factory: Callable[..., MockResponse]
    ) -> None:
        """
        Register a route with a response factory.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint_pattern: Regex pattern for matching the endpoint.
            response_factory: Function that returns a MockResponse.
        """
        pattern = re.compile(endpoint_pattern)
        self.routes[(method.upper(), pattern)] = response_factory

    def register_json_response(
        self,
        method: str,
        endpoint_pattern: str,
        json_data: Dict[str, Any],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Register a route with a JSON response.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint_pattern: Regex pattern for matching the endpoint.
            json_data: JSON data to return in the response.
            status_code: HTTP status code for the response.
            headers: Response headers.
        """
        def response_factory(*args, **kwargs):
            return MockResponse(
                status_code=status_code,
                json_data=json_data,
                headers=headers
            )

        self.register_route(method, endpoint_pattern, response_factory)

    def register_error_response(
        self,
        method: str,
        endpoint_pattern: str,
        error_message: str,
        status_code: int = 400,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Register a route with an error response.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint_pattern: Regex pattern for matching the endpoint.
            error_message: Error message to return in the response.
            status_code: HTTP status code for the response.
            headers: Response headers.
        """
        def response_factory(*args, **kwargs):
            return MockResponse(
                status_code=status_code,
                json_data={"error": error_message},
                headers=headers,
                reason="Error"
            )

        self.register_route(method, endpoint_pattern, response_factory)

    def handle_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> MockResponse:
        """
        Handle a request and return a mock response.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint: API endpoint.
            **kwargs: Additional request parameters.

        Returns:
            A MockResponse object.
        """
        method = method.upper()

        for (route_method, pattern), response_factory in self.routes.items():
            if method == route_method and pattern.match(endpoint):
                response = response_factory(endpoint=endpoint, **kwargs)

                # If the response is an error response, raise the appropriate exception
                if 400 <= response.status_code < 600:
                    from pyport.error_handling import handle_error_response
                    handle_error_response(response, endpoint, method)

                return response

        return self.default_response

    def mock_client_request(self, client):
        """
        Mock the client's make_request method to use this server.

        Args:
            client: The PortClient instance to mock.

        Returns:
            A MagicMock object that replaces the client's make_request method.
        """
        mock_make_request = MagicMock(side_effect=self._mock_make_request)
        client.make_request = mock_make_request
        return mock_make_request

    def _mock_make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> MockResponse:
        """
        Mock implementation of the client's make_request method.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint: API endpoint.
            **kwargs: Additional request parameters.

        Returns:
            A MockResponse object.
        """
        # Import error handling here to avoid circular imports
        from pyport.exceptions import PortApiError

        response = self.handle_request(method, endpoint, **kwargs)

        # Handle error responses
        if 400 <= response.status_code < 600:
            # Use the generic PortApiError for all error types
            raise PortApiError(
                f"API error: {response.text}",
                status_code=response.status_code,
                endpoint=endpoint,
                method=method
            )

        return response


# Example usage:
def create_mock_server():
    """Create a mock server with some example routes."""
    server = MockServer()

    # Register some example routes
    server.register_json_response(
        "GET",
        r"^blueprints$",
        {
            "blueprints": [
                {"identifier": "service", "title": "Service"},
                {"identifier": "microservice", "title": "Microservice"}
            ]
        }
    )

    server.register_json_response(
        "GET",
        r"^blueprints/service$",
        {
            "blueprint": {
                "identifier": "service",
                "title": "Service",
                "properties": {
                    "language": {
                        "type": "string",
                        "title": "Language",
                        "enum": ["Python", "JavaScript", "Java", "Go"]
                    }
                }
            }
        }
    )

    server.register_json_response(
        "POST",
        r"^blueprints$",
        {
            "blueprint": {
                "identifier": "new-blueprint",
                "title": "New Blueprint"
            }
        }
    )

    server.register_error_response(
        "GET",
        r"^blueprints/non-existent$",
        "Blueprint not found",
        status_code=404
    )

    return server
