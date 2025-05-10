"""
Type definitions for the sidebars API.
"""
from typing import Optional, TypedDict


class Sidebar(TypedDict, total=False):
    """Type definition for a sidebar."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
