# Integrations Service

The Integrations service provides methods for managing integrations in Port. Integrations connect external systems to Port, allowing data synchronization and automation.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Integrations service
integrations_service = client.integrations
```

## Methods

### get_integrations

```python
def get_integrations(
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve all integrations in the organization.

#### Parameters

- **params** (dict, optional): Additional query parameters for the request.

#### Returns

- **Dict[str, Any]**: A dictionary containing the integrations list.

#### Example

```python
# Get all integrations
integrations = client.integrations.get_integrations()
for integration in integrations.get("integrations", []):
    print(f"Integration: {integration['title']}")
```

### get_integration

```python
def get_integration(
    integration_id: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve a specific integration by its ID.

#### Parameters

- **integration_id** (str): The ID of the integration to retrieve.
- **params** (dict, optional): Additional query parameters.

#### Returns

- **Dict[str, Any]**: A dictionary containing the integration details.

#### Raises

- **PortResourceNotFoundError**: If the integration does not exist.
- **PortApiError**: If the API request fails.

#### Example

```python
# Get a specific integration
integration = client.integrations.get_integration("github_integration_123")
print(f"Status: {integration['integration']['status']}")
```

### update_integration

```python
def update_integration(
    integration_id: str,
    integration_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update an existing integration.

#### Parameters

- **integration_id** (str): The ID of the integration to update.
- **integration_data** (dict): The updated integration data.
- **params** (dict, optional): Additional query parameters.

#### Returns

- **Dict[str, Any]**: The updated integration.

#### Raises

- **PortResourceNotFoundError**: If the integration does not exist.
- **PortValidationError**: If the integration data is invalid.
- **PortApiError**: If the API request fails.

#### Example

```python
# Update integration configuration
updated_integration = client.integrations.update_integration(
    "github_integration_123",
    {
        "config": {
            "token": "new_github_token",
            "repositories": ["repo1", "repo2"]
        }
    }
)
```

### update_integration_config

```python
def update_integration_config(
    integration_id: str,
    config_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update the configuration of an integration.

#### Parameters

- **integration_id** (str): The ID of the integration.
- **config_data** (dict): The new configuration data.
- **params** (dict, optional): Additional query parameters.

#### Returns

- **Dict[str, Any]**: The updated integration configuration.

#### Example

```python
# Update only the configuration
config_result = client.integrations.update_integration_config(
    "github_integration_123",
    {
        "token": "updated_token",
        "webhook_secret": "new_secret"
    }
)
```

### resync_integration

```python
def resync_integration(
    integration_id: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Trigger a resync for an integration.

#### Parameters

- **integration_id** (str): The ID of the integration to resync.
- **params** (dict, optional): Additional query parameters.

#### Returns

- **Dict[str, Any]**: The resync operation result.

#### Example

```python
# Trigger integration resync
resync_result = client.integrations.resync_integration("github_integration_123")
print(f"Resync status: {resync_result['status']}")
```

## Integration Types

Port supports various integration types:

- **GitHub**: Repository and workflow integration
- **GitLab**: Project and pipeline integration
- **Kubernetes**: Cluster and resource integration
- **AWS**: Cloud resource integration
- **Azure DevOps**: Project and pipeline integration
- **Jira**: Issue and project integration
- **PagerDuty**: Incident management integration
- **Datadog**: Monitoring and metrics integration
- **Custom**: Webhook-based custom integrations

## Integration Status

Integrations can have the following statuses:

- **ACTIVE**: Integration is running and syncing data
- **INACTIVE**: Integration is disabled
- **ERROR**: Integration has encountered an error
- **SYNCING**: Integration is currently syncing data
- **PENDING**: Integration is being set up

## Configuration Management

Each integration type has specific configuration requirements:

### GitHub Integration
```python
github_config = {
    "token": "github_personal_access_token",
    "app_host": "https://github.com",
    "repositories": ["owner/repo1", "owner/repo2"],
    "webhook_secret": "optional_webhook_secret"
}
```

### Kubernetes Integration
```python
k8s_config = {
    "kubeconfig": "base64_encoded_kubeconfig",
    "cluster_name": "production-cluster",
    "namespaces": ["default", "production"]
}
```

## Error Handling

Integration operations can fail for various reasons:

- **Authentication errors**: Invalid tokens or credentials
- **Network errors**: Connection timeouts or unreachable endpoints
- **Configuration errors**: Invalid or missing configuration parameters
- **Rate limiting**: API rate limits exceeded

See the [Error Handling](../error_handling.md) documentation for more details.
