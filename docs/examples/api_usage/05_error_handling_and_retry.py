#!/usr/bin/env python3
"""
Error Handling and Retry Configuration Example for PyPort

This example demonstrates how to handle errors and configure retry behavior
when using the PyPort library.
"""

import os
import sys
import json
import uuid
import time
from typing import Dict, Any, Set

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from pyport import PortClient
from pyport.exceptions import PortApiError
from pyport.retry import RetryConfig, RetryStrategy


def print_json(data: Dict[str, Any]) -> None:
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))


def main():
    """Main function demonstrating error handling and retry configuration."""
    # Get API credentials from environment variables
    client_id = os.environ.get('PORT_CLIENT_ID')
    client_secret = os.environ.get('PORT_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("Error: PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables must be set.")
        print("Please set these variables and try again:")
        print("  export PORT_CLIENT_ID=your-client-id")
        print("  export PORT_CLIENT_SECRET=your-client-secret")
        sys.exit(1)

    # 1. Basic error handling
    print("\n1. Basic error handling example...")
    
    # Initialize the client
    client = PortClient(
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Try to get a non-existent blueprint
    print("\nTrying to get a non-existent blueprint...")
    try:
        non_existent_id = f"non-existent-{uuid.uuid4().hex}"
        blueprint = client.blueprints.get_blueprint(non_existent_id)
        print("✅ Blueprint retrieved successfully (this should not happen)!")
    except PortApiError as e:
        print(f"✅ Caught expected error: {e}")
        print(f"  Status code: {e.status_code}")
        print(f"  Endpoint: {e.endpoint}")
        print(f"  Method: {e.method}")

    # 2. Custom retry configuration
    print("\n2. Custom retry configuration example...")
    
    # Initialize a client with custom retry configuration
    custom_retry_client = PortClient(
        client_id=client_id,
        client_secret=client_secret,
        max_retries=5,                      # Maximum number of retry attempts
        retry_delay=0.5,                    # Initial delay between retries (in seconds)
        max_delay=10.0,                     # Maximum delay between retries (in seconds)
        retry_strategy=RetryStrategy.EXPONENTIAL,  # Use exponential backoff
        retry_jitter=True,                  # Add jitter to retry delays
        retry_status_codes={429, 500, 502, 503, 504},  # Status codes to retry on
        retry_on={ConnectionError, TimeoutError}  # Exceptions to retry on
    )
    
    print("✅ Client with custom retry configuration initialized!")
    print("\nRetry configuration details:")
    print(f"  Max retries: 5")
    print(f"  Initial delay: 0.5 seconds")
    print(f"  Maximum delay: 10.0 seconds")
    print(f"  Retry strategy: Exponential backoff")
    print(f"  Jitter: Enabled")
    print(f"  Status codes to retry on: 429, 500, 502, 503, 504")
    print(f"  Exceptions to retry on: ConnectionError, TimeoutError")

    # 3. Creating a retry configuration object
    print("\n3. Creating a RetryConfig object...")
    
    retry_config = RetryConfig(
        max_retries=3,
        retry_delay=1.0,
        max_delay=5.0,
        retry_strategy=RetryStrategy.LINEAR,
        retry_jitter=False,
        retry_status_codes={429, 503},
        retry_on={ConnectionError}
    )
    
    print("✅ RetryConfig object created!")
    print("\nRetryConfig details:")
    print(f"  Max retries: {retry_config.max_retries}")
    print(f"  Initial delay: {retry_config.retry_delay} seconds")
    print(f"  Maximum delay: {retry_config.max_delay} seconds")
    print(f"  Retry strategy: {retry_config.retry_strategy}")
    print(f"  Jitter: {'Enabled' if retry_config.retry_jitter else 'Disabled'}")
    print(f"  Status codes to retry on: {retry_config.retry_status_codes}")
    print(f"  Exceptions to retry on: {retry_config.retry_on}")

    # 4. Using the retry configuration with a client
    print("\n4. Using the RetryConfig object with a client...")
    
    config_client = PortClient(
        client_id=client_id,
        client_secret=client_secret,
        retry_config=retry_config
    )
    
    print("✅ Client with RetryConfig object initialized!")

    # 5. Handling different types of errors
    print("\n5. Handling different types of errors...")
    
    # Try to create a blueprint with invalid data
    print("\nTrying to create a blueprint with invalid data...")
    try:
        invalid_blueprint = {
            "identifier": "invalid-blueprint",
            # Missing required fields
        }
        
        blueprint = client.blueprints.create_blueprint(invalid_blueprint)
        print("✅ Blueprint created successfully (this should not happen)!")
    except PortApiError as e:
        print(f"✅ Caught expected error: {e}")
        print(f"  Status code: {e.status_code}")
        print(f"  Endpoint: {e.endpoint}")
        print(f"  Method: {e.method}")

    # 6. Using try/except with specific error handling
    print("\n6. Using try/except with specific error handling...")
    
    # Create a blueprint for testing
    test_blueprint_id = f"test-blueprint-{uuid.uuid4().hex[:8]}"
    
    try:
        # Try to create a blueprint
        blueprint_data = {
            "identifier": test_blueprint_id,
            "title": "Test Blueprint",
            "schema": {
                "properties": {
                    "name": {
                        "type": "string",
                        "title": "Name"
                    }
                }
            }
        }
        
        blueprint = client.blueprints.create_blueprint(blueprint_data)
        print("✅ Blueprint created successfully!")
        
        # Now try to create it again (should fail with a conflict)
        print("\nTrying to create the same blueprint again...")
        blueprint = client.blueprints.create_blueprint(blueprint_data)
        print("❌ Blueprint created again (this should not happen)!")
    except PortApiError as e:
        if e.status_code == 409:  # Conflict
            print(f"✅ Caught expected conflict error: {e}")
            print("  This is expected when trying to create a resource that already exists.")
        elif e.status_code == 400:  # Bad Request
            print(f"✅ Caught validation error: {e}")
            print("  This means the blueprint data was invalid.")
        elif e.status_code == 401:  # Unauthorized
            print(f"❌ Authentication error: {e}")
            print("  Please check your API credentials.")
        elif e.status_code == 403:  # Forbidden
            print(f"❌ Permission error: {e}")
            print("  You don't have permission to perform this action.")
        elif e.status_code == 404:  # Not Found
            print(f"❌ Resource not found: {e}")
            print("  The requested resource does not exist.")
        elif e.status_code >= 500:  # Server Error
            print(f"❌ Server error: {e}")
            print("  There was an error on the server side.")
        else:
            print(f"❌ Unexpected error: {e}")
    finally:
        # Clean up by deleting the blueprint
        try:
            client.blueprints.delete_blueprint(test_blueprint_id)
            print("\n✅ Test blueprint deleted successfully!")
        except PortApiError:
            print("\n❌ Failed to delete test blueprint.")

    print("\nError handling and retry configuration example completed!")


if __name__ == "__main__":
    main()
