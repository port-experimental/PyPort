# High-Level Architecture Diagram

```mermaid
graph TD
    User[User Code] --> PortClient
    
    subgraph "PyPort Library"
        PortClient[PortClient] --> AuthManager
        PortClient --> RequestManager
        PortClient --> APIServices
        
        AuthManager[AuthManager] --> RequestManager
        RequestManager[RequestManager] --> RetryLogic
        RequestManager --> ErrorHandling
        RequestManager --> Logging
        
        APIServices --> Blueprints
        APIServices --> Entities
        APIServices --> Actions
        APIServices --> OtherServices[Other Services]
        
        Blueprints --> BaseAPIService
        Entities --> BaseAPIService
        Actions --> BaseAPIService
        OtherServices --> BaseAPIService
        
        BaseAPIService --> RequestManager
    end
    
    RequestManager --> PortAPI[Port API]
    
    style PortClient fill:#f9f,stroke:#333,stroke-width:2px
    style BaseAPIService fill:#bbf,stroke:#333,stroke-width:2px
    style RequestManager fill:#bfb,stroke:#333,stroke-width:2px
    style AuthManager fill:#fbb,stroke:#333,stroke-width:2px
```

This diagram shows the high-level architecture of the PyPort library. The main components are:

- **PortClient**: The main entry point for the library, providing access to all API services.
- **AuthManager**: Handles authentication and token management.
- **RequestManager**: Manages HTTP requests and responses.
- **BaseAPIService**: Base class for all API services, providing common functionality.
- **API Services**: Individual service classes for different parts of the API (Blueprints, Entities, Actions, etc.).
- **RetryLogic**: Handles retrying failed requests.
- **ErrorHandling**: Converts API errors to appropriate exceptions.
- **Logging**: Provides logging functionality for debugging and monitoring.

The user interacts with the `PortClient` class, which provides access to the various API services. Each service inherits from `BaseAPIService` and uses the `RequestManager` to make requests to the Port API. The `AuthManager` ensures that requests are properly authenticated, and the `RetryLogic`, `ErrorHandling`, and `Logging` components provide additional functionality for robustness and debugging.
