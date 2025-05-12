# Blueprints Service

The Blueprints service provides methods for managing blueprint definitions in Port. Blueprints define the structure of entities in your software catalog.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Blueprints service
blueprints_service = client.blueprints
```

## Methods

### get_blueprints

```python
def get_blueprints(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]
```

Retrieve all blueprints.

#### Parameters

- **page** (int, optional): The page number to retrieve. Default is None.
- **per_page** (int, optional): The number of items per page. Default is None.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **List[Dict[str, Any]]**: A list of blueprint dictionaries.

#### Raises

- **PortApiError**: If the API request fails.

#### Example

```python
# Get all blueprints
blueprints = client.blueprints.get_blueprints()

# Get blueprints with pagination
blueprints_page1 = client.blueprints.get_blueprints(page=1, per_page=10)

# Get blueprints with additional query parameters
filtered_blueprints = client.blueprints.get_blueprints(
    params={"filter": "value"}
)
```

### get_blueprint

```python
def get_blueprint(
    blueprint_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve a specific blueprint by its identifier.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint to retrieve.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the blueprint details.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Get a specific blueprint
service_blueprint = client.blueprints.get_blueprint("service")

# Get a blueprint with additional query parameters
service_blueprint = client.blueprints.get_blueprint(
    "service",
    params={"include": "properties"}
)
```

### create_blueprint

```python
def create_blueprint(
    blueprint_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Create a new blueprint.

#### Parameters

- **blueprint_data** (dict): A dictionary containing the blueprint data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the created blueprint.

#### Raises

- **PortValidationError**: If the blueprint data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Create a new blueprint
new_blueprint = client.blueprints.create_blueprint({
    "identifier": "microservice",
    "title": "Microservice",
    "properties": {
        "language": {
            "type": "string",
            "title": "Language",
            "enum": ["Python", "JavaScript", "Java", "Go"]
        }
    }
})
```

### update_blueprint

```python
def update_blueprint(
    blueprint_identifier: str,
    blueprint_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update an existing blueprint.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint to update.
- **blueprint_data** (dict): A dictionary containing the updated blueprint data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the updated blueprint.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortValidationError**: If the blueprint data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Update a blueprint
updated_blueprint = client.blueprints.update_blueprint(
    "microservice",
    {"title": "Cloud Microservice"}
)
```

### delete_blueprint

```python
def delete_blueprint(
    blueprint_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> bool
```

Delete a blueprint.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint to delete.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **bool**: True if the blueprint was deleted successfully, False otherwise.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Delete a blueprint
success = client.blueprints.delete_blueprint("microservice")
if success:
    print("Blueprint deleted successfully")
else:
    print("Failed to delete blueprint")
```

### get_blueprint_permissions

```python
def get_blueprint_permissions(
    blueprint_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve the permissions for a specific blueprint.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the blueprint permissions.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Get blueprint permissions
permissions = client.blueprints.get_blueprint_permissions("service")
```

### update_blueprint_permissions

```python
def update_blueprint_permissions(
    blueprint_identifier: str,
    permissions_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update the permissions for a specific blueprint.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **permissions_data** (dict): A dictionary containing the updated permissions data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the updated blueprint permissions.

#### Raises

- **PortResourceNotFoundError**: If the blueprint does not exist.
- **PortValidationError**: If the permissions data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Update blueprint permissions
updated_permissions = client.blueprints.update_blueprint_permissions(
    "service",
    {
        "teams": [
            {
                "identifier": "devops",
                "permissions": ["read", "write"]
            }
        ]
    }
)
```
