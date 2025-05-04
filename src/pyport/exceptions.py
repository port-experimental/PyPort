"""
Custom exceptions for the PyPort client library.
"""
from typing import Dict, Optional, Any


class PortApiError(Exception):
    """Base exception for all Port API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        endpoint: Optional[str] = None,
        method: Optional[str] = None,
        response_body: Optional[Dict[str, Any]] = None,
        request_params: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.endpoint = endpoint
        self.method = method
        self.response_body = response_body
        self.request_params = request_params

        # Build a detailed error message
        detailed_message = message
        if method and endpoint:
            detailed_message += f" [Method: {method}, Endpoint: {endpoint}]"
        if status_code:
            detailed_message += f" [Status: {status_code}]"

        super().__init__(detailed_message)

    def is_client_error(self) -> bool:
        """Return True if this is a client error (4xx)."""
        return 400 <= (self.status_code or 0) < 500

    def is_server_error(self) -> bool:
        """Return True if this is a server error (5xx)."""
        return 500 <= (self.status_code or 0) < 600

    def is_transient(self) -> bool:
        """Return True if this error is likely transient and can be retried."""
        if self.is_server_error():
            return True
        if isinstance(self, PortRateLimitError):
            return True
        if isinstance(self, PortConnectionError) or isinstance(self, PortTimeoutError):
            return True
        return False


class PortAuthenticationError(PortApiError):
    """Raised when authentication fails (401 Unauthorized)."""
    pass


class PortPermissionError(PortApiError):
    """Raised when the client doesn't have permission to access a resource (403 Forbidden)."""
    pass


class PortResourceNotFoundError(PortApiError):
    """Raised when a requested resource is not found (404 Not Found)."""
    pass


class PortValidationError(PortApiError):
    """Raised when the request data fails validation (400 Bad Request)."""
    pass


class PortRateLimitError(PortApiError):
    """Raised when the client has exceeded the rate limit (429 Too Many Requests)."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        endpoint: Optional[str] = None,
        method: Optional[str] = None,
        response_body: Optional[Dict[str, Any]] = None,
        request_params: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None
    ):
        self.retry_after = retry_after
        super().__init__(
            message,
            status_code,
            endpoint,
            method,
            response_body,
            request_params
        )


class PortServerError(PortApiError):
    """Raised when the server encounters an error (5xx status codes)."""
    pass


class PortTimeoutError(PortApiError):
    """Raised when a request times out."""
    pass


class PortConnectionError(PortApiError):
    """Raised when there's a connection error."""
    pass


class PortConfigurationError(Exception):
    """Raised when there's an issue with the client configuration."""
    pass
