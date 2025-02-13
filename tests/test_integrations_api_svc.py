import unittest
from unittest.mock import MagicMock
from src.pyport.integrations.integrations_api_svc import Integrations

class TestIntegrations(unittest.TestCase):
    def setUp(self):
        # Create a dummy client with a mocked make_request method.
        self.mock_client = MagicMock()
        self.integrations = Integrations(self.mock_client)

    def test_get_integrations(self):
        # Setup a fake response for get_integrations.
        fake_integrations = [{"id": "int1"}, {"id": "int2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"integrations": fake_integrations}
        self.mock_client.make_request.return_value = mock_response

        result = self.integrations.get_integrations()
        self.mock_client.make_request.assert_called_once_with("GET", "integrations")
        self.assertEqual(result, fake_integrations)

    def test_get_integration(self):
        integration_id = "int1"
        fake_integration = {"id": integration_id, "name": "Test Integration"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"integration": fake_integration}
        self.mock_client.make_request.return_value = mock_response

        result = self.integrations.get_integration(integration_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"integrations/{integration_id}")
        self.assertEqual(result, fake_integration)

    def test_create_integration(self):
        integration_data = {"name": "New Integration"}
        fake_response_data = {"id": "int_new", "name": "New Integration"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.integrations.create_integration(integration_data)
        self.mock_client.make_request.assert_called_once_with("POST", "integrations", json=integration_data)
        self.assertEqual(result, fake_response_data)

    def test_update_integration(self):
        integration_id = "int1"
        integration_data = {"name": "Updated Integration"}
        fake_response_data = {"id": integration_id, "name": "Updated Integration"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.integrations.update_integration(integration_id, integration_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"integrations/{integration_id}", json=integration_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_integration(self):
        integration_id = "int1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.integrations.delete_integration(integration_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"integrations/{integration_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
