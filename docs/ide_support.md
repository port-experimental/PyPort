# IDE Support in PyPort

PyPort v0.2.6 introduces significant improvements to IDE support, making it easier to discover and use the library's features in your favorite development environment.

## Enhanced Type Hints

All PyPort classes and methods now include comprehensive type hints that enable your IDE to provide accurate autocompletion and type checking. This helps prevent errors and makes it easier to explore the API.

### Client Properties

The `PortClient` class now exposes all service classes as properties with explicit return types:

```python
from pyport import PortClient

client = PortClient(client_id="your-client-id", client_secret="your-client-secret")

# Your IDE will now show all available methods on the blueprints service
client.blueprints.get_blueprint("service")
```

### Method Parameters and Return Types

All methods include detailed type annotations for parameters and return values:

```python
def get_blueprint(self, blueprint_identifier: str) -> Blueprint:
    """
    Get a specific blueprint by its identifier.
    
    Args:
        blueprint_identifier: The unique identifier of the blueprint to retrieve.
        
    Returns:
        A dictionary containing the blueprint details.
        
    Raises:
        PortResourceNotFoundError: If the blueprint does not exist.
        PortApiError: If another API error occurs.
    """
```

## Comprehensive Docstrings

Every class and method includes detailed docstrings that appear in your IDE's tooltips and documentation panels:

- **Class docstrings** explain the purpose of the class and provide usage examples
- **Method docstrings** describe parameters, return values, and possible exceptions
- **Property docstrings** explain what each property represents and how to use it

## Type Stub Files

PyPort includes type stub files (.pyi) that provide additional type information to IDEs without affecting runtime behavior. These files help your IDE understand the structure of the library even better.

## IDE-Specific Features

### PyCharm

In PyCharm, you'll notice:
- Parameter info when calling methods
- Autocompletion for properties and methods
- Documentation in quick-info tooltips
- Type checking in the editor

### Visual Studio Code

In VS Code with the Python extension, you'll see:
- IntelliSense suggestions for properties and methods
- Hover information with full documentation
- Parameter hints when calling methods
- Type checking with Pylance

### Other IDEs

Any IDE that supports Python type hints (including Jupyter notebooks) will benefit from these improvements.

## Example: Exploring the API

The improved IDE support makes it much easier to explore the PyPort API:

1. Type `client.` and see a list of all available services
2. Select a service (e.g., `client.blueprints`) and see all available methods
3. Start typing a method name to get autocompletion
4. View parameter information when calling a method
5. See return type information to understand what data to expect

This makes the library more accessible, especially for new users who are still learning the API.
