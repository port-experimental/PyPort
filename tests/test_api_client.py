import os
import unittest
from unittest.mock import patch, MagicMock
import requests

from src.pyport.api_client import PortClient

class TestPortClient(unittest.TestCase):
    def setUp(self):
        # Ensure environment variables are set for tests that don't patch them
        os.environ['PORT_CLIENT_ID'] = 'dummy_id'
        os.environ['PORT_CLIENT_SECRET'] = 'dummy_secret'

    def tearDown(self):
        os.environ.pop('PORT_CLIENT_ID', None)
        os.environ.pop('PORT_CLIENT_SECRET', None)

    @patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
    def test_initialization(self, mock_get_token):
        """Test that PortClient initializes sub-clients and session headers correctly."""
        client = PortClient(auto_refresh=False)
        self.assertEqual(client.token, 'dummy_token')
        self.assertEqual(client._session.headers.get("Authorization"), "Bearer dummy_token")
        self.assertIsNotNone(client.blueprints)
        self.assertIsNotNone(client.entities)
        self.assertIsNotNone(client.actions)
        self.assertIsNotNone(client.pages)

    '''
    @Todo: Fix the below test cases
    def test_get_local_env_cred_failure(self):
        """Test that _get_local_env_cred raises ValueError when env variables are missing."""
        os.environ.pop('PORT_CLIENT_ID', None)
        os.environ.pop('PORT_CLIENT_SECRET', None)
        client = PortClient(auto_refresh=False)
        with self.assertRaises(ValueError) as context:
            client._get_local_env_cred()
        self.assertIn("Environment variables PORT_CLIENT_ID or PORT_CLIENT_SECRET are not set", str(context.exception))
    '''

    @patch('src.pyport.api_client.requests.post')
    def test_get_access_token_success(self, mock_post):
        """Test that _get_access_token returns the token on a successful API call."""
        expected_token = "real_dummy_token"
        dummy_response = MagicMock()
        dummy_response.status_code = 200
        dummy_response.json.return_value = {"accessToken": expected_token}
        mock_post.return_value = dummy_response

        # Clear env variables to force _get_local_env_cred to use patch
        os.environ['PORT_CLIENT_ID'] = 'dummy_id'
        os.environ['PORT_CLIENT_SECRET'] = 'dummy_secret'

        client = PortClient(auto_refresh=False)
        # Force calling _get_access_token by directly invoking it:
        token = client._get_access_token()
        self.assertEqual(token, expected_token)

    @patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
    @patch('src.pyport.api_client.requests.Session.request')
    def test_make_request_success(self, mock_request, mock_get_token):
        """Test that make_request returns the expected JSON on success."""
        expected_json = {"key": "value"}
        dummy_response = MagicMock()
        dummy_response.status_code = 200
        dummy_response.json.return_value = expected_json
        mock_request.return_value = dummy_response

        client = PortClient(auto_refresh=False)
        response = client.make_request('GET', 'test-endpoint')
        mock_request.assert_called_once_with('GET', f"{client.api_url}/test-endpoint")
        self.assertEqual(response.json(), expected_json)

    @patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
    @patch('src.pyport.api_client.requests.Session.request')
    def test_make_request_failure(self, mock_request, mock_get_token):
        """Test that make_request raises an exception on HTTP error."""
        dummy_response = MagicMock()
        dummy_response.status_code = 404
        dummy_response.raise_for_status.side_effect = requests.HTTPError("Not Found")
        mock_request.return_value = dummy_response

        client = PortClient(auto_refresh=False)
        with self.assertRaises(requests.HTTPError) as context:
            client.make_request('GET', 'nonexistent-endpoint')
        self.assertIn("Not Found", str(context.exception))


if __name__ == '__main__':
    unittest.main()
