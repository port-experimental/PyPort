# Snapshot Tests

This directory contains snapshots for snapshot tests. Snapshots are serialized representations of test outputs that are used to detect changes in behavior.

## What are Snapshot Tests?

Snapshot tests capture the output of a component or function and compare it against a previously saved "snapshot" to detect changes. They are particularly useful for testing API responses, serialization/deserialization, and other data transformations.

## Directory Structure

Snapshots are organized by test module and class. For example, snapshots for the `TestBlueprintService` class in the `tests.test_blueprints` module would be stored in:

```
tests/snapshots/tests/test_blueprints/TestBlueprintService.json
```

## Updating Snapshots

To update snapshots, run the tests with the `UPDATE_SNAPSHOTS` environment variable set to `1`:

```bash
UPDATE_SNAPSHOTS=1 python -m unittest tests/test_blueprints.py
```

## Best Practices

1. **Review Snapshot Changes**: Always review snapshot changes carefully to ensure they are expected.
2. **Keep Snapshots Focused**: Snapshots should be focused on specific functionality to make changes easier to understand.
3. **Include Snapshots in Version Control**: Snapshots should be included in version control to track changes over time.
4. **Use Descriptive Snapshot IDs**: When using multiple snapshots in a single test, use descriptive IDs to make it clear what each snapshot represents.
