import unittest
from unittest.mock import MagicMock, patch
from src.pyport.custom.custom_api_svc import Custom
from src.pyport.api_client import PortClient


class TestCustomService(unittest.TestCase):
    def setUp(self):
        patcher_env = patch('src.pyport.api_client.PortClient._get_local_env_cred', return_value=('dummy_id', 'dummy_secret'))
        self.addCleanup(patcher_env.stop)
        self.mock_get_local_env_cred = patcher_env.start()

        patcher_token = patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
        self.addCleanup(patcher_token.stop)
        self.mock_get_access_token = patcher_token.start()

        self.client = PortClient(client_secret="dummy_secret", client_id="dummy_id", us_region=True)
        self.client.make_request = MagicMock()
        self.custom = Custom(self.client)
        self.test_path = "custom/endpoint"

    def test_send_request_get(self):
        # Test a simple GET request
        dummy_response = MagicMock()
        dummy_response.content = True
        dummy_response.json.return_value = {"data": "test_data"}
        self.client.make_request.return_value = dummy_response

        result = self.custom.send_request(self.test_path)
        self.client.make_request.assert_called_once_with('GET', self.test_path)
        self.assertEqual(result, {"data": "test_data"})

    def test_send_request_post_with_json(self):
        # Test a POST request with JSON data
        json_data = {"key": "value"}
        dummy_response = MagicMock()
        dummy_response.content = True
        dummy_response.json.return_value = {"success": True}
        self.client.make_request.return_value = dummy_response

        result = self.custom.send_request(self.test_path, method="post", json_data=json_data)
        self.client.make_request.assert_called_once_with('POST', self.test_path, json=json_data)
        self.assertEqual(result, {"success": True})

    def test_send_request_with_params(self):
        # Test a request with query parameters
        params = {"filter": "value"}
        dummy_response = MagicMock()
        dummy_response.content = True
        dummy_response.json.return_value = {"filtered": "data"}
        self.client.make_request.return_value = dummy_response

        result = self.custom.send_request(self.test_path, params=params)
        self.client.make_request.assert_called_once_with('GET', self.test_path, params=params)
        self.assertEqual(result, {"filtered": "data"})

    def test_send_request_with_headers(self):
        # Test a request with custom headers
        headers = {"X-Custom-Header": "value"}
        dummy_response = MagicMock()
        dummy_response.content = True
        dummy_response.json.return_value = {"data": "with_custom_header"}
        self.client.make_request.return_value = dummy_response

        result = self.custom.send_request(self.test_path, headers=headers)
        self.client.make_request.assert_called_once_with('GET', self.test_path, headers=headers)
        self.assertEqual(result, {"data": "with_custom_header"})

    def test_send_request_with_data(self):
        # Test a request with form data
        data = "raw_data"
        dummy_response = MagicMock()
        dummy_response.content = True
        dummy_response.json.return_value = {"received": "raw_data"}
        self.client.make_request.return_value = dummy_response

        result = self.custom.send_request(self.test_path, method="PUT", data=data)
        self.client.make_request.assert_called_once_with('PUT', self.test_path, data=data)
        self.assertEqual(result, {"received": "raw_data"})

    def test_send_request_no_content(self):
        # Test a request that returns no content (e.g., 204 No Content)
        dummy_response = MagicMock()
        dummy_response.content = False
        self.client.make_request.return_value = dummy_response

        result = self.custom.send_request(self.test_path, method="DELETE")
        self.client.make_request.assert_called_once_with('DELETE', self.test_path)
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main() 