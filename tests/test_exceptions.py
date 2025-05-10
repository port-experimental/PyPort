import unittest

from pyport.exceptions import (
    PortApiError,
    PortAuthenticationError,
    PortPermissionError,
    PortResourceNotFoundError,
    PortValidationError,
    PortRateLimitError,
    PortServerError,
    PortTimeoutError,
    PortConnectionError,
    PortConfigurationError
)


class TestExceptions(unittest.TestCase):
    def test_port_api_error_init(self):
        # Test basic initialization
        error = PortApiError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsNone(error.status_code)
        self.assertIsNone(error.endpoint)
        self.assertIsNone(error.method)
        self.assertIsNone(error.response_body)
        self.assertIsNone(error.request_params)

        # Test initialization with all parameters
        error = PortApiError(
            message="Test error",
            status_code=400,
            endpoint="test-endpoint",
            method="GET",
            response_body={"error": "Bad request"},
            request_params={"param": "value"}
        )
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.endpoint, "test-endpoint")
        self.assertEqual(error.method, "GET")
        self.assertEqual(error.response_body, {"error": "Bad request"})
        self.assertEqual(error.request_params, {"param": "value"})
        self.assertIn("Test error", str(error))
        self.assertIn("GET", str(error))
        self.assertIn("test-endpoint", str(error))
        self.assertIn("400", str(error))

    def test_port_api_error_is_client_error(self):
        # Test is_client_error method
        error = PortApiError("Test error", status_code=400)
        self.assertTrue(error.is_client_error())

        error = PortApiError("Test error", status_code=499)
        self.assertTrue(error.is_client_error())

        error = PortApiError("Test error", status_code=500)
        self.assertFalse(error.is_client_error())

        error = PortApiError("Test error")  # No status code
        self.assertFalse(error.is_client_error())

    def test_port_api_error_is_server_error(self):
        # Test is_server_error method
        error = PortApiError("Test error", status_code=500)
        self.assertTrue(error.is_server_error())

        error = PortApiError("Test error", status_code=599)
        self.assertTrue(error.is_server_error())

        error = PortApiError("Test error", status_code=400)
        self.assertFalse(error.is_server_error())

        error = PortApiError("Test error")  # No status code
        self.assertFalse(error.is_server_error())

    def test_port_api_error_is_transient(self):
        # Test is_transient method
        error = PortApiError("Test error", status_code=500)
        self.assertTrue(error.is_transient())

        error = PortRateLimitError("Test error", status_code=429)
        self.assertTrue(error.is_transient())

        error = PortConnectionError("Test error")
        self.assertTrue(error.is_transient())

        error = PortTimeoutError("Test error")
        self.assertTrue(error.is_transient())

        error = PortValidationError("Test error", status_code=400)
        self.assertFalse(error.is_transient())

    def test_port_authentication_error(self):
        # Test PortAuthenticationError
        error = PortAuthenticationError("Authentication failed")
        self.assertIsInstance(error, PortApiError)
        self.assertEqual(str(error), "Authentication failed")

    def test_port_permission_error(self):
        # Test PortPermissionError
        error = PortPermissionError("Permission denied")
        self.assertIsInstance(error, PortApiError)
        self.assertEqual(str(error), "Permission denied")

    def test_port_resource_not_found_error(self):
        # Test PortResourceNotFoundError
        error = PortResourceNotFoundError("Resource not found")
        self.assertIsInstance(error, PortApiError)
        self.assertEqual(str(error), "Resource not found")

    def test_port_validation_error(self):
        # Test PortValidationError
        error = PortValidationError("Validation failed")
        self.assertIsInstance(error, PortApiError)
        self.assertEqual(str(error), "Validation failed")

    def test_port_rate_limit_error(self):
        # Test PortRateLimitError
        error = PortRateLimitError("Rate limit exceeded", retry_after=60)
        self.assertIsInstance(error, PortApiError)
        self.assertEqual(str(error), "Rate limit exceeded")
        self.assertEqual(error.retry_after, 60)

    def test_port_server_error(self):
        # Test PortServerError
        error = PortServerError("Server error")
        self.assertIsInstance(error, PortApiError)
        self.assertEqual(str(error), "Server error")

    def test_port_timeout_error(self):
        # Test PortTimeoutError
        error = PortTimeoutError("Request timed out")
        self.assertIsInstance(error, PortApiError)
        self.assertEqual(str(error), "Request timed out")

    def test_port_connection_error(self):
        # Test PortConnectionError
        error = PortConnectionError("Connection failed")
        self.assertIsInstance(error, PortApiError)
        self.assertEqual(str(error), "Connection failed")

    def test_port_configuration_error(self):
        # Test PortConfigurationError
        error = PortConfigurationError("Configuration error")
        # PortConfigurationError is a direct subclass of Exception, not PortApiError
        self.assertEqual(str(error), "Configuration error")


if __name__ == "__main__":
    unittest.main()
