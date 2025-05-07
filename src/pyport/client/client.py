"""
Main client module for the Port API.

This module provides the PortClient class, which is the main entry point
for interacting with the Port API.
"""

import logging
import requests
from typing import Optional, Set, Type, Union

from src.pyport.action_runs.action_runs_api_svc import ActionRuns
from src.pyport.actions.actions_api_svc import Actions
from src.pyport.apps.apps_api_svc import Apps
from src.pyport.audit.audit_api_svc import Audit
from src.pyport.blueprints.blueprint_api_svc import Blueprints
from src.pyport.checklist.checklist_api_svc import Checklist
from src.pyport.client.auth import AuthManager
from src.pyport.client.request import RequestManager
from src.pyport.constants import PORT_API_URL, PORT_API_US_URL, GENERIC_HEADERS
from src.pyport.entities.entities_api_svc import Entities
# PortApiError is not used directly
from src.pyport.integrations.integrations_api_svc import Integrations
from src.pyport.logging import configure_logging, logger
from src.pyport.migrations.migrations_api_svc import Migrations
from src.pyport.organization.organization_api_svc import Organizations
from src.pyport.pages.pages_api_svc import Pages
from src.pyport.retry import RetryConfig, RetryStrategy
from src.pyport.roles.roles_api_svc import Roles
from src.pyport.scorecards.scorecards_api_svc import Scorecards
from src.pyport.search.search_api_svc import Search
from src.pyport.sidebars.sidebars_api_svc import Sidebars
from src.pyport.teams.teams_api_svc import Teams
from src.pyport.users.users_api_svc import Users


