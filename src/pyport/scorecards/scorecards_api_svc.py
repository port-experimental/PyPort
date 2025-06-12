"""Scorecards API service for managing Port scorecards.

This module provides methods for creating, retrieving, updating, and deleting
scorecards and scorecard rules in Port."""

from typing import Dict, Optional, Any

from ..services.base_api_service import BaseAPIService


class Scorecards(BaseAPIService):
    """Scorecards API category for managing scorecards.

    This class provides methods for interacting with the Scorecards API endpoints.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all scorecards for a blueprint
        >>> scorecards = client.scorecards.get_scorecards("blueprint-id")
        >>> # Get a specific scorecard
        >>> scorecard = client.scorecards.get_scorecard("blueprint-id", "scorecard-id")
    """

    def __init__(self, client):
        """Initialize the Scorecards API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="scorecards", response_key="scorecard")

    def get_scorecards(self, page: Optional[int] = None, per_page: Optional[int] = None,
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve all scorecards.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A dictionary containing scorecards data.

        Raises:
            PortApiError: If the API request fails.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Make the request
        response = self._make_request_with_params('GET', "scorecards", params=all_params)
        return response

    def create_scorecard(self, blueprint_identifier: str, scorecard_data: Dict[str, Any],
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new scorecard for a blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.
            scorecard_data: A dictionary containing scorecard data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created scorecard.

        Raises:
            PortValidationError: If the scorecard data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "scorecards")
        response = self._make_request_with_params('POST', endpoint, json=scorecard_data, params=params)
        return response

    def update_scorecard(self, blueprint_identifier: str, scorecard_identifier: str,
                         scorecard_data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing scorecard.

        Args:
            blueprint_identifier: The identifier of the blueprint.
            scorecard_identifier: The identifier of the scorecard to update.
            scorecard_data: A dictionary with updated scorecard data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated scorecard.

        Raises:
            PortResourceNotFoundError: If the scorecard does not exist.
            PortValidationError: If the scorecard data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "scorecards", scorecard_identifier)
        response = self._make_request_with_params('PUT', endpoint, json=scorecard_data, params=params)
        return response
