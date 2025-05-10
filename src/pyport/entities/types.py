"""
Type definitions for the entities API.
"""
from typing import Optional, TypedDict


class Entity(TypedDict, total=False):
    """Type definition for a entitie."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
