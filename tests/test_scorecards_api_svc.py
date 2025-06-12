import unittest
from unittest.mock import MagicMock
# Import directly from the source.
from pyport.scorecards.scorecards_api_svc import Scorecards

class TestScorecards(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.scorecards = Scorecards(self.mock_client)

    def test_create_scorecard(self):
        blueprint_id = "service"
        scorecard_data = {"name": "New Scorecard"}
        expected_result = {"id": "score_new", "name": "New Scorecard"}
        self.scorecards._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.scorecards.create_scorecard(blueprint_id, scorecard_data)
        self.scorecards._make_request_with_params.assert_called_once_with('POST', f'blueprints/{blueprint_id}/scorecards', json=scorecard_data, params=None)
        self.assertEqual(result, expected_result)

    def test_update_scorecard(self):
        blueprint_id = "service"
        scorecard_id = "score1"
        scorecard_data = {"name": "Updated Scorecard"}
        expected_result = {"id": scorecard_id, "name": "Updated Scorecard"}
        self.scorecards._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.scorecards.update_scorecard(blueprint_id, scorecard_id, scorecard_data)
        self.scorecards._make_request_with_params.assert_called_once_with('PUT', f'blueprints/{blueprint_id}/scorecards/{scorecard_id}', json=scorecard_data, params=None)
        self.assertEqual(result, expected_result)

    def test_get_scorecards(self):
        expected_result = {"scorecards": [{"id": "score1"}, {"id": "score2"}]}
        self.scorecards._make_request_with_params = MagicMock(return_value=expected_result)

        result = self.scorecards.get_scorecards()
        self.scorecards._make_request_with_params.assert_called_once_with('GET', 'scorecards', params={})
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
