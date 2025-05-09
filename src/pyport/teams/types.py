"""
Type definitions for the teams API.
"""
from typing import Optional, TypedDict


class Team(TypedDict, total=False):
    """Type definition for a team."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
