"""
Type definitions for the blueprints API.
"""
from typing import Optional, TypedDict


class Blueprint(TypedDict, total=False):
    """Type definition for a blueprint."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
