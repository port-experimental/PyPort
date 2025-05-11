"""
Blueprint utility functions.

This module provides high-level utility functions for working with blueprints.
"""
from typing import Dict, Any

from ..client.client import PortClient


def clear_blueprint(client: PortClient, blueprint_id: str) -> Dict[str, Any]:
    """
    Delete all entities in a blueprint.
    Args:
        client: PortClient instance
        blueprint_id: ID of the blueprint to clear
    Returns:
        dict: Summary of the operation with count of deleted entities
    """
    # Get all entities for the blueprint
    entities = client.entities.get_entities(blueprint=blueprint_id)

    # Track deletion results
    results = {
        'blueprint_id': blueprint_id,
        'total_entities': len(entities['data']),
        'deleted_entities': 0,
        'failed_entities': 0,
        'errors': []
    }

    # Delete each entity
    for entity in entities['data']:
        try:
            client.entities.delete_entity(
                blueprint=blueprint_id,
                entity=entity['identifier']
            )
            results['deleted_entities'] += 1
        except Exception as e:
            results['failed_entities'] += 1
            results['errors'].append({
                'entity_id': entity['identifier'],
                'error': str(e)
            })

    return results
