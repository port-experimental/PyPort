# Actions Service

The Actions service provides methods for managing actions in Port. Actions are self-service operations that can be performed on entities in your software catalog.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Actions service
actions_service = client.actions
```

## Methods

### get_actions

```python
def get_actions(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]
```

Retrieve all actions in the organization.

#### Parameters

- **page** (int, optional): The page number to retrieve. Default is None.
- **per_page** (int, optional): The number of items per page. Default is None.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **List[Dict[str, Any]]**: A list of action dictionaries.

#### Raises

- **PortApiError**: If the API request fails.

#### Example

```python
# Get all actions
actions = client.actions.get_actions()

# Get actions with pagination
actions_page1 = client.actions.get_actions(page=1, per_page=10)
```

### get_action

```python
def get_action(
    action_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve a specific action by its identifier.

#### Parameters

- **action_identifier** (str): The identifier of the action to retrieve.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the action details.

#### Raises

- **PortResourceNotFoundError**: If the action does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Get a specific action
deploy_action = client.actions.get_action("deploy-service")
```

### create_action

```python
def create_action(
    action_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Create a new action.

#### Parameters

- **action_data** (dict): A dictionary containing the action data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the created action.

#### Raises

- **PortValidationError**: If the action data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Create a new action
new_action = client.actions.create_action({
    "identifier": "restart-service",
    "title": "Restart Service",
    "description": "Restart a microservice",
    "trigger": {
        "type": "self-service",
        "operation": "DAY-2",
        "userInputs": {
            "properties": {
                "reason": {
                    "type": "string",
                    "title": "Restart Reason"
                }
            }
        }
    },
    "invocationMethod": {
        "type": "WEBHOOK",
        "url": "https://api.example.com/restart"
    }
})
```

### update_action

```python
def update_action(
    action_identifier: str,
    action_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update an existing action.

#### Parameters

- **action_identifier** (str): The identifier of the action to update.
- **action_data** (dict): A dictionary containing the updated action data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the updated action.

#### Raises

- **PortResourceNotFoundError**: If the action does not exist.
- **PortValidationError**: If the action data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Update an action
updated_action = client.actions.update_action(
    "restart-service",
    {"description": "Restart a microservice with logging"}
)
```

### delete_action

```python
def delete_action(
    action_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> bool
```

Delete an action.

#### Parameters

- **action_identifier** (str): The identifier of the action to delete.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **bool**: True if the action was deleted successfully, False otherwise.

#### Raises

- **PortResourceNotFoundError**: If the action does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Delete an action
success = client.actions.delete_action("restart-service")
if success:
    print("Action deleted successfully")
```

## Action Types

Actions in Port can be of different types:

- **Self-Service Actions**: Triggered manually by users
- **Automation Actions**: Triggered automatically by events
- **Day-2 Operations**: Ongoing operational tasks
- **CREATE**: Entity creation actions
- **DELETE**: Entity deletion actions

## Invocation Methods

Actions can use different invocation methods:

- **WEBHOOK**: HTTP webhook calls
- **KAFKA**: Kafka message publishing
- **AZURE_DEVOPS**: Azure DevOps pipeline triggers
- **GITLAB**: GitLab pipeline triggers
- **GITHUB**: GitHub workflow triggers

## Error Handling

All action methods can raise exceptions for various error conditions. See the [Error Handling](../error_handling.md) documentation for more details.
