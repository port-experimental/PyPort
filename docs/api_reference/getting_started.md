# Getting Started with PyPort

This guide will help you get started with the PyPort client library for the Port IDP REST API.

## Installation

Install PyPort using pip:

```bash
pip install pyport
```

## Authentication

To use the PyPort client, you'll need a client ID and client secret from Port. You can obtain these from the Port dashboard.

```python
from pyport import PortClient

# Initialize the client
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)
```

The client will automatically handle authentication and token refresh.

## Basic Operations

### Working with Blueprints

Blueprints define the structure of entities in Port.

```python
# Get all blueprints
blueprints = client.blueprints.get_blueprints()

# Get a specific blueprint
service_blueprint = client.blueprints.get_blueprint("service")

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

# Update a blueprint
updated_blueprint = client.blueprints.update_blueprint(
    "microservice",
    {"title": "Cloud Microservice"}
)

# Delete a blueprint
success = client.blueprints.delete_blueprint("microservice")
```

### Working with Entities

Entities are instances of blueprints that represent real-world resources.

```python
# Get all entities of a blueprint
services = client.entities.get_entities("service")

# Get a specific entity
api_service = client.entities.get_entity("service", "api-service")

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

# Update an entity
updated_entity = client.entities.update_entity(
    "service",
    "payment-service",
    {"properties": {"language": "TypeScript"}}
)

# Delete an entity
success = client.entities.delete_entity("service", "payment-service")
```

### Working with Actions

Actions define operations that can be performed on entities.

```python
# Get all actions
actions = client.actions.get_actions()

# Get a specific action
deploy_action = client.actions.get_action("deploy")

# Create a new action
new_action = client.actions.create_action({
    "identifier": "restart",
    "title": "Restart Service",
    "blueprint": "service",
    "trigger": "manual",
    "requiredApproval": False
})

# Update an action
updated_action = client.actions.update_action(
    "restart",
    {"title": "Restart Service (Production)"}
)

# Delete an action
success = client.actions.delete_action("restart")
```

## Error Handling

PyPort provides custom exceptions for different error types:

```python
from pyport import PortClient
from pyport.exceptions import (
    PortApiError,
    PortAuthError,
    PortResourceNotFoundError,
    PortValidationError,
    PortServerError,
    PortNetworkError,
    PortTimeoutError
)

try:
    client = PortClient(
        client_id="your-client-id",
        client_secret="your-client-secret"
    )
    
    # This will raise PortResourceNotFoundError if the blueprint doesn't exist
    blueprint = client.blueprints.get_blueprint("non-existent-blueprint")
    
except PortResourceNotFoundError as e:
    print(f"Blueprint not found: {e}")
    
except PortValidationError as e:
    print(f"Validation error: {e}")
    
except PortAuthError as e:
    print(f"Authentication error: {e}")
    
except PortApiError as e:
    print(f"API error: {e}")
```

## Logging

PyPort includes built-in logging that can be configured when initializing the client:

```python
import logging
from pyport import PortClient

# Initialize the client with custom logging
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    log_level=logging.DEBUG,
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## Next Steps

- Explore the [Client](client.md) documentation for more details on client configuration
- Check out the [Services](services/README.md) documentation for all available API services
- Learn about [Error Handling](error_handling.md) for more advanced error handling techniques
- Discover [Utilities](utilities.md) for helper functions and tools
