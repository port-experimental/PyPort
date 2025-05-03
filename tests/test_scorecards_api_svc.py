import unittest
from unittest.mock import MagicMock
# Import directly from the source.
from src.pyport.scorecards.scorecards_api_svc import Scorecards

class TestScorecards(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.scorecards = Scorecards(self.mock_client)

    def test_create_scorecard(self):
        scorecard_data = {"name": "New Scorecard"}
        fake_response_data = {"id": "score_new", "name": "New Scorecard"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.scorecards.create_scorecard(scorecard_data)
        self.mock_client.make_request.assert_called_once_with("POST", "scorecards", json=scorecard_data)
        self.assertEqual(result, fake_response_data)

    def test_update_scorecard(self):
        scorecard_id = "score1"
        scorecard_data = {"name": "Updated Scorecard"}
        fake_response_data = {"id": scorecard_id, "name": "Updated Scorecard"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.scorecards.update_scorecard(scorecard_id, scorecard_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"scorecards/{scorecard_id}", json=scorecard_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_scorecard(self):
        scorecard_id = "score1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.scorecards.delete_scorecard(scorecard_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"scorecards/{scorecard_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
