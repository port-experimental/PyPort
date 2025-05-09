"""
Type definitions for the scorecards API.
"""
from typing import Optional, TypedDict


class Scorecard(TypedDict, total=False):
    """Type definition for a scorecard."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
