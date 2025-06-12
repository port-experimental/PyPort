# Webhooks Service

The Webhooks service provides methods for managing webhooks in Port. Webhooks allow you to receive real-time notifications when events occur in your Port organization.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Webhooks service
webhooks_service = client.webhooks
```

## Methods

### get_webhooks

```python
def get_webhooks(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve all webhooks in the organization.

#### Parameters

- **page** (int, optional): The page number to retrieve. Default is None.
- **per_page** (int, optional): The number of items per page. Default is None.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing webhooks data.

#### Raises

- **PortApiError**: If the API request fails.

#### Example

```python
# Get all webhooks
webhooks = client.webhooks.get_webhooks()
for webhook in webhooks.get("webhooks", []):
    print(f"Webhook: {webhook['identifier']} - URL: {webhook['url']}")

# Get webhooks with pagination
webhooks_page1 = client.webhooks.get_webhooks(page=1, per_page=10)
```

### get_webhook

```python
def get_webhook(
    webhook_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve a specific webhook by its identifier.

#### Parameters

- **webhook_identifier** (str): The identifier of the webhook to retrieve.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the webhook details.

#### Raises

- **PortResourceNotFoundError**: If the webhook does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Get a specific webhook
webhook = client.webhooks.get_webhook("entity-created-webhook")
print(f"Webhook URL: {webhook['webhook']['url']}")
print(f"Events: {webhook['webhook']['events']}")
```

### create_webhook

```python
def create_webhook(
    webhook_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Create a new webhook.

#### Parameters

- **webhook_data** (dict): A dictionary containing the webhook data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the created webhook.

#### Raises

- **PortValidationError**: If the webhook data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Create a new webhook
new_webhook = client.webhooks.create_webhook({
    "identifier": "entity-updated-webhook",
    "title": "Entity Updated Notifications",
    "description": "Webhook for entity update events",
    "url": "https://api.example.com/webhooks/port",
    "events": ["entity.created", "entity.updated"],
    "headers": {
        "Authorization": "Bearer your-api-token",
        "Content-Type": "application/json"
    },
    "security": {
        "secret": "your-webhook-secret"
    }
})
```

### update_webhook

```python
def update_webhook(
    webhook_identifier: str,
    webhook_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update an existing webhook.

#### Parameters

- **webhook_identifier** (str): The identifier of the webhook to update.
- **webhook_data** (dict): A dictionary containing the updated webhook data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the updated webhook.

#### Raises

- **PortResourceNotFoundError**: If the webhook does not exist.
- **PortValidationError**: If the webhook data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Update a webhook
updated_webhook = client.webhooks.update_webhook(
    "entity-updated-webhook",
    {
        "url": "https://api.example.com/webhooks/port/v2",
        "events": ["entity.created", "entity.updated", "entity.deleted"]
    }
)
```

### delete_webhook

```python
def delete_webhook(
    webhook_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> bool
```

Delete a webhook.

#### Parameters

- **webhook_identifier** (str): The identifier of the webhook to delete.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **bool**: True if the webhook was deleted successfully, False otherwise.

#### Raises

- **PortResourceNotFoundError**: If the webhook does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Delete a webhook
success = client.webhooks.delete_webhook("entity-updated-webhook")
if success:
    print("Webhook deleted successfully")
```

## Webhook Structure

Webhooks in Port have the following structure:

```python
{
    "identifier": "entity-created-webhook",
    "title": "Entity Created Notifications",
    "description": "Webhook for new entity events",
    "url": "https://api.example.com/webhooks/port",
    "events": ["entity.created"],
    "headers": {
        "Authorization": "Bearer token",
        "Content-Type": "application/json"
    },
    "security": {
        "secret": "webhook-secret"
    },
    "enabled": true,
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-20T14:45:00Z"
}
```

## Webhook Events

Port supports various webhook events:

### Entity Events
- **entity.created**: When an entity is created
- **entity.updated**: When an entity is updated
- **entity.deleted**: When an entity is deleted

### Action Events
- **action.created**: When an action is created
- **action.updated**: When an action is updated
- **action.deleted**: When an action is deleted

### Action Run Events
- **run.created**: When an action run is created
- **run.updated**: When an action run status changes
- **run.completed**: When an action run completes

### Blueprint Events
- **blueprint.created**: When a blueprint is created
- **blueprint.updated**: When a blueprint is updated
- **blueprint.deleted**: When a blueprint is deleted

## Webhook Security

### Secret Verification
Port signs webhook payloads with a secret:

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected_signature}", signature)
```

### Headers
Include authentication headers for your webhook endpoint:

```python
webhook_headers = {
    "Authorization": "Bearer your-api-token",
    "X-API-Key": "your-api-key",
    "Content-Type": "application/json"
}
```

## Webhook Payload

Webhook payloads contain event information:

```json
{
    "event": "entity.created",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "entity": {
            "identifier": "payment-service",
            "title": "Payment Service",
            "blueprint": "service",
            "properties": {
                "language": "Python"
            }
        }
    },
    "organization": "your-org-id",
    "source": "port"
}
```

## Error Handling

Webhook operations can fail for various reasons:

- **Invalid URL**: Webhook URL is not reachable
- **Authentication errors**: Invalid headers or secrets
- **Event validation**: Invalid event types specified
- **Rate limiting**: Too many webhook requests

See the [Error Handling](../error_handling.md) documentation for more details.
