#!/usr/bin/env python3
"""
Entity Management Example for PyPort

This example demonstrates how to manage entities using the PyPort library,
including creating, updating, and deleting entities.
"""

import os
import sys
import json
import uuid
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from pyport import PortClient
from pyport.exceptions import PortApiError


def print_json(data: Dict[str, Any]) -> None:
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))


def main():
    """Main function demonstrating entity management."""
    # Get API credentials from environment variables
    client_id = os.environ.get('PORT_CLIENT_ID')
    client_secret = os.environ.get('PORT_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("Error: PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables must be set.")
        print("Please set these variables and try again:")
        print("  export PORT_CLIENT_ID=your-client-id")
        print("  export PORT_CLIENT_SECRET=your-client-secret")
        sys.exit(1)

    # Initialize the Port client
    print("\n1. Initializing the Port client...")
    client = PortClient(
        client_id=client_id,
        client_secret=client_secret
    )
    print("✅ Client initialized successfully!")

    # First, we need to create a blueprint for our entities
    # Generate a unique identifier for our test blueprint
    test_blueprint_id = f"test-blueprint-{uuid.uuid4().hex[:8]}"
    print(f"\nUsing test blueprint identifier: {test_blueprint_id}")

    # Create a new blueprint
    print("\n2. Creating a blueprint for our entities...")
    try:
        blueprint_data = {
            "identifier": test_blueprint_id,
            "title": "Test Service",
            "icon": "Microservice",
            "schema": {
                "properties": {
                    "language": {
                        "type": "string",
                        "title": "Language",
                        "enum": ["Python", "JavaScript", "Java", "Go", "Ruby"]
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
                    },
                    "tags": {
                        "type": "array",
                        "title": "Tags",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["language"]
            }
        }
        
        new_blueprint = client.blueprints.create_blueprint(blueprint_data)
        print("✅ Blueprint created successfully!")
    except PortApiError as e:
        print(f"❌ Error creating blueprint: {e}")
        sys.exit(1)

    # Generate a unique identifier for our test entity
    test_entity_id = f"test-entity-{uuid.uuid4().hex[:8]}"
    print(f"\nUsing test entity identifier: {test_entity_id}")

    # Create a new entity
    print("\n3. Creating a new entity...")
    try:
        entity_data = {
            "identifier": test_entity_id,
            "title": "Test Entity",
            "blueprint": test_blueprint_id,
            "properties": {
                "language": "Python",
                "version": "2.0.0",
                "repository": "https://github.com/example/test-service",
                "tags": ["test", "example", "pyport"]
            },
            "relations": {}
        }
        
        new_entity = client.entities.create_entity(test_blueprint_id, entity_data)
        print("✅ Entity created successfully!")
        print("\nNew entity details:")
        print_json(new_entity)
    except PortApiError as e:
        print(f"❌ Error creating entity: {e}")
        sys.exit(1)

    # Get the entity we just created
    print("\n4. Getting the entity we just created...")
    try:
        entity = client.entities.get_entity(test_blueprint_id, test_entity_id)
        print("✅ Entity retrieved successfully!")
        print("\nEntity details:")
        print_json(entity)
    except PortApiError as e:
        print(f"❌ Error retrieving entity: {e}")
        sys.exit(1)

    # Update the entity
    print("\n5. Updating the entity...")
    try:
        update_data = {
            "title": "Updated Test Entity",
            "properties": {
                "language": "JavaScript",
                "version": "3.0.0",
                "repository": "https://github.com/example/updated-test-service",
                "tags": ["test", "example", "pyport", "updated"]
            }
        }
        
        updated_entity = client.entities.update_entity(test_blueprint_id, test_entity_id, update_data)
        print("✅ Entity updated successfully!")
        print("\nUpdated entity details:")
        print_json(updated_entity)
    except PortApiError as e:
        print(f"❌ Error updating entity: {e}")

    # Get all entities for the blueprint
    print("\n6. Getting all entities for the blueprint...")
    try:
        entities = client.entities.get_entities(test_blueprint_id)
        print(f"✅ Retrieved {len(entities)} entities!")
        
        # Print the entities
        print("\nEntities:")
        for i, entity in enumerate(entities):
            print(f"\nEntity {i+1}:")
            print_json(entity)
    except PortApiError as e:
        print(f"❌ Error retrieving entities: {e}")

    # Search for entities
    print("\n7. Searching for entities...")
    try:
        search_query = {
            "blueprint": test_blueprint_id,
            "properties": {
                "language": "JavaScript"
            }
        }
        
        search_results = client.entities.search_entities(search_query)
        print(f"✅ Search returned {len(search_results)} results!")
        
        # Print the search results
        print("\nSearch results:")
        for i, result in enumerate(search_results):
            print(f"\nResult {i+1}:")
            print_json(result)
    except PortApiError as e:
        print(f"❌ Error searching for entities: {e}")

    # Delete the entity
    print("\n8. Deleting the entity...")
    try:
        success = client.entities.delete_entity(test_blueprint_id, test_entity_id)
        if success:
            print("✅ Entity deleted successfully!")
        else:
            print("❌ Failed to delete entity.")
    except PortApiError as e:
        print(f"❌ Error deleting entity: {e}")

    # Verify the entity was deleted
    print("\n9. Verifying the entity was deleted...")
    try:
        entity = client.entities.get_entity(test_blueprint_id, test_entity_id)
        print("❌ Entity still exists!")
    except PortApiError as e:
        print(f"✅ Entity was deleted successfully: {e}")

    # Clean up by deleting the blueprint
    print("\n10. Cleaning up by deleting the blueprint...")
    try:
        success = client.blueprints.delete_blueprint(test_blueprint_id)
        if success:
            print("✅ Blueprint deleted successfully!")
        else:
            print("❌ Failed to delete blueprint.")
    except PortApiError as e:
        print(f"❌ Error deleting blueprint: {e}")

    print("\nEntity management example completed!")


if __name__ == "__main__":
    main()
