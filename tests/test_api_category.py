import unittest
from unittest.mock import MagicMock

from src.pyport.models.api_category import BaseResource


class TestBaseResource(unittest.TestCase):
    def test_initialization(self):
        # Test that BaseResource initializes with a client
        mock_client = MagicMock()
        resource = BaseResource(mock_client)
        
        # Check that the client is stored correctly
        self.assertEqual(resource._client, mock_client)
        
        # Check that we can access the client
        self.assertIs(resource._client, mock_client)


if __name__ == "__main__":
    unittest.main()
