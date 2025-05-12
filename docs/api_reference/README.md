# PyPort API Reference

This directory contains comprehensive documentation for the PyPort API client library.

## Table of Contents

- [Getting Started](getting_started.md)
- [Client](client.md)
- [Services](services/README.md)
- [Error Handling](error_handling.md)
- [Utilities](utilities.md)
- [Type System](types.md)

## Overview

PyPort is a Python client library for the Port IDP REST API. It provides a clean, Pythonic interface for interacting with the API, handling authentication, error handling, and logging automatically.

The library is organized into several modules:

- **Client**: The main entry point for the library, providing access to all API services
- **Services**: Individual API services for different parts of the Port API
- **Error Handling**: Custom exceptions and error handling mechanisms
- **Utilities**: Helper functions for common operations
- **Type System**: Type definitions for API responses and parameters

## Usage Example

```python
from pyport import PortClient

# Initialize the client
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Get all blueprints
blueprints = client.blueprints.get_blueprints()

# Get a specific entity
entity = client.entities.get_entity("service", "my-service")

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

For more detailed examples, see the [Getting Started](getting_started.md) guide.
