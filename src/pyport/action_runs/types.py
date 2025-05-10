"""
Type definitions for the action runs API.
"""
from typing import Optional, TypedDict


class ActionRun(TypedDict, total=False):
    """Type definition for a action run."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
