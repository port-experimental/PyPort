# Teams Service

The Teams service provides methods for managing teams in Port. Teams are groups of users that can be assigned ownership and permissions for entities and actions.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Teams service
teams_service = client.teams
```

## Methods

### get_teams

```python
def get_teams(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve all teams in the organization.

#### Parameters

- **page** (int, optional): The page number to retrieve. Default is None.
- **per_page** (int, optional): The number of items per page. Default is None.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing teams data.

#### Raises

- **PortApiError**: If the API request fails.

#### Example

```python
# Get all teams
teams = client.teams.get_teams()
for team in teams.get("teams", []):
    print(f"Team: {team['name']}")

# Get teams with pagination
teams_page1 = client.teams.get_teams(page=1, per_page=10)
```

### get_team

```python
def get_team(
    team_identifier: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve a specific team by its identifier.

#### Parameters

- **team_identifier** (str): The identifier of the team to retrieve.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the team details.

#### Raises

- **PortResourceNotFoundError**: If the team does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Get a specific team
team = client.teams.get_team("backend-team")
print(f"Team: {team['team']['name']}")
print(f"Members: {len(team['team']['users'])}")
```

## Team Structure

Teams in Port have the following structure:

```python
{
    "identifier": "backend-team",
    "name": "Backend Team",
    "description": "Team responsible for backend services",
    "users": [
        {
            "email": "john@example.com",
            "role": "member"
        },
        {
            "email": "jane@example.com", 
            "role": "admin"
        }
    ],
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-20T14:45:00Z"
}
```

## Team Roles

Team members can have different roles:

- **admin**: Full administrative access to the team
- **member**: Standard team member access

## Team Usage

Teams are used throughout Port for:

### Entity Ownership
```python
# Entities can be owned by teams
entity = {
    "identifier": "payment-service",
    "title": "Payment Service",
    "team": "backend-team",  # Team ownership
    "properties": {
        "language": "Python"
    }
}
```

### Action Permissions
```python
# Actions can be restricted to specific teams
action = {
    "identifier": "deploy-service",
    "title": "Deploy Service",
    "permissions": {
        "execute": {
            "teams": ["backend-team", "devops-team"]
        }
    }
}
```

### Scorecard Rules
```python
# Scorecards can have team-specific rules
scorecard_rule = {
    "identifier": "security-compliance",
    "title": "Security Compliance",
    "level": "Gold",
    "query": {
        "combinator": "and",
        "conditions": [
            {
                "property": "team",
                "operator": "=",
                "value": "security-team"
            }
        ]
    }
}
```

## Team Management Best Practices

### 1. Team Naming
- Use descriptive, consistent naming conventions
- Consider organizational structure (e.g., "backend-team", "frontend-team")
- Avoid special characters in team identifiers

### 2. Team Ownership
- Assign clear ownership for entities
- Use teams for access control and permissions
- Regular review of team memberships

### 3. Team Hierarchy
- Consider nested team structures for large organizations
- Use team prefixes for department-based organization
- Maintain clear team responsibilities

## Integration with Other Services

Teams integrate with other Port services:

- **Entities**: Team ownership and filtering
- **Actions**: Team-based permissions and approvals
- **Scorecards**: Team-specific scoring and rules
- **Audit**: Team-based activity tracking

## Error Handling

All team methods can raise exceptions for various error conditions:

- **PortResourceNotFoundError**: Team not found
- **PortValidationError**: Invalid team data
- **PortAuthError**: Insufficient permissions
- **PortApiError**: General API errors

See the [Error Handling](../error_handling.md) documentation for more details.
