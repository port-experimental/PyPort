from typing import Dict, List, Optional, Any

from ..services.base_api_service import BaseAPIService


class Pages(BaseAPIService):
    """Pages API category for managing pages and widgets.

    This class provides methods for interacting with the Pages API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all pages for a blueprint
        >>> pages = client.pages.get_pages("blueprint-id")
        >>> # Get a specific page
        >>> page = client.pages.get_page("blueprint-id", "page-id")
    """

    def __init__(self, client):
        """Initialize the Pages API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="pages", response_key="page")

    def get_pages(self, blueprint_identifier: str, page: Optional[int] = None,
                  per_page: Optional[int] = None,
                  params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all pages for a specified blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of page dictionaries.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "pages")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("pages", [])

    def get_page(self, blueprint_identifier: str, page_identifier: str,
                 params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve a single page by its identifier.

        Args:
            blueprint_identifier: The blueprint identifier.
            page_identifier: The identifier of the page.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the page.

        Raises:
            PortResourceNotFoundError: If the blueprint or page does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "pages", page_identifier)

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("page", {})

    def create_page(self, blueprint_identifier: str, page_data: Dict[str, Any],
                    params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new page under the specified blueprint.

        Args:
            blueprint_identifier: The blueprint identifier.
            page_data: A dictionary containing data for the new page.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the created page.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortValidationError: If the page data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "pages")

        # Make the request
        response = self._make_request_with_params('POST', endpoint, json=page_data, params=params)
        return response

    def update_page(self, blueprint_identifier: str, page_identifier: str,
                    page_data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing page.

        Args:
            blueprint_identifier: The blueprint identifier.
            page_identifier: The identifier of the page to update.
            page_data: A dictionary containing updated data for the page.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated page.

        Raises:
            PortResourceNotFoundError: If the blueprint or page does not exist.
            PortValidationError: If the page data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "pages", page_identifier)

        # Make the request
        response = self._make_request_with_params('PUT', endpoint, json=page_data, params=params)
        return response

    def delete_page(self, blueprint_identifier: str, page_identifier: str,
                    params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a page.

        Args:
            blueprint_identifier: The blueprint identifier.
            page_identifier: The identifier of the page to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the blueprint or page does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "pages", page_identifier)

        # Make the request
        response = self._client.make_request('DELETE', endpoint)
        return response.status_code == 204

    # Page Widgets Methods

    def get_page_widgets(self, page_identifier: str, page: Optional[int] = None,
                         per_page: Optional[int] = None,
                         params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all widgets for a specific page.

        Args:
            page_identifier: The identifier of the page.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of widget dictionaries.

        Raises:
            PortResourceNotFoundError: If the page does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = self._build_endpoint("pages", page_identifier, "widgets")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("widgets", [])

    def create_page_widget(self, page_identifier: str, widget_data: Dict[str, Any],
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new widget for a specific page.

        Args:
            page_identifier: The identifier of the page.
            widget_data: A dictionary containing widget data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created widget.

        Raises:
            PortResourceNotFoundError: If the page does not exist.
            PortValidationError: If the widget data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("pages", page_identifier, "widgets")

        # Make the request
        response = self._make_request_with_params('POST', endpoint, json=widget_data, params=params)
        return response

    def get_page_widget(self, page_identifier: str, widget_id: str,
                        params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific page widget.

        Args:
            page_identifier: The identifier of the page.
            widget_id: The identifier of the widget.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the page widget.

        Raises:
            PortResourceNotFoundError: If the page or widget does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("pages", page_identifier, "widgets", widget_id)

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("widget", {})

    def update_page_widget(self, page_identifier: str, widget_id: str,
                           widget_data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing page widget.

        Args:
            page_identifier: The identifier of the page.
            widget_id: The identifier of the widget to update.
            widget_data: A dictionary with updated widget data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated page widget.

        Raises:
            PortResourceNotFoundError: If the page or widget does not exist.
            PortValidationError: If the widget data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("pages", page_identifier, "widgets", widget_id)

        # Make the request
        response = self._make_request_with_params('PUT', endpoint, json=widget_data, params=params)
        return response

    def delete_page_widget(self, page_identifier: str, widget_id: str,
                           params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a page widget.

        Args:
            page_identifier: The identifier of the page.
            widget_id: The identifier of the widget to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the page or widget does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("pages", page_identifier, "widgets", widget_id)

        # Make the request
        response = self._client.make_request('DELETE', endpoint)
        return response.status_code == 204

    # Page Permissions Methods

    def get_page_permissions(self, page_identifier: str,
                             params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve permissions for a specific page.

        Args:
            page_identifier: The identifier of the page.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the page permissions.

        Raises:
            PortResourceNotFoundError: If the page does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("pages", page_identifier, "permissions")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("permissions", {})

    def update_page_permissions(self, page_identifier: str, permissions_data: Dict[str, Any],
                                params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update permissions for a specific page.

        Args:
            page_identifier: The identifier of the page.
            permissions_data: A dictionary containing updated permissions data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated page permissions.

        Raises:
            PortResourceNotFoundError: If the page does not exist.
            PortValidationError: If the permissions data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("pages", page_identifier, "permissions")

        # Make the request
        response = self._make_request_with_params('PUT', endpoint, json=permissions_data, params=params)
        return response
