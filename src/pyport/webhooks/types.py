"""
Type definitions for the webhooks API.
"""
from typing import Optional, TypedDict


class Webhook(TypedDict, total=False):
    """Type definition for a webhook."""
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    createdBy: str
    updatedBy: str
