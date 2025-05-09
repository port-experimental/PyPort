"""
Type definitions for the roles API.
"""
from typing import Optional, TypedDict


class Role(TypedDict, total=False):
    """Type definition for a role."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