class PortClient:
    """
    Main client for interacting with the Port API.

    This class provides a unified interface for all Port API operations,
    handling authentication, request management, and error handling.
    It exposes various service classes as properties for accessing
    different parts of the API.

    Attributes:
        blueprints: Access to blueprint-related operations
        entities: Access to entity-related operations
        actions: Access to action-related operations
        action_runs: Access to action run-related operations
        pages: Access to page-related operations
        integrations: Access to integration-related operations
        organizations: Access to organization-related operations
        teams: Access to team-related operations
        users: Access to user-related operations
        roles: Access to role-related operations
        audit: Access to audit-related operations
        migrations: Access to migration-related operations
        search: Access to search-related operations
        sidebars: Access to sidebar-related operations
        checklist: Access to checklist-related operations
        apps: Access to app-related operations
        scorecards: Access to scorecard-related operations

    Examples:
        >>> # Create a client
        >>> client = PortClient(
        ...     client_id="your-client-id",
        ...     client_secret="your-client-secret"
        ... )
        >>>
        >>> # Get all blueprints
        >>> blueprints = client.blueprints.get_blueprints()
        >>>
        >>> # Get a specific entity
        >>> entity = client.entities.get_entity("service", "my-service")
    """

    def __init__(self, client_id: str, client_secret: str, us_region: bool = False,
                 auto_refresh: bool = True, refresh_interval: int = 900,
                 log_level: int = logging.INFO, log_format: Optional[str] = None,
                 log_handler: Optional[logging.Handler] = None,
                 # Retry configuration
                 max_retries: int = 3,
                 retry_delay: float = 1.0,
                 max_delay: float = 10.0,
                 retry_strategy: Union[str, RetryStrategy] = RetryStrategy.EXPONENTIAL,
                 retry_jitter: bool = True,
                 retry_status_codes: Optional[Set[int]] = None,
                 retry_on: Optional[Union[Type[Exception], Set[Type[Exception]]]] = None,
                 idempotent_methods: Optional[Set[str]] = None,
                 # Testing configuration
                 skip_auth: bool = False):
        """
        Initialize the PortClient.

        Args:
            client_id: API client ID obtained from Port.
            client_secret: API client secret obtained from Port.
            us_region: Whether to use the US region API URL (default: False).
                Set to True if your Port instance is in the US region.
            auto_refresh: If True, a background thread will refresh the token periodically (default: True).
                Set to False if you want to manage token refresh manually.
            refresh_interval: Token refresh interval in seconds (default: 900 sec = 15 minutes).
                Tokens typically expire after 30 minutes, so refreshing every 15 minutes is recommended.
            log_level: The logging level to use (default: logging.INFO).
                Use logging.DEBUG for more detailed logs including request/response information.
            log_format: The format string to use for log messages (default: None).
                If None, a default format will be used: "%(asctime)s - %(name)s - %(levelname)s - %(message)s".
            log_handler: A logging handler to use (default: None).
                If None, a StreamHandler will be created that outputs to stderr.
            max_retries: Maximum number of retry attempts for transient errors (default: 3).
                Set to 0 to disable retries.
            retry_delay: Initial delay between retries in seconds (default: 1.0).
                This delay will be adjusted based on the retry strategy.
            max_delay: Maximum delay between retries in seconds (default: 10.0).
                No retry will wait longer than this, regardless of the strategy.
            retry_strategy: Strategy for calculating retry delays (default: RetryStrategy.EXPONENTIAL).
                Options: CONSTANT, LINEAR, EXPONENTIAL, FIBONACCI.
            retry_jitter: Whether to add random jitter to retry delays (default: True).
                Helps prevent thundering herd problems when multiple clients retry simultaneously.
            retry_status_codes: HTTP status codes that should trigger retries (default: {429, 500, 502, 503, 504}).
                Only applies to status codes returned by the API.
            retry_on: Exception types or a function that returns True if the exception should be retried.
                If None, uses default logic based on exception type and status code.
            idempotent_methods: HTTP methods that are safe to retry (default: {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}).
                Non-idempotent methods like POST are not retried by default to avoid duplicate operations.
            skip_auth: Whether to skip authentication (default: False).
                This is primarily used for testing.
        """
        # Set up basic client properties
        self.api_url = PORT_API_US_URL if us_region else PORT_API_URL

        # Configure components
        self._setup_logging(log_level, log_format, log_handler)
        self._setup_retry_config(max_retries, retry_delay, max_delay, retry_strategy, retry_jitter,
                                 retry_status_codes, retry_on, idempotent_methods)

        # Initialize authentication manager
        self._auth_manager = AuthManager(
            client_id=client_id,
            client_secret=client_secret,
            api_url=self.api_url,
            auto_refresh=auto_refresh,
            refresh_interval=refresh_interval,
            skip_auth=skip_auth
        )

        # For backward compatibility
        self.token = self._auth_manager.token

        # Initialize session with the token from the auth manager
        self._init_session()

        # Initialize request manager
        self._request_manager = RequestManager(
            api_url=self.api_url,
            session=self._session,
            retry_config=self.retry_config
        )

        # Initialize API service classes
        self._init_sub_clients()

    def _setup_logging(self, log_level: int, log_format: Optional[str], log_handler: Optional[logging.Handler]) -> None:
        """
        Set up logging configuration.

        Args:
            log_level: The logging level to use.
            log_format: The format string to use for log messages.
            log_handler: A logging handler to use.
        """
        configure_logging(level=log_level, format_string=log_format, handler=log_handler)
        self._logger = logger

    def _setup_retry_config(self, max_retries: int, retry_delay: float, max_delay: float,
                            retry_strategy: Union[str, RetryStrategy], retry_jitter: bool,
                            retry_status_codes: Optional[Set[int]],
                            retry_on: Optional[Union[Type[Exception], Set[Type[Exception]]]],
                            idempotent_methods: Optional[Set[str]]
                            ) -> None:
        """
        Set up retry configuration.

        Args:
            max_retries: Maximum number of retry attempts.
            retry_delay: Initial delay between retries in seconds.
            max_delay: Maximum delay between retries in seconds.
            retry_strategy: Strategy for calculating retry delays.
            retry_jitter: Whether to add random jitter to retry delays.
            retry_status_codes: HTTP status codes that should trigger retries.
            retry_on: Exception types or function that determines if an exception should be retried.
            idempotent_methods: HTTP methods that are safe to retry.
        """
        # Convert string strategy to enum if needed
        if isinstance(retry_strategy, str):
            retry_strategy = RetryStrategy(retry_strategy)

        # Create retry configuration
        self.retry_config = RetryConfig(
            max_retries=max_retries,
            retry_delay=retry_delay,
            max_delay=max_delay,
            strategy=retry_strategy,
            jitter=retry_jitter,
            retry_status_codes=retry_status_codes or {429, 500, 502, 503, 504},
            retry_on=retry_on,
            idempotent_methods=idempotent_methods or {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"},
            retry_hook=self._request_manager._log_retry_attempt if hasattr(self, '_request_manager') else None
        )

    def _init_session(self):
        """Initialize the HTTP session."""
        self._session = requests.Session()
        self._session.headers.update(GENERIC_HEADERS)
        self._session.headers.update({"Authorization": f"Bearer {self._auth_manager.token}"})

    def default_headers(self) -> dict:
        """Return a copy of the default request headers."""
        return dict(self._session.headers)

    def _init_sub_clients(self):
        """Initializes all API sub-clients."""
        # Map of attribute names to their corresponding service classes
        service_classes = {
            'blueprints': Blueprints,
            'entities': Entities,
            'actions': Actions,
            'pages': Pages,
            'integrations': Integrations,
            'action_runs': ActionRuns,
            'organizations': Organizations,
            'teams': Teams,
            'users': Users,
            'roles': Roles,
            'audit': Audit,
            'migrations': Migrations,
            'search': Search,
            'sidebars': Sidebars,
            'checklist': Checklist,
            'apps': Apps,
            'scorecards': Scorecards,
        }

        # Initialize each service class
        for attr_name, service_class in service_classes.items():
            setattr(self, attr_name, service_class(self))

        # Future services (commented out for now)
        # 'webhooks': Webhooks,
        # 'data_sources': DataSources,

    def make_request(self, method: str, endpoint: str, retries: int = None, retry_delay: float = None,
                     correlation_id: str = None, **kwargs) -> requests.Response:
        """
        Make an HTTP request to the API with error handling and retry logic.

        This method delegates to the request manager's make_request method.

        Args:
            method: HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            endpoint: API endpoint appended to the base URL.
            retries: Number of retry attempts for transient errors.
            retry_delay: Initial delay between retries in seconds.
            correlation_id: A correlation ID for tracking the request.
            **kwargs: Additional parameters passed to requests.request.

        Returns:
            A requests.Response object containing the API response.

        Raises:
            PortApiError: If the request fails.
        """
        return self._request_manager.make_request(
            method=method,
            endpoint=endpoint,
            retries=retries,
            retry_delay=retry_delay,
            correlation_id=correlation_id,
            **kwargs
        )

    # Private methods for backward compatibility

    def _get_local_env_cred(self):
        """Get client credentials from environment variables."""
        return self._auth_manager._get_local_env_cred()

    def _get_access_token(self):
        """Get an access token from the API."""
        return self._auth_manager._get_access_token()

    def _prepare_auth_request(self):
        """Prepare the authentication request."""
        return self._auth_manager._prepare_auth_request()

    def _handle_auth_response(self, response, endpoint):
        """Handle the authentication response."""
        return self._auth_manager._handle_auth_response(response, endpoint)

    def _extract_token_from_response(self, response_data, endpoint):
        """Extract the access token from the response data."""
        return self._auth_manager._extract_token_from_response(response_data, endpoint)

    def _handle_unexpected_auth_error(self, e, correlation_id):
        """Handle unexpected errors during authentication."""
        return self._auth_manager._handle_unexpected_auth_error(e, correlation_id)

    def _validate_credentials(self, client_id, client_secret, source):
        """Validate that client credentials are present."""
        return self._auth_manager._validate_credentials(client_id, client_secret, source)

    def _handle_response(self, response, endpoint, method, correlation_id):
        """Handle the response, returning it if successful or raising an appropriate exception."""
        return self._request_manager._handle_response(response, endpoint, method, correlation_id)

    def _make_single_request(self, method, url, endpoint, correlation_id=None, **kwargs):
        """Make a single HTTP request and handle the response."""
        return self._request_manager._make_single_request(method, url, endpoint, correlation_id, **kwargs)
