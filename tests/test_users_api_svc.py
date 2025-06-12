import unittest
from unittest.mock import MagicMock
from pyport.users.users_api_svc import Users

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.users = Users(self.mock_client)

    def test_get_users(self):
        expected_result = {"users": [{"id": "user1"}, {"id": "user2"}]}
        self.users._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.users.get_users()
        self.users._make_request_with_params.assert_called_once_with('GET', 'users', params={})
        self.assertEqual(result, expected_result)

    def test_get_user(self):
        user_email = "user@example.com"
        expected_result = {"user": {"email": user_email, "name": "Test User"}}
        self.users._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.users.get_user(user_email)
        self.users._make_request_with_params.assert_called_once_with('GET', f'users/{user_email}', params=None)
        self.assertEqual(result, expected_result)

    def test_invite_user(self):
        invitation_data = {"email": "newuser@example.com", "role": "viewer"}
        expected_result = {"success": True, "invitation_id": "inv123"}
        self.users._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.users.invite_user(invitation_data)
        self.users._make_request_with_params.assert_called_once_with('POST', 'users/invite', json=invitation_data, params=None)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
