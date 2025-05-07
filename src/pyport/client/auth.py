"""
Authentication module for the Port API client.

This module handles authentication with the Port API, including:
- Token acquisition and management
- Token refresh
- Credential validation
"""

import json
import os
import threading
import time
from typing import Dict, Any, Optional, Tuple

import requests

# No need to import PORT_API_URL and PORT_API_US_URL as they're not used directly
from src.pyport.error_handling import handle_request_exception
from src.pyport.exceptions import PortApiError, PortAuthenticationError, PortConfigurationError
from src.pyport.logging import log_request, log_response, log_error, get_correlation_id, logger


class AuthManager:
    """
    Manages authentication with the Port API.

    This class handles token acquisition, refresh, and validation.
    """

    def __init__(self, client_id: str, client_secret: str, api_url: str,
                 auto_refresh: bool = True, refresh_interval: int = 900,
                 skip_auth: bool = False):
        """
        Initialize the AuthManager.

        Args:
            client_id: API client ID obtained from Port.
            client_secret: API client secret obtained from Port.
            api_url: The base URL for the Port API.
            auto_refresh: Whether to automatically refresh the token.
            refresh_interval: Token refresh interval in seconds.
            skip_auth: Whether to skip authentication (for testing).
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url
        self._auto_refresh = auto_refresh
        self._refresh_interval = refresh_interval
        self._logger = logger
        self._lock = threading.Lock()

        # Initialize token
        if skip_auth:
            # Use a dummy token for testing
            self.token = "dummy_token"
        else:
            self.token = self._get_access_token()

        # Start token refresh thread if enabled and not skipping auth
        if self._auto_refresh and not skip_auth:
            self._start_token_refresh_thread()

    def _start_token_refresh_thread(self):
        """Start a background thread to refresh the token periodically."""
        refresh_thread = threading.Thread(target=self._token_refresh_loop, daemon=True)
        refresh_thread.start()
        self._logger.info("Token refresh thread started.")

    def _token_refresh_loop(self):
        """
        Background thread that periodically refreshes the access token.
        """
        while True:
            # Wait for the refresh interval
            time.sleep(self._refresh_interval)

            # Attempt to refresh the token
            self._refresh_token()

    def _refresh_token(self):
        """
        Refresh the access token.
        """
        try:
            self._logger.debug("Refreshing access token...")
            new_token = self._get_access_token()

            # Update the token
            with self._lock:
                self.token = new_token

            self._logger.info("Access token refreshed successfully.")
        except Exception as e:
            self._handle_token_refresh_error(e)

    def _handle_token_refresh_error(self, error):
        """
        Handle errors that occur during token refresh.

        Args:
            error: The error that occurred.
        """
        if isinstance(error, PortAuthenticationError):
            # Authentication errors
            self._logger.error(f"Authentication error during token refresh: {str(error)}")
        elif isinstance(error, PortApiError):
            # Other API errors
            self._logger.error(f"API error during token refresh: {str(error)}")
        else:
            # Unexpected errors
            self._logger.error(f"Unexpected error during token refresh: {str(error)}")

    def _get_access_token(self) -> str:
        """
        Get an access token from the API.

        Returns:
            The access token.

        Raises:
            PortAuthenticationError: If authentication fails.
            PortApiError: If another API error occurs.
            PortConfigurationError: If client credentials are missing.
        """
        # Generate a correlation ID for this request
        correlation_id = get_correlation_id()

        try:
            # Prepare and send the authentication request
            return self._send_auth_request(correlation_id)
        except (PortApiError, PortAuthenticationError, PortConfigurationError):
            # Re-raise these exceptions as they're already properly formatted
            raise
        except Exception as e:
            # Catch any other exceptions and convert to PortApiError
            return self._handle_unexpected_auth_error(e, correlation_id)

    def _send_auth_request(self, correlation_id: str) -> str:
        """
        Prepare and send the authentication request.

        Args:
            correlation_id: A correlation ID for tracking the request.

        Returns:
            The access token.

        Raises:
            PortApiError: If the request fails.
        """
        # Prepare request
        endpoint, headers, payload = self._prepare_auth_request()
        url = f'{self.api_url}/v1/{endpoint}'

        self._logger.debug("Sending authentication request to obtain access token...")

        # Log the request (masking sensitive data)
        log_request("POST", url, headers=headers, json_data=json.loads(payload),
                    correlation_id=correlation_id)

        try:
            # Make the request
            response = requests.post(url, headers=headers, data=payload, timeout=10)

            # Log the response
            log_response(response, correlation_id)

            return self._handle_auth_response(response, endpoint)
        except requests.RequestException as e:
            # Convert requests exceptions to Port exceptions
            error = handle_request_exception(e, endpoint, "POST")
            log_error(error, correlation_id)
            raise error

    def _handle_unexpected_auth_error(self, e: Exception, correlation_id: str) -> str:
        """
        Handle unexpected errors during authentication.

        Args:
            e: The exception that occurred.
            correlation_id: A correlation ID for tracking the request.

        Raises:
            PortApiError: A formatted API error with context about the original exception.
        """
        self._logger.error(f"An unexpected error occurred while obtaining access token: {str(e)}")
        error = PortApiError(
            f"Unexpected error during authentication: {str(e)}",
            endpoint="auth/access_token",
            method="POST"
        )
        log_error(error, correlation_id)
        raise error from e

    def _prepare_auth_request(self) -> Tuple[str, Dict[str, str], str]:
        """
        Prepare the authentication request.

        Returns:
            A tuple of (endpoint, headers, payload).
        """
        # Get credentials
        client_id, client_secret = self._get_credentials()

        # Prepare request
        endpoint = "auth/access_token"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = json.dumps({
            "clientId": client_id,
            "clientSecret": client_secret
        })

        return endpoint, headers, payload

    def _handle_auth_response(self, response: requests.Response, endpoint: str) -> str:
        """
        Handle the authentication response.

        Args:
            response: The HTTP response.
            endpoint: The API endpoint.

        Returns:
            The access token.

        Raises:
            PortAuthenticationError: If authentication fails.
            PortApiError: If another API error occurs.
        """
        if response.status_code == 200:
            # Extract token from response
            try:
                response_data = response.json()
                token = self._extract_token_from_response(response_data, endpoint)
                return token
            except (ValueError, KeyError) as e:
                raise PortAuthenticationError(
                    f"Failed to extract access token from response: {str(e)}",
                    endpoint=endpoint,
                    method="POST",
                    response_body=response.text
                )
        else:
            # Handle error response
            error = handle_request_exception(
                requests.RequestException(f"Authentication failed with status code {response.status_code}"),
                endpoint,
                "POST"
            )
            raise error

    def _extract_token_from_response(self, response_data: Dict[str, Any], endpoint: str) -> str:
        """
        Extract the access token from the response data.

        Args:
            response_data: The response data.
            endpoint: The API endpoint.

        Returns:
            The access token.

        Raises:
            PortAuthenticationError: If the token is missing from the response.
        """
        token = response_data.get('accessToken')
        if not token:
            raise PortAuthenticationError(
                "Access token not found in response",
                endpoint=endpoint,
                method="POST",
                response_body=response_data
            )
        return token

    def _get_credentials(self) -> Tuple[str, str]:
        """
        Get client credentials.

        Returns:
            A tuple of (client_id, client_secret).

        Raises:
            PortConfigurationError: If credentials are missing.
        """
        # Use provided credentials
        if self.client_id and self.client_secret:
            return self.client_id, self.client_secret

        # Try to get credentials from environment variables
        return self._get_local_env_cred()

    def _get_local_env_cred(self) -> Tuple[str, str]:
        """
        Get client credentials from environment variables.

        Returns:
            A tuple of (client_id, client_secret).

        Raises:
            PortConfigurationError: If credentials are missing.
        """
        # Get credentials from environment variables
        client_id = os.getenv("PORT_CLIENT_ID")
        client_secret = os.getenv("PORT_CLIENT_SECRET")

        # Validate credentials
        self._validate_credentials(client_id, client_secret, "environment variables")

        return client_id, client_secret

    def _validate_credentials(self, client_id: Optional[str], client_secret: Optional[str], source: str):
        """
        Validate that client credentials are present.

        Args:
            client_id: The client ID to validate.
            client_secret: The client secret to validate.
            source: The source of the credentials (for error messages).

        Raises:
            PortConfigurationError: If credentials are missing.
        """
        if not client_id or not client_secret:
            self._logger.error(f"Missing credentials from {source}.")
            raise PortConfigurationError(f"Client ID or client secret not found in {source}")
