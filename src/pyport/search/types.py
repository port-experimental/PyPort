"""
Type definitions for the search API.
"""
from typing import Optional, TypedDict


class SearchResult(TypedDict, total=False):
    """Type definition for a search."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
