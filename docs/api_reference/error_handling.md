# Error Handling

PyPort provides a comprehensive error handling system that makes it easy to handle different types of errors that can occur when interacting with the Port API.

## Exception Hierarchy

PyPort defines a hierarchy of exception classes for different error types:

- **PortApiError**: Base class for all API-related errors
  - **PortAuthError**: Authentication errors (401 Unauthorized)
  - **PortResourceNotFoundError**: Resource not found errors (404 Not Found)
  - **PortValidationError**: Validation errors (400 Bad Request)
  - **PortServerError**: Server errors (500 Internal Server Error)
  - **PortNetworkError**: Network-related errors
  - **PortTimeoutError**: Request timeout errors

## Basic Error Handling

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

## Error Information

All PyPort exceptions provide detailed information about the error:

```python
try:
    client.blueprints.get_blueprint("non-existent-blueprint")
except PortApiError as e:
    print(f"Error type: {e.error_type}")
    print(f"Error message: {e.message}")
    print(f"Status code: {e.status_code}")
    print(f"Endpoint: {e.endpoint}")
    print(f"Method: {e.method}")
    print(f"Correlation ID: {e.correlation_id}")
```

## Retry Logic

PyPort includes built-in retry logic for transient errors. You can configure the retry behavior when initializing the client:

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    max_retries=5,
    retry_delay=0.5,
    max_delay=60.0,
    retry_strategy="exponential",
    retry_jitter=True
)
```

You can also specify retry parameters for individual requests:

```python
response = client.make_request(
    "GET",
    "blueprints",
    retries=3,
    retry_delay=1.0
)
```

## Circuit Breaker

PyPort includes a circuit breaker pattern to prevent repeated requests to a failing API. The circuit breaker will open after a certain number of consecutive failures, preventing further requests for a period of time.

The circuit breaker is automatically enabled and configured based on the retry settings.

## Logging

PyPort logs detailed information about errors, which can be useful for debugging:

```python
import logging
from pyport import PortClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    log_level=logging.DEBUG
)

try:
    client.blueprints.get_blueprint("non-existent-blueprint")
except PortApiError:
    pass  # Error is already logged
```

## Custom Error Handling

You can define custom error handling logic for specific error types:

```python
from pyport import PortClient
from pyport.exceptions import PortResourceNotFoundError

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

def get_blueprint_or_create(blueprint_id, blueprint_data):
    try:
        return client.blueprints.get_blueprint(blueprint_id)
    except PortResourceNotFoundError:
        print(f"Blueprint {blueprint_id} not found, creating it...")
        return client.blueprints.create_blueprint(blueprint_data)

# Use the custom error handling function
blueprint = get_blueprint_or_create(
    "microservice",
    {
        "identifier": "microservice",
        "title": "Microservice",
        "properties": {
            "language": {
                "type": "string",
                "title": "Language",
                "enum": ["Python", "JavaScript", "Java", "Go"]
            }
        }
    }
)
```
