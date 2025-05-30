#!/usr/bin/env python3
"""
Action Management Example for PyPort

This example demonstrates how to manage actions using the PyPort library,
including creating, updating, and deleting actions, as well as running actions.
"""

import os
import sys
import json
import uuid
import time
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from pyport import PortClient
from pyport.exceptions import PortApiError


def print_json(data: Dict[str, Any]) -> None:
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))


def main():
    """Main function demonstrating action management."""
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

    # Create an entity for our action to run on
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
                "version": "1.0.0"
            }
        }
        
        new_entity = client.entities.create_entity(test_blueprint_id, entity_data)
        print("✅ Entity created successfully!")
    except PortApiError as e:
        print(f"❌ Error creating entity: {e}")
        sys.exit(1)

    # Generate a unique identifier for our test action
    test_action_id = f"test-action-{uuid.uuid4().hex[:8]}"
    print(f"\nUsing test action identifier: {test_action_id}")

    # Create a new action
    print("\n4. Creating a new action...")
    try:
        action_data = {
            "identifier": test_action_id,
            "title": "Test Action",
            "icon": "Bolt",
            "description": "A test action created by the PyPort example script",
            "userInputs": {
                "properties": {
                    "message": {
                        "type": "string",
                        "title": "Message",
                        "description": "A message to include in the action run"
                    }
                },
                "required": ["message"]
            },
            "invocationMethod": {
                "type": "WEBHOOK",
                "url": "https://example.com/webhook",
                "agent": False
            },
            "trigger": {
                "type": "MANUAL"
            },
            "requiredApproval": False
        }
        
        new_action = client.actions.create_action(action_data)
        print("✅ Action created successfully!")
        print("\nNew action details:")
        print_json(new_action)
    except PortApiError as e:
        print(f"❌ Error creating action: {e}")
        sys.exit(1)

    # Get the action we just created
    print("\n5. Getting the action we just created...")
    try:
        action = client.actions.get_action(test_action_id)
        print("✅ Action retrieved successfully!")
        print("\nAction details:")
        print_json(action)
    except PortApiError as e:
        print(f"❌ Error retrieving action: {e}")
        sys.exit(1)

    # Update the action
    print("\n6. Updating the action...")
    try:
        update_data = {
            "title": "Updated Test Action",
            "description": "This action has been updated",
            "userInputs": {
                "properties": {
                    "message": {
                        "type": "string",
                        "title": "Message",
                        "description": "A message to include in the action run"
                    },
                    "priority": {
                        "type": "string",
                        "title": "Priority",
                        "enum": ["Low", "Medium", "High"],
                        "default": "Medium"
                    }
                },
                "required": ["message", "priority"]
            }
        }
        
        updated_action = client.actions.update_action(test_action_id, update_data)
        print("✅ Action updated successfully!")
        print("\nUpdated action details:")
        print_json(updated_action)
    except PortApiError as e:
        print(f"❌ Error updating action: {e}")

    # Run the action
    print("\n7. Running the action...")
    try:
        run_data = {
            "entity": {
                "identifier": test_entity_id,
                "blueprint": test_blueprint_id
            },
            "properties": {
                "message": "Hello from PyPort example script!",
                "priority": "High"
            }
        }
        
        action_run = client.action_runs.create_action_run(test_action_id, run_data)
        print("✅ Action run created successfully!")
        print("\nAction run details:")
        print_json(action_run)
        
        # Store the run ID for later
        run_id = action_run.get("id")
    except PortApiError as e:
        print(f"❌ Error running action: {e}")
        run_id = None

    # Get action runs
    if run_id:
        print("\n8. Getting action runs...")
        try:
            # Wait a moment for the run to be processed
            time.sleep(2)
            
            runs = client.action_runs.get_action_runs(test_action_id)
            print(f"✅ Retrieved {len(runs)} action runs!")
            
            # Print the runs
            print("\nAction runs:")
            for i, run in enumerate(runs):
                print(f"\nRun {i+1}:")
                print_json(run)
            
            # Get a specific run
            print(f"\n9. Getting specific action run (ID: {run_id})...")
            run = client.action_runs.get_action_run(test_action_id, run_id)
            print("✅ Action run retrieved successfully!")
            print("\nAction run details:")
            print_json(run)
        except PortApiError as e:
            print(f"❌ Error retrieving action runs: {e}")

    # Delete the action
    print("\n10. Deleting the action...")
    try:
        success = client.actions.delete_action(test_action_id)
        if success:
            print("✅ Action deleted successfully!")
        else:
            print("❌ Failed to delete action.")
    except PortApiError as e:
        print(f"❌ Error deleting action: {e}")

    # Verify the action was deleted
    print("\n11. Verifying the action was deleted...")
    try:
        action = client.actions.get_action(test_action_id)
        print("❌ Action still exists!")
    except PortApiError as e:
        print(f"✅ Action was deleted successfully: {e}")

    # Clean up by deleting the entity and blueprint
    print("\n12. Cleaning up by deleting the entity...")
    try:
        success = client.entities.delete_entity(test_blueprint_id, test_entity_id)
        if success:
            print("✅ Entity deleted successfully!")
        else:
            print("❌ Failed to delete entity.")
    except PortApiError as e:
        print(f"❌ Error deleting entity: {e}")

    print("\n13. Cleaning up by deleting the blueprint...")
    try:
        success = client.blueprints.delete_blueprint(test_blueprint_id)
        if success:
            print("✅ Blueprint deleted successfully!")
        else:
            print("❌ Failed to delete blueprint.")
    except PortApiError as e:
        print(f"❌ Error deleting blueprint: {e}")

    print("\nAction management example completed!")


if __name__ == "__main__":
    main()
