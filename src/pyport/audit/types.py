"""
Type definitions for the audit API.
"""
from typing import Optional, TypedDict


class AuditLog(TypedDict, total=False):
    """Type definition for a audit."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
