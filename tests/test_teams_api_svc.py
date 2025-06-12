import unittest
from unittest.mock import MagicMock
from pyport.teams.teams_api_svc import Teams

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
        expected_result = {"team": {"id": team_id, "name": "Test Team"}}
        self.teams._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.teams.get_team(team_id)
        self.teams._make_request_with_params.assert_called_once_with('GET', f'teams/{team_id}', params=None)
        self.assertEqual(result, expected_result)

    def test_get_teams(self):
        expected_result = {"teams": [{"id": "team1"}, {"id": "team2"}]}
        self.teams._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.teams.get_teams()
        self.teams._make_request_with_params.assert_called_once_with('GET', 'teams', params={})
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
