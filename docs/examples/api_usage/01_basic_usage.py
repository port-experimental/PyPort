#!/usr/bin/env python3
"""
Basic Usage Example for PyPort

This example demonstrates the basic usage of the PyPort library,
including client initialization and simple API operations.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from pyport import PortClient
from pyport.exceptions import PortApiError


def print_json(data: Dict[str, Any]) -> None:
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))


def main():
    """Main function demonstrating basic PyPort usage."""
    # Get API credentials from environment variables
    client_id = os.environ.get('PORT_CLIENT_ID')
    client_secret = os.environ.get('PORT_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("Error: PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables must be set.")
        print("Please set these variables and try again:")
        print("  export PORT_CLIENT_ID=your-client-id")
        print("  export PORT_CLIENT_SECRET=your-client-secret")
        sys.exit(1)

    # Initialize the Port client
    print("\n1. Initializing the Port client...")
    client = PortClient(
        client_id=client_id,
        client_secret=client_secret
    )
    print("✅ Client initialized successfully!")

    # Get all blueprints
    print("\n2. Getting all blueprints...")
    try:
        blueprints = client.blueprints.get_blueprints()
        print(f"✅ Retrieved {len(blueprints)} blueprints!")
        
        # Print the first blueprint if available
        if blueprints:
            print("\nFirst blueprint details:")
            print_json(blueprints[0])
    except PortApiError as e:
        print(f"❌ Error retrieving blueprints: {e}")

    # Get all entities for a specific blueprint
    print("\n3. Getting entities for a specific blueprint...")
    try:
        # Use the first blueprint's identifier if available, otherwise use "service"
        blueprint_id = blueprints[0]["identifier"] if blueprints else "service"
        print(f"Using blueprint: {blueprint_id}")
        
        entities = client.entities.get_entities(blueprint_id)
        print(f"✅ Retrieved {len(entities)} entities for blueprint '{blueprint_id}'!")
        
        # Print the first entity if available
        if entities:
            print("\nFirst entity details:")
            print_json(entities[0])
    except PortApiError as e:
        print(f"❌ Error retrieving entities: {e}")

    # Get all actions
    print("\n4. Getting all actions...")
    try:
        actions = client.actions.get_actions()
        print(f"✅ Retrieved {len(actions)} actions!")
        
        # Print the first action if available
        if actions:
            print("\nFirst action details:")
            print_json(actions[0])
    except PortApiError as e:
        print(f"❌ Error retrieving actions: {e}")

    # Get organization details
    print("\n5. Getting organization details...")
    try:
        organizations = client.organizations.get_organizations()
        print(f"✅ Retrieved {len(organizations)} organizations!")
        
        # Print the first organization if available
        if organizations:
            print("\nOrganization details:")
            print_json(organizations[0])
    except PortApiError as e:
        print(f"❌ Error retrieving organization details: {e}")

    print("\nBasic usage example completed!")


if __name__ == "__main__":
    main()
