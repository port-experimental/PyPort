# Users Service

The Users service provides methods for managing users in Port. Users are individuals who can access and interact with your Port organization.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Users service
users_service = client.users
```

## Methods

### get_users

```python
def get_users(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve all users in the organization.

#### Parameters

- **page** (int, optional): The page number to retrieve. Default is None.
- **per_page** (int, optional): The number of items per page. Default is None.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing users data.

#### Raises

- **PortApiError**: If the API request fails.

#### Example

```python
# Get all users
users = client.users.get_users()
for user in users.get("users", []):
    print(f"User: {user['email']} - Role: {user['role']}")

# Get users with pagination
users_page1 = client.users.get_users(page=1, per_page=20)
```

### get_user

```python
def get_user(
    user_email: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve a specific user by their email address.

#### Parameters

- **user_email** (str): The email address of the user to retrieve.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary containing the user details.

#### Raises

- **PortResourceNotFoundError**: If the user does not exist.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Get a specific user
user = client.users.get_user("john.doe@example.com")
print(f"User: {user['user']['email']}")
print(f"Role: {user['user']['role']}")
print(f"Teams: {user['user']['teams']}")
```

### invite_user

```python
def invite_user(
    invitation_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Invite a user to the organization.

#### Parameters

- **invitation_data** (dict): A dictionary containing invitation data.
- **params** (dict, optional): Additional query parameters for the request. Default is None.

#### Returns

- **Dict[str, Any]**: A dictionary representing the invitation result.

#### Raises

- **PortValidationError**: If the invitation data is invalid.
- **PortApiError**: If the API request fails for another reason.

#### Example

```python
# Invite a new user
invitation = client.users.invite_user({
    "email": "newuser@example.com",
    "role": "member",
    "teams": ["backend-team"]
})
print(f"Invitation sent to: {invitation['email']}")
```

## User Structure

Users in Port have the following structure:

```python
{
    "email": "john.doe@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "role": "admin",
    "status": "active",
    "teams": [
        {
            "name": "backend-team",
            "role": "member"
        },
        {
            "name": "devops-team", 
            "role": "admin"
        }
    ],
    "createdAt": "2024-01-15T10:30:00Z",
    "lastLogin": "2024-01-20T14:45:00Z"
}
```

## User Roles

Users can have different organization-level roles:

- **admin**: Full administrative access to the organization
- **member**: Standard user access with team-based permissions
- **viewer**: Read-only access to the organization

## User Status

Users can have different statuses:

- **active**: User is active and can access the organization
- **pending**: User has been invited but hasn't accepted yet
- **suspended**: User access has been temporarily suspended
- **inactive**: User account is deactivated

## Team Membership

Users can be members of multiple teams with different roles:

### Team Roles
- **admin**: Administrative access within the team
- **member**: Standard team member access

### Managing Team Membership
```python
# Users are assigned to teams during invitation
invitation_data = {
    "email": "developer@example.com",
    "role": "member",
    "teams": [
        {
            "name": "backend-team",
            "role": "member"
        },
        {
            "name": "security-team",
            "role": "admin"
        }
    ]
}
```

## User Permissions

User permissions are determined by:

1. **Organization Role**: Admin, Member, or Viewer
2. **Team Membership**: Access to team-owned resources
3. **Entity Permissions**: Specific entity-level access
4. **Action Permissions**: Ability to execute specific actions

## User Management Best Practices

### 1. Role Assignment
- Use the principle of least privilege
- Assign admin roles sparingly
- Regular review of user permissions

### 2. Team Organization
- Organize users into logical teams
- Use team-based access control
- Maintain clear team hierarchies

### 3. User Lifecycle
- Prompt user onboarding with proper team assignments
- Regular access reviews
- Proper offboarding procedures

## Integration with SSO

Port supports Single Sign-On (SSO) integration:

- **SAML 2.0**: Enterprise SSO providers
- **OAuth 2.0**: Google, GitHub, Microsoft
- **OIDC**: OpenID Connect providers

When SSO is enabled, user management may be handled by your identity provider.

## Error Handling

All user methods can raise exceptions for various error conditions:

- **PortResourceNotFoundError**: User not found
- **PortValidationError**: Invalid user data or email format
- **PortAuthError**: Insufficient permissions
- **PortApiError**: General API errors

See the [Error Handling](../error_handling.md) documentation for more details.
