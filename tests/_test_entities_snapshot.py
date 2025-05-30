"""
Snapshot tests for the Entities API service.

This module contains snapshot tests for the Entities API service. These tests
capture the structure and content of API responses to detect changes in behavior.
"""

import unittest
from unittest.mock import MagicMock

from pyport.entities.entities_api_svc import Entities
from tests.snapshots.utils.snapshot_test import SnapshotTest


class TestEntitiesSnapshot(SnapshotTest):
    """
    Snapshot tests for the Entities API service.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock client
        self.mock_client = MagicMock()
        
        # Create a mock response for get_entities
        self.mock_entities_response = [
            {
                "id": "entity-1",
                "identifier": "service-1",
                "title": "Service 1",
                "blueprint": "service",
                "properties": {
                    "language": "Python",
                    "version": "1.0.0",
                    "repository": "https://github.com/example/service-1"
                },
                "relations": {},
                "createdAt": "2023-05-15T12:00:00Z",
                "updatedAt": "2023-05-15T12:00:00Z"
            },
            {
                "id": "entity-2",
                "identifier": "service-2",
                "title": "Service 2",
                "blueprint": "service",
                "properties": {
                    "language": "JavaScript",
                    "version": "2.0.0",
                    "repository": "https://github.com/example/service-2"
                },
                "relations": {},
                "createdAt": "2023-05-15T12:00:00Z",
                "updatedAt": "2023-05-15T12:00:00Z"
            }
        ]
        
        # Create a mock response for get_entity
        self.mock_entity_response = self.mock_entities_response[0]
        
        # Configure the mock client
        self.mock_client._make_request_with_params.return_value = MagicMock()
        
        # Create the entities service
        self.entities = Entities(self.mock_client)
    
    def test_get_entities_response(self):
        """Test the structure of the get_entities response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "entities": self.mock_entities_response
        }
        
        # Act
        entities = self.entities.get_entities("service")
        
        # Assert
        self.assert_matches_snapshot(entities)
    
    def test_get_entity_response(self):
        """Test the structure of the get_entity response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "entity": self.mock_entity_response
        }
        
        # Act
        entity = self.entities.get_entity("service", "service-1")
        
        # Assert
        self.assert_matches_snapshot(entity)
    
    def test_create_entity_response(self):
        """Test the structure of the create_entity response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "entity": self.mock_entity_response
        }
        
        # Act
        entity = self.entities.create_entity("service", {
            "identifier": "service-1",
            "title": "Service 1",
            "properties": {
                "language": "Python",
                "version": "1.0.0",
                "repository": "https://github.com/example/service-1"
            }
        })
        
        # Assert
        self.assert_matches_snapshot(entity)
    
    def test_update_entity_response(self):
        """Test the structure of the update_entity response."""
        # Arrange
        updated_entity = dict(self.mock_entity_response)
        updated_entity["title"] = "Updated Service 1"
        
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "entity": updated_entity
        }
        
        # Act
        entity = self.entities.update_entity("service", "service-1", {
            "title": "Updated Service 1"
        })
        
        # Assert
        self.assert_matches_snapshot(entity)
    
    def test_delete_entity_response(self):
        """Test the structure of the delete_entity response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.status_code = 204
        
        # Act
        result = self.entities.delete_entity("service", "service-1")
        
        # Assert
        self.assert_matches_snapshot(result)
    
    def test_search_entities_response(self):
        """Test the structure of the search_entities response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "entities": self.mock_entities_response
        }
        
        # Act
        entities = self.entities.search_entities({
            "blueprint": "service",
            "properties": {
                "language": "Python"
            }
        })
        
        # Assert
        self.assert_matches_snapshot(entities)


if __name__ == "__main__":
    unittest.main()
