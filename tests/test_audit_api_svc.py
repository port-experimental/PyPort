import unittest
from unittest.mock import MagicMock
from src.pyport.audit.audit_api_svc import Audit

class TestAudit(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.audit = Audit(self.mock_client)

    def test_get_audit_logs(self):
        fake_audits = [{"id": "audit1"}, {"id": "audit2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"audits": fake_audits}
        self.mock_client.make_request.return_value = mock_response

        result = self.audit.get_audit_logs()
        self.mock_client.make_request.assert_called_once_with("GET", "audit")
        self.assertEqual(result, fake_audits)

    def test_get_audit_log(self):
        audit_id = "audit1"
        fake_audit = {"id": audit_id, "event": "login"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"audit": fake_audit}
        self.mock_client.make_request.return_value = mock_response

        result = self.audit.get_audit_log(audit_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"audit/{audit_id}")
        self.assertEqual(result, fake_audit)

if __name__ == "__main__":
    unittest.main()
