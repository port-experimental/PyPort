import unittest
from unittest.mock import MagicMock
# Import directly from the source code.
from src.pyport.apps.apps_api_svc import Apps

class TestApps(unittest.TestCase):
    def setUp(self):
        # Create a dummy client with a mocked make_request method.
        self.mock_client = MagicMock()
        self.apps = Apps(self.mock_client)

    def test_get_apps(self):
        fake_apps = [{"id": "app1"}, {"id": "app2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"apps": fake_apps}
        self.mock_client.make_request.return_value = mock_response

        result = self.apps.get_apps()
        self.mock_client.make_request.assert_called_once_with("GET", "apps")
        self.assertEqual(result, fake_apps)

    def test_get_app(self):
        app_id = "app1"
        fake_app = {"id": app_id, "name": "Test App"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"app": fake_app}
        self.mock_client.make_request.return_value = mock_response

        result = self.apps.get_app(app_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"apps/{app_id}")
        self.assertEqual(result, fake_app)

    def test_create_app(self):
        app_data = {"name": "New App"}
        fake_response_data = {"id": "app_new", "name": "New App"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.apps.create_app(app_data)
        self.mock_client.make_request.assert_called_once_with("POST", "apps", json=app_data)
        self.assertEqual(result, fake_response_data)

    def test_update_app(self):
        app_id = "app1"
        app_data = {"name": "Updated App"}
        fake_response_data = {"id": app_id, "name": "Updated App"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.apps.update_app(app_id, app_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"apps/{app_id}", json=app_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_app(self):
        app_id = "app1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.apps.delete_app(app_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"apps/{app_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
