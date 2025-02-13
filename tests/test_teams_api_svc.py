import unittest
from unittest.mock import MagicMock
from src.pyport.teams.teams_api_svc import Teams

class TestTeams(unittest.TestCase):
    def setUp(self):
        # Create a dummy client with a mocked make_request method.
        self.mock_client = MagicMock()
        self.teams = Teams(self.mock_client)

    def test_get_teams(self):
        fake_teams = [{"id": "team1"}, {"id": "team2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"teams": fake_teams}
        self.mock_client.make_request.return_value = mock_response

        result = self.teams.get_teams()
        self.mock_client.make_request.assert_called_once_with("GET", "teams")
        self.assertEqual(result, fake_teams)

    def test_get_team(self):
        team_id = "team1"
        fake_team = {"id": team_id, "name": "Test Team"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"team": fake_team}
        self.mock_client.make_request.return_value = mock_response

        result = self.teams.get_team(team_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"teams/{team_id}")
        self.assertEqual(result, fake_team)

    def test_create_team(self):
        team_data = {"name": "New Team"}
        fake_response_data = {"id": "team_new", "name": "New Team"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.teams.create_team(team_data)
        self.mock_client.make_request.assert_called_once_with("POST", "teams", json=team_data)
        self.assertEqual(result, fake_response_data)

    def test_update_team(self):
        team_id = "team1"
        team_data = {"name": "Updated Team"}
        fake_response_data = {"id": team_id, "name": "Updated Team"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.teams.update_team(team_id, team_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"teams/{team_id}", json=team_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_team(self):
        team_id = "team1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.teams.delete_team(team_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"teams/{team_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
