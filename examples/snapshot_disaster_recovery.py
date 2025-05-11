#!/usr/bin/env python
"""
Disaster recovery script to restore the most recent backup.

This script:
1. Finds the most recent snapshot
2. Restores all data from that snapshot
3. Reports on the restoration results

Use this script in case of data loss or corruption in your Port environment.
"""
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from pyport import PortClient
from pyport.utils import list_snapshots, restore_snapshot


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


def find_latest_snapshot(backup_dir=None):
    """Find the most recent snapshot."""
    print("Finding the most recent snapshot...")
    
    # Get all snapshots
    snapshots = list_snapshots(backup_dir=backup_dir)
    
    if not snapshots:
        print("No snapshots found.")
        return None
    
    # Sort by timestamp (newest first)
    snapshots.sort(key=lambda x: x['timestamp'], reverse=True)
    latest_snapshot = snapshots[0]
    
    print(f"Found latest snapshot: {latest_snapshot['snapshot_id']} from {latest_snapshot['timestamp']}")
    print(f"This snapshot contains:")
    print(f"  - Blueprints: {latest_snapshot.get('include_blueprints', False)}")
    print(f"  - Entities: {latest_snapshot.get('include_entities', False)}")
    print(f"  - Actions: {latest_snapshot.get('include_actions', False)}")
    print(f"  - Pages: {latest_snapshot.get('include_pages', False)}")
    print(f"  - Scorecards: {latest_snapshot.get('include_scorecards', False)}")
    
    return latest_snapshot


def perform_disaster_recovery(snapshot_id, backup_dir=None):
    """Restore from the specified snapshot."""
    print(f"\nPerforming disaster recovery from snapshot: {snapshot_id}")
    
    # Create the client
    client = create_client()
    
    # Confirm before restoring
    confirm = input("WARNING: This will overwrite all data in your Port environment. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Disaster recovery cancelled.")
        return
    
    # Double-check
    confirm = input("Are you absolutely sure? This cannot be undone. (yes/no): ")
    if confirm.lower() != 'yes':
        print("Disaster recovery cancelled.")
        return
    
    print("\nStarting disaster recovery process...")
    
    # Restore from the snapshot
    result = restore_snapshot(
        client=client,
        snapshot_id=snapshot_id,
        backup_dir=backup_dir
    )
    
    print("\n=== Disaster Recovery Results ===")
    print(f"Restored from snapshot: {result['snapshot_id']}")
    print(f"Restored items:")
    print(f"  - Blueprints: {result['restored_blueprints']}")
    print(f"  - Entities: {result['restored_entities']}")
    print(f"  - Actions: {result['restored_actions']}")
    print(f"  - Pages: {result['restored_pages']}")
    print(f"  - Scorecards: {result['restored_scorecards']}")
    
    if result['errors']:
        print(f"\nErrors encountered: {len(result['errors'])}")
        print("Here are the first 10 errors:")
        for error in result['errors'][:10]:
            print(f"  - {error['type']} {error['id']}: {error['error']}")
        
        if len(result['errors']) > 10:
            print(f"  ... and {len(result['errors']) - 10} more errors.")
    else:
        print("\nNo errors encountered during recovery.")
    
    print("\nDisaster recovery process completed.")


def main():
    """Run the disaster recovery process."""
    print("PyPort Disaster Recovery")
    print("=======================")
    
    # Show options
    print("\nAvailable options:")
    print("1. Use default backup directory")
    print("2. Specify a custom backup directory")
    print("q. Quit")
    
    choice = input("\nEnter your choice (1-2, q): ")
    
    backup_dir = None
    
    if choice == '1':
        pass  # Use default backup directory
    elif choice == '2':
        backup_dir = input("Enter the path to your backup directory: ")
    elif choice.lower() == 'q':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Using default backup directory.")
    
    # Find the latest snapshot
    latest_snapshot = find_latest_snapshot(backup_dir)
    
    if not latest_snapshot:
        print("Cannot proceed with disaster recovery. No snapshots found.")
        return
    
    # Perform disaster recovery
    perform_disaster_recovery(latest_snapshot['snapshot_id'], backup_dir)


if __name__ == "__main__":
    main()
