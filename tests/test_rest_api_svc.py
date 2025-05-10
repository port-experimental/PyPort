import unittest
from unittest.mock import patch, MagicMock
import requests

from pyport.services.rest_api_svc import post_request

class TestPostRequest(unittest.TestCase):

    @patch('src.pyport.services.rest_api_svc.requests.post')
    def test_successful_with_all_params(self, mock_post):
        # Create a fake successful response.
        fake_response = MagicMock(spec=requests.Response)
        fake_response.raise_for_status.return_value = None  # No exception.
        fake_response.status_code = 200
        mock_post.return_value = fake_response

        url = "http://example.com/api"
        headers = {"Content-Type": "application/json"}
        params = {"q": "test"}
        data = {"key": "value"}

        result = post_request(url, headers=headers, params=params, data=data)

        # Check that requests.post was called correctly.
        mock_post.assert_called_once_with(url, headers=headers, params=params, json=data, timeout=10)
        self.assertEqual(result, fake_response)

    @patch('src.pyport.services.rest_api_svc.requests.post')
    def test_successful_with_minimal_params(self, mock_post):
        # Test calling post_request with only the URL.
        fake_response = MagicMock(spec=requests.Response)
        fake_response.raise_for_status.return_value = None
        fake_response.status_code = 200
        mock_post.return_value = fake_response

        url = "http://example.com/api"
        result = post_request(url)

        mock_post.assert_called_once_with(url, headers=None, params=None, json=None, timeout=10)
        self.assertEqual(result, fake_response)

    @patch('src.pyport.services.rest_api_svc.requests.post')
    def test_failure_request_exception(self, mock_post):
        # Simulate requests.post raising a RequestException.
        mock_post.side_effect = requests.exceptions.RequestException("Error occurred")

        url = "http://example.com/api"
        result = post_request(url)
        self.assertIsNone(result)

    @patch('src.pyport.services.rest_api_svc.requests.post')
    def test_failure_raise_for_status(self, mock_post):
        # Create a fake response that raises an HTTPError when raise_for_status is called.
        fake_response = MagicMock(spec=requests.Response)
        fake_response.raise_for_status.side_effect = requests.HTTPError("Bad status")
        fake_response.status_code = 400
        mock_post.return_value = fake_response

        url = "http://example.com/api"
        result = post_request(url)
        self.assertIsNone(result)

    @patch('src.pyport.services.rest_api_svc.requests.post')
    @patch('src.pyport.services.rest_api_svc.logging.error')
    def test_logging_on_failure(self, mock_log_error, mock_post):
        # Simulate a failure so that logging.error is called.
        mock_post.side_effect = requests.exceptions.RequestException("Test error")
        url = "http://example.com/api"
        result = post_request(url)
        self.assertIsNone(result)
        # Ensure logging.error was called with a message containing "Request failed"
        mock_log_error.assert_called()
        args, _ = mock_log_error.call_args
        self.assertIn("Request failed", args[0])

if __name__ == '__main__':
    unittest.main()
