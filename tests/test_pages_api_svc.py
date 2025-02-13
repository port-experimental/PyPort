import unittest
from unittest.mock import MagicMock, patch
5
from src.pyport.pages.pages_api_svc import Pages
from src.pyport.api_client import PortClient

class TestPagesService(unittest.TestCase):
    def setUp(self):
        # Patch environment-dependent methods to return dummy values.
        patcher_env = patch('src.pyport.api_client.PortClient._get_local_env_cred', return_value=('dummy_id', 'dummy_secret'))
        self.addCleanup(patcher_env.stop)
        self.mock_get_local_env_cred = patcher_env.start()

        patcher_token = patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
        self.addCleanup(patcher_token.stop)
        self.mock_get_access_token = patcher_token.start()

        # Create a dummy PortClient and override its make_request method.
        self.client = PortClient(auto_refresh=False)
        self.client.make_request = MagicMock()
        self.pages = Pages(self.client)
        self.blueprint_id = "bp_123"
        self.page_id = "page_456"

    def test_get_pages(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"pages": [{"id": self.page_id}]}
        self.client.make_request.return_value = dummy_response

        result = self.pages.get_pages(self.blueprint_id)
        self.client.make_request.assert_called_once_with('GET', f"blueprints/{self.blueprint_id}/pages")
        self.assertEqual(result, [{"id": self.page_id}])

    def test_get_page(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"page": {"id": self.page_id}}
        self.client.make_request.return_value = dummy_response

        result = self.pages.get_page(self.blueprint_id, self.page_id)
        self.client.make_request.assert_called_once_with('GET', f"blueprints/{self.blueprint_id}/pages/{self.page_id}")
        self.assertEqual(result, {"id": self.page_id})

    def test_create_page(self):
        page_data = {"title": "Test Page"}
        dummy_response = MagicMock()
        dummy_response.json.return_value = page_data
        self.client.make_request.return_value = dummy_response

        result = self.pages.create_page(self.blueprint_id, page_data)
        self.client.make_request.assert_called_once_with('POST', f"blueprints/{self.blueprint_id}/pages", json=page_data)
        self.assertEqual(result, page_data)

    def test_update_page(self):
        page_data = {"title": "Updated Test Page"}
        dummy_response = MagicMock()
        dummy_response.json.return_value = page_data
        self.client.make_request.return_value = dummy_response

        result = self.pages.update_page(self.blueprint_id, self.page_id, page_data)
        self.client.make_request.assert_called_once_with('PUT', f"blueprints/{self.blueprint_id}/pages/{self.page_id}", json=page_data)
        self.assertEqual(result, page_data)

    def test_delete_page(self):
        dummy_response = MagicMock()
        dummy_response.status_code = 204
        self.client.make_request.return_value = dummy_response

        result = self.pages.delete_page(self.blueprint_id, self.page_id)
        self.client.make_request.assert_called_once_with('DELETE', f"blueprints/{self.blueprint_id}/pages/{self.page_id}")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
