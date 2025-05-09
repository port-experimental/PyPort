"""
Type definitions for the checklist API.
"""
from typing import Optional, TypedDict


class ChecklistItem(TypedDict, total=False):
    """Type definition for a checklist."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
