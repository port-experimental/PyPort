#!/usr/bin/env python3
"""
Advanced Search and Filtering Example for PyPort

This example demonstrates how to use advanced search and filtering capabilities
of the PyPort library to find specific resources.
"""

import os
import sys
import json
import uuid
from typing import Dict, Any, List

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from pyport import PortClient
from pyport.exceptions import PortApiError


def print_json(data: Dict[str, Any]) -> None:
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))


def create_test_data(client: PortClient) -> Dict[str, str]:
    """Create test data for the example.
    
    Args:
        client: The Port client.
        
    Returns:
        A dictionary with the IDs of the created resources.
    """
    # Generate unique identifiers
    blueprint_id = f"test-blueprint-{uuid.uuid4().hex[:8]}"
    
    # Create a blueprint
    blueprint_data = {
        "identifier": blueprint_id,
        "title": "Test Service",
        "icon": "Microservice",
        "schema": {
            "properties": {
                "language": {
                    "type": "string",
                    "title": "Language",
                    "enum": ["Python", "JavaScript", "Java", "Go", "Ruby"]
                },
                "version": {
                    "type": "string",
                    "title": "Version"
                },
                "team": {
                    "type": "string",
                    "title": "Team",
                    "enum": ["Frontend", "Backend", "DevOps", "Data"]
                },
                "status": {
                    "type": "string",
                    "title": "Status",
                    "enum": ["Active", "Deprecated", "In Development"]
                },
                "tags": {
                    "type": "array",
                    "title": "Tags",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    }
    
    client.blueprints.create_blueprint(blueprint_data)
    
    # Create entities
    entities = [
        {
            "identifier": f"entity-python-{uuid.uuid4().hex[:8]}",
            "title": "Python Service",
            "properties": {
                "language": "Python",
                "version": "3.9.0",
                "team": "Backend",
                "status": "Active",
                "tags": ["api", "core", "backend"]
            }
        },
        {
            "identifier": f"entity-js-{uuid.uuid4().hex[:8]}",
            "title": "JavaScript Frontend",
            "properties": {
                "language": "JavaScript",
                "version": "ES2021",
                "team": "Frontend",
                "status": "Active",
                "tags": ["ui", "frontend", "react"]
            }
        },
        {
            "identifier": f"entity-java-{uuid.uuid4().hex[:8]}",
            "title": "Java Service",
            "properties": {
                "language": "Java",
                "version": "17",
                "team": "Backend",
                "status": "Deprecated",
                "tags": ["api", "legacy", "backend"]
            }
        },
        {
            "identifier": f"entity-go-{uuid.uuid4().hex[:8]}",
            "title": "Go Microservice",
            "properties": {
                "language": "Go",
                "version": "1.18",
                "team": "DevOps",
                "status": "In Development",
                "tags": ["microservice", "infrastructure"]
            }
        },
        {
            "identifier": f"entity-ruby-{uuid.uuid4().hex[:8]}",
            "title": "Ruby Service",
            "properties": {
                "language": "Ruby",
                "version": "3.1.0",
                "team": "Data",
                "status": "Active",
                "tags": ["data", "etl", "pipeline"]
            }
        }
    ]
    
    entity_ids = []
    for entity_data in entities:
        entity = client.entities.create_entity(blueprint_id, entity_data)
        entity_ids.append(entity["identifier"])
    
    return {
        "blueprint_id": blueprint_id,
        "entity_ids": entity_ids
    }


def cleanup_test_data(client: PortClient, blueprint_id: str, entity_ids: List[str]) -> None:
    """Clean up test data.
    
    Args:
        client: The Port client.
        blueprint_id: The blueprint ID.
        entity_ids: List of entity IDs.
    """
    # Delete entities
    for entity_id in entity_ids:
        try:
            client.entities.delete_entity(blueprint_id, entity_id)
        except PortApiError:
            pass
    
    # Delete blueprint
    try:
        client.blueprints.delete_blueprint(blueprint_id)
    except PortApiError:
        pass


def main():
    """Main function demonstrating advanced search and filtering."""
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

    # Create test data
    print("\n2. Creating test data...")
    try:
        test_data = create_test_data(client)
        blueprint_id = test_data["blueprint_id"]
        entity_ids = test_data["entity_ids"]
        print(f"✅ Test data created successfully! Blueprint ID: {blueprint_id}")
    except PortApiError as e:
        print(f"❌ Error creating test data: {e}")
        sys.exit(1)

    # Basic search by property value
    print("\n3. Basic search by property value...")
    try:
        search_query = {
            "blueprint": blueprint_id,
            "properties": {
                "language": "Python"
            }
        }
        
        results = client.entities.search_entities(search_query)
        print(f"✅ Search returned {len(results)} results!")
        
        print("\nPython services:")
        for result in results:
            print(f"  - {result['title']} ({result['identifier']})")
            print(f"    Language: {result['properties']['language']}")
            print(f"    Team: {result['properties']['team']}")
    except PortApiError as e:
        print(f"❌ Error searching entities: {e}")

    # Search with multiple criteria
    print("\n4. Search with multiple criteria...")
    try:
        search_query = {
            "blueprint": blueprint_id,
            "properties": {
                "team": "Backend",
                "status": "Active"
            }
        }
        
        results = client.entities.search_entities(search_query)
        print(f"✅ Search returned {len(results)} results!")
        
        print("\nActive Backend services:")
        for result in results:
            print(f"  - {result['title']} ({result['identifier']})")
            print(f"    Language: {result['properties']['language']}")
            print(f"    Status: {result['properties']['status']}")
    except PortApiError as e:
        print(f"❌ Error searching entities: {e}")

    # Search with array contains
    print("\n5. Search for entities with specific tags...")
    try:
        search_query = {
            "blueprint": blueprint_id,
            "properties": {
                "tags": {
                    "$contains": "api"
                }
            }
        }
        
        results = client.entities.search_entities(search_query)
        print(f"✅ Search returned {len(results)} results!")
        
        print("\nServices with 'api' tag:")
        for result in results:
            print(f"  - {result['title']} ({result['identifier']})")
            print(f"    Tags: {', '.join(result['properties']['tags'])}")
    except PortApiError as e:
        print(f"❌ Error searching entities: {e}")

    # Search with logical operators
    print("\n6. Search with logical operators (OR)...")
    try:
        search_query = {
            "blueprint": blueprint_id,
            "$or": [
                {
                    "properties": {
                        "language": "Python"
                    }
                },
                {
                    "properties": {
                        "language": "Go"
                    }
                }
            ]
        }
        
        results = client.entities.search_entities(search_query)
        print(f"✅ Search returned {len(results)} results!")
        
        print("\nPython or Go services:")
        for result in results:
            print(f"  - {result['title']} ({result['identifier']})")
            print(f"    Language: {result['properties']['language']}")
    except PortApiError as e:
        print(f"❌ Error searching entities: {e}")

    # Search with complex query
    print("\n7. Search with complex query...")
    try:
        search_query = {
            "blueprint": blueprint_id,
            "$and": [
                {
                    "$or": [
                        {
                            "properties": {
                                "team": "Backend"
                            }
                        },
                        {
                            "properties": {
                                "team": "DevOps"
                            }
                        }
                    ]
                },
                {
                    "properties": {
                        "status": {
                            "$ne": "Deprecated"
                        }
                    }
                }
            ]
        }
        
        results = client.entities.search_entities(search_query)
        print(f"✅ Search returned {len(results)} results!")
        
        print("\nNon-deprecated Backend or DevOps services:")
        for result in results:
            print(f"  - {result['title']} ({result['identifier']})")
            print(f"    Team: {result['properties']['team']}")
            print(f"    Status: {result['properties']['status']}")
    except PortApiError as e:
        print(f"❌ Error searching entities: {e}")

    # Search with text search
    print("\n8. Search with text search...")
    try:
        search_query = {
            "blueprint": blueprint_id,
            "title": {
                "$contains": "Service"
            }
        }
        
        results = client.entities.search_entities(search_query)
        print(f"✅ Search returned {len(results)} results!")
        
        print("\nEntities with 'Service' in the title:")
        for result in results:
            print(f"  - {result['title']} ({result['identifier']})")
    except PortApiError as e:
        print(f"❌ Error searching entities: {e}")

    # Clean up test data
    print("\n9. Cleaning up test data...")
    cleanup_test_data(client, blueprint_id, entity_ids)
    print("✅ Test data cleaned up successfully!")

    print("\nAdvanced search and filtering example completed!")


if __name__ == "__main__":
    main()
