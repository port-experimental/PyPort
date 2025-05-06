"""
Error handling utilities for the PyPort client library.

This module provides centralized error handling for the PyPort client library.
It includes functions for converting HTTP errors to Port-specific exceptions,
handling request exceptions, and decorators for adding error handling to functions.

Example usage:

```python
# Using the with_error_handling decorator
from src.pyport.error_handling import with_error_handling

@with_error_handling
def get_blueprint(blueprint_id):
    # This function will have error handling added
    response = client.make_request("GET", f"blueprints/{blueprint_id}")
    return response.json()

# Using custom error handlers
@with_error_handling(
    on_not_found=lambda: {"message": "Blueprint not found"},
    on_error=lambda e: {"error": str(e)}
)
def get_blueprint_with_handlers(blueprint_id):
    response = client.make_request("GET", f"blueprints/{blueprint_id}")
    return response.json()
```
"""
import json
import logging
from typing import Dict, Any, Optional, Type, Callable, TypeVar

import requests

from src.pyport.exceptions import (
    PortApiError,
    PortAuthenticationError,
    PortPermissionError,
    PortResourceNotFoundError,
    PortValidationError,
    PortRateLimitError,
    PortServerError,
    PortTimeoutError,
    PortConnectionError
)

logger = logging.getLogger("pyport")

# Type for functions that can be wrapped with error handling
T = TypeVar('T')
ErrorHandler = Callable[[PortApiError], Any]


def handle_request_exception(
    exc: requests.RequestException,
    endpoint: str,
    method: str,
    **kwargs
) -> PortApiError:
    """
    Convert a requests exception to a Port API exception.

    This function handles exceptions that occur during the HTTP request process,
    such as timeouts, connection errors, and other network-related issues.
    It converts these exceptions into Port-specific exceptions that provide
    more context and are easier to handle in application code.

    Args:
        exc: The requests exception that occurred during the request.
            This can be any exception from the requests library, such as
            Timeout, ConnectionError, etc.
        endpoint: The API endpoint that was being accessed when the exception occurred.
            This is used for context in the exception message.
        method: The HTTP method that was being used (GET, POST, etc.).
            This is used for context in the exception message.
        **kwargs: Additional context for the exception.
            These are passed through to the Port exception constructor.

    Returns:
        A Port API exception that corresponds to the requests exception.
        The specific type depends on the input exception:
        - requests.Timeout -> PortTimeoutError
        - requests.ConnectionError -> PortConnectionError
        - Other requests.RequestException -> PortApiError

    Examples:
        >>> try:
        ...     response = requests.get("https://api.example.com/resource", timeout=1)
        ... except requests.Timeout as e:
        ...     port_error = handle_request_exception(e, "resource", "GET")
        ...     print(type(port_error))  # <class 'PortTimeoutError'>
    """
    if isinstance(exc, requests.Timeout):
        return PortTimeoutError(
            f"Request timed out: {str(exc)}",
            endpoint=endpoint,
            method=method,
            **kwargs
        )
    elif isinstance(exc, requests.ConnectionError):
        return PortConnectionError(
            f"Connection error: {str(exc)}",
            endpoint=endpoint,
            method=method,
            **kwargs
        )
    else:
        return PortApiError(
            f"Request error: {str(exc)}",
            endpoint=endpoint,
            method=method,
            **kwargs
        )


def _extract_error_detail(response: requests.Response) -> tuple[str, Optional[Dict[str, Any]]]:
    """Extract error details from a response."""
    try:
        response_body = response.json()
        if isinstance(response_body, dict):
            error_detail = response_body.get('message', '')
            return error_detail, response_body
    except (ValueError, json.JSONDecodeError):
        pass

    # Not JSON or couldn't parse
    error_detail = response.text[:100] + "..." if len(response.text) > 100 else response.text
    return error_detail, None


def _get_exception_class_and_message(status_code: int, error_detail: str) -> tuple[Type[PortApiError], str]:
    """Get the appropriate exception class and message based on status code."""
    exception_map = {
        400: (PortValidationError, f"Bad request: {error_detail}"),
        401: (PortAuthenticationError, f"Authentication failed: {error_detail}"),
        403: (PortPermissionError, f"Permission denied: {error_detail}"),
        404: (PortResourceNotFoundError, f"Resource not found: {error_detail}"),
        429: (PortRateLimitError, f"Rate limit exceeded: {error_detail}")
    }

    if status_code in exception_map:
        return exception_map[status_code]
    elif 500 <= status_code < 600:
        return PortServerError, f"Server error: {error_detail}"
    else:
        return PortApiError, f"API error: {error_detail}"


