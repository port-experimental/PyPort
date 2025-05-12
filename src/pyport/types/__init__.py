"""
Type definitions for the PyPort client library.

This module imports and re-exports all type definitions from the submodules.
"""
from typing import Dict, List, Union, Any, TypeVar

# Import types from api_responses and api_parameters
# These imports are used by other modules in the package
from .api_responses import EntityPropertyValue as EntityProperty
from .api_responses import (
    BaseResource, Blueprint, Entity, Team, Role, Organization, Pagination,
    BlueprintProperty, BlueprintResponse, BlueprintsResponse,
    EntityResponse, EntitiesResponse,
    Action, ActionResponse, ActionsResponse,
    ActionRun, ActionRunResponse, ActionRunsResponse
)
from .api_parameters import PaginationParams

# Re-export all types for external use
__all__ = [
    'EntityProperty', 'BaseResource', 'Blueprint', 'Entity', 'Team', 'Role',
    'Organization', 'Pagination', 'BlueprintProperty', 'BlueprintResponse',
    'BlueprintsResponse', 'EntityResponse', 'EntitiesResponse', 'Action',
    'ActionResponse', 'ActionsResponse', 'ActionRun', 'ActionRunResponse',
    'ActionRunsResponse', 'PaginationParams', 'JsonDict', 'JsonList', 'JsonValue'
]

# Generic Types
T = TypeVar('T')  # Generic type for resource items
R = TypeVar('R')  # Generic type for response objects

# JSON Types
JsonDict = Dict[str, Any]
JsonList = List[JsonDict]
JsonValue = Union[str, int, float, bool, None, JsonDict, List[Any]]
