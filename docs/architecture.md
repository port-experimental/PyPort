# PyPort Architecture

This document provides an overview of the PyPort library architecture for contributors. It explains the design principles, code organization, and key components of the library.

> **Note**: For visual representations of the architecture, see the [Architecture Diagrams](architecture/architecture.md).

## Design Principles

PyPort is designed with the following principles in mind:

1. **Simplicity**: The API should be simple and intuitive to use.
2. **Consistency**: All parts of the API should follow consistent patterns.
3. **Robustness**: The library should handle errors gracefully and provide helpful error messages.
4. **Extensibility**: The library should be easy to extend with new features.
5. **Type Safety**: The library should provide comprehensive type annotations for better IDE support and type checking.

## Code Organization

The PyPort library is organized into the following main components:

```
pyport/
├── client/                 # Client module
│   ├── client.py           # Main client class
│   ├── auth.py             # Authentication manager
│   └── request.py          # Request manager
├── services/               # Base service classes
│   └── base_api_service.py # Base class for all API services
├── [service_modules]/      # Individual API service modules
│   ├── [service]_api_svc.py # API service implementation
│   └── types.py            # Service-specific types
├── models/                 # Data models
│   └── api_category.py     # Base resource model
├── types/                  # Type definitions
│   ├── api_responses.py    # API response types
│   └── api_parameters.py   # API parameter types
├── utils/                  # Utility functions
│   └── ...
├── exceptions.py           # Exception classes
├── error_handling.py       # Error handling utilities
├── logging.py              # Logging utilities
├── retry.py                # Retry logic
└── constants.py            # Constants
```

## Key Components

### Client

The `PortClient` class is the main entry point for the library. It provides access to all API services and handles authentication, request management, and error handling.

```python
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)
```

The client is composed of several components:

- **AuthManager**: Handles authentication and token management.
- **RequestManager**: Manages HTTP requests and responses.
- **API Services**: Individual service classes for different parts of the API.

### API Services

Each API service is implemented as a separate class that inherits from `BaseAPIService`. This provides a consistent interface and behavior across all services.

```python
class Blueprints(BaseAPIService):
    def __init__(self, client):
        super().__init__(client, resource_name="blueprints")

    def get_blueprints(self, page=None, per_page=None, params=None):
        # Implementation
```

The `BaseAPIService` class provides common functionality for all API services, such as:

- Building endpoints
- Handling pagination
- Extracting data from responses
- Making requests with parameters

### Error Handling

PyPort provides a comprehensive error handling system with a hierarchy of exception classes:

```
PortApiError
├── PortAuthError
├── PortResourceNotFoundError
├── PortValidationError
├── PortServerError
├── PortNetworkError
└── PortTimeoutError
```

The `error_handling.py` module contains utilities for handling errors from the API and converting them to appropriate exception types.

### Retry Logic

PyPort includes built-in retry logic for transient errors. The `retry.py` module implements various retry strategies:

- Exponential backoff
- Fixed delay
- Linear backoff

The retry logic also includes a circuit breaker pattern to prevent repeated requests to a failing API.

### Logging

PyPort includes a logging system that provides detailed information about API requests, responses, and errors. The `logging.py` module configures the logging system and provides utilities for logging.

### Type System

PyPort uses a comprehensive type system to provide better IDE support and type checking. The `types/` directory contains type definitions for API responses and parameters.

Type stubs (.pyi files) provide additional type information to IDEs without affecting runtime behavior.

## Request Flow

When you make a request using PyPort, the following sequence of events occurs:

1. **Client Method Call**: You call a method on a service object (e.g., `client.blueprints.get_blueprint("service")`).
2. **Service Method**: The service method builds the endpoint and prepares the request parameters.
3. **BaseAPIService**: The base service class handles common functionality like pagination and parameter handling.
4. **Client Request**: The service calls the client's `make_request` method.
5. **Authentication**: The client ensures a valid authentication token is available.
6. **Request Execution**: The client sends the HTTP request to the API.
7. **Retry Logic**: If the request fails with a transient error, the client retries the request according to the retry configuration.
8. **Error Handling**: If the request fails with a non-transient error, the client converts the error to an appropriate exception.
9. **Response Processing**: If the request succeeds, the client processes the response and returns the data.

## Adding a New Feature

To add a new feature to PyPort, follow these steps:

1. **Identify the Service**: Determine which service the feature belongs to, or create a new service if needed.
2. **Update the Service Class**: Add a new method to the service class that implements the feature.
3. **Add Type Annotations**: Add type annotations to the method parameters and return value.
4. **Add Documentation**: Add docstrings to the method that explain its purpose, parameters, return value, and possible exceptions.
5. **Add Tests**: Add tests for the new feature to ensure it works correctly.
6. **Update Documentation**: Update the API reference documentation to include the new feature.

### Example: Adding a New Method to the Blueprints Service

```python
def get_blueprint_schema(
    self,
    blueprint_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get the JSON schema for a specific blueprint.

    Args:
        blueprint_identifier: The identifier of the blueprint.
        params: Additional query parameters for the request.

    Returns:
        A dictionary containing the blueprint schema.

    Raises:
        PortResourceNotFoundError: If the blueprint does not exist.
        PortApiError: If the API request fails for another reason.
    """
    endpoint = self._build_endpoint(
        self._resource_name, blueprint_identifier, "schema"
    )
    response = self._make_request_with_params("GET", endpoint, params=params)
    return self._extract_response_data(response)
```

## Contributing Guidelines

When contributing to PyPort, please follow these guidelines:

1. **Code Style**: Follow the PEP 8 style guide for Python code.
2. **Type Annotations**: Add type annotations to all function parameters and return values.
3. **Documentation**: Add docstrings to all classes and methods.
4. **Tests**: Add tests for all new features and bug fixes.
5. **Error Handling**: Handle errors gracefully and provide helpful error messages.
6. **Backwards Compatibility**: Maintain backwards compatibility with existing code.

## Testing

PyPort uses the `unittest` framework for testing. Tests are organized in the `tests/` directory, with a separate test file for each module.

To run the tests, use the following command:

```bash
python -m unittest discover
```

## Continuous Integration

PyPort uses GitHub Actions for continuous integration. The CI workflow runs tests, linting, and type checking on every pull request and push to the main branch.

## Release Process

To release a new version of PyPort, follow these steps:

1. **Update Version**: Update the version number in `version.txt`.
2. **Update Changelog**: Update the changelog with the changes in the new version.
3. **Run Tests**: Run the tests to ensure everything is working correctly.
4. **Build Package**: Build the package using `python setup.py sdist bdist_wheel`.
5. **Upload to PyPI**: Upload the package to PyPI using `twine upload dist/*`.
6. **Create Release**: Create a new release on GitHub with release notes.

## Conclusion

This document provides an overview of the PyPort library architecture for contributors. It explains the design principles, code organization, and key components of the library.

For more detailed information, refer to the API reference documentation and the source code.
