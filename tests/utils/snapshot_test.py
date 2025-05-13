"""
Snapshot testing utilities for PyPort.

This module provides a base class and utilities for snapshot testing.
Snapshot testing captures the output of a component or function and compares it
against a previously saved "snapshot" to detect changes.
"""

import os
import json
import inspect
import unittest
import datetime
import difflib
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Tuple

# Get the version of PyPort
try:
    from pyport import __version__ as pyport_version
except ImportError:
    pyport_version = "unknown"


class SnapshotTest(unittest.TestCase):
    """
    Base class for snapshot tests.
    
    This class extends unittest.TestCase to add snapshot testing capabilities.
    It provides methods to compare outputs with stored snapshots and update
    snapshots when needed.
    
    Example:
        class TestBlueprintService(SnapshotTest):
            def test_get_blueprint_response(self):
                # Arrange
                client = create_test_client()
                
                # Act
                blueprint = client.blueprints.get_blueprint("service")
                
                # Assert
                self.assert_matches_snapshot(blueprint)
    """
    
    # Directory where snapshots are stored
    SNAPSHOTS_DIR = Path("tests/snapshots")
    
    # Environment variable to control snapshot updates
    UPDATE_SNAPSHOTS_ENV = "UPDATE_SNAPSHOTS"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._snapshots_loaded = False
        self._snapshots = {}
    
    def assert_matches_snapshot(self, value: Any, snapshot_id: Optional[str] = None) -> None:
        """
        Assert that the given value matches the stored snapshot.
        
        Args:
            value: The value to compare with the snapshot.
            snapshot_id: Optional identifier for the snapshot. If not provided,
                a default identifier will be used.
                
        Raises:
            AssertionError: If the value does not match the snapshot.
        """
        # Get the test method name
        test_name = self._testMethodName
        
        # If no snapshot_id is provided, use a default
        if snapshot_id is None:
            snapshot_id = "default"
        
        # Load snapshots if not already loaded
        if not self._snapshots_loaded:
            self._load_snapshots()
        
        # Get the current snapshot data
        current_data = self._serialize_value(value)
        
        # Check if we should update snapshots
        update_snapshots = os.environ.get(self.UPDATE_SNAPSHOTS_ENV, "0").lower() in ("1", "true", "yes")
        
        # Check if the test exists in the snapshots
        if test_name not in self._snapshots:
            self._snapshots[test_name] = {}
        
        # Check if the snapshot exists
        if snapshot_id not in self._snapshots[test_name] or update_snapshots:
            # Create or update the snapshot
            self._snapshots[test_name][snapshot_id] = {
                "data": current_data,
                "metadata": {
                    "created_at": datetime.datetime.now().isoformat(),
                    "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                    "pyport_version": pyport_version
                }
            }
            # Save the snapshots
            self._save_snapshots()
            # Skip the assertion if we're updating snapshots
            if update_snapshots:
                return
        
        # Get the expected data from the snapshot
        expected_data = self._snapshots[test_name][snapshot_id]["data"]
        
        # Compare the current data with the expected data
        self._assert_equal(expected_data, current_data, snapshot_id)
    
    def _assert_equal(self, expected: Any, actual: Any, snapshot_id: str) -> None:
        """
        Assert that the expected and actual values are equal.
        
        Args:
            expected: The expected value from the snapshot.
            actual: The actual value to compare.
            snapshot_id: The identifier for the snapshot.
            
        Raises:
            AssertionError: If the values are not equal.
        """
        if expected != actual:
            # Generate a diff of the values
            expected_str = json.dumps(expected, indent=2, sort_keys=True)
            actual_str = json.dumps(actual, indent=2, sort_keys=True)
            diff = difflib.unified_diff(
                expected_str.splitlines(),
                actual_str.splitlines(),
                fromfile=f"expected ({snapshot_id})",
                tofile=f"actual ({snapshot_id})",
                lineterm=""
            )
            
            # Build the error message
            error_message = [
                f"Snapshot '{snapshot_id}' does not match for test '{self._testMethodName}'.",
                "To update the snapshot, run the tests with UPDATE_SNAPSHOTS=1.",
                "Diff:",
                *diff
            ]
            
            # Raise an assertion error with the diff
            self.fail("\n".join(error_message))
    
    def _serialize_value(self, value: Any) -> Any:
        """
        Serialize a value for storage in a snapshot.
        
        Args:
            value: The value to serialize.
            
        Returns:
            The serialized value.
        """
        # If the value is a dict, serialize each value
        if isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        
        # If the value is a list, serialize each item
        if isinstance(value, list):
            return [self._serialize_value(item) for item in value]
        
        # If the value is a tuple, convert to list and serialize
        if isinstance(value, tuple):
            return [self._serialize_value(item) for item in value]
        
        # If the value is a set, convert to sorted list and serialize
        if isinstance(value, set):
            return sorted([self._serialize_value(item) for item in value])
        
        # If the value has a to_dict method, use it
        if hasattr(value, "to_dict") and callable(value.to_dict):
            return self._serialize_value(value.to_dict())
        
        # Return the value as is for basic types
        return value
    
    def _get_snapshot_file_path(self) -> Path:
        """
        Get the path to the snapshot file for the current test class.
        
        Returns:
            The path to the snapshot file.
        """
        # Get the module name and class name
        module_name = self.__class__.__module__
        class_name = self.__class__.__name__
        
        # Create the directory structure
        module_path = module_name.replace(".", "/")
        snapshot_dir = self.SNAPSHOTS_DIR / module_path
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Return the snapshot file path
        return snapshot_dir / f"{class_name}.json"
    
    def _load_snapshots(self) -> None:
        """
        Load snapshots from the snapshot file.
        """
        snapshot_file = self._get_snapshot_file_path()
        
        # If the snapshot file exists, load it
        if snapshot_file.exists():
            with open(snapshot_file, "r") as f:
                self._snapshots = json.load(f)
        
        # Mark snapshots as loaded
        self._snapshots_loaded = True
    
    def _save_snapshots(self) -> None:
        """
        Save snapshots to the snapshot file.
        """
        snapshot_file = self._get_snapshot_file_path()
        
        # Create the directory if it doesn't exist
        snapshot_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the snapshots
        with open(snapshot_file, "w") as f:
            json.dump(self._snapshots, f, indent=2, sort_keys=True)
