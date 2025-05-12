"""
Tests for the PortClient properties and type annotations.
"""

import unittest
from unittest.mock import MagicMock, patch

from pyport.client.client import PortClient
from pyport.actions.actions_api_svc import Actions
from pyport.action_runs.action_runs_api_svc import ActionRuns
from pyport.apps.apps_api_svc import Apps
from pyport.audit.audit_api_svc import Audit
from pyport.blueprints.blueprint_api_svc import Blueprints
from pyport.checklist.checklist_api_svc import Checklist
from pyport.entities.entities_api_svc import Entities
from pyport.integrations.integrations_api_svc import Integrations
from pyport.migrations.migrations_api_svc import Migrations
from pyport.organization.organization_api_svc import Organizations
from pyport.pages.pages_api_svc import Pages
from pyport.roles.roles_api_svc import Roles
from pyport.scorecards.scorecards_api_svc import Scorecards
from pyport.search.search_api_svc import Search
from pyport.sidebars.sidebars_api_svc import Sidebars
from pyport.teams.teams_api_svc import Teams
from pyport.users.users_api_svc import Users


class TestClientProperties(unittest.TestCase):
    """Test cases for the PortClient properties."""

    @patch('pyport.client.auth.AuthManager')
    @patch('pyport.client.request.RequestManager')
    @patch('requests.Session')
    def setUp(self, mock_session, mock_request_manager, mock_auth_manager):
        """Set up test fixtures."""
        # Mock the token property
        mock_auth_manager_instance = mock_auth_manager.return_value
        mock_auth_manager_instance.token = "test-token"
        
        # Create a client with mocked dependencies
        self.client = PortClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            skip_auth=True
        )
        
        # Replace the session with a mock
        self.client._session = mock_session.return_value
        
        # Replace the request manager with a mock
        self.client._request_manager = mock_request_manager.return_value

    def test_property_types(self):
        """Test that all properties return the correct types."""
        self.assertIsInstance(self.client.blueprints, Blueprints)
        self.assertIsInstance(self.client.entities, Entities)
        self.assertIsInstance(self.client.actions, Actions)
        self.assertIsInstance(self.client.action_runs, ActionRuns)
        self.assertIsInstance(self.client.pages, Pages)
        self.assertIsInstance(self.client.integrations, Integrations)
        self.assertIsInstance(self.client.organizations, Organizations)
        self.assertIsInstance(self.client.teams, Teams)
        self.assertIsInstance(self.client.users, Users)
        self.assertIsInstance(self.client.roles, Roles)
        self.assertIsInstance(self.client.audit, Audit)
        self.assertIsInstance(self.client.migrations, Migrations)
        self.assertIsInstance(self.client.search, Search)
        self.assertIsInstance(self.client.sidebars, Sidebars)
        self.assertIsInstance(self.client.checklist, Checklist)
        self.assertIsInstance(self.client.apps, Apps)
        self.assertIsInstance(self.client.scorecards, Scorecards)

    def test_property_caching(self):
        """Test that properties are cached and return the same instance."""
        # Get the property twice
        blueprints1 = self.client.blueprints
        blueprints2 = self.client.blueprints
        
        # Verify they are the same instance
        self.assertIs(blueprints1, blueprints2)
        
        # Do the same for another property
        entities1 = self.client.entities
        entities2 = self.client.entities
        self.assertIs(entities1, entities2)

    def test_property_initialization(self):
        """Test that properties are initialized with the client."""
        # Check that the client is passed to the service
        self.assertEqual(self.client.blueprints._client, self.client)
        self.assertEqual(self.client.entities._client, self.client)
        self.assertEqual(self.client.actions._client, self.client)
        
        # Check a few more services
        self.assertEqual(self.client.users._client, self.client)
        self.assertEqual(self.client.teams._client, self.client)
        self.assertEqual(self.client.roles._client, self.client)


if __name__ == "__main__":
    unittest.main()
