import sys
import os
import unittest
from unittest.mock import patch, MagicMock

from pyport.api_client import PortClient
from pyport.exceptions import PortResourceNotFoundError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

class TestPortClientRequests(unittest.TestCase):
    @patch('src.pyport.client.request.requests.Session.request')
    def test_make_request_success(self, mock_request):
        """Test that make_request returns the expected JSON on a successful API call."""
        expected_json = {"key": "value"}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_json
        mock_request.return_value = mock_response

        client = PortClient(client_secret="dummy_secret", client_id="dummy_id", us_region=True, skip_auth=True)
        response = client.make_request('GET', 'test-endpoint')
        self.assertEqual(response.json(), expected_json)

    @patch('src.pyport.client.request.requests.Session.request')
    def test_make_request_failure(self, mock_request):
        """Test that make_request raises an exception on HTTP errors."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '{"error": "Resource not found"}'
        mock_response.raise_for_status.side_effect = Exception("Not Found")
        mock_request.return_value = mock_response

        client = PortClient(client_secret="dummy_secret", client_id="dummy_id", us_region=True, skip_auth=True)
        with self.assertRaises(Exception) as context:
            client.make_request('GET', 'nonexistent-endpoint')
        # Check that we get a PortResourceNotFoundError with status code 404
        self.assertEqual(context.exception.status_code, 404)


if __name__ == '__main__':
    unittest.main()
