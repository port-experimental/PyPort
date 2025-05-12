"""Type stub file for the BaseAPIService class."""

from typing import Any, Dict, List, Optional, Union, TypeVar, overload

from ..models.api_category import BaseResource as BaseResourceModel, ApiClient
from ..types import JsonDict, PaginationParams

T = TypeVar('T')  # Generic type for resource items
R = TypeVar('R')  # Generic type for response objects

class BaseAPIService(BaseResourceModel):
    """Base class for all API service classes."""
    
    _response_key: Optional[str]
    
    def __init__(
        self,
        client: ApiClient,
        resource_name: Optional[str] = None,
        response_key: Optional[str] = None
    ) -> None: ...
    
    def _extract_response_data(
        self,
        response: JsonDict,
        key: Optional[str] = None
    ) -> Union[JsonDict, List[JsonDict]]: ...
    
    def _handle_pagination_params(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None
    ) -> PaginationParams: ...
    
    def _build_endpoint(self, *parts: str) -> str: ...
    
    def _make_request_with_params(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> JsonDict: ...
    
    def get_all(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[JsonDict]: ...
    
    def get_by_id(
        self,
        resource_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> JsonDict: ...
    
    def create_resource(
        self,
        resource_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> JsonDict: ...
    
    def update_resource(
        self,
        resource_id: str,
        resource_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> JsonDict: ...
    
    def delete_resource(
        self,
        resource_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bool: ...
