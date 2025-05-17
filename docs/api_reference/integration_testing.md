# Integration Testing with PyPort

This guide explains how to perform integration testing with the PyPort client library using real credentials.

## Overview

Integration testing with PyPort allows you to verify that your code works correctly with the actual Port API. This is important for ensuring that your application will function properly in production.

## Setting Up Integration Tests

### Environment Variables

PyPort integration tests use environment variables to store API credentials. This approach keeps sensitive information out of your code and allows for easy configuration across different environments.

Create a `.env` file with your Port API credentials:

```
PORT_CLIENT_ID = 'your-client-id'
PORT_CLIENT_SECRET = 'your-client-secret'
```

### Simple Integration Test Client

PyPort includes a simple integration test client that you can use as a starting point for your own tests. This client:

1. Loads environment variables from a `.env` file
2. Initializes the PyPort client with the credentials
3. Tests the connection by fetching blueprints
4. Reports the PyPort version being used

Here's the basic structure of the integration test client:

```python
import os
import subprocess
import sys
from dotenv import load_dotenv
from pyport import PortClient

# Load environment variables from .env file
load_dotenv()

# Access environment variables
PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

# Initialize the client with credentials
port_client = PortClient(client_id=PORT_CLIENT_ID, client_secret=PORT_CLIENT_SECRET, us_region=True)

# Test API connection by fetching blueprints
blueprints = port_client.blueprints.get_blueprints()

print(f"Successfully fetched {len(blueprints)} blueprints")
```

## Testing with Specific Versions

You can test your code with specific versions of PyPort to ensure compatibility across different releases. The integration test client can be modified to install and use a specific version:

```python
import os
import subprocess
import sys
from dotenv import load_dotenv

# Set default version to test
VERSION = "0.2.7"

# Get version from command line argument if provided
if len(sys.argv) > 1:
    VERSION = sys.argv[1]

print(f"Testing PyPort version: {VERSION}")

# Install the specified version
print(f"Installing PyPort version {VERSION}...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", f"pyport=={VERSION}"],
    check=True
)

# Now import the client after installing the specified version
from pyport import PortClient

# Load environment variables from .env file
load_dotenv()

# Access environment variables
PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

# Initialize the client with credentials
port_client = PortClient(client_id=PORT_CLIENT_ID, client_secret=PORT_CLIENT_SECRET, us_region=True)

# Test API connection by fetching blueprints
blueprints = port_client.blueprints.get_blueprints()

# Get installed version using pip
result = subprocess.run(
    [sys.executable, "-m", "pip", "show", "pyport"],
    capture_output=True,
    text=True,
    check=True
)

# Extract version from pip show output
for line in result.stdout.split('\n'):
    if line.startswith('Version:'):
        installed_version = line.split(':', 1)[1].strip()
        break
else:
    installed_version = "unknown"

print(f"Using PyPort version: {installed_version}")
print(f"Successfully fetched {len(blueprints)} blueprints")
```

To use this script:

```bash
# Test with default version (0.2.7)
python simple_pyport_client.py

# Test with a specific version
python simple_pyport_client.py 0.2.6
```

## Best Practices for Integration Testing

1. **Use a dedicated test environment**: If possible, use a separate Port environment for testing to avoid affecting production data.

2. **Clean up after tests**: Delete any test data created during integration tests to keep your environment clean.

3. **Handle rate limiting**: Be aware of API rate limits and implement appropriate retry logic in your tests.

4. **Test error scenarios**: Test how your code handles API errors by intentionally causing them (e.g., using invalid credentials).

5. **Isolate tests**: Make sure each test is independent and doesn't rely on the state created by other tests.

## Example Integration Test

Here's a complete example of an integration test that creates a blueprint, adds an entity, and then cleans up:

```python
import os
import uuid
from dotenv import load_dotenv
from pyport import PortClient
from pyport.exceptions import PortApiError

# Load environment variables
load_dotenv()

# Access environment variables
PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

# Generate a unique identifier for this test run
test_id = uuid.uuid4().hex[:8]
blueprint_id = f"test-blueprint-{test_id}"
entity_id = f"test-entity-{test_id}"

# Initialize the client
client = PortClient(client_id=PORT_CLIENT_ID, client_secret=PORT_CLIENT_SECRET, us_region=True)

try:
    # Create a test blueprint
    blueprint = client.blueprints.create_blueprint({
        "identifier": blueprint_id,
        "title": "Test Blueprint",
        "schema": {
            "properties": {
                "test_property": {
                    "type": "string",
                    "title": "Test Property"
                }
            }
        }
    })
    print(f"Created blueprint: {blueprint_id}")
    
    # Create a test entity
    entity = client.entities.create_entity(
        blueprint_id,
        {
            "identifier": entity_id,
            "title": "Test Entity",
            "properties": {
                "test_property": "test value"
            }
        }
    )
    print(f"Created entity: {entity_id}")
    
    # Verify the entity was created correctly
    fetched_entity = client.entities.get_entity(blueprint_id, entity_id)
    assert fetched_entity["identifier"] == entity_id
    assert fetched_entity["properties"]["test_property"] == "test value"
    print("Entity verification successful")
    
finally:
    # Clean up: Delete the entity and blueprint
    try:
        client.entities.delete_entity(blueprint_id, entity_id)
        print(f"Deleted entity: {entity_id}")
    except PortApiError:
        print(f"Failed to delete entity: {entity_id}")
    
    try:
        client.blueprints.delete_blueprint(blueprint_id)
        print(f"Deleted blueprint: {blueprint_id}")
    except PortApiError:
        print(f"Failed to delete blueprint: {blueprint_id}")
```

This test creates a unique blueprint and entity for each run, verifies that the entity was created correctly, and then cleans up by deleting both the entity and blueprint, even if the test fails.
