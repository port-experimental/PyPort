import unittest
from unittest.mock import MagicMock
from src.pyport.search.search_api_svc import Search

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.search = Search(self.mock_client)

    def test_search_entities(self):
        query_params = {"q": "test"}
        fake_results = [{"id": "entity1"}, {"id": "entity2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": fake_results}
        self.mock_client.make_request.return_value = mock_response

        result = self.search.search_entities(query_params)
        self.mock_client.make_request.assert_called_once_with("GET", "search/entities", params=query_params)
        self.assertEqual(result, fake_results)

    def test_search_blueprints(self):
        query_params = {"q": "blueprint"}
        fake_results = [{"id": "bp1"}, {"id": "bp2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": fake_results}
        self.mock_client.make_request.return_value = mock_response

        result = self.search.search_blueprints(query_params)
        self.mock_client.make_request.assert_called_once_with("GET", "search/blueprints", params=query_params)
        self.assertEqual(result, fake_results)

if __name__ == "__main__":
    unittest.main()
