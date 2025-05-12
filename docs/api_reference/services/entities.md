# Entities Service

The Entities service provides methods for managing entities in Port. Entities are instances of blueprints that represent real-world resources in your software catalog.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Entities service
entities_service = client.entities
```

## Methods

### get_entities

```python
def get_entities(
    blueprint_identifier: str,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]
```

Retrieve all entities of a specific blueprint.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **page** (int, optional): The page number to retrieve. Default is None.
- **per_page** (int, optional): The number of items per page. Default is None.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **List[Dict[str, Any]]**: A list of entity dictionaries.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Get all service entities
services = client.entities.get_entities("service")

# Get service entities with pagination
services_page1 = client.entities.get_entities("service", page=1, per_page=10)

# Get service entities with additional query parameters
filtered_services = client.entities.get_entities(
    "service",
    params={"filter": "value"}
)
```

### get_entity

```python
def get_entity(
    blueprint_identifier: str,
    entity_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve a specific entity by its identifier.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **entity_identifier** (str): The identifier of the entity to retrieve.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the entity details.

#### Raises

- **PortResourceNotFoundError**: If the blueprint or entity does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Get a specific entity
api_service = client.entities.get_entity("service", "api-service")

# Get an entity with additional query parameters
api_service = client.entities.get_entity(
    "service",
    "api-service",
    params={"include": "properties"}
)
```

### create_entity

```python
def create_entity(
    blueprint_identifier: str,
    entity_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Create a new entity.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **entity_data** (dict): A dictionary containing the entity data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the created entity.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortValidationError**: If the entity data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Create a new entity
new_entity = client.entities.create_entity(
    "service",
    {
        "identifier": "payment-service",
        "title": "Payment Service",
        "properties": {
            "language": "Python",
            "url": "https://github.com/example/payment-service"
        }
    }
)
```

### update_entity

```python
def update_entity(
    blueprint_identifier: str,
    entity_identifier: str,
    entity_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update an existing entity.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **entity_identifier** (str): The identifier of the entity to update.
- **entity_data** (dict): A dictionary containing the updated entity data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the updated entity.

#### Raises

- **PortResourceNotFoundError**: If the blueprint or entity does not exist.
- **PortValidationError**: If the entity data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Update an entity
updated_entity = client.entities.update_entity(
    "service",
    "payment-service",
    {"properties": {"language": "TypeScript"}}
)
```

### delete_entity

```python
def delete_entity(
    blueprint_identifier: str,
    entity_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> bool
```

Delete an entity.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **entity_identifier** (str): The identifier of the entity to delete.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **bool**: True if the entity was deleted successfully, False otherwise.

#### Raises

- **PortResourceNotFoundError**: If the blueprint or entity does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Delete an entity
success = client.entities.delete_entity("service", "payment-service")
if success:
    print("Entity deleted successfully")
else:
    print("Failed to delete entity")
```

### bulk_create_entities

```python
def bulk_create_entities(
    blueprint_identifier: str,
    entities_data: List[Dict[str, Any]],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Create multiple entities in a single request.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **entities_data** (list): A list of dictionaries containing entity data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the results of the bulk operation.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortValidationError**: If any entity data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Create multiple entities
result = client.entities.bulk_create_entities(
    "service",
    [
        {
            "identifier": "payment-service",
            "title": "Payment Service",
            "properties": {"language": "Python"}
        },
        {
            "identifier": "auth-service",
            "title": "Authentication Service",
            "properties": {"language": "JavaScript"}
        }
    ]
)
```

### bulk_update_entities

```python
def bulk_update_entities(
    blueprint_identifier: str,
    entities_data: List[Dict[str, Any]],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update multiple entities in a single request.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **entities_data** (list): A list of dictionaries containing updated entity data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the results of the bulk operation.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortValidationError**: If any entity data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Update multiple entities
result = client.entities.bulk_update_entities(
    "service",
    [
        {
            "identifier": "payment-service",
            "properties": {"language": "TypeScript"}
        },
        {
            "identifier": "auth-service",
            "properties": {"language": "TypeScript"}
        }
    ]
)
```

### bulk_delete_entities

```python
def bulk_delete_entities(
    blueprint_identifier: str,
    entity_identifiers: List[str],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Delete multiple entities in a single request.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **entity_identifiers** (list): A list of entity identifiers to delete.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the results of the bulk operation.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Delete multiple entities
result = client.entities.bulk_delete_entities(
    "service",
    ["payment-service", "auth-service"]
)
```
