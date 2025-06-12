# Utilities

PyPort includes several utility functions to help with common operations.

## Importing Utilities

```python
from pyport.utils import (
    clear_blueprint,
    save_snapshot,
    restore_snapshot,
    list_snapshots
)
```

## Blueprint Utilities

### clear_blueprint

```python
def clear_blueprint(
    client: PortClient,
    blueprint_identifier: str
) -> Dict[str, Any]
```

Delete all entities of a specific blueprint using Port's bulk delete API.

This utility function wraps the existing `delete_all_blueprint_entities` API method
to provide a convenient interface for clearing blueprints.

#### Parameters

- **client** (PortClient): The Port client instance.
- **blueprint_identifier** (str): The identifier of the blueprint.

#### Returns

- **Dict[str, Any]**: A dictionary containing the results from the Port API.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
from pyport import PortClient
from pyport.utils import clear_blueprint

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Delete all entities in the "service" blueprint
result = clear_blueprint(client, "service")
print(f"Operation result: {result}")

# Alternative: Use the API method directly
result = client.blueprints.delete_all_blueprint_entities("service")
```

## Snapshot Utilities

### save_snapshot

```python
def save_snapshot(
    client: PortClient,
    prefix: str = "snapshot",
    include_blueprints: bool = True,
    include_entities: bool = True,
    include_actions: bool = True,
    include_pages: bool = False,
    include_scorecards: bool = False
) -> Dict[str, Any]
```

Save a snapshot of the Port data.

#### Parameters

- **client** (PortClient): The Port client instance.
- **prefix** (str, optional): A prefix for the snapshot ID. Default is "snapshot".
- **include_blueprints** (bool, optional): Whether to include blueprints in the snapshot. Default is True.
- **include_entities** (bool, optional): Whether to include entities in the snapshot. Default is True.
- **include_actions** (bool, optional): Whether to include actions in the snapshot. Default is True.
- **include_pages** (bool, optional): Whether to include pages in the snapshot. Default is False.
- **include_scorecards** (bool, optional): Whether to include scorecards in the snapshot. Default is False.

#### Returns

- **Dict[str, Any]**: A dictionary containing the results of the operation.

#### Raises

- **PortApiError**: If the API request fails.

#### Example

```python
from pyport import PortClient
from pyport.utils import save_snapshot

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Save a snapshot of the Port data
snapshot = save_snapshot(
    client,
    prefix="my-backup",
    include_blueprints=True,
    include_entities=True,
    include_actions=True
)
print(f"Snapshot saved: {snapshot['snapshot_id']}")
```

### restore_snapshot

```python
def restore_snapshot(
    client: PortClient,
    snapshot_id: str,
    restore_blueprints: bool = True,
    restore_entities: bool = True,
    restore_actions: bool = True,
    restore_pages: bool = False,
    restore_scorecards: bool = False,
    clear_existing: bool = False
) -> Dict[str, Any]
```

Restore a snapshot of the Port data.

#### Parameters

- **client** (PortClient): The Port client instance.
- **snapshot_id** (str): The ID of the snapshot to restore.
- **restore_blueprints** (bool, optional): Whether to restore blueprints. Default is True.
- **restore_entities** (bool, optional): Whether to restore entities. Default is True.
- **restore_actions** (bool, optional): Whether to restore actions. Default is True.
- **restore_pages** (bool, optional): Whether to restore pages. Default is False.
- **restore_scorecards** (bool, optional): Whether to restore scorecards. Default is False.
- **clear_existing** (bool, optional): Whether to clear existing data before restoring. Default is False.

#### Returns

- **Dict[str, Any]**: A dictionary containing the results of the operation.

#### Raises

- **FileNotFoundError**: If the snapshot does not exist.
- **PortApiError**: If the API request fails.

#### Example

```python
from pyport import PortClient
from pyport.utils import restore_snapshot

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Restore a snapshot
restore_result = restore_snapshot(
    client,
    "my-backup_20230101_120000",
    restore_blueprints=True,
    restore_entities=True,
    clear_existing=True
)
print(f"Restored {restore_result['restored_blueprints']} blueprints and {restore_result['restored_entities']} entities")
```

### list_snapshots

```python
def list_snapshots() -> List[Dict[str, Any]]
```

List all available snapshots.

#### Returns

- **List[Dict[str, Any]]**: A list of dictionaries containing snapshot information.

#### Example

```python
from pyport.utils import list_snapshots

# List all available snapshots
snapshots = list_snapshots()
for snapshot in snapshots:
    print(f"{snapshot['snapshot_id']} ({snapshot['timestamp']})")
```
