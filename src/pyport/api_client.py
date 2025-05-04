import json
import logging
import os
import threading
import time
from typing import Any, Callable, Dict, Optional, TypeVar, Union

import requests

from pyport.action_runs.action_runs_api_svc import ActionRuns
from pyport.actions.actions_api_svc import Actions
from pyport.apps.apps_api_svc import Apps
from pyport.audit.audit_api_svc import Audit
from pyport.checklist.checklist_api_svc import Checklist
from pyport.constants import PORT_API_US_URL, PORT_API_URL, GENERIC_HEADERS
from pyport.data_sources.data_sources_api_svc import DataSources
from pyport.entities.entities_api_svc import Entities
from pyport.error_handling import handle_error_response, handle_request_exception, with_error_handling
from pyport.exceptions import (
    PortApiError, PortAuthenticationError, PortConfigurationError,
    PortConnectionError, PortPermissionError, PortRateLimitError,
    PortResourceNotFoundError, PortServerError, PortTimeoutError, PortValidationError
)
from pyport.integrations.integrations_api_svc import Integrations
from pyport.migrations.migrations_api_svc import Migrations
from pyport.organization.organization_api_svc import Organizations
from pyport.pages.pages_api_svc import Pages
from pyport.blueprints.blueprint_api_svc import Blueprints
from pyport.roles.roles_api_svc import Roles
from pyport.scorecards.scorecards_api_svc import Scorecards
from pyport.search.search_api_svc import Search
from pyport.sidebars.sidebars_api_svc import Sidebars
from pyport.teams.teams_api_svc import Teams
from pyport.users.users_api_svc import Users
from pyport.webhooks.webhooks_api_svc import Webhooks

# Type variable for generic functions
T = TypeVar('T')


