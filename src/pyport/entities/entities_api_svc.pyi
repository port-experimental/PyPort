"""Type stub file for the Entities API service."""

from typing import Dict, List, Any, Optional, Union, Tuple

from ..services.base_api_service import BaseAPIService

# Type aliases
Entity = Dict[str, Any]
EntityResponse = Dict[str, Any]
EntitiesResponse = Dict[str, Any]
JsonDict = Dict[str, Any]
JsonList = List[Dict[str, Any]]
Pagination = Dict[str, Any]

class Entities(BaseAPIService):
    """Entities API category for managing entities in Port."""
    
    def __init__(self, client) -> None: ...
    
    def get_entities(
        self,
        blueprint_identifier: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Entity]: ...
    
    def get_entity(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Entity: ...
    
    def create_entity(
        self,
        blueprint_identifier: str,
        entity_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Entity: ...
    
    def update_entity(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        entity_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Entity: ...
    
    def delete_entity(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bool: ...
    
    def get_entity_by_run_id(
        self,
        run_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Entity: ...
    
    def get_entity_by_selector(
        self,
        selector: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Entity: ...
    
    def get_entities_by_selector(
        self,
        selector: Dict[str, Any],
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Entity]: ...
    
    def get_entity_changelog(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]: ...
    
    def get_entity_dependencies(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]: ...
    
    def get_entity_dependents(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]: ...
    
    def get_entity_relations(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        relation_type: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]: ...
    
    def create_entity_relation(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        relation_type: str,
        relation_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]: ...
    
    def delete_entity_relation(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        relation_type: str,
        target_blueprint: str,
        target_entity: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bool: ...
    
    def get_entity_runs(
        self,
        blueprint_identifier: str,
        entity_identifier: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]: ...
    
    def bulk_create_entities(
        self,
        blueprint_identifier: str,
        entities_data: List[Dict[str, Any]],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]: ...
    
    def bulk_update_entities(
        self,
        blueprint_identifier: str,
        entities_data: List[Dict[str, Any]],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]: ...
    
    def bulk_delete_entities(
        self,
        blueprint_identifier: str,
        entity_identifiers: List[str],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]: ...
    
    def bulk_upsert_entities(
        self,
        blueprint_identifier: str,
        entities_data: List[Dict[str, Any]],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]: ...
