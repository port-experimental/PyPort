#!/usr/bin/env python
"""
Basic examples of using the snapshot utilities in PyPort.

This script demonstrates how to:
1. Create a snapshot (backup)
2. List available snapshots
3. Restore from a snapshot
"""
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from pyport import PortClient
from pyport.utils import save_snapshot, list_snapshots, restore_snapshot


def create_client():
    """Create a PortClient instance using environment variables."""
    client_id = os.environ.get("PORT_CLIENT_ID")
    client_secret = os.environ.get("PORT_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("Error: PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables must be set.")
        print("Example:")
        print("  export PORT_CLIENT_ID=your-client-id")
        print("  export PORT_CLIENT_SECRET=your-client-secret")
        sys.exit(1)
    
    return PortClient(
        client_id=client_id,
        client_secret=client_secret
    )


def create_snapshot_example():
    """Example of creating a snapshot."""
    print("\n=== Creating a Snapshot ===")
    
    client = create_client()
    
    # Create a basic snapshot with default settings
    snapshot = save_snapshot(
        client=client,
        prefix="example-backup"
    )
    
    print(f"Snapshot created: {snapshot['snapshot_id']}")
    print(f"Saved {len(snapshot['files'])} files")
    print(f"Metadata file: {snapshot['metadata_file']}")
    
    return snapshot['snapshot_id']


def list_snapshots_example():
    """Example of listing available snapshots."""
    print("\n=== Listing Available Snapshots ===")
    
    # List all available snapshots
    snapshots = list_snapshots()
    
    if not snapshots:
        print("No snapshots found.")
        return None
    
    # Print snapshot information
    for snapshot in snapshots:
        print(f"Snapshot ID: {snapshot['snapshot_id']}")
        print(f"Created: {snapshot['timestamp']}")
        print(f"Contains:")
        print(f"  - Blueprints: {snapshot.get('include_blueprints', False)}")
        print(f"  - Entities: {snapshot.get('include_entities', False)}")
        print(f"  - Actions: {snapshot.get('include_actions', False)}")
        print(f"  - Pages: {snapshot.get('include_pages', False)}")
        print(f"  - Scorecards: {snapshot.get('include_scorecards', False)}")
        print(f"Total files: {len(snapshot.get('files', []))}")
        print("---")
    
    # Return the most recent snapshot ID
    return snapshots[0]['snapshot_id'] if snapshots else None


def restore_snapshot_example(snapshot_id):
    """Example of restoring from a snapshot."""
    print("\n=== Restoring from a Snapshot ===")
    
    if not snapshot_id:
        print("No snapshot ID provided. Please create a snapshot first.")
        return
    
    client = create_client()
    
    # Confirm before restoring
    confirm = input(f"Restore from snapshot {snapshot_id}? This will overwrite data. (y/n): ")
    if confirm.lower() != 'y':
        print("Restore cancelled.")
        return
    
    # Restore from the specified snapshot
    result = restore_snapshot(
        client=client,
        snapshot_id=snapshot_id
    )
    
    print(f"Restore completed for snapshot: {result['snapshot_id']}")
    print(f"Restored items:")
    print(f"  - Blueprints: {result['restored_blueprints']}")
    print(f"  - Entities: {result['restored_entities']}")
    print(f"  - Actions: {result['restored_actions']}")
    print(f"  - Pages: {result['restored_pages']}")
    print(f"  - Scorecards: {result['restored_scorecards']}")
    
    if result['errors']:
        print(f"Errors encountered: {len(result['errors'])}")
        for error in result['errors'][:5]:  # Show first 5 errors
            print(f"  - {error['type']} {error['id']}: {error['error']}")


def main():
    """Run the examples."""
    print("PyPort Snapshot Utilities Examples")
    print("==================================")
    
    # Show available commands
    print("\nAvailable commands:")
    print("1. Create a snapshot")
    print("2. List available snapshots")
    print("3. Restore from a snapshot")
    print("4. Run all examples in sequence")
    print("q. Quit")
    
    choice = input("\nEnter your choice (1-4, q): ")
    
    if choice == '1':
        create_snapshot_example()
    elif choice == '2':
        list_snapshots_example()
    elif choice == '3':
        snapshot_id = input("Enter the snapshot ID to restore: ")
        restore_snapshot_example(snapshot_id)
    elif choice == '4':
        # Run all examples in sequence
        snapshot_id = create_snapshot_example()
        list_snapshots_example()
        restore_snapshot_example(snapshot_id)
    elif choice.lower() == 'q':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please try again.")
    
    print("\nExamples completed.")


if __name__ == "__main__":
    main()
