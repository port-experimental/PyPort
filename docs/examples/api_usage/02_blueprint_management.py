#!/usr/bin/env python3
"""
Blueprint Management Example for PyPort

This example demonstrates how to manage blueprints using the PyPort library,
including creating, updating, and deleting blueprints.
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
    """Main function demonstrating blueprint management."""
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

    # Generate a unique identifier for our test blueprint
    test_blueprint_id = f"test-blueprint-{uuid.uuid4().hex[:8]}"
    print(f"\nUsing test blueprint identifier: {test_blueprint_id}")

    # Create a new blueprint
    print("\n2. Creating a new blueprint...")
    try:
        blueprint_data = {
            "identifier": test_blueprint_id,
            "title": "Test Blueprint",
            "icon": "Microservice",
            "description": "A test blueprint created by the PyPort example script",
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
            },
            "calculationProperties": {
                "languageIcon": {
                    "title": "Language Icon",
                    "calculation": "return `https://cdn.example.com/icons/${entity.properties.language.toLowerCase()}.png`",
                    "type": "string",
                    "format": "url"
                }
            },
            "relations": {}
        }
        
        new_blueprint = client.blueprints.create_blueprint(blueprint_data)
        print("✅ Blueprint created successfully!")
        print("\nNew blueprint details:")
        print_json(new_blueprint)
    except PortApiError as e:
        print(f"❌ Error creating blueprint: {e}")
        sys.exit(1)

    # Get the blueprint we just created
    print("\n3. Getting the blueprint we just created...")
    try:
        blueprint = client.blueprints.get_blueprint(test_blueprint_id)
        print("✅ Blueprint retrieved successfully!")
    except PortApiError as e:
        print(f"❌ Error retrieving blueprint: {e}")
        sys.exit(1)

    # Update the blueprint
    print("\n4. Updating the blueprint...")
    try:
        update_data = {
            "title": "Updated Test Blueprint",
            "description": "This blueprint has been updated",
            "schema": {
                "properties": {
                    "language": {
                        "type": "string",
                        "title": "Language",
                        "enum": ["Python", "JavaScript", "Java", "Go", "Ruby", "Rust"],
                        "enumColors": {
                            "Python": "blue",
                            "JavaScript": "yellow",
                            "Java": "red",
                            "Go": "lightBlue",
                            "Ruby": "darkRed",
                            "Rust": "orange"
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
                    },
                    "tags": {
                        "type": "array",
                        "title": "Tags",
                        "items": {
                            "type": "string"
                        }
                    },
                    "maintainer": {
                        "type": "string",
                        "title": "Maintainer"
                    }
                },
                "required": ["language", "version"]
            }
        }
        
        updated_blueprint = client.blueprints.update_blueprint(test_blueprint_id, update_data)
        print("✅ Blueprint updated successfully!")
        print("\nUpdated blueprint details:")
        print_json(updated_blueprint)
    except PortApiError as e:
        print(f"❌ Error updating blueprint: {e}")

    # Get the blueprint's system structure
    print("\n5. Getting the blueprint's system structure...")
    try:
        structure = client.blueprints.get_blueprint_system_structure(test_blueprint_id)
        print("✅ Blueprint system structure retrieved successfully!")
        print("\nBlueprint system structure:")
        print_json(structure)
    except PortApiError as e:
        print(f"❌ Error retrieving blueprint system structure: {e}")

    # Delete the blueprint
    print("\n6. Deleting the blueprint...")
    try:
        success = client.blueprints.delete_blueprint(test_blueprint_id)
        if success:
            print("✅ Blueprint deleted successfully!")
        else:
            print("❌ Failed to delete blueprint.")
    except PortApiError as e:
        print(f"❌ Error deleting blueprint: {e}")

    # Verify the blueprint was deleted
    print("\n7. Verifying the blueprint was deleted...")
    try:
        blueprint = client.blueprints.get_blueprint(test_blueprint_id)
        print("❌ Blueprint still exists!")
    except PortApiError as e:
        print(f"✅ Blueprint was deleted successfully: {e}")

    print("\nBlueprint management example completed!")


if __name__ == "__main__":
    main()