def handle_error_response(
    response: requests.Response,
    endpoint: str,
    method: str
) -> PortApiError:
    """
    Create an appropriate exception based on the response status code.

    This function analyzes an HTTP error response and creates the most appropriate
    Port-specific exception based on the status code and response content.
    It extracts error details from the response body and includes them in the
    exception message for better error reporting.

    The function maps HTTP status codes to specific exception types:
    - 400: PortValidationError (invalid request data)
    - 401: PortAuthenticationError (authentication failed)
    - 403: PortPermissionError (permission denied)
    - 404: PortResourceNotFoundError (resource not found)
    - 429: PortRateLimitError (rate limit exceeded)
    - 5xx: PortServerError (server-side error)
    - Other: PortApiError (generic API error)

    For rate limit errors (429), it also extracts the Retry-After header
    and includes it in the exception for proper retry handling.

    Args:
        response: The HTTP response object containing the error details.
            This should be a response with a non-2xx status code.
        endpoint: The API endpoint that was accessed.
            This is included in the exception for context.
        method: The HTTP method that was used (GET, POST, etc.).
            This is included in the exception for context.

    Returns:
        A Port API exception of the appropriate type based on the status code.
        The exception includes the status code, endpoint, method, and response body.

    Examples:
        >>> response = requests.get("https://api.example.com/not-found")
        >>> if response.status_code != 200:
        ...     error = handle_error_response(response, "not-found", "GET")
        ...     print(type(error))  # <class 'PortResourceNotFoundError'>
    """
    # Extract error details
    error_detail, response_body = _extract_error_detail(response)

    # Get the exception class and message
    status_code = response.status_code
    exception_class, message = _get_exception_class_and_message(status_code, error_detail)

    # Create the exception with common kwargs
    kwargs = {
        "status_code": status_code,
        "endpoint": endpoint,
        "method": method,
        "response_body": response_body
    }

    # Add retry_after for rate limit errors
    if status_code == 429:
        retry_after = response.headers.get('Retry-After')
        retry_seconds = int(retry_after) if retry_after and retry_after.isdigit() else None
        kwargs["retry_after"] = retry_seconds

    return exception_class(message, **kwargs)


def with_error_handling(
    func: Optional[Callable[..., T]] = None,
    *,
    on_error: Optional[ErrorHandler] = None,
    on_not_found: Optional[Callable[[], Any]] = None,
    on_validation_error: Optional[Callable[[PortValidationError], Any]] = None,
    on_authentication_error: Optional[Callable[[PortAuthenticationError], Any]] = None,
    on_permission_error: Optional[Callable[[PortPermissionError], Any]] = None,
    on_rate_limit_error: Optional[Callable[[PortRateLimitError], Any]] = None,
    on_server_error: Optional[Callable[[PortServerError], Any]] = None,
    on_timeout_error: Optional[Callable[[PortTimeoutError], Any]] = None,
    on_connection_error: Optional[Callable[[PortConnectionError], Any]] = None
) -> Callable[..., T]:
    """
    Decorator to add error handling to a function.

    This decorator can be used in two ways:

    1. As a simple decorator:
       @with_error_handling
       def my_function():
           ...

    2. As a decorator with arguments:
       @with_error_handling(on_not_found=lambda: None)
       def my_function():
           ...

    Args:
        func: The function to wrap.
        on_error: Handler for all PortApiError exceptions.
        on_not_found: Handler for PortResourceNotFoundError exceptions.
        on_validation_error: Handler for PortValidationError exceptions.
        on_authentication_error: Handler for PortAuthenticationError exceptions.
        on_permission_error: Handler for PortPermissionError exceptions.
        on_rate_limit_error: Handler for PortRateLimitError exceptions.
        on_server_error: Handler for PortServerError exceptions.
        on_timeout_error: Handler for PortTimeoutError exceptions.
        on_connection_error: Handler for PortConnectionError exceptions.

    Returns:
        The wrapped function.
    """
    def decorator(fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                return _handle_exception(e)
        return wrapper

    def _handle_exception(e):
        """Handle an exception based on its type."""
        # Handle specific exception types
        if isinstance(e, PortResourceNotFoundError) and on_not_found:
            return on_not_found()

        # Map exception types to their handlers
        handlers = {
            PortValidationError: on_validation_error,
            PortAuthenticationError: on_authentication_error,
            PortPermissionError: on_permission_error,
            PortRateLimitError: on_rate_limit_error,
            PortServerError: on_server_error,
            PortTimeoutError: on_timeout_error,
            PortConnectionError: on_connection_error
        }

        # Check for a specific handler for this exception type
        for exc_type, handler in handlers.items():
            if isinstance(e, exc_type) and handler:
                return handler(e)

        # Fall back to the generic error handler
        if isinstance(e, PortApiError) and on_error:
            return on_error(e)

        # If no handler was found, re-raise the exception
        raise

    # Handle both @with_error_handling and @with_error_handling()
    if func is None:
        return decorator
    return decorator(func)
