# Type System

PyPort includes a comprehensive type system that defines the structure of API responses and parameters. This helps with IDE autocompletion, type checking, and documentation.

## Importing Types

```python
from pyport.types import (
    Blueprint,
    Entity,
    Action,
    ActionRun,
    Team,
    Role,
    Organization,
    Pagination,
    EntityProperty
)
```

## Common Types

### JsonDict

```python
JsonDict = Dict[str, Any]
```

A dictionary with string keys and any values.

### JsonList

```python
JsonList = List[JsonDict]
```

A list of dictionaries with string keys and any values.

### JsonValue

```python
JsonValue = Union[str, int, float, bool, None, JsonDict, List[Any]]
```

A JSON-serializable value.

## API Response Types

### Blueprint

```python
Blueprint = Dict[str, Any]
```

A dictionary representing a blueprint.

#### Example

```python
{
    "identifier": "service",
    "title": "Service",
    "properties": {
        "language": {
            "type": "string",
            "title": "Language",
            "enum": ["Python", "JavaScript", "Java", "Go"]
        }
    }
}
```

### Entity

```python
Entity = Dict[str, Any]
```

A dictionary representing an entity.

#### Example

```python
{
    "identifier": "payment-service",
    "title": "Payment Service",
    "blueprint": "service",
    "properties": {
        "language": "Python",
        "url": "https://github.com/example/payment-service"
    }
}
```

### Action

```python
Action = Dict[str, Any]
```

A dictionary representing an action.

#### Example

```python
{
    "identifier": "deploy",
    "title": "Deploy Service",
    "blueprint": "service",
    "trigger": "manual",
    "requiredApproval": False
}
```

### ActionRun

```python
ActionRun = Dict[str, Any]
```

A dictionary representing an action run.

#### Example

```python
{
    "id": "run-123",
    "action": "deploy",
    "blueprint": "service",
    "entity": "payment-service",
    "status": "success",
    "createdAt": "2023-01-01T12:00:00Z",
    "updatedAt": "2023-01-01T12:05:00Z"
}
```

### Team

```python
Team = Dict[str, Any]
```

A dictionary representing a team.

#### Example

```python
{
    "identifier": "devops",
    "title": "DevOps Team",
    "members": ["user1", "user2"]
}
```

### Role

```python
Role = Dict[str, Any]
```

A dictionary representing a role.

#### Example

```python
{
    "identifier": "admin",
    "title": "Administrator",
    "permissions": ["read", "write", "delete"]
}
```

### Organization

```python
Organization = Dict[str, Any]
```

A dictionary representing an organization.

#### Example

```python
{
    "name": "Example Organization",
    "domain": "example.com"
}
```

### Pagination

```python
Pagination = Dict[str, Any]
```

A dictionary representing pagination information.

#### Example

```python
{
    "page": 1,
    "per_page": 10,
    "total": 100,
    "total_pages": 10
}
```

### EntityProperty

```python
EntityProperty = Union[str, int, float, bool, None, List[Any], Dict[str, Any]]
```

A value of an entity property.

## API Parameter Types

### PaginationParams

```python
PaginationParams = Dict[str, int]
```

A dictionary containing pagination parameters.

#### Example

```python
{
    "page": 1,
    "per_page": 10
}
```

## Type Annotations

PyPort uses type annotations throughout the codebase to provide better IDE support and documentation. For example:

```python
def get_blueprint(
    self,
    blueprint_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> Blueprint:
    """
    Get a specific blueprint by its identifier.
    
    Args:
        blueprint_identifier: The unique identifier of the blueprint to retrieve.
        params: Optional query parameters for the request.
        
    Returns:
        A dictionary containing the blueprint details.
        
    Raises:
        PortResourceNotFoundError: If the blueprint does not exist.
        PortApiError: If another API error occurs.
    """
```

## Type Stubs

PyPort includes type stub files (.pyi) that provide additional type information to IDEs without affecting runtime behavior. These files help your IDE understand the structure of the library even better.

Type stubs are located alongside the Python files they describe, with the same name but a .pyi extension.
