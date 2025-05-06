import unittest
from unittest.mock import MagicMock

from src.pyport.webhooks.webhooks_api_svc import Webhooks


class TestWebhooks(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.webhooks = Webhooks(self.mock_client)

    def test_get_webhooks(self):
        # Setup
        expected_webhooks = [{"id": "webhook1"}, {"id": "webhook2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"webhooks": expected_webhooks}
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.webhooks.get_webhooks()

        # Assert
        self.mock_client.make_request.assert_called_once_with("GET", "webhooks")
        self.assertEqual(result, expected_webhooks)

    def test_get_webhook(self):
        # Setup
        webhook_id = "webhook123"
        expected_webhook = {"id": webhook_id, "name": "Test Webhook"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"webhook": expected_webhook}
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.webhooks.get_webhook(webhook_id)

        # Assert
        self.mock_client.make_request.assert_called_once_with("GET", f"webhooks/{webhook_id}")
        self.assertEqual(result, expected_webhook)


if __name__ == "__main__":
    unittest.main()
