"""
Type definitions for the integrations API.
"""
from typing import Optional, TypedDict


class Integration(TypedDict, total=False):
    """Type definition for a integration."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
