# Action Runs Service

The Action Runs service provides methods for managing action executions in Port. Action runs represent the execution instances of actions, including their status, logs, and approval workflows.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Action Runs service
action_runs_service = client.action_runs
```

## Methods

### get_action_runs

```python
def get_action_runs(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve action runs with optional pagination.

**Note**: Port API does not support traditional pagination for this endpoint. The `page` parameter is used for filtering by action ID.

#### Parameters

- **page** (int, optional): Used as action ID filter, not traditional pagination
- **per_page** (int, optional): Number of items per page
- **params** (dict, optional): Additional query parameters

#### Returns

- **Dict[str, Any]**: A dictionary containing action runs data

#### Example

```python
# Get all action runs
runs = client.action_runs.get_action_runs()

# Filter by action ID (using page parameter)
runs_for_action = client.action_runs.get_action_runs(page="deploy-action")
```

### get_action_run

```python
def get_action_run(
    run_id: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve a specific action run by its ID.

#### Parameters

- **run_id** (str): The ID of the action run to retrieve
- **params** (dict, optional): Additional query parameters

#### Returns

- **Dict[str, Any]**: A dictionary containing the action run details

#### Example

```python
# Get a specific action run
run = client.action_runs.get_action_run("run_123456")
print(f"Status: {run['status']}")
```

### update_action_run

```python
def update_action_run(
    run_id: str,
    run_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update an action run's status or other properties.

#### Parameters

- **run_id** (str): The ID of the action run to update
- **run_data** (dict): The data to update
- **params** (dict, optional): Additional query parameters

#### Returns

- **Dict[str, Any]**: The updated action run

#### Example

```python
# Update action run status
updated_run = client.action_runs.update_action_run(
    "run_123456",
    {"status": "SUCCESS", "summary": "Deployment completed"}
)
```

### approve_action_run

```python
def approve_action_run(
    run_id: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Approve an action run that requires approval.

#### Parameters

- **run_id** (str): The ID of the action run to approve
- **params** (dict, optional): Additional query parameters

#### Returns

- **Dict[str, Any]**: The approved action run

#### Example

```python
# Approve an action run
approved_run = client.action_runs.approve_action_run("run_123456")
```

### get_action_run_logs

```python
def get_action_run_logs(
    run_id: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve logs for a specific action run.

#### Parameters

- **run_id** (str): The ID of the action run
- **params** (dict, optional): Additional query parameters

#### Returns

- **Dict[str, Any]**: A dictionary containing the action run logs

#### Example

```python
# Get action run logs
logs = client.action_runs.get_action_run_logs("run_123456")
for log in logs.get("logs", []):
    print(f"{log['timestamp']}: {log['message']}")
```

### add_action_run_log

```python
def add_action_run_log(
    run_id: str,
    log_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Add a log entry to an action run.

#### Parameters

- **run_id** (str): The ID of the action run
- **log_data** (dict): The log data to add
- **params** (dict, optional): Additional query parameters

#### Returns

- **Dict[str, Any]**: Confirmation of the log addition

#### Example

```python
# Add a log entry
log_result = client.action_runs.add_action_run_log(
    "run_123456",
    {
        "message": "Starting deployment process",
        "level": "INFO",
        "timestamp": "2024-01-15T10:30:00Z"
    }
)
```

### get_action_run_approvers

```python
def get_action_run_approvers(
    run_id: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Get the list of approvers for an action run.

#### Parameters

- **run_id** (str): The ID of the action run
- **params** (dict, optional): Additional query parameters

#### Returns

- **Dict[str, Any]**: A dictionary containing the approvers list

#### Example

```python
# Get action run approvers
approvers = client.action_runs.get_action_run_approvers("run_123456")
for approver in approvers.get("approvers", []):
    print(f"Approver: {approver['email']}")
```

## Action Run Statuses

Action runs can have the following statuses:

- **IN_PROGRESS**: The action is currently running
- **SUCCESS**: The action completed successfully
- **FAILURE**: The action failed
- **WAITING_FOR_APPROVAL**: The action is waiting for approval
- **APPROVED**: The action has been approved
- **REJECTED**: The action has been rejected
- **CANCELLED**: The action was cancelled

## Error Handling

All action run methods can raise exceptions for various error conditions. See the [Error Handling](../error_handling.md) documentation for more details.
