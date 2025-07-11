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
        self.client.blueprints = MagicMock()

    def test_clear_blueprint(self):
        """Test clearing a blueprint using the API's delete all entities method."""
        # Mock the delete_all_blueprint_entities response
        expected_result = {
            'deleted': True,
            'message': 'All entities deleted successfully'
        }
        self.client.blueprints.delete_all_blueprint_entities.return_value = expected_result

        # Call the function
        result = clear_blueprint(self.client, 'test-blueprint')

        # Check the result
        self.assertEqual(result, expected_result)

        # Check that delete_all_blueprint_entities was called
        self.client.blueprints.delete_all_blueprint_entities.assert_called_once_with('test-blueprint')

    def test_clear_blueprint_with_api_error(self):
        """Test clearing a blueprint when the API call fails."""
        # Mock the delete_all_blueprint_entities to raise an exception
        from pyport.error_handling import PortApiError
        self.client.blueprints.delete_all_blueprint_entities.side_effect = PortApiError("API Error")

        # Call the function and expect it to raise the exception
        with self.assertRaises(PortApiError):
            clear_blueprint(self.client, 'test-blueprint')

        # Check that delete_all_blueprint_entities was called
        self.client.blueprints.delete_all_blueprint_entities.assert_called_once_with('test-blueprint')


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
            include_entities=False,  # Default is now False
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
        self.assertFalse(metadata['include_entities'])  # Now False
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

        # Entity files should not be created since include_entities=False
        entity_dir = snapshot_dir / 'entities'
        self.assertFalse(entity_dir.exists())

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
            'include_entities': False,  # Now False
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
        self.assertFalse(result[0]['include_entities'])  # Now False
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

        # No entity directory since include_entities=False

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
            'include_entities': False,  # Now False
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
            restore_entities=False,  # Now False
            restore_actions=True,
            restore_pages=True,
            restore_scorecards=True
        )

        # Check the result
        self.assertEqual(result['snapshot_id'], 'test_20230101_120000')
        self.assertEqual(result['restored_blueprints'], 2)
        self.assertEqual(result['restored_entities'], 0)  # No entities restored
        self.assertEqual(result['restored_actions'], 2)
        self.assertEqual(result['restored_pages'], 2)
        self.assertEqual(result['restored_scorecards'], 2)
        self.assertEqual(result['errors'], [])

        # Check that the client methods were called
        self.assertEqual(self.client.blueprints.create_blueprint.call_count, 2)
        self.assertEqual(self.client.entities.create_entity.call_count, 0)  # No entities created
        self.assertEqual(self.client.actions.create_action.call_count, 2)
        self.assertEqual(self.client.pages.create_page.call_count, 2)
        self.assertEqual(self.client.scorecards.create_scorecard.call_count, 2)


if __name__ == '__main__':
    unittest.main()
