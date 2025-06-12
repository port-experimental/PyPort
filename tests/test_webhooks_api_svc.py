import unittest
from unittest.mock import MagicMock

from pyport.webhooks.webhooks_api_svc import Webhooks


class TestWebhooks(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.webhooks = Webhooks(self.mock_client)

    def test_get_webhooks(self):
        # Setup
        expected_result = {"webhooks": [{"id": "webhook1"}, {"id": "webhook2"}]}
        self.webhooks._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.webhooks.get_webhooks()

        # Assert
        self.webhooks._make_request_with_params.assert_called_once_with('GET', 'webhooks', params={})
        self.assertEqual(result, expected_result)

    def test_get_webhook(self):
        # Setup
        webhook_id = "webhook123"
        expected_result = {"webhook": {"id": webhook_id, "name": "Test Webhook"}}
        self.webhooks._make_request_with_params = MagicMock(return_value=expected_result)

        # Execute
        result = self.webhooks.get_webhook(webhook_id)

        # Assert
        self.webhooks._make_request_with_params.assert_called_once_with('GET', f'webhooks/{webhook_id}', params=None)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
