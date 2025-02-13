import sys
import os
import unittest
from unittest.mock import patch, MagicMock

from src.pyport.api_client import PortClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

class TestPortClientRequests(unittest.TestCase):
    @patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
    @patch('src.pyport.api_client.requests.Session.request')
    def test_make_request_success(self, mock_request, mock_get_token):
        """Test that make_request returns the expected JSON on a successful API call."""
        expected_json = {"key": "value"}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_json
        mock_request.return_value = mock_response

        client = PortClient(auto_refresh=False)
        response = client.make_request('GET', 'test-endpoint')
        self.assertEqual(response.json(), expected_json)

    @patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
    @patch('src.pyport.api_client.requests.Session.request')
    def test_make_request_failure(self, mock_request, mock_get_token):
        """Test that make_request raises an exception on HTTP errors."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("Not Found")
        mock_request.return_value = mock_response

        client = PortClient(auto_refresh=False)
        with self.assertRaises(Exception) as context:
            client.make_request('GET', 'nonexistent-endpoint')
        self.assertIn("Not Found", str(context.exception))


if __name__ == '__main__':
    unittest.main()
