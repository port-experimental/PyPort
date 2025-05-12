"""
Type definitions for API responses.

This module defines TypedDict classes for API responses,
making it easier to understand the structure of data returned by the API.
"""
from typing import Dict, List, Optional, Any, TypedDict, Union


# Common Types
class Pagination(TypedDict, total=False):
    """Pagination information returned by list endpoints."""
    page: int
    per_page: int
    total: int
    total_pages: int


# Base Resource Types
class BaseResource(TypedDict, total=False):
    """Base type for all resources."""
    id: str
    identifier: str
    title: str
    name: str
    description: Optional[str]
    createdAt: str
    createdBy: str
    updatedAt: str
    updatedBy: str


# Blueprint Types
class BlueprintProperty(TypedDict, total=False):
    """A property definition in a blueprint."""
    type: str
    title: str
    description: Optional[str]
    format: Optional[str]
    default: Any
    enum: Optional[List[str]]
    required: bool


class BlueprintRelation(TypedDict, total=False):
    """A relation definition in a blueprint."""
    title: str
    description: Optional[str]
    target: str
    required: bool
    many: bool


class Blueprint(BaseResource, total=False):
    """A blueprint definition."""
    icon: Optional[str]
    schema: Dict[str, Any]
    properties: Dict[str, BlueprintProperty]
    relations: Dict[str, BlueprintRelation]
    calculationProperties: Dict[str, Any]


# Entity Types
class EntityPropertyValue(TypedDict, total=False):
    """A property value in an entity."""
    value: Any
    type: str


class EntityRelationValue(TypedDict, total=False):
    """A relation value in an entity."""
    identifier: str
    title: str
    blueprint: str


class Entity(BaseResource, total=False):
    """An entity definition."""
    blueprint: str
    properties: Dict[str, Union[EntityPropertyValue, Any]]
    relations: Dict[str, Union[EntityRelationValue, List[EntityRelationValue], Any]]


# Action Types
class ActionTrigger(TypedDict, total=False):
    """An action trigger definition."""
    type: str
    entity: Optional[str]
    blueprint: Optional[str]
    schedule: Optional[Dict[str, Any]]


class ActionInvocationMethod(TypedDict, total=False):
    """An action invocation method definition."""
    type: str
    url: Optional[str]
    method: Optional[str]
    agent: Optional[str]


class Action(BaseResource, total=False):
    """An action definition."""
    blueprint: str
    trigger: ActionTrigger
    invocationMethod: ActionInvocationMethod


# Action Run Types
class ActionRunLog(TypedDict, total=False):
    """A log entry for an action run."""
    timestamp: str
    message: str
    level: str


class ActionRun(BaseResource, total=False):
    """An action run definition."""
    action: str
    status: str
    trigger: Dict[str, Any]
    logs: Optional[List[ActionRunLog]]


# User Types
class User(BaseResource, total=False):
    """A user definition."""
    email: str
    firstName: str
    lastName: str
    status: str
    role: str


# Team Types
class Team(BaseResource, total=False):
    """A team definition."""
    members: List[str]


# Role Types
class Role(BaseResource, total=False):
    """A role definition."""
    permissions: List[str]


# Organization Types
class Organization(BaseResource, total=False):
    """An organization definition."""
    domain: Optional[str]
    logo: Optional[str]


# Integration Types
class Integration(BaseResource, total=False):
    """An integration definition."""
    type: str
    config: Dict[str, Any]
    status: str


# Webhook Types
class Webhook(BaseResource, total=False):
    """A webhook definition."""
    url: str
    secret: Optional[str]
    events: List[str]
    status: str


# Page Types
class Page(BaseResource, total=False):
    """A page definition."""
    blueprint: str
    content: Dict[str, Any]


# Scorecard Types
class Scorecard(BaseResource, total=False):
    """A scorecard definition."""
    blueprint: str
    rules: List[Dict[str, Any]]


# Sidebar Types
class Sidebar(BaseResource, total=False):
    """A sidebar definition."""
    blueprint: str
    items: List[Dict[str, Any]]


# App Types
class App(BaseResource, total=False):
    """An app definition."""
    type: str
    config: Dict[str, Any]
    status: str


# Checklist Types
class ChecklistItem(BaseResource, total=False):
    """A checklist item definition."""
    blueprint: str
    status: str
    assignee: Optional[str]


# Migration Types
class Migration(BaseResource, total=False):
    """A migration definition."""
    status: str
    details: Dict[str, Any]


# Audit Types
class AuditLog(BaseResource, total=False):
    """An audit log entry."""
    action: str
    resource: str
    resourceId: str
    details: Dict[str, Any]


# Data Source Types
class DataSource(BaseResource, total=False):
    """A data source definition."""
    type: str
    config: Dict[str, Any]
    status: str


