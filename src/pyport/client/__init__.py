"""
Port API Client package.

This package provides the main client for interacting with the Port API.
It is split into multiple modules for better organization:

- auth.py: Authentication and token management
- request.py: Request handling and processing
- client.py: Main client class and initialization

The PortClient class is the main entry point for the library.
"""

from src.pyport.client.client import PortClient

__all__ = ["PortClient"]
