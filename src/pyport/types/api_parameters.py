"""
Type definitions for API parameters.

This module defines TypedDict classes for API parameters,
making it easier to understand the structure of data sent to the API.
"""
from typing import Dict, List, Optional, Any, TypedDict, Union, Literal


# Common Types
class PaginationParams(TypedDict, total=False):
    """Pagination parameters for list endpoints."""
    page: int
    per_page: int


# Blueprint Parameters
class BlueprintPropertyParams(TypedDict, total=False):
    """Parameters for a blueprint property."""
    type: str
    title: str
    description: Optional[str]
    format: Optional[str]
    default: Any
    enum: Optional[List[str]]
    required: bool


class BlueprintRelationParams(TypedDict, total=False):
    """Parameters for a blueprint relation."""
    title: str
    description: Optional[str]
    target: str
    required: bool
    many: bool


class BlueprintParams(TypedDict, total=False):
    """Parameters for creating or updating a blueprint."""
    identifier: str
    title: str
    description: Optional[str]
    icon: Optional[str]
    properties: Dict[str, BlueprintPropertyParams]
    relations: Dict[str, BlueprintRelationParams]
    calculationProperties: Dict[str, Any]


# Entity Parameters
class EntityPropertyParams(TypedDict, total=False):
    """Parameters for an entity property."""
    value: Any


class EntityRelationParams(TypedDict, total=False):
    """Parameters for an entity relation."""
    identifier: str
    title: Optional[str]


class EntityParams(TypedDict, total=False):
    """Parameters for creating or updating an entity."""
    identifier: str
    title: str
    properties: Dict[str, Union[EntityPropertyParams, Any]]
    relations: Dict[str, Union[EntityRelationParams, List[EntityRelationParams], Any]]


class EntityBulkParams(TypedDict):
    """Parameters for bulk entity operations."""
    entities: List[EntityParams]


# Entity Search Parameters
class EntitySearchFilter(TypedDict, total=False):
    """Filter parameters for entity search."""
    blueprint: Optional[str]
    title: Optional[str]
    identifier: Optional[str]


class EntitySearchSort(TypedDict, total=False):
    """Sort parameters for entity search."""
    field: str
    direction: Literal["ASC", "DESC"]


class EntitySearchParams(TypedDict, total=False):
    """Parameters for entity search."""
    query: Optional[str]
    filter: Optional[EntitySearchFilter]
    sort: Optional[List[EntitySearchSort]]
    page: Optional[int]
    per_page: Optional[int]


# Action Parameters
class ActionTriggerParams(TypedDict, total=False):
    """Parameters for an action trigger."""
    type: str
    entity: Optional[str]
    blueprint: Optional[str]
    schedule: Optional[Dict[str, Any]]


class ActionInvocationMethodParams(TypedDict, total=False):
    """Parameters for an action invocation method."""
    type: str
    url: Optional[str]
    method: Optional[str]
    agent: Optional[str]


class ActionParams(TypedDict, total=False):
    """Parameters for creating or updating an action."""
    identifier: str
    title: str
    description: Optional[str]
    blueprint: str
    trigger: ActionTriggerParams
    invocationMethod: ActionInvocationMethodParams


# User Parameters
class UserParams(TypedDict, total=False):
    """Parameters for creating or updating a user."""
    email: str
    firstName: str
    lastName: str
    role: str


# Team Parameters
class TeamParams(TypedDict, total=False):
    """Parameters for creating or updating a team."""
    name: str
    description: Optional[str]
    members: List[str]


# Role Parameters
class RoleParams(TypedDict, total=False):
    """Parameters for creating or updating a role."""
    name: str
    description: Optional[str]
    permissions: List[str]


# Organization Parameters
class OrganizationParams(TypedDict, total=False):
    """Parameters for creating or updating an organization."""
    name: str
    description: Optional[str]
    domain: Optional[str]
    logo: Optional[str]


# Integration Parameters
class IntegrationParams(TypedDict, total=False):
    """Parameters for creating or updating an integration."""
    name: str
    description: Optional[str]
    type: str
    config: Dict[str, Any]


# Webhook Parameters
class WebhookParams(TypedDict, total=False):
    """Parameters for creating or updating a webhook."""
    name: str
    description: Optional[str]
    url: str
    secret: Optional[str]
    events: List[str]


# Page Parameters
class PageParams(TypedDict, total=False):
    """Parameters for creating or updating a page."""
    name: str
    description: Optional[str]
    blueprint: str
    content: Dict[str, Any]


# Scorecard Parameters
class ScorecardRuleParams(TypedDict, total=False):
    """Parameters for a scorecard rule."""
    name: str
    description: Optional[str]
    condition: Dict[str, Any]
    score: int


class ScorecardParams(TypedDict, total=False):
    """Parameters for creating or updating a scorecard."""
    name: str
    description: Optional[str]
    blueprint: str
    rules: List[ScorecardRuleParams]


# Sidebar Parameters
class SidebarItemParams(TypedDict, total=False):
    """Parameters for a sidebar item."""
    type: str
    title: str
    icon: Optional[str]
    link: Optional[str]


class SidebarParams(TypedDict, total=False):
    """Parameters for creating or updating a sidebar."""
    name: str
    description: Optional[str]
    blueprint: str
    items: List[SidebarItemParams]


# App Parameters
class AppParams(TypedDict, total=False):
    """Parameters for creating or updating an app."""
    name: str
    description: Optional[str]
    type: str
    config: Dict[str, Any]


# Checklist Parameters
class ChecklistItemParams(TypedDict, total=False):
    """Parameters for creating or updating a checklist item."""
    name: str
    description: Optional[str]
    blueprint: str
    assignee: Optional[str]


# Data Source Parameters
class DataSourceParams(TypedDict, total=False):
    """Parameters for creating or updating a data source."""
    name: str
    description: Optional[str]
    type: str
    config: Dict[str, Any]
