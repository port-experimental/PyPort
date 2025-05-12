# PortClient

The `PortClient` class is the main entry point for the PyPort library. It provides access to all API services and handles authentication, request management, and error handling.

## Initialization

```python
from pyport import PortClient

client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    us_region=False,
    auto_refresh=True,
    refresh_interval=900,
    log_level=logging.INFO,
    log_format=None,
    log_handler=None,
    max_retries=3,
    retry_delay=0.1,
    max_delay=60.0,
    retry_strategy="exponential",
    retry_jitter=True,
    retry_status_codes=None,
    retry_on=None,
    idempotent_methods=None,
    skip_auth=False
)
```

### Parameters

- **client_id** (str): The client ID for authentication.
- **client_secret** (str): The client secret for authentication.
- **us_region** (bool, optional): Whether to use the US region API endpoint. Default is False.
- **auto_refresh** (bool, optional): Whether to automatically refresh the token. Default is True.
- **refresh_interval** (int, optional): The interval in seconds to refresh the token. Default is 900 (15 minutes).
- **log_level** (int, optional): The logging level. Default is logging.INFO.
- **log_format** (str, optional): The logging format. Default is None (uses a standard format).
- **log_handler** (logging.Handler, optional): A custom logging handler. Default is None.
- **max_retries** (int, optional): The maximum number of retries for failed requests. Default is 3.
- **retry_delay** (float, optional): The initial delay between retries in seconds. Default is 0.1.
- **max_delay** (float, optional): The maximum delay between retries in seconds. Default is 60.0.
- **retry_strategy** (str or RetryStrategy, optional): The retry strategy to use. Default is "exponential".
- **retry_jitter** (bool, optional): Whether to add jitter to retry delays. Default is True.
- **retry_status_codes** (set of int, optional): HTTP status codes to retry on. Default is None (uses a standard set).
- **retry_on** (Exception or set of Exception, optional): Exception types to retry on. Default is None (uses a standard set).
- **idempotent_methods** (set of str, optional): HTTP methods that are idempotent and can be retried. Default is None (uses a standard set).
- **skip_auth** (bool, optional): Whether to skip authentication (for testing). Default is False.

## Properties

The `PortClient` class provides access to all API services through properties:

- **blueprints** (Blueprints): Access to blueprint-related operations.
- **entities** (Entities): Access to entity-related operations.
- **actions** (Actions): Access to action-related operations.
- **action_runs** (ActionRuns): Access to action run-related operations.
- **pages** (Pages): Access to page-related operations.
- **integrations** (Integrations): Access to integration-related operations.
- **organizations** (Organizations): Access to organization-related operations.
- **teams** (Teams): Access to team-related operations.
- **users** (Users): Access to user-related operations.
- **roles** (Roles): Access to role-related operations.
- **audit** (Audit): Access to audit-related operations.
- **migrations** (Migrations): Access to migration-related operations.
- **search** (Search): Access to search-related operations.
- **sidebars** (Sidebars): Access to sidebar-related operations.
- **checklist** (Checklist): Access to checklist-related operations.
- **apps** (Apps): Access to app-related operations.
- **scorecards** (Scorecards): Access to scorecard-related operations.

## Methods

### make_request

```python
def make_request(
    method: str,
    endpoint: str,
    retries: int = None,
    retry_delay: float = None,
    correlation_id: str = None,
    **kwargs
) -> requests.Response
```

Make an HTTP request to the API with error handling and retry logic.

#### Parameters

- **method** (str): The HTTP method to use (GET, POST, PUT, DELETE, etc.).
- **endpoint** (str): The API endpoint to request.
- **retries** (int, optional): The number of retries for this request. Default is None (uses the client's default).
- **retry_delay** (float, optional): The initial delay between retries in seconds. Default is None (uses the client's default).
- **correlation_id** (str, optional): A correlation ID for tracking the request. Default is None (generates a new ID).
- **kwargs**: Additional keyword arguments to pass to the requests library.

#### Returns

- **requests.Response**: The response from the API.

#### Raises

- **PortApiError**: If the API returns an error.
- **PortAuthError**: If there is an authentication error.
- **PortResourceNotFoundError**: If the requested resource is not found.
- **PortValidationError**: If the request data is invalid.
- **PortServerError**: If the server returns an error.
- **PortNetworkError**: If there is a network error.
- **PortTimeoutError**: If the request times out.

### default_headers

```python
def default_headers() -> dict
```

Return a copy of the default request headers.

#### Returns

- **dict**: The default headers used for API requests.

## Examples

### Basic Usage

```python
from pyport import PortClient

# Initialize the client
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Get all blueprints
blueprints = client.blueprints.get_blueprints()

# Get a specific entity
entity = client.entities.get_entity("service", "my-service")
```

### Custom Request

```python
from pyport import PortClient

# Initialize the client
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Make a custom request
response = client.make_request(
    "GET",
    "custom/endpoint",
    params={"filter": "value"},
    headers={"Custom-Header": "Value"}
)

# Process the response
data = response.json()
```

### Error Handling

```python
from pyport import PortClient
from pyport.exceptions import PortResourceNotFoundError, PortApiError

# Initialize the client
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

try:
    # This will raise PortResourceNotFoundError if the blueprint doesn't exist
    blueprint = client.blueprints.get_blueprint("non-existent-blueprint")
    
except PortResourceNotFoundError as e:
    print(f"Blueprint not found: {e}")
    
except PortApiError as e:
    print(f"API error: {e}")
```
