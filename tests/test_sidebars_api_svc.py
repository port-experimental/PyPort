import unittest
from unittest.mock import MagicMock
from src.pyport.sidebars.sidebars_api_svc import Sidebars

class TestSidebars(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.sidebars = Sidebars(self.mock_client)

    def test_get_sidebars(self):
        fake_sidebars = [{"id": "sidebar1"}, {"id": "sidebar2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"sidebars": fake_sidebars}
        self.mock_client.make_request.return_value = mock_response

        result = self.sidebars.get_sidebars()
        self.mock_client.make_request.assert_called_once_with("GET", "sidebars")
        self.assertEqual(result, fake_sidebars)

    def test_get_sidebar(self):
        sidebar_id = "sidebar1"
        fake_sidebar = {"id": sidebar_id, "name": "Main Sidebar"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"sidebar": fake_sidebar}
        self.mock_client.make_request.return_value = mock_response

        result = self.sidebars.get_sidebar(sidebar_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"sidebars/{sidebar_id}")
        self.assertEqual(result, fake_sidebar)

    def test_create_sidebar(self):
        sidebar_data = {"name": "New Sidebar"}
        fake_response_data = {"id": "sidebar_new", "name": "New Sidebar"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.sidebars.create_sidebar(sidebar_data)
        self.mock_client.make_request.assert_called_once_with("POST", "sidebars", json=sidebar_data)
        self.assertEqual(result, fake_response_data)

    def test_update_sidebar(self):
        sidebar_id = "sidebar1"
        sidebar_data = {"name": "Updated Sidebar"}
        fake_response_data = {"id": sidebar_id, "name": "Updated Sidebar"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.sidebars.update_sidebar(sidebar_id, sidebar_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"sidebars/{sidebar_id}", json=sidebar_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_sidebar(self):
        sidebar_id = "sidebar1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.sidebars.delete_sidebar(sidebar_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"sidebars/{sidebar_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
