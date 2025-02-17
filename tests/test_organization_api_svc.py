import unittest
from unittest.mock import MagicMock
from src.pyport.organization.organization_api_svc import Organizations

class TestOrganizations(unittest.TestCase):
    def setUp(self):
        # Create a dummy client with a mocked make_request method.
        self.mock_client = MagicMock()
        # Instantiate Organizations with the dummy client.
        self.organizations = Organizations(self.mock_client)

    def test_get_organizations(self):
        fake_orgs = [{"id": "org1"}, {"id": "org2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"organizations": fake_orgs}
        self.mock_client.make_request.return_value = mock_response

        result = self.organizations.get_organizations()
        self.mock_client.make_request.assert_called_once_with("GET", "organizations")
        self.assertEqual(result, fake_orgs)

    def test_get_organization(self):
        organization_id = "org1"
        fake_org = {"id": organization_id, "name": "Test Organization"}
        mock_response = MagicMock()
        mock_response.json.return_value = {"organization": fake_org}
        self.mock_client.make_request.return_value = mock_response

        result = self.organizations.get_organization(organization_id)
        self.mock_client.make_request.assert_called_once_with("GET", f"organizations/{organization_id}")
        self.assertEqual(result, fake_org)

    def test_create_organization(self):
        org_data = {"name": "New Organization"}
        fake_response_data = {"id": "org_new", "name": "New Organization"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.organizations.create_organization(org_data)
        self.mock_client.make_request.assert_called_once_with("POST", "organizations", json=org_data)
        self.assertEqual(result, fake_response_data)

    def test_update_organization(self):
        organization_id = "org1"
        org_data = {"name": "Updated Organization"}
        fake_response_data = {"id": organization_id, "name": "Updated Organization"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_response_data
        self.mock_client.make_request.return_value = mock_response

        result = self.organizations.update_organization(organization_id, org_data)
        self.mock_client.make_request.assert_called_once_with("PUT", f"organizations/{organization_id}", json=org_data)
        self.assertEqual(result, fake_response_data)

    def test_delete_organization(self):
        organization_id = "org1"
        mock_response = MagicMock()
        mock_response.status_code = 204
        self.mock_client.make_request.return_value = mock_response

        result = self.organizations.delete_organization(organization_id)
        self.mock_client.make_request.assert_called_once_with("DELETE", f"organizations/{organization_id}")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
