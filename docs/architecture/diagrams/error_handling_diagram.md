# Error Handling Diagram

```mermaid
graph TD
    API[Port API] -->|Error Response| RequestManager
    
    RequestManager[RequestManager] -->|Handle Error| ErrorHandling
    
    ErrorHandling[Error Handling] -->|4xx/5xx Status Code| MapError
    
    MapError{Map Error} -->|401| PortAuthError
    MapError -->|404| PortResourceNotFoundError
    MapError -->|400, 422| PortValidationError
    MapError -->|5xx| PortServerError
    MapError -->|Network Error| PortNetworkError
    MapError -->|Timeout| PortTimeoutError
    MapError -->|Other| PortApiError
    
    PortAuthError -->|Propagate| Service
    PortResourceNotFoundError -->|Propagate| Service
    PortValidationError -->|Propagate| Service
    PortServerError -->|Retry?| RetryLogic
    PortNetworkError -->|Retry?| RetryLogic
    PortTimeoutError -->|Retry?| RetryLogic
    
    RetryLogic{Retry Logic} -->|Max Retries Exceeded| Service
    RetryLogic -->|Retry| RequestManager
    
    Service[API Service] -->|Propagate| Client
    Client[PortClient] -->|Propagate| User
    
    style ErrorHandling fill:#f99,stroke:#333,stroke-width:2px
    style MapError fill:#f99,stroke:#333,stroke-width:2px
    style RetryLogic fill:#9f9,stroke:#333,stroke-width:2px
```

This diagram illustrates the error handling flow in the PyPort library:

1. When the Port API returns an error response, the RequestManager passes it to the error handling component.
2. The error handling component maps the HTTP status code to an appropriate exception type:
   - 401: PortAuthError (authentication error)
   - 404: PortResourceNotFoundError (resource not found)
   - 400, 422: PortValidationError (validation error)
   - 5xx: PortServerError (server error)
   - Network errors: PortNetworkError
   - Timeouts: PortTimeoutError
   - Other errors: PortApiError (base class)
3. For certain types of errors (server errors, network errors, timeouts), the retry logic determines whether to retry the request.
4. If the maximum number of retries is exceeded, or if the error is not retryable, the exception is propagated up the call stack to the user.

This approach provides a consistent and robust error handling mechanism that helps users understand and handle errors from the Port API.
