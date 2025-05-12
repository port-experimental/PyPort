"""
Main client module for the Port API.

This module provides the PortClient class, which is the main entry point
for interacting with the Port API.
"""

import logging
import requests
from typing import Optional, Set, Type, Union

from ..action_runs.action_runs_api_svc import ActionRuns
from ..actions.actions_api_svc import Actions
from ..apps.apps_api_svc import Apps
from ..audit.audit_api_svc import Audit
from ..blueprints.blueprint_api_svc import Blueprints
from ..checklist.checklist_api_svc import Checklist
from .auth import AuthManager
from .request import RequestManager
from ..constants import PORT_API_URL, PORT_API_US_URL, GENERIC_HEADERS
from ..entities.entities_api_svc import Entities
# PortApiError is not used directly
from ..integrations.integrations_api_svc import Integrations
from ..logging import configure_logging, logger
from ..migrations.migrations_api_svc import Migrations
from ..organization.organization_api_svc import Organizations
from ..pages.pages_api_svc import Pages
from ..retry import RetryConfig, RetryStrategy
from ..roles.roles_api_svc import Roles
from ..scorecards.scorecards_api_svc import Scorecards
from ..search.search_api_svc import Search
from ..sidebars.sidebars_api_svc import Sidebars
from ..teams.teams_api_svc import Teams
from ..users.users_api_svc import Users


class PortClient:
    """
    Main client for interacting with the Port API.

    This class provides a unified interface for all Port API operations,
    handling authentication, request management, and error handling.
    It exposes various service classes as properties for accessing
    different parts of the API.

    Attributes:
        blueprints (Blueprints): Access to blueprint-related operations.
            Use this to create, read, update, and delete blueprints.
            Example: client.blueprints.get_blueprint("service")

        entities (Entities): Access to entity-related operations.
            Use this to create, read, update, and delete entities.
            Example: client.entities.get_entity("service", "my-service")

        actions (Actions): Access to action-related operations.
            Use this to create, read, update, and delete actions.
            Example: client.actions.get_action("action-id")

        action_runs (ActionRuns): Access to action run-related operations.
            Use this to create, read, update, and delete action runs.
            Example: client.action_runs.get_action_run("run-id")

        pages (Pages): Access to page-related operations.
            Use this to create, read, update, and delete pages.
            Example: client.pages.get_page("blueprint-id", "page-id")

        integrations (Integrations): Access to integration-related operations.
            Use this to create, read, update, and delete integrations.
            Example: client.integrations.get_integration("integration-id")

        organizations (Organizations): Access to organization-related operations.
            Use this to read and update organization settings.
            Example: client.organizations.get_organization()

        teams (Teams): Access to team-related operations.
            Use this to create, read, update, and delete teams.
            Example: client.teams.get_team("team-id")

        users (Users): Access to user-related operations.
            Use this to create, read, update, and delete users.
            Example: client.users.get_user("user-id")

        roles (Roles): Access to role-related operations.
            Use this to create, read, update, and delete roles.
            Example: client.roles.get_role("role-id")

        audit (Audit): Access to audit-related operations.
            Use this to retrieve audit logs.
            Example: client.audit.get_audit_logs()

        migrations (Migrations): Access to migration-related operations.
            Use this to create, read, update, and delete migrations.
            Example: client.migrations.get_migration("migration-id")

        search (Search): Access to search-related operations.
            Use this to search for entities.
            Example: client.search.search_entities({"query": "service"})

        sidebars (Sidebars): Access to sidebar-related operations.
            Use this to create, read, update, and delete sidebars.
            Example: client.sidebars.get_sidebar("sidebar-id")

        checklist (Checklist): Access to checklist-related operations.
            Use this to create, read, update, and delete checklists.
            Example: client.checklist.get_checklist("checklist-id")

        apps (Apps): Access to app-related operations.
            Use this to create, read, update, and delete apps.
            Example: client.apps.get_app("app-id")

        scorecards (Scorecards): Access to scorecard-related operations.
            Use this to create, read, update, and delete scorecards.
            Example: client.scorecards.get_scorecard("blueprint-id", "scorecard-id")

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
        >>>
        >>> # Create a new blueprint
        >>> new_blueprint = client.blueprints.create_blueprint({
        ...     "identifier": "microservice",
        ...     "title": "Microservice",
        ...     "properties": {
        ...         "language": {
        ...             "type": "string",
        ...             "title": "Language",
        ...             "enum": ["Python", "JavaScript", "Java", "Go"]
        ...         }
        ...     }
        ... })
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
        # Initialize each service class with proper type annotations
        self._blueprints: Blueprints = Blueprints(self)
        self._entities: Entities = Entities(self)
        self._actions: Actions = Actions(self)
        self._pages: Pages = Pages(self)
        self._integrations: Integrations = Integrations(self)
        self._action_runs: ActionRuns = ActionRuns(self)
        self._organizations: Organizations = Organizations(self)
        self._teams: Teams = Teams(self)
        self._users: Users = Users(self)
        self._roles: Roles = Roles(self)
        self._audit: Audit = Audit(self)
        self._migrations: Migrations = Migrations(self)
        self._search: Search = Search(self)
        self._sidebars: Sidebars = Sidebars(self)
        self._checklist: Checklist = Checklist(self)
        self._apps: Apps = Apps(self)
        self._scorecards: Scorecards = Scorecards(self)

        # Future services (commented out for now)
        # self._webhooks: Webhooks = Webhooks(self)
        # self._data_sources: DataSources = DataSources(self)

    # Property decorators for API services with explicit return types
    @property
    def blueprints(self) -> Blueprints:
        """Access blueprint-related operations."""
        return self._blueprints

    @property
    def entities(self) -> Entities:
        """Access entity-related operations."""
        return self._entities

    @property
    def actions(self) -> Actions:
        """Access action-related operations."""
        return self._actions

    @property
    def pages(self) -> Pages:
        """Access page-related operations."""
        return self._pages

    @property
    def integrations(self) -> Integrations:
        """Access integration-related operations."""
        return self._integrations

    @property
    def action_runs(self) -> ActionRuns:
        """Access action run-related operations."""
        return self._action_runs

    @property
    def organizations(self) -> Organizations:
        """Access organization-related operations."""
        return self._organizations

    @property
    def teams(self) -> Teams:
        """Access team-related operations."""
        return self._teams

    @property
    def users(self) -> Users:
        """Access user-related operations."""
        return self._users

    @property
    def roles(self) -> Roles:
        """Access role-related operations."""
        return self._roles

    @property
    def audit(self) -> Audit:
        """Access audit-related operations."""
        return self._audit

    @property
    def migrations(self) -> Migrations:
        """Access migration-related operations."""
        return self._migrations

    @property
    def search(self) -> Search:
        """Access search-related operations."""
        return self._search

    @property
    def sidebars(self) -> Sidebars:
        """Access sidebar-related operations."""
        return self._sidebars

    @property
    def checklist(self) -> Checklist:
        """Access checklist-related operations."""
        return self._checklist

    @property
    def apps(self) -> Apps:
        """Access app-related operations."""
        return self._apps

    @property
    def scorecards(self) -> Scorecards:
        """Access scorecard-related operations."""
        return self._scorecards

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