class PortClient:
    def __init__(self, client_id: str, client_secret: str, us_region: bool = False,
                 auto_refresh: bool = True, refresh_interval: int = 900):
        """
        Initialize the PortClient.

        :param client_id: API client ID.
        :param client_secret: API client secret.
        :param us_region: Whether to use the US region API URL.
        :param auto_refresh: If True, a background thread will refresh the token periodically.
        :param refresh_interval: Token refresh interval in seconds (default 900 sec = 15 minutes).
        """
        self.api_url = PORT_API_US_URL if us_region else PORT_API_URL
        self._logger = logging.getLogger(__name__)
        self._lock = threading.Lock()

        # Obtain the initial token.
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self._get_access_token()
        # Initialize the session and sub-clients.
        self._init_session()
        self._init_sub_clients()

        # Start a background thread to auto-refresh the token if enabled.
        self._auto_refresh = auto_refresh
        self._refresh_interval = refresh_interval
        if self._auto_refresh:
            self._start_token_refresh_thread()

    def _init_session(self):
        """Initializes the persistent session and default headers."""
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        })

    @property
    def default_headers(self) -> dict:
        """Return a copy of the default request headers."""
        return dict(self._session.headers)

    def _init_sub_clients(self):
        """Initializes all API sub-clients."""
        self.blueprints = Blueprints(self)
        self.entities = Entities(self)
        self.actions = Actions(self)
        self.pages = Pages(self)
        self.integrations = Integrations(self)
        self.action_runs = ActionRuns(self)
        self.organizations = Organizations(self)
        self.teams = Teams(self)
        self.users = Users(self)
        self.roles = Roles(self)
        self.audit = Audit(self)
        self.migrations = Migrations(self)
        self.search = Search(self)
        self.sidebars = Sidebars(self)
        self.checklist = Checklist(self)
        self.apps = Apps(self)
        self.scorecards = Scorecards(self)
        self.webhooks = Webhooks(self)
        self.data_sources = DataSources(self)

    def _start_token_refresh_thread(self):
        refresh_thread = threading.Thread(target=self._token_refresh_loop, daemon=True)
        refresh_thread.start()
        self._logger.info("Token refresh thread started.")

    def _handle_token_refresh_error(self, error: Exception) -> None:
        """
        Handle errors that occur during token refresh.

        :param error: The exception that occurred.
        """
        if isinstance(error, PortRateLimitError):
            # For rate limiting, respect the retry-after header
            retry_after = error.retry_after or self._refresh_interval
            self._logger.warning(
                f"Rate limit exceeded during token refresh. "
                f"Will retry after {retry_after} seconds. Error: {str(error)}"
            )
            # Sleep for the retry-after period minus the time already slept
            time.sleep(max(1, retry_after - 1))
        elif isinstance(error, (PortAuthenticationError, PortPermissionError)):
            # Authentication errors are critical and should be logged as errors
            self._logger.error(
                f"Authentication error during token refresh. "
                f"Check your client credentials. Error: {str(error)}"
            )
            # Sleep for a longer period before retrying
            time.sleep(min(300, self._refresh_interval * 2))  # Max 5 minutes
        elif isinstance(error, (PortServerError, PortTimeoutError, PortConnectionError)):
            # Transient errors, log as warnings and retry normally
            self._logger.warning(f"Transient error during token refresh: {str(error)}")
        elif isinstance(error, PortApiError):
            # Other API errors
            self._logger.error(f"API error during token refresh: {str(error)}")
        else:
            # Unexpected errors
            self._logger.error(f"Unexpected error during token refresh: {str(error)}")

    def _token_refresh_loop(self):
        """
        Background thread that periodically refreshes the access token.
        """
        while True:
            time.sleep(self._refresh_interval)
            try:
                self._logger.debug("Refreshing access token...")
                new_token = self._get_access_token()
                with self._lock:
                    self.token = new_token
                    self._session.headers.update({"Authorization": f"Bearer {self.token}"})
                self._logger.info("Access token refreshed successfully.")
            except Exception as e:
                self._handle_token_refresh_error(e)

    def _extract_token_from_response(self, response_data: Dict[str, Any], endpoint: str) -> str:
        """Extract the access token from the response data."""
        token = response_data.get('accessToken')
        if not token:
            self._logger.error("Access token not found in the response.")
            raise PortApiError(
                "Access token not present in the API response",
                endpoint=endpoint,
                method="POST",
                response_body=response_data
            )
        return token

    def _prepare_auth_request(self) -> tuple[str, Dict[str, str], str]:
        """
        Prepare the authentication request.

        :return: A tuple of (endpoint, headers, payload).
        """
        # Get credentials if needed
        if not self.client_id or not self.client_secret:
            self.client_id, self.client_secret = self._get_local_env_cred()

        # Prepare request data
        headers = GENERIC_HEADERS
        credentials = {'clientId': self.client_id, 'clientSecret': self.client_secret}
        payload = json.dumps(credentials)
        endpoint = "auth/access_token"

        return endpoint, headers, payload

    def _handle_auth_response(self, response: requests.Response, endpoint: str) -> str:
        """
        Handle the authentication response.

        :param response: The response from the authentication request.
        :param endpoint: The API endpoint.
        :return: The access token.
        :raises PortApiError: If the response is invalid or doesn't contain a token.
        """
        if response.status_code == 200:
            try:
                return self._extract_token_from_response(response.json(), endpoint)
            except json.JSONDecodeError as e:
                raise PortApiError(
                    "Invalid JSON response from authentication endpoint",
                    endpoint=endpoint,
                    method="POST"
                ) from e

        # Handle error response
        raise handle_error_response(response, endpoint, "POST")

    def _get_access_token(self) -> str:
        """
        Get an access token from the API.

        :return: The access token.
        :raises PortAuthenticationError: If authentication fails.
        :raises PortApiError: If another API error occurs.
        :raises PortConfigurationError: If client credentials are missing.
        """
        try:
            # Prepare request
            endpoint, headers, payload = self._prepare_auth_request()
            url = f'{self.api_url}/v1/{endpoint}'

            self._logger.debug("Sending authentication request to obtain access token...")

            try:
                # Make the request
                response = requests.post(url, headers=headers, data=payload, timeout=10)
                return self._handle_auth_response(response, endpoint)
            except requests.RequestException as e:
                # Convert requests exceptions to Port exceptions
                raise handle_request_exception(e, endpoint, "POST")

        except (PortApiError, PortAuthenticationError, PortConfigurationError):
            # Re-raise these exceptions as they're already properly formatted
            raise
        except Exception as e:
            # Catch any other exceptions and convert to PortApiError
            self._logger.error(f"An unexpected error occurred while obtaining access token: {str(e)}")
            raise PortApiError(
                f"Unexpected error during authentication: {str(e)}",
                endpoint="auth/access_token",
                method="POST"
            ) from e

    def _get_local_env_cred(self):
        """
        Get client credentials from environment variables.

        :return: A tuple of (client_id, client_secret).
        :raises PortConfigurationError: If credentials are missing.
        """
        PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
        PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")
        if not PORT_CLIENT_ID or not PORT_CLIENT_SECRET:
            self._logger.error("Missing environment variables: PORT_CLIENT_ID or PORT_CLIENT_SECRET.")
            raise PortConfigurationError("Environment variables PORT_CLIENT_ID or PORT_CLIENT_SECRET are not set")
        return PORT_CLIENT_ID, PORT_CLIENT_SECRET

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log the request details without sensitive information."""
        has_auth = 'auth' in kwargs
        has_headers = 'headers' in kwargs
        has_json = 'json' in kwargs
        self._logger.debug(
            f"Making {method} request to {url} "
            f"(auth: {has_auth}, headers: {has_headers}, json payload: {has_json})"
        )

    def _log_response(self, url: str, response: requests.Response) -> None:
        """Log the response details."""
        content_length = len(response.content) if response.content else 0
        self._logger.debug(
            f"Received response from {url}: status={response.status_code}, "
            f"content_length={content_length} bytes"
        )

    def _handle_response(self, response: requests.Response, endpoint: str, method: str) -> requests.Response:
        """Handle the response, returning it if successful or raising an appropriate exception."""
        if 200 <= response.status_code < 300:
            return response

        # Handle error response
        error = handle_error_response(response, endpoint, method)
        raise error

    def _retry_request(self, error: PortApiError, attempt: int, retries: int, retry_delay: float) -> float:
        """Handle retry logic for transient errors. Returns the sleep time."""
        if not error.is_transient() or attempt >= retries:
            raise error

        # For rate limiting, use the retry-after header if available
        if isinstance(error, PortRateLimitError) and error.retry_after:
            sleep_time = error.retry_after
        else:
            sleep_time = retry_delay * (2 ** attempt)  # Exponential backoff

        self._logger.warning(
            f"{error.__class__.__name__} occurred. "
            f"Retrying in {sleep_time:.2f} seconds. Attempt {attempt + 1}/{retries}."
        )
        return sleep_time

    def _make_single_request(self, method: str, url: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make a single HTTP request and handle the response.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param url: The full URL to request.
        :param endpoint: The API endpoint (for error reporting).
        :param kwargs: Additional parameters passed to requests.request.
        :return: The response if successful.
        :raises PortApiError: If the request fails.
        """
        try:
            # Make the request
            response = self._session.request(method, url, **kwargs)
            self._log_response(url, response)

            # Handle the response
            return self._handle_response(response, endpoint, method)
        except requests.RequestException as e:
            # Convert requests exceptions to Port exceptions
            raise handle_request_exception(e, endpoint, method)

    def make_request(self, method: str, endpoint: str, retries: int = 3, retry_delay: float = 1.0, **kwargs) -> requests.Response:
        """
        Make an HTTP request to the API with error handling and retry logic.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param endpoint: API endpoint appended to the base URL.
        :param retries: Number of retry attempts for transient errors (default: 3).
        :param retry_delay: Initial delay between retries in seconds (default: 1.0).
        :param kwargs: Additional parameters passed to requests.request.
        :return: A requests.Response object.
        :raises PortApiError: Base class for all Port API errors.
        """
        url = f"{self.api_url}/v1/{endpoint}"
        self._log_request(method, url, **kwargs)

        for attempt in range(retries + 1):
            try:
                return self._make_single_request(method, url, endpoint, **kwargs)
            except PortApiError as error:
                # Handle retry logic
                if error.is_transient() and attempt < retries:
                    sleep_time = self._retry_request(error, attempt, retries, retry_delay)
                    time.sleep(sleep_time)
                else:
                    # If not retrying, re-raise the error
                    raise

        # This should never be reached due to the raise in the loop
        raise PortApiError(f"Unexpected error in make_request for {method} {endpoint}")

    def with_error_handling(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute a function with standard error handling.

        :param func: The function to execute.
        :param args: Positional arguments to pass to the function.
        :param kwargs: Keyword arguments to pass to the function.
        :return: The result of the function.
        :raises PortApiError: If an error occurs and is not handled.
        """
        return with_error_handling(func)(*args, **kwargs)
