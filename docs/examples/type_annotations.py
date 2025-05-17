"""
Example demonstrating the use of type annotations with PyPort.

This example shows how to use type annotations to get better IDE support
and type checking when working with the PyPort client library.
"""

from typing import Dict, List, Any, Optional, cast
from pyport import PortClient
from pyport.types import Blueprint, Entity, Action, ActionRun

# Initialize the client
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Get all blueprints with type annotation
blueprints: List[Blueprint] = client.blueprints.get_blueprints()

# Get a specific blueprint with type annotation
service_blueprint: Blueprint = client.blueprints.get_blueprint("service")

# Access blueprint properties with proper type hints
blueprint_id: str = service_blueprint["identifier"]
blueprint_title: str = service_blueprint["title"]
blueprint_properties: Dict[str, Any] = service_blueprint["properties"]

# Create a new blueprint with type annotation
new_blueprint_data: Dict[str, Any] = {
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
new_blueprint: Blueprint = client.blueprints.create_blueprint(new_blueprint_data)

# Get all entities of a blueprint with type annotation
services: List[Entity] = client.entities.get_entities("service")

# Get a specific entity with type annotation
api_service: Entity = client.entities.get_entity("service", "api-service")

# Access entity properties with proper type hints
entity_id: str = api_service["identifier"]
entity_title: str = api_service["title"]
entity_properties: Dict[str, Any] = api_service["properties"]

# Create a new entity with type annotation
new_entity_data: Dict[str, Any] = {
    "identifier": "payment-service",
    "title": "Payment Service",
    "properties": {
        "language": "Python",
        "url": "https://github.com/example/payment-service"
    }
}
new_entity: Entity = client.entities.create_entity("service", new_entity_data)

# Get all actions with type annotation
actions: List[Action] = client.actions.get_actions()

# Get a specific action with type annotation
deploy_action: Action = client.actions.get_action("deploy")

# Get all action runs with type annotation
action_runs: List[ActionRun] = client.action_runs.get_action_runs()

# Get a specific action run with type annotation
action_run: ActionRun = client.action_runs.get_action_run("run-123")

# Using Optional for parameters that might be None
def get_entities_with_pagination(
    blueprint_id: str,
    page: Optional[int] = None,
    per_page: Optional[int] = None
) -> List[Entity]:
    """Get entities with optional pagination."""
    return client.entities.get_entities(blueprint_id, page, per_page)

# Using the function with different parameter combinations
all_services = get_entities_with_pagination("service")
first_page = get_entities_with_pagination("service", 1)
first_page_custom_size = get_entities_with_pagination("service", 1, 50)

# Using cast for more specific type information
def get_entity_property(entity: Entity, property_name: str) -> Any:
    """Get a property value from an entity."""
    properties = entity.get("properties", {})
    return properties.get(property_name)

# Get a string property with proper type annotation
language = cast(str, get_entity_property(api_service, "language"))

# Get a numeric property with proper type annotation
version = cast(int, get_entity_property(api_service, "version"))

# Get a boolean property with proper type annotation
is_active = cast(bool, get_entity_property(api_service, "is_active"))

# Using type annotations with error handling
from pyport.exceptions import PortResourceNotFoundError, PortApiError

try:
    # This will raise PortResourceNotFoundError if the blueprint doesn't exist
    blueprint: Blueprint = client.blueprints.get_blueprint("non-existent-blueprint")
    
except PortResourceNotFoundError as e:
    # The exception has type annotations for its properties
    error_message: str = e.message
    status_code: int = e.status_code
    endpoint: str = e.endpoint
    
    print(f"Blueprint not found: {error_message}")
    
except PortApiError as e:
    print(f"API error: {e}")
