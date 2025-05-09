"""
Type definitions for the apps API.
"""
from typing import Optional, TypedDict


class App(TypedDict, total=False):
    """Type definition for a app."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
