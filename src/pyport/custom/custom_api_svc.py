"""Custom API service for Port custom resources.

This module provides methods for managing custom resources and
custom API operations in Port."""

from typing import Dict, Any, Optional
from ..models.api_category import BaseResource

# Define valid HTTP methods
VALID_HTTP_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}


def validate_http_method(method: str) -> None:
    """
    Validate that the provided HTTP method is one of the allowed values.
    Raises a ValueError if the method is invalid.
    """
    if method.upper() not in VALID_HTTP_METHODS:
        raise ValueError(f"Invalid HTTP method: {method}. Valid methods are: {', '.join(VALID_HTTP_METHODS)}")


def validate_path(path: str) -> None:
    """
    Validate that the provided path is a non-empty string that does not contain spaces.
    Raises a ValueError if the path is invalid.
    """
    if not path or not isinstance(path, str):
        raise ValueError("Path must be a non-empty string.")
    if ' ' in path:
        raise ValueError("Path should not contain spaces.")


class Custom(BaseResource):
    """
    Custom API category to execute arbitrary REST API commands.
    This module exposes a generic function that allows you to send any REST request,
    specifying the HTTP method, path, headers, parameters, and payload.
    """

    def _prepare_headers(self, headers: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
        """
        Prepare headers for the request by merging with default headers.

        :param headers: Custom headers to include in the request.
        :return: Merged headers or None if no custom headers provided.
        """
        default_headers = self._client.default_headers

        if headers:
            merged_headers = default_headers.copy()
            merged_headers.update(headers)
            return merged_headers
        return None

    def send_request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json_data: Optional[Any] = None,
        timeout: int = 10
    ) -> Any:
        """
        Send a custom REST API request after validating the method and path.

        :param method: HTTP method (GET, POST, PUT, DELETE, etc.)
        :param path: API path (e.g. "blueprints/123/entities").
        :param headers: Optional headers to include in the request.
        :param params: Optional URL query parameters.
        :param data: Optional raw data to send in the request body.
        :param json_data: Optional JSON data to send in the request body.
        :param timeout: Request timeout in seconds.
        :return: The response object from requests.
        :raises: ValueError if the HTTP method or path is invalid.
        """
        # Validate inputs
        validate_http_method(method)
        validate_path(path)

        # Prepare headers
        merged_headers = self._prepare_headers(headers)

        # Delegate to the client's make_request method
        return self._client.make_request(
            method,
            path,
            headers=merged_headers,
            params=params,
            data=data,
            json=json_data,
            timeout=timeout
        )
