"""
Type definitions for the data sources API.
"""
from typing import Optional, TypedDict


class DataSource(TypedDict, total=False):
    """Type definition for a data source."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
