import unittest
from unittest.mock import MagicMock

from src.pyport.data_sources.data_sources_api_svc import DataSources


class TestDataSources(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.data_sources = DataSources(self.mock_client)

    def test_get_data_sources(self):
        # Setup
        expected_data_sources = [{"id": "ds1"}, {"id": "ds2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"dataSources": expected_data_sources}
        self.mock_client.make_request.return_value = mock_response

        # Execute
        result = self.data_sources.get_data_sources()

        # Assert
        self.mock_client.make_request.assert_called_once_with("GET", "data-sources")
        self.assertEqual(result, expected_data_sources)


if __name__ == "__main__":
    unittest.main()
