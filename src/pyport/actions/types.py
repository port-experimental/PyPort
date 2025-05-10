"""
Type definitions for the actions API.
"""
from typing import Optional, TypedDict


class Action(TypedDict, total=False):
    """Type definition for a action."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
