import unittest
from unittest.mock import MagicMock
from src.pyport.checklist.checklist_api_svc import Checklist

class TestChecklist(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.checklist = Checklist(self.mock_client)

    def test_get_checklists(self):
        fake_checklists = [{"id": "cl1"}, {"id": "cl2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"checklists": fake_checklists}
        self.mock_client.make_request.return_value = mock_response

        result = self.checklist.get_checklists()
        self.mock_client.make_request.assert_called_once_with("GET", "checklists")
        self.assertEqual(result, fake_checklists)

    def test_get_checklist(self):
        checklist_id = "cl1"
        fake_checklist = {"id": checklist_id, "name": "Test Checklist"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"checklist": fake_checklist}
        self.mock_client.make_request.return_value = mock_response

        result = self.checklist.get_checklist(checklist_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"checklists/{checklist_id}")
        self.assertEqual(result, fake_checklist)

    def test_create_checklist(self):
        checklist_data = {"name": "New Checklist"}
        fake_response_data = {"id": "cl_new", "name": "New Checklist"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.checklist.create_checklist(checklist_data)
        self.mock_client.make_request.assert_called_once_with("POST", "checklists", json=checklist_data)
        self.assertEqual(result, fake_response_data)

    def test_update_checklist(self):
        checklist_id = "cl1"
        checklist_data = {"name": "Updated Checklist"}
        fake_response_data = {"id": checklist_id, "name": "Updated Checklist"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.checklist.update_checklist(checklist_id, checklist_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"checklists/{checklist_id}", json=checklist_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_checklist(self):
        checklist_id = "cl1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.checklist.delete_checklist(checklist_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"checklists/{checklist_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
