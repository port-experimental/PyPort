import unittest
from unittest.mock import MagicMock, patch
from src.pyport.entities.entities_api_svc import Entities
from src.pyport.api_client import PortClient

class TestEntitiesService(unittest.TestCase):
    def setUp(self):
        patcher_env = patch('src.pyport.api_client.PortClient._get_local_env_cred', return_value=('dummy_id', 'dummy_secret'))
        self.addCleanup(patcher_env.stop)
        self.mock_get_local_env_cred = patcher_env.start()

        patcher_token = patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
        self.addCleanup(patcher_token.stop)
        self.mock_get_access_token = patcher_token.start()

        self.client = PortClient(auto_refresh=False)
        self.client.make_request = MagicMock()
        self.entities = Entities(self.client)
        self.blueprint_id = "bp_123"
        self.entity_id = "ent_456"

    def test_get_entities(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"entities": [{"id": self.entity_id}]}
        self.client.make_request.return_value = dummy_response

        result = self.entities.get_entities(self.blueprint_id)
        self.client.make_request.assert_called_once_with('GET', f"blueprints/{self.blueprint_id}/entities")
        self.assertEqual(result, [{"id": self.entity_id}])

    def test_get_entity(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {"entity": {"id": self.entity_id}}
        self.client.make_request.return_value = dummy_response

        result = self.entities.get_entity(self.blueprint_id, self.entity_id)
        self.client.make_request.assert_called_once_with('GET', f"blueprints/{self.blueprint_id}/entities/{self.entity_id}")
        self.assertEqual(result, {"id": self.entity_id})

    def test_create_entity(self):
        entity_data = {"name": "Test Entity"}
        dummy_response = MagicMock()
        dummy_response.json.return_value = entity_data
        self.client.make_request.return_value = dummy_response

        result = self.entities.create_entity(self.blueprint_id, entity_data)
        self.client.make_request.assert_called_once_with('POST', f"blueprints/{self.blueprint_id}/entities", json=entity_data)
        self.assertEqual(result, entity_data)

    def test_delete_entity(self):
        dummy_response = MagicMock()
        dummy_response.status_code = 204
        self.client.make_request.return_value = dummy_response

        result = self.entities.delete_entity(self.blueprint_id, self.entity_id)
        self.client.make_request.assert_called_once_with('DELETE', f"blueprints/{self.blueprint_id}/entities/{self.entity_id}")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