# Response Types
class SingleResourceResponse(TypedDict, total=False):
    """A response containing a single resource."""
    pass


class ListResourceResponse(TypedDict, total=False):
    """A response containing a list of resources."""
    pagination: Optional[Pagination]


# Blueprint Response Types
class BlueprintResponse(SingleResourceResponse):
    """Response from a blueprint endpoint."""
    blueprint: Blueprint


class BlueprintsResponse(ListResourceResponse):
    """Response from the blueprints list endpoint."""
    blueprints: List[Blueprint]


# Entity Response Types
class EntityResponse(SingleResourceResponse):
    """Response from an entity endpoint."""
    entity: Entity


class EntitiesResponse(ListResourceResponse):
    """Response from the entities list endpoint."""
    entities: List[Entity]


# Action Response Types
class ActionResponse(SingleResourceResponse):
    """Response from an action endpoint."""
    action: Action


class ActionsResponse(ListResourceResponse):
    """Response from the actions list endpoint."""
    actions: List[Action]


# Action Run Response Types
class ActionRunResponse(SingleResourceResponse):
    """Response from an action run endpoint."""
    run: ActionRun


class ActionRunsResponse(ListResourceResponse):
    """Response from the action runs list endpoint."""
    runs: List[ActionRun]


# User Response Types
class UserResponse(SingleResourceResponse):
    """Response from a user endpoint."""
    user: User


class UsersResponse(ListResourceResponse):
    """Response from the users list endpoint."""
    users: List[User]


# Team Response Types
class TeamResponse(SingleResourceResponse):
    """Response from a team endpoint."""
    team: Team


class TeamsResponse(ListResourceResponse):
    """Response from the teams list endpoint."""
    teams: List[Team]


# Role Response Types
class RoleResponse(SingleResourceResponse):
    """Response from a role endpoint."""
    role: Role


class RolesResponse(ListResourceResponse):
    """Response from the roles list endpoint."""
    roles: List[Role]


# Organization Response Types
class OrganizationResponse(SingleResourceResponse):
    """Response from an organization endpoint."""
    organization: Organization


class OrganizationsResponse(ListResourceResponse):
    """Response from the organizations list endpoint."""
    organizations: List[Organization]


# Integration Response Types
class IntegrationResponse(SingleResourceResponse):
    """Response from an integration endpoint."""
    integration: Integration


class IntegrationsResponse(ListResourceResponse):
    """Response from the integrations list endpoint."""
    integrations: List[Integration]


# Webhook Response Types
class WebhookResponse(SingleResourceResponse):
    """Response from a webhook endpoint."""
    webhook: Webhook


class WebhooksResponse(ListResourceResponse):
    """Response from the webhooks list endpoint."""
    webhooks: List[Webhook]


# Page Response Types
class PageResponse(SingleResourceResponse):
    """Response from a page endpoint."""
    page: Page


class PagesResponse(ListResourceResponse):
    """Response from the pages list endpoint."""
    pages: List[Page]


# Scorecard Response Types
class ScorecardResponse(SingleResourceResponse):
    """Response from a scorecard endpoint."""
    scorecard: Scorecard


class ScorecardsResponse(ListResourceResponse):
    """Response from the scorecards list endpoint."""
    scorecards: List[Scorecard]


# Sidebar Response Types
class SidebarResponse(SingleResourceResponse):
    """Response from a sidebar endpoint."""
    sidebar: Sidebar


class SidebarsResponse(ListResourceResponse):
    """Response from the sidebars list endpoint."""
    sidebars: List[Sidebar]


# App Response Types
class AppResponse(SingleResourceResponse):
    """Response from an app endpoint."""
    app: App


class AppsResponse(ListResourceResponse):
    """Response from the apps list endpoint."""
    apps: List[App]


# Checklist Response Types
class ChecklistItemResponse(SingleResourceResponse):
    """Response from a checklist item endpoint."""
    item: ChecklistItem


class ChecklistItemsResponse(ListResourceResponse):
    """Response from the checklist items list endpoint."""
    items: List[ChecklistItem]


# Migration Response Types
class MigrationResponse(SingleResourceResponse):
    """Response from a migration endpoint."""
    migration: Migration


class MigrationsResponse(ListResourceResponse):
    """Response from the migrations list endpoint."""
    migrations: List[Migration]


# Audit Response Types
class AuditLogResponse(SingleResourceResponse):
    """Response from an audit log endpoint."""
    log: AuditLog


class AuditLogsResponse(ListResourceResponse):
    """Response from the audit logs list endpoint."""
    logs: List[AuditLog]


# Data Source Response Types
class DataSourceResponse(SingleResourceResponse):
    """Response from a data source endpoint."""
    dataSource: DataSource


class DataSourcesResponse(ListResourceResponse):
    """Response from the data sources list endpoint."""
    dataSources: List[DataSource]
