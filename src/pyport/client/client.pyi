"""Type stub file for the PortClient class."""

from typing import Dict, List, Optional, Set, Type, Union, Any
import logging
import requests

from ..action_runs.action_runs_api_svc import ActionRuns
from ..actions.actions_api_svc import Actions
from ..apps.apps_api_svc import Apps
from ..audit.audit_api_svc import Audit
from ..blueprints.blueprint_api_svc import Blueprints
from ..checklist.checklist_api_svc import Checklist
from ..client.auth import AuthManager
from ..client.request import RequestManager
from ..entities.entities_api_svc import Entities
from ..integrations.integrations_api_svc import Integrations
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
    """Main client for interacting with the Port API."""
    
    api_url: str
    retry_config: RetryConfig
    token: str
    
    _auth_manager: AuthManager
    _request_manager: RequestManager
    _session: requests.Session
    _logger: logging.Logger
    
    # Private service instances
    _blueprints: Blueprints
    _entities: Entities
    _actions: Actions
    _pages: Pages
    _integrations: Integrations
    _action_runs: ActionRuns
    _organizations: Organizations
    _teams: Teams
    _users: Users
    _roles: Roles
    _audit: Audit
    _migrations: Migrations
    _search: Search
    _sidebars: Sidebars
    _checklist: Checklist
    _apps: Apps
    _scorecards: Scorecards
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        us_region: bool = ...,
        auto_refresh: bool = ...,
        refresh_interval: int = ...,
        log_level: int = ...,
        log_format: Optional[str] = ...,
        log_handler: Optional[logging.Handler] = ...,
        max_retries: int = ...,
        retry_delay: float = ...,
        max_delay: float = ...,
        retry_strategy: Union[str, RetryStrategy] = ...,
        retry_jitter: bool = ...,
        retry_status_codes: Optional[Set[int]] = ...,
        retry_on: Optional[Union[Type[Exception], Set[Type[Exception]]]] = ...,
        idempotent_methods: Optional[Set[str]] = ...,
        skip_auth: bool = ...
    ) -> None: ...
    
    def _setup_logging(
        self,
        log_level: int,
        log_format: Optional[str],
        log_handler: Optional[logging.Handler]
    ) -> None: ...
    
    def _setup_retry_config(
        self,
        max_retries: int,
        retry_delay: float,
        max_delay: float,
        retry_strategy: Union[str, RetryStrategy],
        retry_jitter: bool,
        retry_status_codes: Optional[Set[int]],
        retry_on: Optional[Union[Type[Exception], Set[Type[Exception]]]],
        idempotent_methods: Optional[Set[str]]
    ) -> None: ...
    
    def _init_session(self) -> None: ...
    
    def default_headers(self) -> Dict[str, str]: ...
    
    def _init_sub_clients(self) -> None: ...
    
    # Property accessors for API services
    @property
    def blueprints(self) -> Blueprints: ...
    
    @property
    def entities(self) -> Entities: ...
    
    @property
    def actions(self) -> Actions: ...
    
    @property
    def pages(self) -> Pages: ...
    
    @property
    def integrations(self) -> Integrations: ...
    
    @property
    def action_runs(self) -> ActionRuns: ...
    
    @property
    def organizations(self) -> Organizations: ...
    
    @property
    def teams(self) -> Teams: ...
    
    @property
    def users(self) -> Users: ...
    
    @property
    def roles(self) -> Roles: ...
    
    @property
    def audit(self) -> Audit: ...
    
    @property
    def migrations(self) -> Migrations: ...
    
    @property
    def search(self) -> Search: ...
    
    @property
    def sidebars(self) -> Sidebars: ...
    
    @property
    def checklist(self) -> Checklist: ...
    
    @property
    def apps(self) -> Apps: ...
    
    @property
    def scorecards(self) -> Scorecards: ...
    
    def make_request(
        self,
        method: str,
        endpoint: str,
        retries: Optional[int] = ...,
        retry_delay: Optional[float] = ...,
        correlation_id: Optional[str] = ...,
        **kwargs
    ) -> requests.Response: ...
    
    # Backward compatibility methods
    def _get_local_env_cred(self) -> Dict[str, str]: ...
    
    def _get_access_token(self) -> str: ...
    
    def _prepare_auth_request(self) -> Dict[str, Any]: ...
    
    def _handle_auth_response(self, response: requests.Response, endpoint: str) -> Dict[str, Any]: ...
    
    def _extract_token_from_response(self, response_data: Dict[str, Any], endpoint: str) -> str: ...
    
    def _handle_unexpected_auth_error(self, e: Exception, correlation_id: Optional[str]) -> None: ...
    
    def _validate_credentials(self, client_id: str, client_secret: str, source: str) -> None: ...
    
    def _handle_response(
        self,
        response: requests.Response,
        endpoint: str,
        method: str,
        correlation_id: Optional[str]
    ) -> requests.Response: ...
    
    def _make_single_request(
        self,
        method: str,
        url: str,
        endpoint: str,
        correlation_id: Optional[str] = ...,
        **kwargs
    ) -> requests.Response: ...
