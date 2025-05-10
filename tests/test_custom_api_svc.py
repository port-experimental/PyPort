import unittest
from unittest.mock import MagicMock
import requests

from pyport.custom.custom_api_svc import (
    validate_http_method,
    validate_path,
    Custom,
    VALID_HTTP_METHODS
)

class TestValidations(unittest.TestCase):
    def test_validate_http_method_valid(self):
        # Ensure all valid methods pass without error.
        for method in VALID_HTTP_METHODS:
            try:
                validate_http_method(method)
            except ValueError:
                self.fail(f"validate_http_method raised ValueError unexpectedly for {method}")

    def test_validate_http_method_invalid(self):
        # An invalid method should raise ValueError.
        with self.assertRaises(ValueError):
            validate_http_method("INVALID")

    def test_validate_path_valid(self):
        # A valid path should pass.
        try:
            validate_path("blueprints/123/entities")
        except ValueError:
            self.fail("validate_path raised ValueError unexpectedly for a valid path.")

    def test_validate_path_empty(self):
        # An empty path should raise ValueError.
        with self.assertRaises(ValueError):
            validate_path("")

    def test_validate_path_with_spaces(self):
        # A path containing spaces should raise ValueError.
        with self.assertRaises(ValueError):
            validate_path("blue prints/123")

class DummyClient:
    """
    A dummy client to simulate the behavior of the main client.
    It provides a public default_headers property and a make_request method.
    """
    def __init__(self):
        self._session = MagicMock()
        self._session.headers = {"Authorization": "Bearer default", "Content-Type": "application/json"}

    @property
    def default_headers(self) -> dict:
        return dict(self._session.headers)

    def make_request(self, method, path, **kwargs):
        # For testing, record the call parameters and return a fake response.
        self.called_method = method
        self.called_path = path
        self.called_kwargs = kwargs
        fake_response = MagicMock(spec=requests.Response)
        fake_response.raise_for_status.return_value = None
        fake_response.status_code = 200
        fake_response.json.return_value = {"dummy": "response"}
        return fake_response

class TestCustomSendRequest(unittest.TestCase):
    def setUp(self):
        # Use DummyClient so we can inspect the parameters passed.
        self.dummy_client = DummyClient()
        self.custom = Custom(self.dummy_client)

    def test_send_request_without_custom_headers(self):
        # When no custom headers are provided, send_request sets merged_headers to None.
        result = self.custom.send_request("GET", "test/path")
        # Verify that make_request was called with headers set to None.
        self.assertEqual(self.dummy_client.called_kwargs.get("headers"), None)
        self.assertEqual(self.dummy_client.called_kwargs.get("params"), None)
        self.assertEqual(self.dummy_client.called_kwargs.get("data"), None)
        self.assertEqual(self.dummy_client.called_kwargs.get("json"), None)
        self.assertEqual(self.dummy_client.called_kwargs.get("timeout"), 10)

    def test_send_request_with_custom_headers(self):
        # When custom headers are provided, they should merge with the default headers.
        custom_headers = {"X-Custom": "value"}
        result = self.custom.send_request("POST", "test/path", headers=custom_headers, json_data={"key": "val"})
        # Expected headers: a copy of default_headers updated with custom_headers.
        expected_headers = self.dummy_client.default_headers.copy()
        expected_headers.update(custom_headers)
        self.assertEqual(self.dummy_client.called_kwargs.get("headers"), expected_headers)
        self.assertEqual(self.dummy_client.called_kwargs.get("json"), {"key": "val"})
        self.assertEqual(self.dummy_client.called_kwargs.get("timeout"), 10)

    def test_send_request_invalid_method(self):
        # An invalid HTTP method should cause a ValueError.
        with self.assertRaises(ValueError):
            self.custom.send_request("INVALID", "test/path")

    def test_send_request_invalid_path(self):
        # An invalid path (e.g. with spaces) should cause a ValueError.
        with self.assertRaises(ValueError):
            self.custom.send_request("GET", "invalid path")

if __name__ == '__main__':
    unittest.main()
