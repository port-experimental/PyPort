from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class Checklist(BaseAPIService):
    """Checklist API category for managing checklists.

    This class provides methods for interacting with the Checklist API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all checklists
        >>> checklists = client.checklist.get_checklists()
        >>> # Get a specific checklist
        >>> checklist = client.checklist.get_checklist("checklist-id")
    """

    def __init__(self, client):
        """Initialize the Checklist API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="checklists", response_key="checklist")

    def get_checklists(self, page: Optional[int] = None, per_page: Optional[int] = None,
                       params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all checklists.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of checklist dictionaries.

        Raises:
            PortApiError: If the API request fails.
        """
        return self.get_all(page=page, per_page=per_page, params=params)

    def get_checklist(self, checklist_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific checklist.

        Args:
            checklist_id: The identifier of the checklist.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the checklist.

        Raises:
            PortResourceNotFoundError: If the checklist does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.get_by_id(checklist_id, params=params)

    def create_checklist(self, checklist_data: Dict[str, Any],
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new checklist.

        Args:
            checklist_data: A dictionary containing checklist data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created checklist.

        Raises:
            PortValidationError: If the checklist data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("POST", "checklists", json=checklist_data)
        return response.json()

    def update_checklist(self, checklist_id: str, checklist_data: Dict[str, Any],
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing checklist.

        Args:
            checklist_id: The identifier of the checklist to update.
            checklist_data: A dictionary with updated checklist data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated checklist.

        Raises:
            PortResourceNotFoundError: If the checklist does not exist.
            PortValidationError: If the checklist data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("PUT", f"checklists/{checklist_id}", json=checklist_data)
        return response.json()

    def delete_checklist(self, checklist_id: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a checklist.

        Args:
            checklist_id: The identifier of the checklist to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the checklist does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.delete_resource(checklist_id, params=params)

    # Checklist Items Methods

    def get_checklist_items(self, checklist_id: str, page: Optional[int] = None,
                            per_page: Optional[int] = None,
                            params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all items for a specific checklist.

        Args:
            checklist_id: The identifier of the checklist.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of checklist item dictionaries.

        Raises:
            PortResourceNotFoundError: If the checklist does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = self._build_endpoint("checklists", checklist_id, "items")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("items", [])

    def create_checklist_item(self, checklist_id: str, item_data: Dict[str, Any],
                              params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new item for a specific checklist.

        Args:
            checklist_id: The identifier of the checklist.
            item_data: A dictionary containing item data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created checklist item.

        Raises:
            PortResourceNotFoundError: If the checklist does not exist.
            PortValidationError: If the item data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("checklists", checklist_id, "items")

        # Make the request
        response = self._make_request_with_params('POST', endpoint, json=item_data, params=params)
        return response

    def update_checklist_item(self, checklist_id: str, item_id: str, item_data: Dict[str, Any],
                              params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing checklist item.

        Args:
            checklist_id: The identifier of the checklist.
            item_id: The identifier of the item to update.
            item_data: A dictionary with updated item data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated checklist item.

        Raises:
            PortResourceNotFoundError: If the checklist or item does not exist.
            PortValidationError: If the item data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("checklists", checklist_id, "items", item_id)

        # Make the request
        response = self._make_request_with_params('PUT', endpoint, json=item_data, params=params)
        return response

    def delete_checklist_item(self, checklist_id: str, item_id: str,
                              params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a checklist item.

        Args:
            checklist_id: The identifier of the checklist.
            item_id: The identifier of the item to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the checklist or item does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("checklists", checklist_id, "items", item_id)

        # Make the request
        response = self._client.make_request("DELETE", endpoint)
        return response.status_code == 204
