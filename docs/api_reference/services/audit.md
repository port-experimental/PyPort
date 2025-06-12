# Audit Service

The Audit service provides methods for accessing audit logs in Port. Audit logs track all activities and changes within your Port organization.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Audit service
audit_service = client.audit
```

## Methods

### get_audit_logs

```python
def get_audit_logs(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve audit logs for the organization.

#### Parameters

- **page** (int, optional): The page number to retrieve. Default is None.
- **per_page** (int, optional): The number of items per page. Default is None.
- **params** (dict, optional): Additional query parameters for filtering logs.

#### Returns

- **Dict[str, Any]**: A dictionary containing audit logs data.

#### Raises

- **PortApiError**: If the API request fails.

#### Example

```python
# Get all audit logs
logs = client.audit.get_audit_logs()
for log in logs.get("logs", []):
    print(f"{log['timestamp']}: {log['action']} by {log['user']}")

# Get audit logs with pagination
logs_page1 = client.audit.get_audit_logs(page=1, per_page=50)

# Filter audit logs by date range
from datetime import datetime, timedelta
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

filtered_logs = client.audit.get_audit_logs(params={
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat()
})
```

## Audit Log Structure

Audit logs in Port have the following structure:

```python
{
    "id": "log_123456",
    "timestamp": "2024-01-15T10:30:00Z",
    "action": "entity.created",
    "user": {
        "email": "john.doe@example.com",
        "name": "John Doe"
    },
    "resource": {
        "type": "entity",
        "identifier": "payment-service",
        "blueprint": "service"
    },
    "details": {
        "changes": {
            "properties": {
                "language": "Python"
            }
        }
    },
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0..."
}
```

## Audit Event Types

Port tracks various types of events:

### Entity Events
- **entity.created**: Entity was created
- **entity.updated**: Entity was updated
- **entity.deleted**: Entity was deleted

### Blueprint Events
- **blueprint.created**: Blueprint was created
- **blueprint.updated**: Blueprint was updated
- **blueprint.deleted**: Blueprint was deleted

### Action Events
- **action.created**: Action was created
- **action.updated**: Action was updated
- **action.deleted**: Action was deleted
- **action.executed**: Action was executed

### User Events
- **user.invited**: User was invited
- **user.login**: User logged in
- **user.logout**: User logged out

### Organization Events
- **organization.updated**: Organization settings changed
- **integration.created**: Integration was created
- **integration.updated**: Integration was updated

## Filtering Audit Logs

You can filter audit logs using various parameters:

### By Date Range
```python
logs = client.audit.get_audit_logs(params={
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-01-31T23:59:59Z"
})
```

### By Action Type
```python
logs = client.audit.get_audit_logs(params={
    "action": "entity.created"
})
```

### By User
```python
logs = client.audit.get_audit_logs(params={
    "user": "john.doe@example.com"
})
```

### By Resource
```python
logs = client.audit.get_audit_logs(params={
    "resource_type": "entity",
    "resource_identifier": "payment-service"
})
```

## Use Cases

### Compliance Monitoring
Track all changes for compliance and security auditing:

```python
# Get all entity modifications in the last 30 days
logs = client.audit.get_audit_logs(params={
    "action": "entity.updated",
    "start_date": (datetime.now() - timedelta(days=30)).isoformat()
})
```

### User Activity Tracking
Monitor user activities and access patterns:

```python
# Get all actions by a specific user
user_logs = client.audit.get_audit_logs(params={
    "user": "admin@example.com"
})
```

### Change History
Track changes to specific resources:

```python
# Get all changes to a specific entity
entity_logs = client.audit.get_audit_logs(params={
    "resource_type": "entity",
    "resource_identifier": "payment-service"
})
```

## Error Handling

All audit methods can raise exceptions for various error conditions:

- **PortAuthError**: Insufficient permissions to access audit logs
- **PortValidationError**: Invalid filter parameters
- **PortApiError**: General API errors

See the [Error Handling](../error_handling.md) documentation for more details.
