# Snapshot Testing in PyPort

This document explains how to use snapshot testing in PyPort to test API responses and other data structures.

## What is Snapshot Testing?

Snapshot testing is a testing approach where you capture the output of a component or function and compare it against a previously saved "snapshot" to detect changes. It's particularly useful for testing API responses, serialization/deserialization, and other data transformations.

## Benefits of Snapshot Testing

- **Regression Detection**: Quickly identify unintended changes in API responses
- **Comprehensive Testing**: Test complex data structures without writing detailed assertions
- **Documentation**: Snapshots serve as documentation of expected API responses
- **Maintainability**: Easier to maintain tests for complex responses
- **Confidence**: Higher confidence in refactoring and changes

## How to Use Snapshot Testing

### 1. Create a Snapshot Test

To create a snapshot test, extend the `SnapshotTest` class from `tests.utils.snapshot_test`:

```python
from tests.snapshots.utils.snapshot_test import SnapshotTest


class TestBlueprintService(SnapshotTest):
    def test_get_blueprint_response(self):
        # Arrange
        client = create_test_client()

        # Act
        blueprint = client.blueprints.get_blueprint("service")

        # Assert
        self.assert_matches_snapshot(blueprint)
```

### 2. Run the Test

When you run the test for the first time, it will create a snapshot of the output:

```bash
python -m unittest tests/test_blueprint_service.py
```

### 3. Update Snapshots

To update snapshots, run the tests with the `UPDATE_SNAPSHOTS` environment variable set to `1`:

```bash
UPDATE_SNAPSHOTS=1 python -m unittest tests/test_blueprint_service.py
```

### 4. Multiple Snapshots in a Single Test

You can use multiple snapshots in a single test by providing a snapshot ID:

```python
def test_multiple_snapshots(self):
    # Arrange
    client = create_test_client()
    
    # Act
    blueprint1 = client.blueprints.get_blueprint("service1")
    blueprint2 = client.blueprints.get_blueprint("service2")
    
    # Assert
    self.assert_matches_snapshot(blueprint1, "service1")
    self.assert_matches_snapshot(blueprint2, "service2")
```

## Best Practices

### 1. Review Snapshot Changes

Always review snapshot changes carefully to ensure they are expected. Snapshot tests can be a powerful tool, but they can also be a source of false positives if not used carefully.

### 2. Keep Snapshots Focused

Snapshots should be focused on specific functionality to make changes easier to understand. Avoid creating snapshots of large, complex objects that change frequently.

### 3. Include Snapshots in Version Control

Snapshots should be included in version control to track changes over time. This allows you to see how API responses have changed over time.

### 4. Use Descriptive Snapshot IDs

When using multiple snapshots in a single test, use descriptive IDs to make it clear what each snapshot represents.

### 5. Mock External Dependencies

When testing API responses, mock external dependencies to ensure consistent results. This makes snapshot tests more reliable and less prone to false positives.

## Example Tests

For examples of snapshot tests, see:

- `tests/test_snapshot_example.py`: Basic examples of snapshot testing
- `tests/test_blueprints_snapshot.py`: Snapshot tests for the Blueprints API service
- `tests/test_entities_snapshot.py`: Snapshot tests for the Entities API service
- `tests/test_actions_snapshot.py`: Snapshot tests for the Actions API service
