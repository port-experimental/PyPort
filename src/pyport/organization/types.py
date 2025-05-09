"""
Type definitions for the organization API.
"""
from typing import Optional, TypedDict


class Organization(TypedDict, total=False):
    """Type definition for a organization."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
