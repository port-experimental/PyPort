#!/usr/bin/env python
"""
Examples of selective snapshot operations in PyPort.

This script demonstrates how to:
1. Create a selective snapshot (backup only specific components)
2. Restore selectively from a snapshot
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


def selective_backup_example():
    """Example of creating a selective snapshot."""
    print("\n=== Creating a Selective Snapshot ===")
    
    client = create_client()
    
    # Create a custom backup directory
    backup_dir = "custom-backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create a selective snapshot with only blueprints and entities
    snapshot = save_snapshot(
        client=client,
        prefix="blueprints-entities-only",
        backup_dir=backup_dir,
        include_blueprints=True,
        include_entities=True,
        include_actions=False,
        include_pages=False,
        include_scorecards=False
    )
    
    print(f"Selective snapshot created: {snapshot['snapshot_id']}")
    print(f"Saved {len(snapshot['files'])} files")
    print(f"Backup directory: {backup_dir}")
    print(f"Metadata file: {snapshot['metadata_file']}")
    
    return snapshot['snapshot_id'], backup_dir


def selective_restore_example():
    """Example of selectively restoring from a snapshot."""
    print("\n=== Selectively Restoring from a Snapshot ===")
    
    # List available snapshots
    snapshots = list_snapshots()
    
    if not snapshots:
        print("No snapshots found. Please create a snapshot first.")
        return
    
    # Print available snapshots
    print("Available snapshots:")
    for i, snapshot in enumerate(snapshots):
        print(f"{i+1}. {snapshot['snapshot_id']} (Created: {snapshot['timestamp']})")
    
    # Select a snapshot
    try:
        selection = int(input("\nSelect a snapshot number to restore from: ")) - 1
        if selection < 0 or selection >= len(snapshots):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    snapshot_id = snapshots[selection]['snapshot_id']
    
    # Get restore options
    print("\nSelect components to restore:")
    restore_blueprints = input("Restore blueprints? (y/n): ").lower() == 'y'
    restore_entities = input("Restore entities? (y/n): ").lower() == 'y'
    restore_actions = input("Restore actions? (y/n): ").lower() == 'y'
    restore_pages = input("Restore pages? (y/n): ").lower() == 'y'
    restore_scorecards = input("Restore scorecards? (y/n): ").lower() == 'y'
    
    # Confirm before restoring
    print(f"\nRestore options:")
    print(f"  - Snapshot: {snapshot_id}")
    print(f"  - Blueprints: {'Yes' if restore_blueprints else 'No'}")
    print(f"  - Entities: {'Yes' if restore_entities else 'No'}")
    print(f"  - Actions: {'Yes' if restore_actions else 'No'}")
    print(f"  - Pages: {'Yes' if restore_pages else 'No'}")
    print(f"  - Scorecards: {'Yes' if restore_scorecards else 'No'}")
    
    confirm = input("\nProceed with restore? This will overwrite data. (y/n): ")
    if confirm.lower() != 'y':
        print("Restore cancelled.")
        return
    
    client = create_client()
    
    # Restore selectively from the snapshot
    result = restore_snapshot(
        client=client,
        snapshot_id=snapshot_id,
        restore_blueprints=restore_blueprints,
        restore_entities=restore_entities,
        restore_actions=restore_actions,
        restore_pages=restore_pages,
        restore_scorecards=restore_scorecards
    )
    
    print(f"\nSelective restore completed for snapshot: {result['snapshot_id']}")
    print(f"Restored items:")
    print(f"  - Blueprints: {result['restored_blueprints']}")
    print(f"  - Entities: {result['restored_entities']}")
    print(f"  - Actions: {result['restored_actions']}")
    print(f"  - Pages: {result['restored_pages']}")
    print(f"  - Scorecards: {result['restored_scorecards']}")
    
    if result['errors']:
        print(f"\nErrors encountered: {len(result['errors'])}")
        for error in result['errors'][:5]:  # Show first 5 errors
            print(f"  - {error['type']} {error['id']}: {error['error']}")


def main():
    """Run the examples."""
    print("PyPort Selective Snapshot Operations Examples")
    print("============================================")
    
    # Show available commands
    print("\nAvailable commands:")
    print("1. Create a selective snapshot (blueprints and entities only)")
    print("2. Restore selectively from a snapshot")
    print("3. Run both examples in sequence")
    print("q. Quit")
    
    choice = input("\nEnter your choice (1-3, q): ")
    
    if choice == '1':
        selective_backup_example()
    elif choice == '2':
        selective_restore_example()
    elif choice == '3':
        # Run both examples in sequence
        selective_backup_example()
        selective_restore_example()
    elif choice.lower() == 'q':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please try again.")
    
    print("\nExamples completed.")


if __name__ == "__main__":
    main()
