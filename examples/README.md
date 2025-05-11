# PyPort Examples

This directory contains example scripts demonstrating how to use PyPort for various tasks.

## Snapshot Utilities Examples

The snapshot utilities allow you to backup, restore, and migrate Port data.

### Basic Usage

- **[snapshot_basic_usage.py](snapshot_basic_usage.py)**: Demonstrates basic snapshot operations
  - Creating a snapshot (backup)
  - Listing available snapshots
  - Restoring from a snapshot

### Advanced Usage

- **[snapshot_selective_operations.py](snapshot_selective_operations.py)**: Demonstrates selective backup and restore
  - Creating a snapshot with only specific components
  - Restoring only selected components from a snapshot

- **[snapshot_scheduled_backup.py](snapshot_scheduled_backup.py)**: Example of a scheduled backup script
  - Creates daily backups with timestamp
  - Manages backup retention (keeps only the last N backups)
  - Can be scheduled with cron or Windows Task Scheduler

- **[snapshot_disaster_recovery.py](snapshot_disaster_recovery.py)**: Disaster recovery script
  - Finds the most recent snapshot
  - Restores all data from that snapshot
  - Reports on the restoration results

- **[snapshot_environment_migration.py](snapshot_environment_migration.py)**: Environment migration script
  - Creates a snapshot of the source environment
  - Restores the snapshot to the target environment
  - Useful for migrating from development to staging or production

## Running the Examples

To run any example, make sure you have set the required environment variables:

```bash
# For basic examples
export PORT_CLIENT_ID=your-client-id
export PORT_CLIENT_SECRET=your-client-secret

# For environment migration
export SOURCE_PORT_CLIENT_ID=source-client-id
export SOURCE_PORT_CLIENT_SECRET=source-client-secret
export TARGET_PORT_CLIENT_ID=target-client-id
export TARGET_PORT_CLIENT_SECRET=target-client-secret
```

Then run the example script:

```bash
python examples/snapshot_basic_usage.py
```

## Blueprint Utilities Examples

- **[clear_blueprint_example.py](clear_blueprint_example.py)**: Demonstrates how to delete all entities in a blueprint

## Notes

- These examples are designed to be run from the project root directory
- They automatically add the `src` directory to the Python path
- Most examples are interactive and will prompt for input when needed
- Be careful when running examples that modify data (especially restore and migration scripts)
