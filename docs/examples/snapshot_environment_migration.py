#!/usr/bin/env python
"""
Environment migration script using snapshots.

This script:
1. Creates a snapshot of the source environment
2. Restores the snapshot to the target environment
3. Reports on the migration results

Use this script to migrate data between different Port environments
(e.g., from development to staging, or staging to production).
"""
import os
import sys
import tempfile
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from pyport import PortClient
from pyport.utils import save_snapshot, restore_snapshot


def create_client(env_prefix=""):
    """
    Create a PortClient instance using environment variables.
    
    Args:
        env_prefix: Prefix for environment variables (e.g., "SOURCE_" or "TARGET_")
    """
    client_id_var = f"{env_prefix}PORT_CLIENT_ID"
    client_secret_var = f"{env_prefix}PORT_CLIENT_SECRET"
    
    client_id = os.environ.get(client_id_var)
    client_secret = os.environ.get(client_secret_var)
    
    if not client_id or not client_secret:
        print(f"Error: {client_id_var} and {client_secret_var} environment variables must be set.")
        print("Example:")
        print(f"  export {client_id_var}=your-client-id")
        print(f"  export {client_secret_var}=your-client-secret")
        sys.exit(1)
    
    return PortClient(
        client_id=client_id,
        client_secret=client_secret
    )


def migrate_environment(source_prefix="SOURCE_", target_prefix="TARGET_", components=None):
    """
    Migrate data from source environment to target environment.
    
    Args:
        source_prefix: Prefix for source environment variables
        target_prefix: Prefix for target environment variables
        components: Dictionary of components to migrate (True/False)
    """
    if components is None:
        components = {
            'blueprints': True,
            'entities': True,
            'actions': True,
            'pages': True,
            'scorecards': True
        }
    
    print("=== Environment Migration ===")
    print(f"Source: Using credentials from {source_prefix}PORT_CLIENT_ID and {source_prefix}PORT_CLIENT_SECRET")
    print(f"Target: Using credentials from {target_prefix}PORT_CLIENT_ID and {target_prefix}PORT_CLIENT_SECRET")
    print("\nComponents to migrate:")
    for component, include in components.items():
        print(f"  - {component.capitalize()}: {'Yes' if include else 'No'}")
    
    # Confirm before proceeding
    confirm = input("\nProceed with migration? This will overwrite data in the target environment. (y/n): ")
    if confirm.lower() != 'y':
        print("Migration cancelled.")
        return
    
    # Initialize clients
    print("\nInitializing clients...")
    source_client = create_client(source_prefix)
    target_client = create_client(target_prefix)
    
    # Create a temporary directory for the migration
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Step 1: Create a snapshot of the source environment
        print("\nStep 1: Creating snapshot of source environment...")
        snapshot = save_snapshot(
            client=source_client,
            prefix="migration",
            backup_dir=temp_dir,
            include_blueprints=components['blueprints'],
            include_entities=components['entities'],
            include_actions=components['actions'],
            include_pages=components['pages'],
            include_scorecards=components['scorecards']
        )
        
        snapshot_id = snapshot['snapshot_id']
        print(f"Snapshot created: {snapshot_id}")
        print(f"Saved {len(snapshot['files'])} files")
        
        # Step 2: Restore the snapshot to the target environment
        print("\nStep 2: Restoring to target environment...")
        result = restore_snapshot(
            client=target_client,
            snapshot_id=snapshot_id,
            backup_dir=temp_dir,
            restore_blueprints=components['blueprints'],
            restore_entities=components['entities'],
            restore_actions=components['actions'],
            restore_pages=components['pages'],
            restore_scorecards=components['scorecards']
        )
        
        print("\n=== Migration Results ===")
        print(f"Migrated items:")
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
            print("\nNo errors encountered during migration.")
    
    print("\nTemporary files cleaned up automatically")
    print("Migration completed!")


def main():
    """Run the environment migration process."""
    print("PyPort Environment Migration")
    print("===========================")
    
    # Get source and target environment prefixes
    print("\nEnvironment Configuration:")
    print("1. Use default prefixes (SOURCE_ and TARGET_)")
    print("2. Specify custom prefixes")
    
    choice = input("\nEnter your choice (1-2): ")
    
    source_prefix = "SOURCE_"
    target_prefix = "TARGET_"
    
    if choice == '2':
        source_prefix = input("Enter source environment prefix (e.g., DEV_): ")
        target_prefix = input("Enter target environment prefix (e.g., PROD_): ")
        
        # Add trailing underscore if not provided
        if source_prefix and not source_prefix.endswith('_'):
            source_prefix += '_'
        if target_prefix and not target_prefix.endswith('_'):
            target_prefix += '_'
    
    # Select components to migrate
    print("\nSelect components to migrate:")
    components = {
        'blueprints': input("Include blueprints? (y/n): ").lower() == 'y',
        'entities': input("Include entities? (y/n): ").lower() == 'y',
        'actions': input("Include actions? (y/n): ").lower() == 'y',
        'pages': input("Include pages? (y/n): ").lower() == 'y',
        'scorecards': input("Include scorecards? (y/n): ").lower() == 'y'
    }
    
    # Perform migration
    migrate_environment(source_prefix, target_prefix, components)


if __name__ == "__main__":
    main()
