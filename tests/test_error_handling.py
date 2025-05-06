import unittest
from unittest.mock import MagicMock, patch

import requests

from src.pyport.error_handling import (
    handle_request_exception,
    handle_error_response,
    with_error_handling
)
from src.pyport.exceptions import (
    PortApiError,
    PortAuthenticationError,
    PortPermissionError,
    PortResourceNotFoundError,
    PortValidationError,
    PortRateLimitError,
    PortServerError,
    PortTimeoutError,
    PortConnectionError
)


class TestErrorHandling(unittest.TestCase):
    def test_handle_request_exception_timeout(self):
        # Test handling of timeout exception
        exc = requests.exceptions.Timeout("Connection timed out")
        result = handle_request_exception(exc, "test-endpoint", "GET")

        self.assertIsInstance(result, PortTimeoutError)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")
        self.assertIn("Connection timed out", str(result))

    def test_handle_request_exception_connection_error(self):
        # Test handling of connection error
        exc = requests.exceptions.ConnectionError("Failed to establish connection")
        result = handle_request_exception(exc, "test-endpoint", "GET")

        self.assertIsInstance(result, PortConnectionError)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")
        self.assertIn("Failed to establish connection", str(result))

    def test_handle_request_exception_generic(self):
        # Test handling of generic request exception
        exc = requests.exceptions.RequestException("Generic error")
        result = handle_request_exception(exc, "test-endpoint", "GET")

        self.assertIsInstance(result, PortApiError)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")
        self.assertIn("Generic error", str(result))

    def test_handle_error_response_400(self):
        # Test handling of 400 Bad Request
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"error": "Invalid input"}'
        mock_response.json.return_value = {"error": "Invalid input"}

        result = handle_error_response(mock_response, "test-endpoint", "POST")

        self.assertIsInstance(result, PortValidationError)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "POST")

    def test_handle_error_response_401(self):
        # Test handling of 401 Unauthorized
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = '{"error": "Unauthorized"}'
        mock_response.json.return_value = {"error": "Unauthorized"}

        result = handle_error_response(mock_response, "test-endpoint", "GET")

        self.assertIsInstance(result, PortAuthenticationError)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")

    def test_handle_error_response_403(self):
        # Test handling of 403 Forbidden
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = '{"error": "Forbidden"}'
        mock_response.json.return_value = {"error": "Forbidden"}

        result = handle_error_response(mock_response, "test-endpoint", "GET")

        self.assertIsInstance(result, PortPermissionError)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")

    def test_handle_error_response_404(self):
        # Test handling of 404 Not Found
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '{"error": "Resource not found"}'
        mock_response.json.return_value = {"error": "Resource not found"}

        result = handle_error_response(mock_response, "test-endpoint", "GET")

        self.assertIsInstance(result, PortResourceNotFoundError)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")
        self.assertIn("Resource not found", str(result))

    def test_handle_error_response_429(self):
        # Test handling of 429 Too Many Requests
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = '{"error": "Rate limit exceeded"}'
        mock_response.json.return_value = {"error": "Rate limit exceeded"}
        mock_response.headers = {"Retry-After": "60"}

        result = handle_error_response(mock_response, "test-endpoint", "GET")

        self.assertIsInstance(result, PortRateLimitError)
        self.assertEqual(result.status_code, 429)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")
        self.assertIn("Rate limit exceeded", str(result))

    def test_handle_error_response_500(self):
        # Test handling of 500 Internal Server Error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = '{"error": "Internal server error"}'
        mock_response.json.return_value = {"error": "Internal server error"}

        result = handle_error_response(mock_response, "test-endpoint", "GET")

        self.assertIsInstance(result, PortServerError)
        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")

    def test_handle_error_response_unknown(self):
        # Test handling of unknown status code
        mock_response = MagicMock()
        mock_response.status_code = 418  # I'm a teapot
        mock_response.text = '{"error": "I\'m a teapot"}'
        mock_response.json.return_value = {"error": "I'm a teapot"}

        result = handle_error_response(mock_response, "test-endpoint", "GET")

        self.assertIsInstance(result, PortApiError)
        self.assertEqual(result.status_code, 418)
        self.assertEqual(result.endpoint, "test-endpoint")
        self.assertEqual(result.method, "GET")

    def test_with_error_handling_success(self):
        # Test successful function execution
        @with_error_handling
        def test_func():
            return "success"

        result = test_func()
        self.assertEqual(result, "success")

    def test_with_error_handling_api_error(self):
        # Test handling of API error
        @with_error_handling
        def test_func():
            raise PortApiError("API error")

        with self.assertRaises(PortApiError):
            test_func()

    def test_with_error_handling_not_found_with_handler(self):
        # Test handling of not found error with custom handler
        not_found_handler = MagicMock(return_value="not found handler result")

        def test_func():
            raise PortResourceNotFoundError("Resource not found")

        wrapped_func = with_error_handling(test_func, on_not_found=not_found_handler)
        result = wrapped_func()
        self.assertEqual(result, "not found handler result")
        not_found_handler.assert_called_once()

    def test_with_error_handling_error_with_handler(self):
        # Test handling of generic error with custom handler
        error_handler = MagicMock(return_value="error handler result")

        def test_func():
            raise PortApiError("API error")

        wrapped_func = with_error_handling(test_func, on_error=error_handler)
        result = wrapped_func()
        self.assertEqual(result, "error handler result")
        error_handler.assert_called_once()


if __name__ == "__main__":
    unittest.main()
