"""
Example tests demonstrating snapshot testing.

This module contains example tests that demonstrate how to use snapshot testing
with PyPort. These tests are meant to be illustrative and do not test actual
functionality.
"""

import unittest
from typing import Dict, Any, List

from tests.utils.snapshot_test import SnapshotTest


class TestSnapshotExample(SnapshotTest):
    """
    Example tests demonstrating snapshot testing.
    """
    
    def test_simple_dict(self):
        """Test snapshot matching with a simple dictionary."""
        # Arrange
        data = {
            "id": "123",
            "name": "Test Entity",
            "properties": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        
        # Act & Assert
        self.assert_matches_snapshot(data)
    
    def test_multiple_snapshots(self):
        """Test using multiple snapshots in a single test."""
        # Arrange
        data1 = {
            "id": "blueprint-1",
            "title": "Service Blueprint",
            "schema": {
                "properties": {
                    "language": {
                        "type": "string",
                        "enum": ["Python", "JavaScript", "Java"]
                    }
                }
            }
        }
        
        data2 = {
            "id": "entity-1",
            "title": "Test Service",
            "blueprint": "blueprint-1",
            "properties": {
                "language": "Python"
            }
        }
        
        # Act & Assert
        self.assert_matches_snapshot(data1, "blueprint")
        self.assert_matches_snapshot(data2, "entity")
    
    def test_list_of_items(self):
        """Test snapshot matching with a list of items."""
        # Arrange
        data = [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "name": "Item 2"},
            {"id": "3", "name": "Item 3"}
        ]
        
        # Act & Assert
        self.assert_matches_snapshot(data)
    
    def test_nested_structures(self):
        """Test snapshot matching with nested structures."""
        # Arrange
        data = {
            "id": "complex-1",
            "metadata": {
                "created_at": "2023-05-15T12:00:00Z",
                "created_by": {
                    "id": "user-1",
                    "name": "Test User"
                }
            },
            "items": [
                {
                    "id": "item-1",
                    "properties": {
                        "key1": "value1",
                        "tags": ["tag1", "tag2"]
                    }
                },
                {
                    "id": "item-2",
                    "properties": {
                        "key1": "value2",
                        "tags": ["tag2", "tag3"]
                    }
                }
            ]
        }
        
        # Act & Assert
        self.assert_matches_snapshot(data)


if __name__ == "__main__":
    unittest.main()
