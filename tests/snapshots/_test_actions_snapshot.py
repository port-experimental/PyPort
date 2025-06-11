"""
Snapshot tests for the Actions API service.

This module contains snapshot tests for the Actions API service. These tests
capture the structure and content of API responses to detect changes in behavior.
"""

import unittest
from unittest.mock import MagicMock

from pyport.actions.actions_api_svc import Actions
from tests.snapshots.utils.snapshot_test import SnapshotTest


class TestActionsSnapshot(SnapshotTest):
    """
    Snapshot tests for the Actions API service.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock client
        self.mock_client = MagicMock()
        
        # Create a mock response for get_actions
        self.mock_actions_response = [
            {
                "id": "action-1",
                "identifier": "deploy",
                "title": "Deploy Service",
                "icon": "Bolt",
                "description": "Deploy a service to production",
                "userInputs": {
                    "properties": {
                        "version": {
                            "type": "string",
                            "title": "Version",
                            "description": "The version to deploy"
                        },
                        "environment": {
                            "type": "string",
                            "title": "Environment",
                            "enum": ["dev", "staging", "production"],
                            "default": "dev"
                        }
                    },
                    "required": ["version"]
                },
                "invocationMethod": {
                    "type": "WEBHOOK",
                    "url": "https://example.com/webhook",
                    "agent": False
                },
                "trigger": {
                    "type": "MANUAL"
                },
                "requiredApproval": False,
                "createdAt": "2023-05-15T12:00:00Z",
                "updatedAt": "2023-05-15T12:00:00Z"
            },
            {
                "id": "action-2",
                "identifier": "restart",
                "title": "Restart Service",
                "icon": "Refresh",
                "description": "Restart a service",
                "userInputs": {
                    "properties": {
                        "environment": {
                            "type": "string",
                            "title": "Environment",
                            "enum": ["dev", "staging", "production"],
                            "default": "dev"
                        }
                    },
                    "required": ["environment"]
                },
                "invocationMethod": {
                    "type": "WEBHOOK",
                    "url": "https://example.com/webhook",
                    "agent": False
                },
                "trigger": {
                    "type": "MANUAL"
                },
                "requiredApproval": False,
                "createdAt": "2023-05-15T12:00:00Z",
                "updatedAt": "2023-05-15T12:00:00Z"
            }
        ]
        
        # Create a mock response for get_action
        self.mock_action_response = self.mock_actions_response[0]
        
        # Configure the mock client
        self.mock_client._make_request_with_params.return_value = MagicMock()
        
        # Create the actions service
        self.actions = Actions(self.mock_client)
    
    def test_get_actions_response(self):
        """Test the structure of the get_actions response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "actions": self.mock_actions_response
        }
        
        # Act
        actions = self.actions.get_actions()
        
        # Assert
        self.assert_matches_snapshot(actions)
    
    def test_get_action_response(self):
        """Test the structure of the get_action response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "action": self.mock_action_response
        }
        
        # Act
        action = self.actions.get_action("deploy")
        
        # Assert
        self.assert_matches_snapshot(action)
    
    def test_create_action_response(self):
        """Test the structure of the create_action response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "action": self.mock_action_response
        }
        
        # Act
        action = self.actions.create_action({
            "identifier": "deploy",
            "title": "Deploy Service",
            "userInputs": {
                "properties": {
                    "version": {
                        "type": "string",
                        "title": "Version"
                    }
                },
                "required": ["version"]
            },
            "invocationMethod": {
                "type": "WEBHOOK",
                "url": "https://example.com/webhook"
            },
            "trigger": {
                "type": "MANUAL"
            }
        })
        
        # Assert
        self.assert_matches_snapshot(action)
    
    def test_update_action_response(self):
        """Test the structure of the update_action response."""
        # Arrange
        updated_action = dict(self.mock_action_response)
        updated_action["title"] = "Updated Deploy Service"
        
        self.mock_client._make_request_with_params.return_value.json.return_value = {
            "action": updated_action
        }
        
        # Act
        action = self.actions.update_action("deploy", {
            "title": "Updated Deploy Service"
        })
        
        # Assert
        self.assert_matches_snapshot(action)
    
    def test_delete_action_response(self):
        """Test the structure of the delete_action response."""
        # Arrange
        self.mock_client._make_request_with_params.return_value.status_code = 204
        
        # Act
        result = self.actions.delete_action("deploy")
        
        # Assert
        self.assert_matches_snapshot(result)


if __name__ == "__main__":
    unittest.main()
