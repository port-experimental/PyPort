"""
Type definitions for the pages API.
"""
from typing import Optional, TypedDict


class Page(TypedDict, total=False):
    """Type definition for a page."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
