# Class Diagram

```mermaid
classDiagram
    class PortClient {
        +AuthManager _auth_manager
        +RequestManager _request_manager
        +Blueprints _blueprints
        +Entities _entities
        +Actions _actions
        +Other services...
        +__init__(client_id, client_secret, ...)
        +blueprints() Blueprints
        +entities() Entities
        +actions() Actions
        +Other service properties...
    }
    
    class AuthManager {
        -str client_id
        -str client_secret
        -str token
        -datetime token_expiry
        +__init__(client_id, client_secret)
        +get_token() str
        +refresh_token() str
        +is_token_valid() bool
    }
    
    class RequestManager {
        -AuthManager auth_manager
        -str base_url
        -RetryConfig retry_config
        +__init__(auth_manager, base_url, ...)
        +make_request(method, endpoint, ...) Response
        +_handle_response(response) Response
        +_handle_error(response) Exception
    }
    
    class BaseAPIService {
        -ApiClient _client
        -str _resource_name
        -str _response_key
        +__init__(client, resource_name, response_key)
        +_build_endpoint(*parts) str
        +_make_request_with_params(method, endpoint, ...) dict
        +_extract_response_data(response, key) dict
        +_handle_pagination_params(page, per_page) dict
    }
    
    class Blueprints {
        +__init__(client)
        +get_blueprints(page, per_page, ...) List[Blueprint]
        +get_blueprint(blueprint_id, ...) Blueprint
        +create_blueprint(blueprint_data, ...) Blueprint
        +update_blueprint(blueprint_id, data, ...) Blueprint
        +delete_blueprint(blueprint_id, ...) bool
    }
    
    class Entities {
        +__init__(client)
        +get_entities(blueprint_id, page, per_page, ...) List[Entity]
        +get_entity(blueprint_id, entity_id, ...) Entity
        +create_entity(blueprint_id, entity_data, ...) Entity
        +update_entity(blueprint_id, entity_id, data, ...) Entity
        +delete_entity(blueprint_id, entity_id, ...) bool
        +search_entities(query, ...) List[Entity]
    }
    
    class RetryConfig {
        +int max_retries
        +float retry_delay
        +float max_delay
        +RetryStrategy retry_strategy
        +bool retry_jitter
        +Set[int] retry_status_codes
        +Set[Exception] retry_on
        +__init__(max_retries, retry_delay, ...)
    }
    
    PortClient --> AuthManager
    PortClient --> RequestManager
    PortClient --> Blueprints
    PortClient --> Entities
    
    RequestManager --> AuthManager
    RequestManager --> RetryConfig
    
    Blueprints --|> BaseAPIService
    Entities --|> BaseAPIService
    
    BaseAPIService --> RequestManager
```

This class diagram shows the main classes in the PyPort library and their relationships:

- **PortClient**: The main client class that provides access to all API services.
- **AuthManager**: Handles authentication and token management.
- **RequestManager**: Manages HTTP requests and responses.
- **BaseAPIService**: Base class for all API services, providing common functionality.
- **Blueprints**: Service class for blueprint-related operations.
- **Entities**: Service class for entity-related operations.
- **RetryConfig**: Configuration for retry behavior.

The diagram shows inheritance relationships (Blueprints and Entities inherit from BaseAPIService) and composition relationships (PortClient contains AuthManager, RequestManager, and service classes).
