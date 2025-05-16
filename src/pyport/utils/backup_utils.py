"""
Backup utility functions.

This module provides high-level utility functions for backing up and restoring
Port data.
"""
import os
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from ..client.client import PortClient

# Set up logging
logger = logging.getLogger(__name__)


def _create_snapshot_directory(backup_dir: Optional[str], prefix: str, timestamp: str) -> Tuple[Path, str]:
    """
    Create the snapshot directory structure.

    Args:
        backup_dir: Base directory for backups
        prefix: Prefix for the snapshot
        timestamp: Timestamp string

    Returns:
        Tuple containing the snapshot directory path and snapshot ID
    """
    # Use default backup directory if none provided
    if backup_dir is None:
        backup_dir = "backups"

    # Create snapshot ID and directory
    snapshot_id = f"{prefix}_{timestamp}"
    snapshot_dir = Path(backup_dir) / snapshot_id
    os.makedirs(snapshot_dir, exist_ok=True)

    return snapshot_dir, snapshot_id


def _save_json_file(data: Dict[str, Any], file_path: Path) -> None:
    """
    Save data to a JSON file.

    Args:
        data: Data to save
        file_path: Path to save the file
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def _save_blueprints(
    client: PortClient,
    snapshot_dir: Path,
    timestamp: str,
    results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Save blueprints to the snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        timestamp: Timestamp string
        results: Results dictionary to update

    Returns:
        Updated results dictionary and blueprints data
    """
    blueprint_dir = snapshot_dir / "blueprints"
    os.makedirs(blueprint_dir, exist_ok=True)

    # Get all blueprints
    blueprints = client.blueprints.get_blueprints()

    # Save all blueprints in a single file
    all_blueprints_file = blueprint_dir / f"all_blueprints_{timestamp}.json"
    _save_json_file(blueprints, all_blueprints_file)
    results['files'].append(str(all_blueprints_file))

    # Save each blueprint in a separate file
    for blueprint in blueprints['data']:
        blueprint_id = blueprint['identifier']
        blueprint_file = blueprint_dir / f"{blueprint_id}_{timestamp}.json"
        _save_json_file(blueprint, blueprint_file)
        results['files'].append(str(blueprint_file))

    return blueprints


def _save_entities(
    client: PortClient,
    snapshot_dir: Path,
    timestamp: str,
    blueprints: Dict[str, Any],
    results: Dict[str, Any]
) -> None:
    """
    Save entities to the snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        timestamp: Timestamp string
        blueprints: Blueprints data
        results: Results dictionary to update
    """
    entity_dir = snapshot_dir / "entities"
    os.makedirs(entity_dir, exist_ok=True)

    for blueprint in blueprints['data']:
        blueprint_id = blueprint['identifier']
        blueprint_entity_dir = entity_dir / blueprint_id
        os.makedirs(blueprint_entity_dir, exist_ok=True)

        # Get entities for this blueprint
        try:
            entities = client.entities.get_entities(blueprint=blueprint_id)

            # Save all entities for this blueprint in a single file
            all_entities_file = blueprint_entity_dir / f"all_entities_{timestamp}.json"
            _save_json_file(entities, all_entities_file)
            results['files'].append(str(all_entities_file))

            # Save each entity in a separate file
            for entity in entities['data']:
                entity_id = entity['identifier']
                entity_file = blueprint_entity_dir / f"{entity_id}_{timestamp}.json"
                _save_json_file(entity, entity_file)
                results['files'].append(str(entity_file))
        except Exception as e:
            logger.error(f"Error getting entities for blueprint {blueprint_id}: {e}")


def _save_actions(
    client: PortClient,
    snapshot_dir: Path,
    timestamp: str,
    blueprints: Dict[str, Any],
    results: Dict[str, Any]
) -> None:
    """
    Save actions to the snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        timestamp: Timestamp string
        blueprints: Blueprints data
        results: Results dictionary to update
    """
    action_dir = snapshot_dir / "actions"
    os.makedirs(action_dir, exist_ok=True)

    for blueprint in blueprints['data']:
        blueprint_id = blueprint['identifier']
        blueprint_action_dir = action_dir / blueprint_id
        os.makedirs(blueprint_action_dir, exist_ok=True)

        try:
            actions = client.actions.get_actions(blueprint_identifier=blueprint_id)

            # Save all actions for this blueprint in a single file
            all_actions_file = blueprint_action_dir / f"all_actions_{timestamp}.json"
            _save_json_file(actions, all_actions_file)
            results['files'].append(str(all_actions_file))

            # Save each action in a separate file
            for action in actions['data']:
                action_id = action['identifier']
                action_file = blueprint_action_dir / f"{action_id}_{timestamp}.json"
                _save_json_file(action, action_file)
                results['files'].append(str(action_file))
        except Exception as e:
            logger.error(f"Error getting actions for blueprint {blueprint_id}: {e}")


