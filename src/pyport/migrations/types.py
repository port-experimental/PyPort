"""
Type definitions for the migrations API.
"""
from typing import Optional, TypedDict


class Migration(TypedDict, total=False):
    """Type definition for a migration."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
