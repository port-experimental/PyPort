"""
Tests for the utility functions.
"""
import os
import json
import shutil
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from pyport import PortClient
from pyport.utils import clear_blueprint, save_snapshot, restore_snapshot, list_snapshots


class TestBlueprintUtils(unittest.TestCase):
    """Test blueprint utility functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock(spec=PortClient)
        self.client.entities = MagicMock()
    
    def test_clear_blueprint(self):
        """Test clearing a blueprint."""
        # Mock the get_entities response
        self.client.entities.get_entities.return_value = {
            'data': [
                {'identifier': 'entity1'},
                {'identifier': 'entity2'},
                {'identifier': 'entity3'}
            ]
        }
        
        # Mock the delete_entity method
        self.client.entities.delete_entity = MagicMock()
        
        # Call the function
        result = clear_blueprint(self.client, 'test-blueprint')
        
        # Check the result
        self.assertEqual(result['blueprint_id'], 'test-blueprint')
        self.assertEqual(result['total_entities'], 3)
        self.assertEqual(result['deleted_entities'], 3)
        self.assertEqual(result['failed_entities'], 0)
        self.assertEqual(result['errors'], [])
        
        # Check that delete_entity was called for each entity
        self.assertEqual(self.client.entities.delete_entity.call_count, 3)
        self.client.entities.delete_entity.assert_any_call(
            blueprint='test-blueprint',
            entity='entity1'
        )
        self.client.entities.delete_entity.assert_any_call(
            blueprint='test-blueprint',
            entity='entity2'
        )
        self.client.entities.delete_entity.assert_any_call(
            blueprint='test-blueprint',
            entity='entity3'
        )
    
    def test_clear_blueprint_with_errors(self):
        """Test clearing a blueprint with errors."""
        # Mock the get_entities response
        self.client.entities.get_entities.return_value = {
            'data': [
                {'identifier': 'entity1'},
                {'identifier': 'entity2'},
                {'identifier': 'entity3'}
            ]
        }
        
        # Mock the delete_entity method to raise an exception for entity2
        def mock_delete_entity(blueprint, entity):
            if entity == 'entity2':
                raise Exception('Test error')
        
        self.client.entities.delete_entity.side_effect = mock_delete_entity
        
        # Call the function
        result = clear_blueprint(self.client, 'test-blueprint')
        
        # Check the result
        self.assertEqual(result['blueprint_id'], 'test-blueprint')
        self.assertEqual(result['total_entities'], 3)
        self.assertEqual(result['deleted_entities'], 2)
        self.assertEqual(result['failed_entities'], 1)
        self.assertEqual(len(result['errors']), 1)
        self.assertEqual(result['errors'][0]['entity_id'], 'entity2')
        self.assertEqual(result['errors'][0]['error'], 'Test error')


class TestBackupUtils(unittest.TestCase):
    """Test backup utility functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock(spec=PortClient)
        self.client.blueprints = MagicMock()
        self.client.entities = MagicMock()
        self.client.actions = MagicMock()
        self.client.pages = MagicMock()
        self.client.scorecards = MagicMock()
        
        # Create a temporary backup directory
        self.backup_dir = Path('temp_backups')
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove the temporary backup directory
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
    
    @patch('pyport.utils.backup_utils.datetime')
    def test_save_snapshot(self, mock_datetime):
        """Test saving a snapshot."""
        # Mock the datetime
        mock_datetime.datetime.now.return_value.strftime.return_value = '20230101_120000'
        
        # Mock the get_blueprints response
        self.client.blueprints.get_blueprints.return_value = {
            'data': [
                {'identifier': 'blueprint1', 'title': 'Blueprint 1'},
                {'identifier': 'blueprint2', 'title': 'Blueprint 2'}
            ]
        }
        
        # Mock the get_entities response
        self.client.entities.get_entities.side_effect = lambda blueprint: {
            'data': [
                {'identifier': f'entity1_{blueprint}', 'title': f'Entity 1 for {blueprint}'},
                {'identifier': f'entity2_{blueprint}', 'title': f'Entity 2 for {blueprint}'}
            ]
        }
        
        # Mock the get_actions response
        self.client.actions.get_actions.side_effect = lambda blueprint_identifier: {
            'data': [
                {'identifier': f'action1_{blueprint_identifier}', 'title': f'Action 1 for {blueprint_identifier}'},
                {'identifier': f'action2_{blueprint_identifier}', 'title': f'Action 2 for {blueprint_identifier}'}
            ]
        }
        
        # Mock the get_pages response
        self.client.pages.get_pages.return_value = {
            'data': [
                {'identifier': 'page1', 'title': 'Page 1'},
                {'identifier': 'page2', 'title': 'Page 2'}
            ]
        }
        
        # Mock the get_scorecards response
        self.client.scorecards.get_scorecards.return_value = {
            'data': [
                {'identifier': 'scorecard1', 'title': 'Scorecard 1'},
                {'identifier': 'scorecard2', 'title': 'Scorecard 2'}
            ]
        }
        
        # Call the function
        result = save_snapshot(
            self.client,
            'test',
            backup_dir=str(self.backup_dir),
            include_blueprints=True,
            include_entities=True,
            include_actions=True,
            include_pages=True,
            include_scorecards=True
        )
        
        # Check the result
        self.assertEqual(result['snapshot_id'], 'test_20230101_120000')
        self.assertEqual(result['timestamp'], '20230101_120000')
        
        # Check that the files were created
        snapshot_dir = self.backup_dir / 'test_20230101_120000'
        self.assertTrue(snapshot_dir.exists())
        
        # Check metadata file
        metadata_file = snapshot_dir / 'metadata.json'
        self.assertTrue(metadata_file.exists())
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        self.assertEqual(metadata['snapshot_id'], 'test_20230101_120000')
        self.assertEqual(metadata['timestamp'], '20230101_120000')
        self.assertEqual(metadata['prefix'], 'test')
        self.assertTrue(metadata['include_blueprints'])
        self.assertTrue(metadata['include_entities'])
        self.assertTrue(metadata['include_actions'])
        self.assertTrue(metadata['include_pages'])
        self.assertTrue(metadata['include_scorecards'])
        
        # Check blueprint files
        blueprint_dir = snapshot_dir / 'blueprints'
        self.assertTrue(blueprint_dir.exists())
        
        all_blueprints_file = blueprint_dir / 'all_blueprints_20230101_120000.json'
        self.assertTrue(all_blueprints_file.exists())
        
        blueprint1_file = blueprint_dir / 'blueprint1_20230101_120000.json'
        self.assertTrue(blueprint1_file.exists())
        
        blueprint2_file = blueprint_dir / 'blueprint2_20230101_120000.json'
        self.assertTrue(blueprint2_file.exists())
        
        # Check entity files
        entity_dir = snapshot_dir / 'entities'
        self.assertTrue(entity_dir.exists())
        
        blueprint1_entity_dir = entity_dir / 'blueprint1'
        self.assertTrue(blueprint1_entity_dir.exists())
        
        all_entities_file = blueprint1_entity_dir / 'all_entities_20230101_120000.json'
        self.assertTrue(all_entities_file.exists())
        
        entity1_file = blueprint1_entity_dir / 'entity1_blueprint1_20230101_120000.json'
        self.assertTrue(entity1_file.exists())
        
        entity2_file = blueprint1_entity_dir / 'entity2_blueprint1_20230101_120000.json'
        self.assertTrue(entity2_file.exists())
        
        # Check action files
        action_dir = snapshot_dir / 'actions'
        self.assertTrue(action_dir.exists())
        
        blueprint1_action_dir = action_dir / 'blueprint1'
        self.assertTrue(blueprint1_action_dir.exists())
        
        all_actions_file = blueprint1_action_dir / 'all_actions_20230101_120000.json'
        self.assertTrue(all_actions_file.exists())
        
        action1_file = blueprint1_action_dir / 'action1_blueprint1_20230101_120000.json'
        self.assertTrue(action1_file.exists())
        
        action2_file = blueprint1_action_dir / 'action2_blueprint1_20230101_120000.json'
        self.assertTrue(action2_file.exists())
        
        # Check page files
        page_dir = snapshot_dir / 'pages'
        self.assertTrue(page_dir.exists())
        
        all_pages_file = page_dir / 'all_pages_20230101_120000.json'
        self.assertTrue(all_pages_file.exists())
        
        page1_file = page_dir / 'page1_20230101_120000.json'
        self.assertTrue(page1_file.exists())
        
        page2_file = page_dir / 'page2_20230101_120000.json'
        self.assertTrue(page2_file.exists())
        
        # Check scorecard files
        scorecard_dir = snapshot_dir / 'scorecards'
        self.assertTrue(scorecard_dir.exists())
        
        all_scorecards_file = scorecard_dir / 'all_scorecards_20230101_120000.json'
        self.assertTrue(all_scorecards_file.exists())
        
        scorecard1_file = scorecard_dir / 'scorecard1_20230101_120000.json'
        self.assertTrue(scorecard1_file.exists())
        
        scorecard2_file = scorecard_dir / 'scorecard2_20230101_120000.json'
        self.assertTrue(scorecard2_file.exists())
    
    @patch('pyport.utils.backup_utils.datetime')
    def test_list_snapshots(self, mock_datetime):
        """Test listing snapshots."""
        # Mock the datetime
        mock_datetime.datetime.now.return_value.strftime.return_value = '20230101_120000'
        
        # Create a test snapshot
        snapshot_dir = self.backup_dir / 'test_20230101_120000'
        os.makedirs(snapshot_dir, exist_ok=True)
        
        metadata = {
            'snapshot_id': 'test_20230101_120000',
            'timestamp': '20230101_120000',
            'prefix': 'test',
            'include_blueprints': True,
            'include_entities': True,
            'include_actions': True,
            'include_pages': True,
            'include_scorecards': True,
            'files': []
        }
        
        metadata_file = snapshot_dir / 'metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Call the function
        result = list_snapshots(backup_dir=str(self.backup_dir))
        
        # Check the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['snapshot_id'], 'test_20230101_120000')
        self.assertEqual(result[0]['timestamp'], '20230101_120000')
        self.assertEqual(result[0]['prefix'], 'test')
        self.assertTrue(result[0]['include_blueprints'])
        self.assertTrue(result[0]['include_entities'])
        self.assertTrue(result[0]['include_actions'])
        self.assertTrue(result[0]['include_pages'])
        self.assertTrue(result[0]['include_scorecards'])
    
    @patch('pyport.utils.backup_utils.datetime')
    def test_restore_snapshot(self, mock_datetime):
        """Test restoring a snapshot."""
        # Mock the datetime
        mock_datetime.datetime.now.return_value.strftime.return_value = '20230101_120000'
        
        # Create a test snapshot
        snapshot_dir = self.backup_dir / 'test_20230101_120000'
        os.makedirs(snapshot_dir, exist_ok=True)
        
        # Create blueprint directory
        blueprint_dir = snapshot_dir / 'blueprints'
        os.makedirs(blueprint_dir, exist_ok=True)
        
        # Create all_blueprints file
        all_blueprints = {
            'data': [
                {'identifier': 'blueprint1', 'title': 'Blueprint 1'},
                {'identifier': 'blueprint2', 'title': 'Blueprint 2'}
            ]
        }
        
        all_blueprints_file = blueprint_dir / 'all_blueprints_20230101_120000.json'
        with open(all_blueprints_file, 'w') as f:
            json.dump(all_blueprints, f, indent=2)
        
        # Create entity directory
        entity_dir = snapshot_dir / 'entities'
        os.makedirs(entity_dir, exist_ok=True)
        
        # Create blueprint1 entity directory
        blueprint1_entity_dir = entity_dir / 'blueprint1'
        os.makedirs(blueprint1_entity_dir, exist_ok=True)
        
        # Create all_entities file
        all_entities = {
            'data': [
                {'identifier': 'entity1_blueprint1', 'title': 'Entity 1 for blueprint1'},
                {'identifier': 'entity2_blueprint1', 'title': 'Entity 2 for blueprint1'}
            ]
        }
        
        all_entities_file = blueprint1_entity_dir / 'all_entities_20230101_120000.json'
        with open(all_entities_file, 'w') as f:
            json.dump(all_entities, f, indent=2)
        
        # Create action directory
        action_dir = snapshot_dir / 'actions'
        os.makedirs(action_dir, exist_ok=True)
        
        # Create blueprint1 action directory
        blueprint1_action_dir = action_dir / 'blueprint1'
        os.makedirs(blueprint1_action_dir, exist_ok=True)
        
        # Create all_actions file
        all_actions = {
            'data': [
                {'identifier': 'action1_blueprint1', 'title': 'Action 1 for blueprint1'},
                {'identifier': 'action2_blueprint1', 'title': 'Action 2 for blueprint1'}
            ]
        }
        
        all_actions_file = blueprint1_action_dir / 'all_actions_20230101_120000.json'
        with open(all_actions_file, 'w') as f:
            json.dump(all_actions, f, indent=2)
        
        # Create page directory
        page_dir = snapshot_dir / 'pages'
        os.makedirs(page_dir, exist_ok=True)
        
        # Create all_pages file
        all_pages = {
            'data': [
                {'identifier': 'page1', 'title': 'Page 1'},
                {'identifier': 'page2', 'title': 'Page 2'}
            ]
        }
        
        all_pages_file = page_dir / 'all_pages_20230101_120000.json'
        with open(all_pages_file, 'w') as f:
            json.dump(all_pages, f, indent=2)
        
        # Create scorecard directory
        scorecard_dir = snapshot_dir / 'scorecards'
        os.makedirs(scorecard_dir, exist_ok=True)
        
        # Create all_scorecards file
        all_scorecards = {
            'data': [
                {'identifier': 'scorecard1', 'title': 'Scorecard 1'},
                {'identifier': 'scorecard2', 'title': 'Scorecard 2'}
            ]
        }
        
        all_scorecards_file = scorecard_dir / 'all_scorecards_20230101_120000.json'
        with open(all_scorecards_file, 'w') as f:
            json.dump(all_scorecards, f, indent=2)
        
        # Create metadata file
        metadata = {
            'snapshot_id': 'test_20230101_120000',
            'timestamp': '20230101_120000',
            'prefix': 'test',
            'include_blueprints': True,
            'include_entities': True,
            'include_actions': True,
            'include_pages': True,
            'include_scorecards': True,
            'files': []
        }
        
        metadata_file = snapshot_dir / 'metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Mock the client methods
        # For blueprints
        self.client.blueprints.get_blueprint.side_effect = Exception('Not found')
        self.client.blueprints.create_blueprint = MagicMock()
        
        # For entities
        self.client.entities.get_entity.side_effect = Exception('Not found')
        self.client.entities.create_entity = MagicMock()
        
        # For actions
        self.client.actions.get_action.side_effect = Exception('Not found')
        self.client.actions.create_action = MagicMock()
        
        # For pages
        self.client.pages.get_page.side_effect = Exception('Not found')
        self.client.pages.create_page = MagicMock()
        
        # For scorecards
        self.client.scorecards.get_scorecard.side_effect = Exception('Not found')
        self.client.scorecards.create_scorecard = MagicMock()
        
        # Call the function
        result = restore_snapshot(
            self.client,
            'test_20230101_120000',
            backup_dir=str(self.backup_dir),
            restore_blueprints=True,
            restore_entities=True,
            restore_actions=True,
            restore_pages=True,
            restore_scorecards=True
        )
        
        # Check the result
        self.assertEqual(result['snapshot_id'], 'test_20230101_120000')
        self.assertEqual(result['restored_blueprints'], 2)
        self.assertEqual(result['restored_entities'], 2)
        self.assertEqual(result['restored_actions'], 2)
        self.assertEqual(result['restored_pages'], 2)
        self.assertEqual(result['restored_scorecards'], 2)
        self.assertEqual(result['errors'], [])
        
        # Check that the client methods were called
        self.assertEqual(self.client.blueprints.create_blueprint.call_count, 2)
        self.assertEqual(self.client.entities.create_entity.call_count, 2)
        self.assertEqual(self.client.actions.create_action.call_count, 2)
        self.assertEqual(self.client.pages.create_page.call_count, 2)
        self.assertEqual(self.client.scorecards.create_scorecard.call_count, 2)


if __name__ == '__main__':
    unittest.main()