def _save_pages(
    client: PortClient,
    snapshot_dir: Path,
    timestamp: str,
    results: Dict[str, Any]
) -> None:
    """
    Save pages to the snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        timestamp: Timestamp string
        results: Results dictionary to update
    """
    page_dir = snapshot_dir / "pages"
    os.makedirs(page_dir, exist_ok=True)

    try:
        pages = client.pages.get_pages()

        # Save all pages in a single file
        all_pages_file = page_dir / f"all_pages_{timestamp}.json"
        _save_json_file(pages, all_pages_file)
        results['files'].append(str(all_pages_file))

        # Save each page in a separate file
        for page in pages['data']:
            page_id = page['identifier']
            page_file = page_dir / f"{page_id}_{timestamp}.json"
            _save_json_file(page, page_file)
            results['files'].append(str(page_file))
    except Exception as e:
        logger.error(f"Error getting pages: {e}")


def _save_scorecards(
    client: PortClient,
    snapshot_dir: Path,
    timestamp: str,
    results: Dict[str, Any]
) -> None:
    """
    Save scorecards to the snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        timestamp: Timestamp string
        results: Results dictionary to update
    """
    scorecard_dir = snapshot_dir / "scorecards"
    os.makedirs(scorecard_dir, exist_ok=True)

    try:
        scorecards = client.scorecards.get_scorecards()

        # Save all scorecards in a single file
        all_scorecards_file = scorecard_dir / f"all_scorecards_{timestamp}.json"
        _save_json_file(scorecards, all_scorecards_file)
        results['files'].append(str(all_scorecards_file))

        # Save each scorecard in a separate file
        for scorecard in scorecards['data']:
            scorecard_id = scorecard['identifier']
            scorecard_file = scorecard_dir / f"{scorecard_id}_{timestamp}.json"
            _save_json_file(scorecard, scorecard_file)
            results['files'].append(str(scorecard_file))
    except Exception as e:
        logger.error(f"Error getting scorecards: {e}")


def _save_metadata(
    snapshot_dir: Path,
    snapshot_id: str,
    timestamp: str,
    prefix: str,
    include_options: Dict[str, bool],
    results: Dict[str, Any]
) -> None:
    """
    Save metadata about the snapshot.

    Args:
        snapshot_dir: Snapshot directory
        snapshot_id: Snapshot ID
        timestamp: Timestamp string
        prefix: Snapshot prefix
        include_options: Dictionary of include options
        results: Results dictionary to update
    """
    metadata = {
        'snapshot_id': snapshot_id,
        'timestamp': timestamp,
        'prefix': prefix,
        **include_options,
        'files': results['files']
    }

    metadata_file = snapshot_dir / "metadata.json"
    _save_json_file(metadata, metadata_file)
    results['metadata_file'] = str(metadata_file)


