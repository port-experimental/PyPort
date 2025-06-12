# Scorecards Service

The Scorecards service provides methods for managing scorecards in Port. Scorecards help you measure and track the quality, compliance, and maturity of your entities.

## Accessing the Service

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Access the Scorecards service
scorecards_service = client.scorecards
```

## Methods

### get_scorecards

```python
def get_scorecards(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Retrieve all scorecards in the organization.

#### Parameters

- **page** (int, optional): The page number to retrieve. Default is None.
- **per_page** (int, optional): The number of items per page. Default is None.
- **params** (dict, optional): Additional query parameters for the request.

#### Returns

- **Dict[str, Any]**: A dictionary containing scorecards data.

#### Example

```python
# Get all scorecards
scorecards = client.scorecards.get_scorecards()
for scorecard in scorecards.get("scorecards", []):
    print(f"Scorecard: {scorecard['title']}")
```

### create_scorecard

```python
def create_scorecard(
    blueprint_identifier: str,
    scorecard_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Create a new scorecard for a specific blueprint.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **scorecard_data** (dict): A dictionary containing the scorecard data.
- **params** (dict, optional): Additional query parameters.

#### Returns

- **Dict[str, Any]**: A dictionary representing the created scorecard.

#### Example

```python
# Create a security scorecard
security_scorecard = client.scorecards.create_scorecard(
    "service",
    {
        "identifier": "security-compliance",
        "title": "Security Compliance",
        "description": "Measures security compliance of services",
        "rules": [
            {
                "identifier": "has-security-scan",
                "title": "Has Security Scan",
                "level": "Bronze",
                "query": {
                    "combinator": "and",
                    "conditions": [
                        {
                            "property": "security_scan_status",
                            "operator": "=",
                            "value": "passed"
                        }
                    ]
                }
            }
        ]
    }
)
```

### update_scorecard

```python
def update_scorecard(
    blueprint_identifier: str,
    scorecard_identifier: str,
    scorecard_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Update an existing scorecard.

#### Parameters

- **blueprint_identifier** (str): The identifier of the blueprint.
- **scorecard_identifier** (str): The identifier of the scorecard to update.
- **scorecard_data** (dict): A dictionary containing the updated scorecard data.
- **params** (dict, optional): Additional query parameters.

#### Returns

- **Dict[str, Any]**: A dictionary representing the updated scorecard.

#### Example

```python
# Update scorecard rules
updated_scorecard = client.scorecards.update_scorecard(
    "service",
    "security-compliance",
    {
        "rules": [
            {
                "identifier": "has-security-scan",
                "title": "Has Security Scan",
                "level": "Bronze",
                "query": {
                    "combinator": "and",
                    "conditions": [
                        {
                            "property": "security_scan_status",
                            "operator": "=",
                            "value": "passed"
                        }
                    ]
                }
            },
            {
                "identifier": "has-vulnerability-scan",
                "title": "Has Vulnerability Scan",
                "level": "Silver",
                "query": {
                    "combinator": "and",
                    "conditions": [
                        {
                            "property": "vulnerability_scan_status",
                            "operator": "=",
                            "value": "passed"
                        }
                    ]
                }
            }
        ]
    }
)
```

## Scorecard Structure

Scorecards in Port have the following structure:

```python
{
    "identifier": "security-compliance",
    "title": "Security Compliance",
    "description": "Measures security compliance of services",
    "blueprint": "service",
    "rules": [
        {
            "identifier": "has-security-scan",
            "title": "Has Security Scan",
            "description": "Service must have a passing security scan",
            "level": "Bronze",
            "query": {
                "combinator": "and",
                "conditions": [
                    {
                        "property": "security_scan_status",
                        "operator": "=",
                        "value": "passed"
                    }
                ]
            }
        }
    ],
    "levels": [
        {
            "color": "paleBlue",
            "title": "Bronze"
        },
        {
            "color": "bronze",
            "title": "Silver"
        },
        {
            "color": "gold",
            "title": "Gold"
        }
    ]
}
```

## Scorecard Levels

Scorecards use levels to indicate different tiers of compliance or quality:

- **Bronze**: Basic compliance level
- **Silver**: Intermediate compliance level
- **Gold**: Advanced compliance level
- **Platinum**: Highest compliance level

## Rule Conditions

Scorecard rules use query conditions to evaluate entities:

### Property Conditions
```python
{
    "property": "language",
    "operator": "=",
    "value": "Python"
}
```

### Relation Conditions
```python
{
    "property": "$team",
    "operator": "relatedTo",
    "value": "backend-team"
}
```

### Existence Conditions
```python
{
    "property": "documentation_url",
    "operator": "isNotEmpty"
}
```

## Query Operators

- **=**: Equals
- **!=**: Not equals
- **>**: Greater than
- **<**: Less than
- **>=**: Greater than or equal
- **<=**: Less than or equal
- **contains**: Contains substring
- **doesNotContain**: Does not contain substring
- **isEmpty**: Property is empty
- **isNotEmpty**: Property is not empty
- **relatedTo**: Related to specific entity

## Use Cases

### Security Compliance
Track security measures across services:

```python
security_scorecard = {
    "identifier": "security-scorecard",
    "title": "Security Scorecard",
    "rules": [
        {
            "identifier": "has-security-scan",
            "title": "Security Scan",
            "level": "Bronze",
            "query": {
                "combinator": "and",
                "conditions": [
                    {
                        "property": "security_scan",
                        "operator": "=",
                        "value": "passed"
                    }
                ]
            }
        }
    ]
}
```

### Production Readiness
Ensure services meet production standards:

```python
production_scorecard = {
    "identifier": "production-readiness",
    "title": "Production Readiness",
    "rules": [
        {
            "identifier": "has-monitoring",
            "title": "Has Monitoring",
            "level": "Bronze"
        },
        {
            "identifier": "has-documentation",
            "title": "Has Documentation", 
            "level": "Silver"
        }
    ]
}
```

## Error Handling

All scorecard methods can raise exceptions for various error conditions. See the [Error Handling](../error_handling.md) documentation for more details.
