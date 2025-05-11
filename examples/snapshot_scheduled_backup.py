#!/usr/bin/env python
"""
Example of a scheduled backup script for Port data.

This script:
1. Creates a daily backup with the current date
2. Manages backup retention (keeps only the last 7 daily backups)

It can be scheduled with cron (Linux/macOS) or Task Scheduler (Windows).

Cron example (daily at 2 AM):
0 2 * * * /path/to/python /path/to/snapshot_scheduled_backup.py

Windows Task Scheduler:
Program/script: C:\path\to\python.exe
Arguments: C:\path\to\snapshot_scheduled_backup.py
"""
import os
import sys
import shutil
import datetime
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from pyport import PortClient
from pyport.utils import save_snapshot, list_snapshots


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


def create_daily_backup():
    """Create a daily backup with the current date."""
    print("Creating daily backup...")
    
    client = create_client()
    
    # Create backup directory if it doesn't exist
    backup_dir = "scheduled-backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create a daily backup with the current date
    today = datetime.datetime.now().strftime("%Y%m%d")
    prefix = f"daily-backup-{today}"
    
    # Create the snapshot
    snapshot = save_snapshot(
        client=client,
        prefix=prefix,
        backup_dir=backup_dir
    )
    
    print(f"Daily backup created: {snapshot['snapshot_id']}")
    print(f"Saved {len(snapshot['files'])} files")
    
    return snapshot, backup_dir


def manage_backup_retention(backup_dir, retention_days=7):
    """
    Manage backup retention by keeping only the specified number of most recent daily backups.
    
    Args:
        backup_dir: Directory containing the backups
        retention_days: Number of daily backups to keep
    """
    print(f"\nManaging backup retention (keeping last {retention_days} daily backups)...")
    
    # List all snapshots
    all_snapshots = list_snapshots(backup_dir=backup_dir)
    
    # Filter for daily backups
    daily_backups = [s for s in all_snapshots if s['prefix'].startswith("daily-backup-")]
    
    if not daily_backups:
        print("No daily backups found.")
        return
    
    print(f"Found {len(daily_backups)} daily backups.")
    
    # Sort by timestamp (newest first) and keep only the specified number
    daily_backups.sort(key=lambda x: x['timestamp'], reverse=True)
    snapshots_to_keep = daily_backups[:retention_days]
    snapshot_ids_to_keep = [s['snapshot_id'] for s in snapshots_to_keep]
    
    # Delete old snapshots
    for snapshot in daily_backups:
        if snapshot['snapshot_id'] not in snapshot_ids_to_keep:
            snapshot_dir = Path(backup_dir) / snapshot['snapshot_id']
            if snapshot_dir.exists():
                print(f"Removing old snapshot: {snapshot['snapshot_id']}")
                shutil.rmtree(snapshot_dir)


def main():
    """Run the scheduled backup process."""
    print("PyPort Scheduled Backup")
    print("======================")
    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create the daily backup
    snapshot, backup_dir = create_daily_backup()
    
    # Manage backup retention
    manage_backup_retention(backup_dir)
    
    print("\nScheduled backup completed successfully.")


if __name__ == "__main__":
    main()
