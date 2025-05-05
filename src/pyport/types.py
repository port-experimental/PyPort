"""
Type definitions for the PyPort client library.

This module defines TypedDict classes for API responses and parameters,
making it easier to understand the structure of data flowing through the library.
"""
from typing import Dict, List, Optional, Union, Any, TypedDict, Literal


# Common Types
class Pagination(TypedDict, total=False):
    """Pagination information returned by list endpoints."""
    page: int
    per_page: int
    total: int
    total_pages: int


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


class Blueprint(TypedDict, total=False):
    """A blueprint definition."""
    identifier: str
    title: str
    description: Optional[str]
    icon: Optional[str]
    schema: Dict[str, Any]
    properties: Dict[str, BlueprintProperty]
    relations: Dict[str, Any]
    calculationProperties: Dict[str, Any]
    createdAt: str
    createdBy: str
    updatedAt: str
    updatedBy: str


class BlueprintResponse(TypedDict):
    """Response from a blueprint endpoint."""
    blueprint: Blueprint


class BlueprintsResponse(TypedDict):
    """Response from the blueprints list endpoint."""
    blueprints: List[Blueprint]
    pagination: Optional[Pagination]


# Entity Types
class EntityProperty(TypedDict, total=False):
    """A property value in an entity."""
    value: Any
    type: str


class Entity(TypedDict, total=False):
    """An entity definition."""
    identifier: str
    title: str
    properties: Dict[str, EntityProperty]
    relations: Dict[str, Any]
    createdAt: str
    createdBy: str
    updatedAt: str
    updatedBy: str
    blueprint: str


class EntityResponse(TypedDict):
    """Response from an entity endpoint."""
    entity: Entity


class EntitiesResponse(TypedDict):
    """Response from the entities list endpoint."""
    entities: List[Entity]
    pagination: Optional[Pagination]


# Action Types
class Action(TypedDict, total=False):
    """An action definition."""
    identifier: str
    title: str
    description: Optional[str]
    blueprint: str
    trigger: Dict[str, Any]
    invocationMethod: Dict[str, Any]
    createdAt: str
    createdBy: str
    updatedAt: str
    updatedBy: str


class ActionResponse(TypedDict):
    """Response from an action endpoint."""
    action: Action


class ActionsResponse(TypedDict):
    """Response from the actions list endpoint."""
    actions: List[Action]
    pagination: Optional[Pagination]


# Action Run Types
class ActionRun(TypedDict, total=False):
    """An action run definition."""
    id: str
    action: str
    status: str
    trigger: Dict[str, Any]
    createdAt: str
    createdBy: str
    updatedAt: str
    updatedBy: str
    logs: Optional[List[Dict[str, Any]]]


class ActionRunResponse(TypedDict):
    """Response from an action run endpoint."""
    run: ActionRun


class ActionRunsResponse(TypedDict):
    """Response from the action runs list endpoint."""
    runs: List[ActionRun]
    pagination: Optional[Pagination]


# User Types
class User(TypedDict, total=False):
    """A user definition."""
    id: str
    email: str
    firstName: str
    lastName: str
    status: str
    role: str
    createdAt: str
    updatedAt: str


class UserResponse(TypedDict):
    """Response from a user endpoint."""
    user: User


class UsersResponse(TypedDict):
    """Response from the users list endpoint."""
    users: List[User]
    pagination: Optional[Pagination]


# Team Types
class Team(TypedDict, total=False):
    """A team definition."""
    id: str
    name: str
    description: Optional[str]
    members: List[str]
    createdAt: str
    updatedAt: str


class TeamResponse(TypedDict):
    """Response from a team endpoint."""
    team: Team


class TeamsResponse(TypedDict):
    """Response from the teams list endpoint."""
    teams: List[Team]
    pagination: Optional[Pagination]


# Role Types
class Role(TypedDict, total=False):
    """A role definition."""
    id: str
    name: str
    description: Optional[str]
    permissions: List[str]
    createdAt: str
    updatedAt: str


class RoleResponse(TypedDict):
    """Response from a role endpoint."""
    role: Role


class RolesResponse(TypedDict):
    """Response from the roles list endpoint."""
    roles: List[Role]
    pagination: Optional[Pagination]


# Generic Types
JsonDict = Dict[str, Any]
JsonList = List[JsonDict]
JsonValue = Union[str, int, float, bool, None, JsonDict, List[Any]]

# HTTP Method Types
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
