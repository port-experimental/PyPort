import unittest
from unittest.mock import MagicMock
from src.pyport.users.users_api_svc import Users

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.users = Users(self.mock_client)

    def test_get_users(self):
        fake_users = [{"id": "user1"}, {"id": "user2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"users": fake_users}
        self.mock_client.make_request.return_value = mock_response

        result = self.users.get_users()
        self.mock_client.make_request.assert_called_once_with("GET", "users")
        self.assertEqual(result, fake_users)

    def test_get_user(self):
        user_id = "user1"
        fake_user = {"id": user_id, "name": "Test User"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"user": fake_user}
        self.mock_client.make_request.return_value = mock_response

        result = self.users.get_user(user_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"users/{user_id}")
        self.assertEqual(result, fake_user)

    def test_create_user(self):
        user_data = {"name": "New User"}
        fake_response_data = {"id": "user_new", "name": "New User"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.users.create_user(user_data)
        self.mock_client.make_request.assert_called_once_with("POST", "users", json=user_data)
        self.assertEqual(result, fake_response_data)

    def test_update_user(self):
        user_id = "user1"
        user_data = {"name": "Updated User"}
        fake_response_data = {"id": user_id, "name": "Updated User"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.users.update_user(user_id, user_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"users/{user_id}", json=user_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_user(self):
        user_id = "user1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.users.delete_user(user_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"users/{user_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
