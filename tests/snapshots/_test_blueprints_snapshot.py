"""
Snapshot tests for the Blueprints API service.

This module contains snapshot tests for the Blueprints API service. These tests
capture the structure and content of API responses to detect changes in behavior.
"""

import unittest
from unittest.mock import MagicMock

from pyport.blueprints.blueprint_api_svc import Blueprints
from tests.snapshots.utils.snapshot_test import SnapshotTest


class TestBlueprintsSnapshot(SnapshotTest):
    """
    Snapshot tests for the Blueprints API service.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock client
        self.mock_client = MagicMock()
        
        # Create a mock response for get_blueprints
        self.mock_blueprints_response = [
            {
                "id": "blueprint-1",
                "identifier": "service",
                "title": "Service Blueprint",
                "icon": "Microservice",
                "description": "A blueprint for services",
                "schema": {
                    "properties": {
                        "language": {
                            "type": "string",
                            "title": "Language",
                            "enum": ["Python", "JavaScript", "Java", "Go", "Ruby"],
                            "enumColors": {
                                "Python": "blue",
                                "JavaScript": "yellow",
                                "Java": "red",
                                "Go": "lightBlue",
                                "Ruby": "darkRed"
                            }
                        },
                        "version": {
                            "type": "string",
                            "title": "Version",
                            "default": "1.0.0"
                        },
                        "repository": {
                            "type": "string",
                            "title": "Repository URL",
                            "format": "url"
                        }
                    },
                    "required": ["language"]
                },
                "calculationProperties": {
                    "languageIcon": {
                        "title": "Language Icon",
                        "calculation": "return `https://cdn.example.com/icons/${entity.properties.language.toLowerCase()}.png`",
                        "type": "string",
                        "format": "url"
                    }
                },
                "relations": {},
                "createdAt": "2023-05-15T12:00:00Z",
                "updatedAt": "2023-05-15T12:00:00Z"
            },
            {
                "id": "blueprint-2",
                "identifier": "database",
                "title": "Database Blueprint",
                "icon": "Database",
                "description": "A blueprint for databases",
                "schema": {
                    "properties": {
                        "type": {
                            "type": "string",
                            "title": "Type",
                            "enum": ["MySQL", "PostgreSQL", "MongoDB", "Redis"],
                            "enumColors": {
                                "MySQL": "blue",
                                "PostgreSQL": "blue",
                                "MongoDB": "green",
                                "Redis": "red"
                            }
                        },
                        "version": {
                            "type": "string",
                            "title": "Version"
                        },
                        "host": {
                            "type": "string",
                            "title": "Host"
                        },
                        "port": {
                            "type": "number",
                            "title": "Port"
                        }
                    },
                    "required": ["type", "host", "port"]
                },
                "calculationProperties": {},
                "relations": {},
                "createdAt": "2023-05-15T12:00:00Z",
                "updatedAt": "2023-05-15T12:00:00Z"
            }
        ]
        
        # Create a mock response for get_blueprint
        self.mock_blueprint_response = self.mock_blueprints_response[0]
        
        # Configure the mock client
        self.mock_client._make_request_with_params.return_value = MagicMock()
        
        # Create the blueprints service
        self.blueprints = Blueprints(self.mock_client)
    
    def test_get_blueprints_response(self):
        """Test the structure of the get_blueprints response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "blueprints": self.mock_blueprints_response
        }
        
        # Act
        blueprints = self.blueprints.get_blueprints()
        
        # Assert
        self.assert_matches_snapshot(blueprints)
    
    def test_get_blueprint_response(self):
        """Test the structure of the get_blueprint response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "blueprint": self.mock_blueprint_response
        }
        
        # Act
        blueprint = self.blueprints.get_blueprint("service")
        
        # Assert
        self.assert_matches_snapshot(blueprint)
    
    def test_create_blueprint_response(self):
        """Test the structure of the create_blueprint response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "blueprint": self.mock_blueprint_response
        }
        
        # Act
        blueprint = self.blueprints.create_blueprint({
            "identifier": "service",
            "title": "Service Blueprint",
            "schema": {
                "properties": {
                    "language": {
                        "type": "string",
                        "enum": ["Python", "JavaScript", "Java"]
                    }
                }
            }
        })
        
        # Assert
        self.assert_matches_snapshot(blueprint)
    
    def test_update_blueprint_response(self):
        """Test the structure of the update_blueprint response."""
        # Arrange
        updated_blueprint = dict(self.mock_blueprint_response)
        updated_blueprint["title"] = "Updated Service Blueprint"
        
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "blueprint": updated_blueprint
        }
        
        # Act
        blueprint = self.blueprints.update_blueprint("service", {
            "title": "Updated Service Blueprint"
        })
        
        # Assert
        self.assert_matches_snapshot(blueprint)
    
    def test_delete_blueprint_response(self):
        """Test the structure of the delete_blueprint response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.status_code = 204
        
        # Act
        result = self.blueprints.delete_blueprint("service")
        
        # Assert
        self.assert_matches_snapshot(result)


if __name__ == "__main__":
    unittest.main()
