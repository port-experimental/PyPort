# Component Diagram

```mermaid
graph TB
    subgraph "Client Module"
        Client[client.py]
        Auth[auth.py]
        Request[request.py]
    end
    
    subgraph "Services Module"
        BaseService[base_api_service.py]
    end
    
    subgraph "API Service Modules"
        Blueprints[blueprint_api_svc.py]
        Entities[entities_api_svc.py]
        Actions[actions_api_svc.py]
        OtherServices[Other service modules]
    end
    
    subgraph "Models Module"
        ApiCategory[api_category.py]
    end
    
    subgraph "Types Module"
        ApiResponses[api_responses.py]
        ApiParameters[api_parameters.py]
    end
    
    subgraph "Utility Modules"
        Exceptions[exceptions.py]
        ErrorHandling[error_handling.py]
        Logging[logging.py]
        Retry[retry.py]
        Constants[constants.py]
        Utils[utils/*.py]
    end
    
    Client --> Auth
    Client --> Request
    Client --> Blueprints
    Client --> Entities
    Client --> Actions
    Client --> OtherServices
    
    Auth --> Request
    Request --> Retry
    Request --> ErrorHandling
    Request --> Logging
    
    Blueprints --> BaseService
    Entities --> BaseService
    Actions --> BaseService
    OtherServices --> BaseService
    
    BaseService --> ApiCategory
    BaseService --> Request
    
    ApiCategory --> ApiResponses
    ApiCategory --> ApiParameters
    
    Request --> Exceptions
    ErrorHandling --> Exceptions
    
    style Client fill:#f9f,stroke:#333,stroke-width:2px
    style BaseService fill:#bbf,stroke:#333,stroke-width:2px
    style Request fill:#bfb,stroke:#333,stroke-width:2px
    style Auth fill:#fbb,stroke:#333,stroke-width:2px
```

This component diagram shows the organization of the PyPort library into modules and their dependencies:

- **Client Module**: Contains the main client class, authentication manager, and request manager.
- **Services Module**: Contains the base service class that provides common functionality for all API services.
- **API Service Modules**: Contains individual service classes for different parts of the API.
- **Models Module**: Contains the base resource model for API resources.
- **Types Module**: Contains type definitions for API responses and parameters.
- **Utility Modules**: Contains utility functions and classes for error handling, logging, retry logic, etc.

The arrows indicate dependencies between components. For example, the client module depends on the authentication manager and request manager, and the API service modules depend on the base service class.
