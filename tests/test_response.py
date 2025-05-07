import unittest
from unittest.mock import MagicMock

from src.pyport.models.response import PortResponse, PortListResponse, PortItemResponse


class TestPortResponse(unittest.TestCase):
    def setUp(self):
        # Create a mock response
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.headers = {"Content-Type": "application/json"}
        self.mock_response.json.return_value = {
            "item": {"id": "123", "name": "Test Item"},
            "metadata": {"created_at": "2023-01-01T00:00:00Z"}
        }

    def test_initialization(self):
        # Test basic initialization
        response = PortResponse(self.mock_response)
        self.assertEqual(response.raw, self.mock_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers, {"Content-Type": "application/json"})
        
        # Test with data_key
        response = PortResponse(self.mock_response, data_key="item")
        self.assertEqual(response.data, {"id": "123", "name": "Test Item"})
        
        # Test with default_value
        response = PortResponse(self.mock_response, data_key="non_existent", default_value=[])
        self.assertEqual(response.data, [])

    def test_json_property(self):
        # Test that json property returns the parsed JSON
        response = PortResponse(self.mock_response)
        self.assertEqual(response.json, {
            "item": {"id": "123", "name": "Test Item"},
            "metadata": {"created_at": "2023-01-01T00:00:00Z"}
        })
        
        # Test that json is cached
        self.mock_response.json.reset_mock()
        _ = response.json
        self.mock_response.json.assert_not_called()

    def test_data_property(self):
        # Test data property with no data_key
        response = PortResponse(self.mock_response)
        self.assertEqual(response.data, {
            "item": {"id": "123", "name": "Test Item"},
            "metadata": {"created_at": "2023-01-01T00:00:00Z"}
        })
        
        # Test data property with data_key
        response = PortResponse(self.mock_response, data_key="item")
        self.assertEqual(response.data, {"id": "123", "name": "Test Item"})
        
        # Test data property with non-existent data_key
        response = PortResponse(self.mock_response, data_key="non_existent")
        self.assertIsNone(response.data)
        
        # Test data property with non-existent data_key and default_value
        response = PortResponse(self.mock_response, data_key="non_existent", default_value=[])
        self.assertEqual(response.data, [])

    def test_bool_operator(self):
        # Test that bool operator returns True for 2xx status codes
        response = PortResponse(self.mock_response)
        self.assertTrue(bool(response))
        
        # Test that bool operator returns False for non-2xx status codes
        self.mock_response.status_code = 404
        response = PortResponse(self.mock_response)
        self.assertFalse(bool(response))


class TestPortListResponse(unittest.TestCase):
    def setUp(self):
        # Create a mock response
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.headers = {"Content-Type": "application/json"}
        self.mock_response.json.return_value = {
            "items": [
                {"id": "1", "name": "Item 1"},
                {"id": "2", "name": "Item 2"},
                {"id": "3", "name": "Item 3"}
            ],
            "metadata": {"total": 3}
        }

    def test_initialization(self):
        # Test initialization with data_key
        response = PortListResponse(self.mock_response, data_key="items")
        self.assertEqual(response.data, [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "name": "Item 2"},
            {"id": "3", "name": "Item 3"}
        ])
        
        # Test initialization with non-existent data_key
        response = PortListResponse(self.mock_response, data_key="non_existent")
        self.assertEqual(response.data, [])  # Should use default_value of []

    def test_iter_operator(self):
        # Test that iter operator allows iteration over items
        response = PortListResponse(self.mock_response, data_key="items")
        items = list(response)
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0], {"id": "1", "name": "Item 1"})
        self.assertEqual(items[1], {"id": "2", "name": "Item 2"})
        self.assertEqual(items[2], {"id": "3", "name": "Item 3"})

    def test_len_operator(self):
        # Test that len operator returns the number of items
        response = PortListResponse(self.mock_response, data_key="items")
        self.assertEqual(len(response), 3)
        
        # Test with empty list
        self.mock_response.json.return_value = {"items": []}
        response = PortListResponse(self.mock_response, data_key="items")
        self.assertEqual(len(response), 0)

    def test_getitem_operator(self):
        # Test that getitem operator allows access to items by index
        response = PortListResponse(self.mock_response, data_key="items")
        self.assertEqual(response[0], {"id": "1", "name": "Item 1"})
        self.assertEqual(response[1], {"id": "2", "name": "Item 2"})
        self.assertEqual(response[2], {"id": "3", "name": "Item 3"})
        
        # Test with invalid index
        with self.assertRaises(IndexError):
            _ = response[3]


class TestPortItemResponse(unittest.TestCase):
    def setUp(self):
        # Create a mock response
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.headers = {"Content-Type": "application/json"}
        self.mock_response.json.return_value = {
            "item": {"id": "123", "name": "Test Item"},
            "metadata": {"created_at": "2023-01-01T00:00:00Z"}
        }

    def test_initialization(self):
        # Test initialization with data_key
        response = PortItemResponse(self.mock_response, data_key="item")
        self.assertEqual(response.data, {"id": "123", "name": "Test Item"})
        
        # Test initialization with no data_key
        response = PortItemResponse(self.mock_response)
        self.assertEqual(response.data, {
            "item": {"id": "123", "name": "Test Item"},
            "metadata": {"created_at": "2023-01-01T00:00:00Z"}
        })
        
        # Test initialization with non-existent data_key
        response = PortItemResponse(self.mock_response, data_key="non_existent")
        self.assertEqual(response.data, {})  # Should use default_value of {}


if __name__ == "__main__":
    unittest.main()
