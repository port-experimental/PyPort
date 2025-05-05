"""
Error handling utilities for the PyPort client library.
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

    :param exc: The requests exception.
    :param endpoint: The API endpoint.
    :param method: The HTTP method.
    :param kwargs: Additional context for the exception.
    :return: A Port API exception.
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

    :param response: The HTTP response.
    :param endpoint: The API endpoint.
    :param method: The HTTP method.
    :return: A Port API exception.
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
    func: Callable[..., T],
    on_error: Optional[ErrorHandler] = None,
    on_not_found: Optional[Callable[[], Any]] = None
) -> Callable[..., T]:
    """
    Decorator to add error handling to a function.

    :param func: The function to wrap.
    :param on_error: Optional handler for errors.
    :param on_not_found: Optional handler for not found errors.
    :return: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PortResourceNotFoundError:
            if on_not_found:
                return on_not_found()
            raise
        except PortApiError as e:
            if on_error:
                return on_error(e)
            raise
    return wrapper