def save_snapshot(
    client: PortClient,
    prefix: str,
    backup_dir: Optional[str] = None,
    include_blueprints: bool = True,
    include_entities: bool = False,
    include_actions: bool = True,
    include_pages: bool = True,
    include_scorecards: bool = True
) -> Dict[str, Any]:
    """
    Save a snapshot of the current state.

    Args:
        client: PortClient instance
        prefix: Prefix for the snapshot files
        backup_dir: Directory to save the snapshot (default: ./backups)
        include_blueprints: Whether to include blueprints in the snapshot (default: True)
        include_entities: Whether to include entities in the snapshot (default: False)
        include_actions: Whether to include actions in the snapshot (default: True)
        include_pages: Whether to include pages in the snapshot (default: True)
        include_scorecards: Whether to include scorecards in the snapshot (default: True)

    Returns:
        dict: Summary of the snapshot with file paths
    """
    # Generate timestamp and create directories
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_dir, snapshot_id = _create_snapshot_directory(backup_dir, prefix, timestamp)

    # Initialize results
    results = {
        'snapshot_id': snapshot_id,
        'timestamp': timestamp,
        'files': []
    }

    # Track what to include in the snapshot
    include_options = {
        'include_blueprints': include_blueprints,
        'include_entities': include_entities,
        'include_actions': include_actions,
        'include_pages': include_pages,
        'include_scorecards': include_scorecards
    }

    # Get blueprints (needed for entities and actions)
    blueprints = None
    if include_blueprints:
        blueprints = _save_blueprints(client, snapshot_dir, timestamp, results)
    elif include_entities or include_actions:
        # We need blueprints for entities or actions even if we don't save them
        blueprints = client.blueprints.get_blueprints()

    # Save entities if requested
    if include_entities and blueprints:
        _save_entities(client, snapshot_dir, timestamp, blueprints, results)

    # Save actions if requested
    if include_actions and blueprints:
        _save_actions(client, snapshot_dir, timestamp, blueprints, results)

    # Save pages if requested
    if include_pages:
        _save_pages(client, snapshot_dir, timestamp, results)

    # Save scorecards if requested
    if include_scorecards:
        _save_scorecards(client, snapshot_dir, timestamp, results)

    # Save metadata
    _save_metadata(snapshot_dir, snapshot_id, timestamp, prefix, include_options, results)

    return results


