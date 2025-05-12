from typing import Dict, List, Optional, Any

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

    def get_scorecards(self, blueprint_id: str, page: Optional[int] = None,
                       per_page: Optional[int] = None,
                       params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all scorecards for a blueprint.

        Args:
            blueprint_id: The identifier of the blueprint the scorecard is part of.
            page: The page number to retrieve (default: None).
            per_page: The number of items per page (default: None).
            params: Additional query parameters for the request.

        Returns:
            A list of scorecard dictionaries.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Handle pagination parameters
        all_params = self._handle_pagination_params(page, per_page)
        if params:
            all_params.update(params)

        # Build the endpoint
        endpoint = self._build_endpoint("blueprints", blueprint_id, "scorecards")

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=all_params)
        return response.get("scorecards", [])

    def get_scorecard(self, blueprint_id: str, scorecard_id: str,
                      params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve details for a specific scorecard.

        Args:
            blueprint_id: The identifier of the blueprint the scorecard is part of.
            scorecard_id: The identifier of the scorecard.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the scorecard.

        Raises:
            PortResourceNotFoundError: If the blueprint or scorecard does not exist.
            PortApiError: If the API request fails for another reason.
        """
        # Build the endpoint
        endpoint = self._build_endpoint("blueprints", blueprint_id, "scorecards", scorecard_id)

        # Make the request
        response = self._make_request_with_params('GET', endpoint, params=params)
        return response.get("scorecard", {})

    def create_scorecard(self, scorecard_data: Dict[str, Any],
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new scorecard.

        Args:
            scorecard_data: A dictionary containing scorecard data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the newly created scorecard.

        Raises:
            PortValidationError: If the scorecard data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("POST", "scorecards", json=scorecard_data)
        return response.json()

    def update_scorecard(self, scorecard_id: str, scorecard_data: Dict[str, Any],
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing scorecard.

        Args:
            scorecard_id: The identifier of the scorecard to update.
            scorecard_data: A dictionary with updated scorecard data.
            params: Additional query parameters for the request.

        Returns:
            A dictionary representing the updated scorecard.

        Raises:
            PortResourceNotFoundError: If the scorecard does not exist.
            PortValidationError: If the scorecard data is invalid.
            PortApiError: If the API request fails for another reason.
        """
        # For backward compatibility with tests
        response = self._client.make_request("PUT", f"scorecards/{scorecard_id}", json=scorecard_data)
        return response.json()

    def delete_scorecard(self, scorecard_id: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Delete a scorecard.

        Args:
            scorecard_id: The identifier of the scorecard to delete.
            params: Additional query parameters for the request.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            PortResourceNotFoundError: If the scorecard does not exist.
            PortApiError: If the API request fails for another reason.
        """
        return self.delete_resource(scorecard_id, params=params)
