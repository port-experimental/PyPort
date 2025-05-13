#!/usr/bin/env python3
"""
Utility Functions Example for PyPort

This example demonstrates how to use the utility functions provided by PyPort
for common operations like snapshots and blueprint management.
"""

import os
import sys
import json
import uuid
import time
from typing import Dict, Any, List

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from pyport import PortClient
from pyport.exceptions import PortApiError
from pyport.utils import (
    clear_blueprint,
    save_snapshot,
    restore_snapshot,
    list_snapshots,
    delete_snapshot
)


def print_json(data: Dict[str, Any]) -> None:
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))


def create_test_blueprint(client: PortClient) -> str:
    """Create a test blueprint with entities.
    
    Args:
        client: The Port client.
        
    Returns:
        The ID of the created blueprint.
    """
    # Generate a unique identifier for the test blueprint
    blueprint_id = f"test-blueprint-{uuid.uuid4().hex[:8]}"
    
    # Create the blueprint
    blueprint_data = {
        "identifier": blueprint_id,
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
                    "title": "Version"
                }
            }
        }
    }
    
    client.blueprints.create_blueprint(blueprint_data)
    
    # Create some entities
    for i in range(3):
        entity_data = {
            "identifier": f"entity-{i}-{uuid.uuid4().hex[:8]}",
            "title": f"Test Entity {i+1}",
            "properties": {
                "language": ["Python", "JavaScript", "Java"][i % 3],
                "version": f"{i+1}.0.0"
            }
        }
        
        client.entities.create_entity(blueprint_id, entity_data)
    
    return blueprint_id


def main():
    """Main function demonstrating utility functions."""
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

    # Create a test blueprint with entities
    print("\n2. Creating a test blueprint with entities...")
    try:
        blueprint_id = create_test_blueprint(client)
        print(f"✅ Test blueprint created successfully! Blueprint ID: {blueprint_id}")
        
        # Get the entities to verify
        entities = client.entities.get_entities(blueprint_id)
        print(f"✅ Created {len(entities)} entities for the blueprint!")
    except PortApiError as e:
        print(f"❌ Error creating test blueprint: {e}")
        sys.exit(1)

    # Save a snapshot
    print("\n3. Saving a snapshot...")
    try:
        snapshot_prefix = f"test-snapshot-{uuid.uuid4().hex[:8]}"
        snapshot = save_snapshot(
            client,
            prefix=snapshot_prefix,
            include_blueprints=True,
            include_entities=True,
            include_actions=True,
            include_scorecards=True
        )
        
        print("✅ Snapshot saved successfully!")
        print("\nSnapshot details:")
        print(f"  ID: {snapshot['id']}")
        print(f"  Created at: {snapshot['createdAt']}")
        print(f"  Status: {snapshot['status']}")
        
        # Store the snapshot ID for later
        snapshot_id = snapshot["id"]
    except PortApiError as e:
        print(f"❌ Error saving snapshot: {e}")
        snapshot_id = None

    # List snapshots
    if snapshot_id:
        print("\n4. Listing snapshots...")
        try:
            snapshots = list_snapshots(client)
            print(f"✅ Retrieved {len(snapshots)} snapshots!")
            
            print("\nAvailable snapshots:")
            for i, snap in enumerate(snapshots):
                print(f"  {i+1}. {snap['id']} (Created: {snap['createdAt']})")
        except PortApiError as e:
            print(f"❌ Error listing snapshots: {e}")

    # Clear the blueprint
    print(f"\n5. Clearing entities from blueprint '{blueprint_id}'...")
    try:
        result = clear_blueprint(client, blueprint_id)
        print(f"✅ Cleared {result['deleted_entities']} entities from the blueprint!")
        
        # Verify the entities were deleted
        entities = client.entities.get_entities(blueprint_id)
        print(f"✅ Blueprint now has {len(entities)} entities!")
    except PortApiError as e:
        print(f"❌ Error clearing blueprint: {e}")

    # Restore the snapshot
    if snapshot_id:
        print("\n6. Restoring the snapshot...")
        try:
            restore_result = restore_snapshot(
                client,
                snapshot_id,
                include_blueprints=True,
                include_entities=True,
                include_actions=True,
                include_scorecards=True
            )
            
            print("✅ Snapshot restored successfully!")
            print("\nRestore details:")
            print(f"  Status: {restore_result['status']}")
            
            # Wait a moment for the restoration to complete
            print("Waiting for restoration to complete...")
            time.sleep(5)
            
            # Verify the entities were restored
            entities = client.entities.get_entities(blueprint_id)
            print(f"✅ Blueprint now has {len(entities)} entities after restoration!")
        except PortApiError as e:
            print(f"❌ Error restoring snapshot: {e}")

    # Delete the snapshot
    if snapshot_id:
        print("\n7. Deleting the snapshot...")
        try:
            delete_result = delete_snapshot(client, snapshot_id)
            print("✅ Snapshot deleted successfully!")
        except PortApiError as e:
            print(f"❌ Error deleting snapshot: {e}")

    # Clean up by deleting the blueprint
    print(f"\n8. Cleaning up by deleting the blueprint '{blueprint_id}'...")
    try:
        success = client.blueprints.delete_blueprint(blueprint_id)
        if success:
            print("✅ Blueprint deleted successfully!")
        else:
            print("❌ Failed to delete blueprint.")
    except PortApiError as e:
        print(f"❌ Error deleting blueprint: {e}")

    print("\nUtility functions example completed!")


if __name__ == "__main__":
    main()