def _load_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Load data from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        The loaded JSON data
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def list_snapshots(backup_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all available snapshots.

    Args:
        backup_dir: Directory containing the snapshots (default: ./backups)

    Returns:
        list: List of snapshot metadata
    """
    if backup_dir is None:
        backup_dir = "backups"

    backup_path = Path(backup_dir)
    if not backup_path.exists():
        return []

    snapshots = []

    for snapshot_dir in backup_path.iterdir():
        if not snapshot_dir.is_dir():
            continue

        metadata_file = snapshot_dir / "metadata.json"
        if not metadata_file.exists():
            continue

        try:
            metadata = _load_json_file(metadata_file)
            snapshots.append(metadata)
        except Exception as e:
            logger.error(f"Error reading metadata from {metadata_file}: {e}")

    # Sort snapshots by timestamp (newest first)
    snapshots.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    return snapshots


def _find_data_file(directory: Path, pattern: str) -> Optional[Path]:
    """
    Find a data file matching the given pattern in a directory.

    Args:
        directory: Directory to search in
        pattern: Glob pattern to match

    Returns:
        Path to the file if found, None otherwise
    """
    return next(directory.glob(pattern), None)


def _restore_resource(
    client: PortClient,
    resource_type: str,
    resource_id: str,
    resource_data: Dict[str, Any],
    blueprint_id: Optional[str] = None,
    results: Dict[str, Any] = None
) -> bool:
    """
    Restore a single resource (blueprint, entity, action, etc.).

    Args:
        client: PortClient instance
        resource_type: Type of resource (blueprint, entity, action, etc.)
        resource_id: ID of the resource
        resource_data: Resource data to restore
        blueprint_id: Blueprint ID (for entities and actions)
        results: Results dictionary to update

    Returns:
        True if the resource was restored successfully, False otherwise
    """
    try:
        # Handle different resource types
        if resource_type == 'blueprint':
            try:
                # Check if blueprint exists
                client.blueprints.get_blueprint(resource_id)
                # Update existing blueprint
                client.blueprints.update_blueprint(
                    blueprint_identifier=resource_id,
                    blueprint_data=resource_data
                )
            except Exception:
                # Create new blueprint
                client.blueprints.create_blueprint(resource_data)

            if results:
                results['restored_blueprints'] += 1

        elif resource_type == 'entity':
            try:
                # Check if entity exists
                client.entities.get_entity(
                    blueprint=blueprint_id,
                    entity=resource_id
                )
                # Update existing entity
                client.entities.update_entity(
                    blueprint=blueprint_id,
                    entity=resource_id,
                    entity_data=resource_data
                )
            except Exception:
                # Create new entity
                client.entities.create_entity(
                    blueprint=blueprint_id,
                    entity_data=resource_data
                )

            if results:
                results['restored_entities'] += 1

        elif resource_type == 'action':
            try:
                # Check if action exists
                client.actions.get_action(
                    blueprint_identifier=blueprint_id,
                    action_identifier=resource_id
                )
                # Update existing action
                client.actions.update_action(
                    blueprint_identifier=blueprint_id,
                    action_identifier=resource_id,
                    action_data=resource_data
                )
            except Exception:
                # Create new action
                client.actions.create_action(
                    blueprint_identifier=blueprint_id,
                    action_data=resource_data
                )

            if results:
                results['restored_actions'] += 1

        elif resource_type == 'page':
            try:
                # Check if page exists
                client.pages.get_page(resource_id)
                # Update existing page
                client.pages.update_page(
                    page_identifier=resource_id,
                    page_data=resource_data
                )
            except Exception:
                # Create new page
                client.pages.create_page(resource_data)

            if results:
                results['restored_pages'] += 1

        elif resource_type == 'scorecard':
            try:
                # Check if scorecard exists
                client.scorecards.get_scorecard(resource_id)
                # Update existing scorecard
                client.scorecards.update_scorecard(
                    scorecard_identifier=resource_id,
                    scorecard_data=resource_data
                )
            except Exception:
                # Create new scorecard
                client.scorecards.create_scorecard(resource_data)

            if results:
                results['restored_scorecards'] += 1

        return True
    except Exception as e:
        if results:
            error_info = {
                'type': resource_type,
                'id': resource_id,
                'error': str(e)
            }

            if blueprint_id:
                error_info['blueprint'] = blueprint_id

            results['errors'].append(error_info)

        logger.error(f"Error restoring {resource_type} {resource_id}: {e}")
        return False


def _restore_blueprints(
    client: PortClient,
    snapshot_dir: Path,
    metadata: Dict[str, Any],
    results: Dict[str, Any]
) -> None:
    """
    Restore blueprints from a snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        metadata: Snapshot metadata
        results: Results dictionary to update
    """
    blueprint_dir = snapshot_dir / "blueprints"
    if not blueprint_dir.exists():
        return

    all_blueprints_file = _find_data_file(blueprint_dir, "all_blueprints_*.json")
    if not all_blueprints_file:
        return

    blueprints_data = _load_json_file(all_blueprints_file)

    for blueprint in blueprints_data.get('data', []):
        resource_id = blueprint.get('identifier')
        if not resource_id:
            continue

        _restore_resource(
            client=client,
            resource_type='blueprint',
            resource_id=resource_id,
            resource_data=blueprint,
            results=results
        )


def _restore_entities(
    client: PortClient,
    snapshot_dir: Path,
    metadata: Dict[str, Any],
    results: Dict[str, Any]
) -> None:
    """
    Restore entities from a snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        metadata: Snapshot metadata
        results: Results dictionary to update
    """
    entity_dir = snapshot_dir / "entities"
    if not entity_dir.exists():
        return

    for blueprint_dir in entity_dir.iterdir():
        if not blueprint_dir.is_dir():
            continue

        blueprint_id = blueprint_dir.name
        all_entities_file = _find_data_file(blueprint_dir, "all_entities_*.json")

        if not all_entities_file:
            continue

        entities_data = _load_json_file(all_entities_file)

        for entity in entities_data.get('data', []):
            resource_id = entity.get('identifier')
            if not resource_id:
                continue

            _restore_resource(
                client=client,
                resource_type='entity',
                resource_id=resource_id,
                resource_data=entity,
                blueprint_id=blueprint_id,
                results=results
            )


def _restore_actions(
    client: PortClient,
    snapshot_dir: Path,
    metadata: Dict[str, Any],
    results: Dict[str, Any]
) -> None:
    """
    Restore actions from a snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        metadata: Snapshot metadata
        results: Results dictionary to update
    """
    action_dir = snapshot_dir / "actions"
    if not action_dir.exists():
        return

    for blueprint_dir in action_dir.iterdir():
        if not blueprint_dir.is_dir():
            continue

        blueprint_id = blueprint_dir.name
        all_actions_file = _find_data_file(blueprint_dir, "all_actions_*.json")

        if not all_actions_file:
            continue

        actions_data = _load_json_file(all_actions_file)

        for action in actions_data.get('data', []):
            resource_id = action.get('identifier')
            if not resource_id:
                continue

            _restore_resource(
                client=client,
                resource_type='action',
                resource_id=resource_id,
                resource_data=action,
                blueprint_id=blueprint_id,
                results=results
            )


def _restore_pages(
    client: PortClient,
    snapshot_dir: Path,
    metadata: Dict[str, Any],
    results: Dict[str, Any]
) -> None:
    """
    Restore pages from a snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        metadata: Snapshot metadata
        results: Results dictionary to update
    """
    page_dir = snapshot_dir / "pages"
    if not page_dir.exists():
        return

    all_pages_file = _find_data_file(page_dir, "all_pages_*.json")
    if not all_pages_file:
        return

    pages_data = _load_json_file(all_pages_file)

    for page in pages_data.get('data', []):
        resource_id = page.get('identifier')
        if not resource_id:
            continue

        _restore_resource(
            client=client,
            resource_type='page',
            resource_id=resource_id,
            resource_data=page,
            results=results
        )


def _restore_scorecards(
    client: PortClient,
    snapshot_dir: Path,
    metadata: Dict[str, Any],
    results: Dict[str, Any]
) -> None:
    """
    Restore scorecards from a snapshot.

    Args:
        client: PortClient instance
        snapshot_dir: Snapshot directory
        metadata: Snapshot metadata
        results: Results dictionary to update
    """
    scorecard_dir = snapshot_dir / "scorecards"
    if not scorecard_dir.exists():
        return

    all_scorecards_file = _find_data_file(scorecard_dir, "all_scorecards_*.json")
    if not all_scorecards_file:
        return

    scorecards_data = _load_json_file(all_scorecards_file)

    for scorecard in scorecards_data.get('data', []):
        resource_id = scorecard.get('identifier')
        if not resource_id:
            continue

        _restore_resource(
            client=client,
            resource_type='scorecard',
            resource_id=resource_id,
            resource_data=scorecard,
            results=results
        )


def restore_snapshot(
    client: PortClient,
    snapshot_id: str,
    backup_dir: Optional[str] = None,
    restore_blueprints: bool = True,
    restore_entities: bool = True,
    restore_actions: bool = True,
    restore_pages: bool = True,
    restore_scorecards: bool = True
) -> Dict[str, Any]:
    """
    Restore from a previously saved snapshot.

    Args:
        client: PortClient instance
        snapshot_id: ID of the snapshot to restore
        backup_dir: Directory containing the snapshots (default: ./backups)
        restore_blueprints: Whether to restore blueprints
        restore_entities: Whether to restore entities
        restore_actions: Whether to restore actions
        restore_pages: Whether to restore pages
        restore_scorecards: Whether to restore scorecards

    Returns:
        dict: Summary of the restore operation
    """
    if backup_dir is None:
        backup_dir = "backups"

    snapshot_dir = Path(backup_dir) / snapshot_id
    if not snapshot_dir.exists():
        raise ValueError(f"Snapshot directory not found: {snapshot_dir}")

    metadata_file = snapshot_dir / "metadata.json"
    if not metadata_file.exists():
        raise ValueError(f"Metadata file not found: {metadata_file}")

    metadata = _load_json_file(metadata_file)

    results = {
        'snapshot_id': snapshot_id,
        'restored_blueprints': 0,
        'restored_entities': 0,
        'restored_actions': 0,
        'restored_pages': 0,
        'restored_scorecards': 0,
        'errors': []
    }

    # Restore blueprints
    if restore_blueprints and metadata.get('include_blueprints', False):
        _restore_blueprints(client, snapshot_dir, metadata, results)

    # Restore entities
    if restore_entities and metadata.get('include_entities', False):
        _restore_entities(client, snapshot_dir, metadata, results)

    # Restore actions
    if restore_actions and metadata.get('include_actions', False):
        _restore_actions(client, snapshot_dir, metadata, results)

    # Restore pages
    if restore_pages and metadata.get('include_pages', False):
        _restore_pages(client, snapshot_dir, metadata, results)

    # Restore scorecards
    if restore_scorecards and metadata.get('include_scorecards', False):
        _restore_scorecards(client, snapshot_dir, metadata, results)

    return results
