import unittest
from typing import Dict, List, Any, Optional

from pyport.types import (
    Pagination,
    BlueprintProperty,
    Blueprint,
    BlueprintResponse,
    BlueprintsResponse,
    EntityProperty,
    Entity,
    EntityResponse,
    EntitiesResponse,
    Action,
    ActionResponse,
    ActionsResponse
)


class TestTypes(unittest.TestCase):
    def test_pagination_type(self):
        # Test that Pagination type can be used correctly
        pagination: Pagination = {
            "page": 1,
            "per_page": 10,
            "total": 100,
            "total_pages": 10
        }
        self.assertEqual(pagination["page"], 1)
        self.assertEqual(pagination["per_page"], 10)
        self.assertEqual(pagination["total"], 100)
        self.assertEqual(pagination["total_pages"], 10)
        
        # Test with optional fields
        pagination: Pagination = {
            "page": 1
        }
        self.assertEqual(pagination["page"], 1)

    def test_blueprint_property_type(self):
        # Test that BlueprintProperty type can be used correctly
        property: BlueprintProperty = {
            "type": "string",
            "title": "Name",
            "description": "The name of the item",
            "format": "text",
            "default": "",
            "enum": ["Option 1", "Option 2"],
            "required": True
        }
        self.assertEqual(property["type"], "string")
        self.assertEqual(property["title"], "Name")
        self.assertEqual(property["description"], "The name of the item")
        self.assertEqual(property["format"], "text")
        self.assertEqual(property["default"], "")
        self.assertEqual(property["enum"], ["Option 1", "Option 2"])
        self.assertEqual(property["required"], True)
        
        # Test with optional fields
        property: BlueprintProperty = {
            "type": "string",
            "title": "Name"
        }
        self.assertEqual(property["type"], "string")
        self.assertEqual(property["title"], "Name")

    def test_blueprint_type(self):
        # Test that Blueprint type can be used correctly
        blueprint: Blueprint = {
            "identifier": "service",
            "title": "Service",
            "properties": {
                "name": {
                    "type": "string",
                    "title": "Name"
                }
            },
            "createdAt": "2023-01-01T00:00:00Z",
            "createdBy": "user1",
            "updatedAt": "2023-01-02T00:00:00Z",
            "updatedBy": "user2"
        }
        self.assertEqual(blueprint["identifier"], "service")
        self.assertEqual(blueprint["title"], "Service")
        self.assertEqual(blueprint["properties"]["name"]["type"], "string")
        self.assertEqual(blueprint["createdAt"], "2023-01-01T00:00:00Z")
        self.assertEqual(blueprint["createdBy"], "user1")
        self.assertEqual(blueprint["updatedAt"], "2023-01-02T00:00:00Z")
        self.assertEqual(blueprint["updatedBy"], "user2")

    def test_blueprint_response_type(self):
        # Test that BlueprintResponse type can be used correctly
        response: BlueprintResponse = {
            "blueprint": {
                "identifier": "service",
                "title": "Service",
                "properties": {
                    "name": {
                        "type": "string",
                        "title": "Name"
                    }
                }
            }
        }
        self.assertEqual(response["blueprint"]["identifier"], "service")
        self.assertEqual(response["blueprint"]["title"], "Service")
        self.assertEqual(response["blueprint"]["properties"]["name"]["type"], "string")

    def test_blueprints_response_type(self):
        # Test that BlueprintsResponse type can be used correctly
        response: BlueprintsResponse = {
            "blueprints": [
                {
                    "identifier": "service",
                    "title": "Service"
                },
                {
                    "identifier": "database",
                    "title": "Database"
                }
            ],
            "pagination": {
                "page": 1,
                "per_page": 10,
                "total": 2,
                "total_pages": 1
            }
        }
        self.assertEqual(len(response["blueprints"]), 2)
        self.assertEqual(response["blueprints"][0]["identifier"], "service")
        self.assertEqual(response["blueprints"][1]["identifier"], "database")
        self.assertEqual(response["pagination"]["page"], 1)
        
        # Test without pagination
        response: BlueprintsResponse = {
            "blueprints": [
                {
                    "identifier": "service",
                    "title": "Service"
                }
            ]
        }
        self.assertEqual(len(response["blueprints"]), 1)
        self.assertEqual(response["blueprints"][0]["identifier"], "service")

    def test_entity_property_type(self):
        # Test that EntityProperty type can be used correctly
        property: EntityProperty = {
            "type": "string",
            "value": "Test Value"
        }
        self.assertEqual(property["type"], "string")
        self.assertEqual(property["value"], "Test Value")

    def test_entity_type(self):
        # Test that Entity type can be used correctly
        entity: Entity = {
            "identifier": "service-1",
            "title": "Service 1",
            "properties": {
                "name": {
                    "type": "string",
                    "value": "Service 1"
                }
            },
            "relations": {},
            "createdAt": "2023-01-01T00:00:00Z",
            "createdBy": "user1",
            "updatedAt": "2023-01-02T00:00:00Z",
            "updatedBy": "user2",
            "blueprint": "service"
        }
        self.assertEqual(entity["identifier"], "service-1")
        self.assertEqual(entity["title"], "Service 1")
        self.assertEqual(entity["properties"]["name"]["type"], "string")
        self.assertEqual(entity["properties"]["name"]["value"], "Service 1")
        self.assertEqual(entity["createdAt"], "2023-01-01T00:00:00Z")
        self.assertEqual(entity["blueprint"], "service")

    def test_entity_response_type(self):
        # Test that EntityResponse type can be used correctly
        response: EntityResponse = {
            "entity": {
                "identifier": "service-1",
                "title": "Service 1",
                "properties": {
                    "name": {
                        "type": "string",
                        "value": "Service 1"
                    }
                },
                "blueprint": "service"
            }
        }
        self.assertEqual(response["entity"]["identifier"], "service-1")
        self.assertEqual(response["entity"]["title"], "Service 1")
        self.assertEqual(response["entity"]["properties"]["name"]["value"], "Service 1")
        self.assertEqual(response["entity"]["blueprint"], "service")

    def test_entities_response_type(self):
        # Test that EntitiesResponse type can be used correctly
        response: EntitiesResponse = {
            "entities": [
                {
                    "identifier": "service-1",
                    "title": "Service 1",
                    "blueprint": "service"
                },
                {
                    "identifier": "service-2",
                    "title": "Service 2",
                    "blueprint": "service"
                }
            ],
            "pagination": {
                "page": 1,
                "per_page": 10,
                "total": 2,
                "total_pages": 1
            }
        }
        self.assertEqual(len(response["entities"]), 2)
        self.assertEqual(response["entities"][0]["identifier"], "service-1")
        self.assertEqual(response["entities"][1]["identifier"], "service-2")
        self.assertEqual(response["pagination"]["page"], 1)
        
        # Test without pagination
        response: EntitiesResponse = {
            "entities": [
                {
                    "identifier": "service-1",
                    "title": "Service 1",
                    "blueprint": "service"
                }
            ]
        }
        self.assertEqual(len(response["entities"]), 1)
        self.assertEqual(response["entities"][0]["identifier"], "service-1")

    def test_action_type(self):
        # Test that Action type can be used correctly
        action: Action = {
            "identifier": "deploy",
            "title": "Deploy Service",
            "description": "Deploy a service to production",
            "blueprint": "service",
            "trigger": {"type": "manual"},
            "invocationMethod": {"type": "webhook"},
            "createdAt": "2023-01-01T00:00:00Z",
            "createdBy": "user1",
            "updatedAt": "2023-01-02T00:00:00Z",
            "updatedBy": "user2"
        }
        self.assertEqual(action["identifier"], "deploy")
        self.assertEqual(action["title"], "Deploy Service")
        self.assertEqual(action["description"], "Deploy a service to production")
        self.assertEqual(action["blueprint"], "service")
        self.assertEqual(action["trigger"]["type"], "manual")
        self.assertEqual(action["invocationMethod"]["type"], "webhook")
        self.assertEqual(action["createdAt"], "2023-01-01T00:00:00Z")
        self.assertEqual(action["createdBy"], "user1")
        
        # Test with optional fields
        action: Action = {
            "identifier": "deploy",
            "title": "Deploy Service",
            "blueprint": "service",
            "trigger": {"type": "manual"},
            "invocationMethod": {"type": "webhook"}
        }
        self.assertEqual(action["identifier"], "deploy")
        self.assertEqual(action["title"], "Deploy Service")
        self.assertEqual(action["blueprint"], "service")

    def test_action_response_type(self):
        # Test that ActionResponse type can be used correctly
        response: ActionResponse = {
            "action": {
                "identifier": "deploy",
                "title": "Deploy Service",
                "blueprint": "service"
            }
        }
        self.assertEqual(response["action"]["identifier"], "deploy")
        self.assertEqual(response["action"]["title"], "Deploy Service")
        self.assertEqual(response["action"]["blueprint"], "service")

    def test_actions_response_type(self):
        # Test that ActionsResponse type can be used correctly
        response: ActionsResponse = {
            "actions": [
                {
                    "identifier": "deploy",
                    "title": "Deploy Service",
                    "blueprint": "service"
                },
                {
                    "identifier": "restart",
                    "title": "Restart Service",
                    "blueprint": "service"
                }
            ],
            "pagination": {
                "page": 1,
                "per_page": 10,
                "total": 2,
                "total_pages": 1
            }
        }
        self.assertEqual(len(response["actions"]), 2)
        self.assertEqual(response["actions"][0]["identifier"], "deploy")
        self.assertEqual(response["actions"][1]["identifier"], "restart")
        self.assertEqual(response["pagination"]["page"], 1)
        
        # Test without pagination
        response: ActionsResponse = {
            "actions": [
                {
                    "identifier": "deploy",
                    "title": "Deploy Service",
                    "blueprint": "service"
                }
            ]
        }
        self.assertEqual(len(response["actions"]), 1)
        self.assertEqual(response["actions"][0]["identifier"], "deploy")


if __name__ == "__main__":
    unittest.main()
