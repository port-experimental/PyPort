"""
Tests for the type stubs.

These tests verify that the type stubs are correctly defined and match the runtime behavior.
"""

import unittest
import os
import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, get_type_hints

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

from pyport.client.client import PortClient
from pyport.blueprints.blueprint_api_svc import Blueprints
from pyport.entities.entities_api_svc import Entities
from pyport.services.base_api_service import BaseAPIService


class TestTypeStubs(unittest.TestCase):
    """Test cases for the type stubs."""

    def test_client_stub_exists(self):
        """Test that the client.pyi stub file exists."""
        stub_path = os.path.join(PROJECT_ROOT, "src", "pyport", "client", "client.pyi")
        self.assertTrue(os.path.exists(stub_path), f"Stub file {stub_path} does not exist")

    def test_init_stub_exists(self):
        """Test that the __init__.pyi stub file exists."""
        stub_path = os.path.join(PROJECT_ROOT, "src", "pyport", "__init__.pyi")
        self.assertTrue(os.path.exists(stub_path), f"Stub file {stub_path} does not exist")

    def test_blueprints_stub_exists(self):
        """Test that the blueprint_api_svc.pyi stub file exists."""
        stub_path = os.path.join(PROJECT_ROOT, "src", "pyport", "blueprints", "blueprint_api_svc.pyi")
        self.assertTrue(os.path.exists(stub_path), f"Stub file {stub_path} does not exist")

    def test_entities_stub_exists(self):
        """Test that the entities_api_svc.pyi stub file exists."""
        stub_path = os.path.join(PROJECT_ROOT, "src", "pyport", "entities", "entities_api_svc.pyi")
        self.assertTrue(os.path.exists(stub_path), f"Stub file {stub_path} does not exist")

    def test_base_api_service_stub_exists(self):
        """Test that the base_api_service.pyi stub file exists."""
        stub_path = os.path.join(PROJECT_ROOT, "src", "pyport", "services", "base_api_service.pyi")
        self.assertTrue(os.path.exists(stub_path), f"Stub file {stub_path} does not exist")

    def test_types_stub_exists(self):
        """Test that the types/__init__.pyi stub file exists."""
        stub_path = os.path.join(PROJECT_ROOT, "src", "pyport", "types", "__init__.pyi")
        self.assertTrue(os.path.exists(stub_path), f"Stub file {stub_path} does not exist")

    def test_client_property_types(self):
        """Test that the client properties have correct type annotations."""
        # Create a client instance
        client = PortClient(client_id="test", client_secret="test", skip_auth=True)

        # Check that the properties return the correct types
        self.assertIsInstance(client.blueprints, Blueprints)
        self.assertIsInstance(client.entities, Entities)

        # Check the property annotations in the class definition
        # This is a bit of a hack, but it works for testing
        property_obj = PortClient.__dict__['blueprints']
        self.assertEqual(property_obj.fget.__annotations__['return'], Blueprints)

        property_obj = PortClient.__dict__['entities']
        self.assertEqual(property_obj.fget.__annotations__['return'], Entities)

    def test_base_api_service_method_types(self):
        """Test that the BaseAPIService methods have correct type annotations."""
        # Get the method object
        method = BaseAPIService.get_all

        # Check the annotations directly
        annotations = method.__annotations__

        # Check the parameter types
        self.assertEqual(annotations.get('page'), Optional[int])
        self.assertEqual(annotations.get('per_page'), Optional[int])

        # Check the return type (should be a list of dictionaries)
        return_type = annotations.get('return')
        self.assertEqual(return_type, List[Dict[str, Any]])


if __name__ == "__main__":
    unittest.main()
