"""
Type definitions for the users API.
"""
from typing import Optional, TypedDict


class User(TypedDict, total=False):
    """Type definition for a user."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
