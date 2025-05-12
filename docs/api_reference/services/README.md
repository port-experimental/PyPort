# API Services

PyPort provides access to various Port API services through the `PortClient` class. Each service is responsible for a specific part of the Port API.

## Available Services

- [Blueprints](blueprints.md): Manage blueprint definitions
- [Entities](entities.md): Manage entities (instances of blueprints)
- [Actions](actions.md): Manage actions that can be performed on entities
- [Action Runs](action_runs.md): Manage action run executions
- [Pages](pages.md): Manage custom pages in the Port UI
- [Integrations](integrations.md): Manage integrations with external systems
- [Organizations](organizations.md): Manage organization settings
- [Teams](teams.md): Manage teams and team memberships
- [Users](users.md): Manage users and user permissions
- [Roles](roles.md): Manage roles and role assignments
- [Audit](audit.md): Access audit logs
- [Migrations](migrations.md): Manage data migrations
- [Search](search.md): Search for entities and other resources
- [Sidebars](sidebars.md): Manage sidebar configurations
- [Checklist](checklist.md): Manage checklists and checklist items
- [Apps](apps.md): Manage custom applications
- [Scorecards](scorecards.md): Manage scorecards for entities

## Common Patterns

All service classes follow a common pattern for CRUD operations:

- **get_[resources]**: Get a list of resources
- **get_[resource]**: Get a specific resource by ID
- **create_[resource]**: Create a new resource
- **update_[resource]**: Update an existing resource
- **delete_[resource]**: Delete a resource

For example, the Blueprints service provides:

- `get_blueprints()`: Get all blueprints
- `get_blueprint(blueprint_id)`: Get a specific blueprint
- `create_blueprint(blueprint_data)`: Create a new blueprint
- `update_blueprint(blueprint_id, blueprint_data)`: Update a blueprint
- `delete_blueprint(blueprint_id)`: Delete a blueprint

## Pagination

Many methods that return lists of resources support pagination:

```python
# Get the first page of blueprints (default page size)
blueprints_page1 = client.blueprints.get_blueprints(page=1)

# Get the second page with a custom page size
blueprints_page2 = client.blueprints.get_blueprints(page=2, per_page=50)
```

## Additional Parameters

Most methods accept an optional `params` parameter for additional query parameters:

```python
# Get blueprints with additional query parameters
blueprints = client.blueprints.get_blueprints(
    params={"filter": "value", "sort": "name"}
)
```

## Error Handling

All service methods can raise exceptions for various error conditions:

- **PortResourceNotFoundError**: If the requested resource is not found
- **PortValidationError**: If the request data is invalid
- **PortAuthError**: If there is an authentication error
- **PortServerError**: If the server returns an error
- **PortNetworkError**: If there is a network error
- **PortTimeoutError**: If the request times out
- **PortApiError**: For other API errors

```python
try:
    blueprint = client.blueprints.get_blueprint("non-existent-blueprint")
except PortResourceNotFoundError as e:
    print(f"Blueprint not found: {e}")
```
