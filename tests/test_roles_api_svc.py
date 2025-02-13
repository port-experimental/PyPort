import unittest
from unittest.mock import MagicMock
from src.pyport.roles.roles_api_svc import Roles

class TestRoles(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.roles = Roles(self.mock_client)

    def test_get_roles(self):
        fake_roles = [{"id": "role1"}, {"id": "role2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"roles": fake_roles}
        self.mock_client.make_request.return_value = mock_response

        result = self.roles.get_roles()
        self.mock_client.make_request.assert_called_once_with("GET", "roles")
        self.assertEqual(result, fake_roles)

    def test_get_role(self):
        role_id = "role1"
        fake_role = {"id": role_id, "name": "Admin"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"role": fake_role}
        self.mock_client.make_request.return_value = mock_response

        result = self.roles.get_role(role_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"roles/{role_id}")
        self.assertEqual(result, fake_role)

    def test_create_role(self):
        role_data = {"name": "Editor"}
        fake_response_data = {"id": "role_new", "name": "Editor"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.roles.create_role(role_data)
        self.mock_client.make_request.assert_called_once_with("POST", "roles", json=role_data)
        self.assertEqual(result, fake_response_data)

    def test_update_role(self):
        role_id = "role1"
        role_data = {"name": "Super Admin"}
        fake_response_data = {"id": role_id, "name": "Super Admin"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.roles.update_role(role_id, role_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"roles/{role_id}", json=role_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_role(self):
        role_id = "role1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.roles.delete_role(role_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"roles/{role_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
