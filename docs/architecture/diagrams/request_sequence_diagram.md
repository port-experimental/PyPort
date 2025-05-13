# Request Sequence Diagram

```mermaid
sequenceDiagram
    participant User as User Code
    participant Client as PortClient
    participant Service as API Service
    participant Base as BaseAPIService
    participant Request as RequestManager
    participant Auth as AuthManager
    participant API as Port API
    
    User->>Client: client.blueprints.get_blueprint("service")
    Client->>Service: get_blueprint("service")
    Service->>Base: _build_endpoint("blueprints", "service")
    Base-->>Service: "/blueprints/service"
    Service->>Base: _make_request_with_params("GET", endpoint)
    Base->>Request: make_request("GET", endpoint)
    Request->>Auth: get_token()
    
    alt Token is valid
        Auth-->>Request: Existing token
    else Token is expired or missing
        Auth->>API: Request new token
        API-->>Auth: New token
        Auth-->>Request: New token
    end
    
    Request->>API: HTTP request with token
    
    alt Request succeeds (200 OK)
        API-->>Request: Response with data
        Request-->>Base: Response
        Base->>Base: _extract_response_data(response)
        Base-->>Service: Blueprint data
        Service-->>Client: Blueprint object
        Client-->>User: Blueprint object
    else Request fails (4xx/5xx)
        API-->>Request: Error response
        
        alt Retryable error
            Request->>Request: Apply retry logic
            Request->>API: Retry request
            API-->>Request: Response
        else Non-retryable error
            Request->>Request: _handle_error(response)
            Request-->>Base: PortApiError
            Base-->>Service: PortApiError
            Service-->>Client: PortApiError
            Client-->>User: PortApiError
        end
    end
```

This sequence diagram illustrates the flow of a typical API request in the PyPort library:

1. The user calls a method on a service object (e.g., `client.blueprints.get_blueprint("service")`).
2. The service method builds the endpoint and prepares the request parameters.
3. The base service class handles common functionality and calls the request manager.
4. The request manager ensures a valid authentication token is available.
5. The request manager sends the HTTP request to the API.
6. If the request succeeds, the response is processed and returned to the user.
7. If the request fails, the error is handled according to the retry configuration and error handling logic.

The diagram shows the interaction between the different components of the library and how they work together to handle API requests and responses.
