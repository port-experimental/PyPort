from typing import Dict, List, Any, Optional

from ..services.base_api_service import BaseAPIService

# Comment out the types import since it doesn't exist yet
# from .types import (
#     Entity, EntityResponse, EntitiesResponse,
#     JsonDict, JsonList, Pagination
# )

# Use regular Dict and List instead
Entity = Dict[str, Any]
EntityResponse = Dict[str, Any]
EntitiesResponse = Dict[str, Any]
JsonDict = Dict[str, Any]
JsonList = List[Dict[str, Any]]
Pagination = Dict[str, Any]


class Entities(BaseAPIService):
    """Entities API category for managing entities in Port.

    Entities are instances of blueprints that represent real-world resources in your
    software catalog. Each entity belongs to a specific blueprint and has properties
    and relations as defined by that blueprint.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all service entities
        >>> services = client.entities.get_entities("service")
        >>> # Get a specific entity
        >>> api_service = client.entities.get_entity("service", "api-service")
        >>> # Create a new entity
        >>> new_entity = client.entities.create_entity(
        ...     "service",
        ...     {
        ...         "identifier": "payment-service",
        ...         "title": "Payment Service",
        ...         "properties": {
        ...             "language": "Python",
        ...             "url": "https://github.com/example/payment-service"
        ...         }
        ...     }
        ... )
    """

    def __init__(self, client):
        """Initialize the Entities API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, response_key="entity")

    def get_entities(
        self, blueprint_identifier: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[Entity]:
        """
        Retrieve a list of all entities for the specified blueprint with pagination support.

        This method retrieves entities that belong to the specified blueprint.
        The results can be paginated using the page and per_page parameters.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.
            page: The page number to retrieve (default: None).
            per_page: The number of entities per page (default: None, max: 1000).

        Returns:
            A list of entity dictionaries. Each entity contains:
            - identifier: The unique identifier of the entity
            - title: The display name of the entity
            - properties: The property values for this entity
            - relations: The relation values for this entity
            - and other metadata

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Get all service entities
            >>> services = client.entities.get_entities("service")
            >>> # Get the second page of service entities, 50 per page
            >>> page2 = client.entities.get_entities("service", page=2, per_page=50)
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities")

        # Get pagination parameters
        params = self._handle_pagination_params(page, per_page)

        # Make the request with pagination parameters
        response = self._make_request_with_params('GET', endpoint, params=params)

        # Extract and return the entities
        return response.get("entities", [])

    def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> Entity:
        """
        Retrieve a specific entity by its identifier.

        This method retrieves detailed information about a specific entity.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.
            entity_identifier: The unique identifier of the entity to retrieve.

        Returns:
            A dictionary containing the entity details:
            - identifier: The unique identifier of the entity
            - title: The display name of the entity
            - properties: The property values for this entity
            - relations: The relation values for this entity
            - and other metadata

        Raises:
            PortResourceNotFoundError: If the blueprint or entity does not exist.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Get a specific service entity
            >>> api_service = client.entities.get_entity("service", "api-service")
            >>> print(api_service["title"])
            'API Service'
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities", entity_identifier)

        # Make the request
        response = self._make_request_with_params('GET', endpoint)

        # Extract and return the entity
        return response.get("entity", {})

    def create_entity(
        self,
        blueprint_identifier: str,
        entity_data: Dict[str, Any],
        upsert: bool = False,
        validation_only: bool = False,
        create_missing_related_entities: bool = False,
        merge: bool = False
    ) -> Entity:
        """
        Create a new entity under the specified blueprint.

        This method creates a new entity with the specified data.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.
            entity_data: A dictionary containing the data for the new entity.
                Must include at minimum:
                - identifier: A unique identifier for the entity (string)
                - title: A display name for the entity (string)

                May also include:
                - properties: Property values for this entity (dict)
                - relations: Relation values for this entity (dict)
            upsert: If True, update the entity if it already exists (default: False).
            validation_only: If True, only validate the entity data without creating it (default: False).
            create_missing_related_entities: If True, create any related entities that don't exist (default: False).
            merge: If True and upsert is True, merge the new data with existing data (default: False).

        Returns:
            A dictionary representing the created entity.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortValidationError: If the entity data is invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Create a simple entity
            >>> new_entity = client.entities.create_entity(
            ...     "service",
            ...     {
            ...         "identifier": "payment-service",
            ...         "title": "Payment Service",
            ...         "properties": {
            ...             "language": "Python",
            ...             "url": "https://github.com/example/payment-service"
            ...         }
            ...     }
            ... )
            >>>
            >>> # Create or update an entity (upsert)
            >>> client.entities.create_entity(
            ...     "service",
            ...     {
            ...         "identifier": "payment-service",
            ...         "title": "Payment Service v2"
            ...     },
            ...     upsert=True
            ... )
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities")

        # Create query parameters
        params = {
            "upsert": str(upsert).lower(),
            "validation_only": str(validation_only).lower(),
            "create_missing_related_entities": str(create_missing_related_entities).lower(),
            "merge": str(merge).lower()
        }

        # Make the request
        return self._make_request_with_params('POST', endpoint, params=params, json=entity_data)

    def update_entity(self, blueprint_identifier: str, entity_identifier: str, entity_data: Dict[str, Any]) -> Entity:
        """
        Update an existing entity.

        This method updates an existing entity with the specified data.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.
            entity_identifier: The unique identifier of the entity to update.
            entity_data: A dictionary containing the updated data for the entity.
                May include any of the fields mentioned in create_entity.

        Returns:
            A dictionary representing the updated entity.

        Raises:
            PortResourceNotFoundError: If the blueprint or entity does not exist.
            PortValidationError: If the entity data is invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Update an entity's title
            >>> updated_entity = client.entities.update_entity(
            ...     "service",
            ...     "payment-service",
            ...     {"title": "Payment Processing Service"}
            ... )
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities", entity_identifier)

        # Make the request
        return self._make_request_with_params('PUT', endpoint, json=entity_data)

    def delete_entity(self, blueprint_identifier: str, entity_identifier: str) -> bool:
        """
        Delete an entity from the specified blueprint.

        This method deletes an entity with the specified identifier.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.
            entity_identifier: The unique identifier of the entity to delete.

        Returns:
            True if deletion was successful, otherwise False.

        Raises:
            PortResourceNotFoundError: If the blueprint or entity does not exist.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Delete an entity
            >>> success = client.entities.delete_entity("service", "payment-service")
            >>> if success:
            ...     print("Entity deleted successfully")
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities", entity_identifier)

        # Make the request
        response = self._client.make_request('DELETE', endpoint)

        # Return True if the status code is 204 (No Content)
        return response.status_code == 204

    def create_entities_bulk(self, blueprint_identifier: str, entities_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple entities in bulk for the specified blueprint.

        This method creates multiple entities in a single request, which is more efficient
        than creating them one by one.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.
            entities_data: A list of dictionaries, each containing data for a new entity.
                Each entity dictionary should follow the same format as in create_entity.

        Returns:
            A dictionary representing the result of the bulk creation, containing:
            - created: The number of entities created
            - errors: Any errors that occurred during creation

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortValidationError: If any entity data is invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Create multiple entities in bulk
            >>> result = client.entities.create_entities_bulk(
            ...     "service",
            ...     [
            ...         {
            ...             "identifier": "payment-service",
            ...             "title": "Payment Service",
            ...             "properties": {"language": "Python"}
            ...         },
            ...         {
            ...             "identifier": "auth-service",
            ...             "title": "Authentication Service",
            ...             "properties": {"language": "Java"}
            ...         }
            ...     ]
            ... )
            >>> print(f"Created {result['created']} entities")
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities", "bulk")

        # Make the request
        return self._make_request_with_params('POST', endpoint, json={"entities": entities_data})

    def get_entities_count(self, blueprint_identifier: str) -> int:
        """
        Get the count of entities for the specified blueprint.

        This method retrieves the total number of entities that belong to the specified blueprint.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.

        Returns:
            The count of entities as an integer.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Get the count of service entities
            >>> count = client.entities.get_entities_count("service")
            >>> print(f"There are {count} service entities")
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities-count")

        # Make the request
        response = self._client.make_request('GET', endpoint)

        # Extract and return the count
        return response.json().get("count", 0)

    def get_all_entities(self, blueprint_identifier: str) -> List[Entity]:
        """
        Retrieve all entities for the specified blueprint, including related entities.

        This method retrieves all entities that belong to the specified blueprint,
        including entities that are related to those entities.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.

        Returns:
            A list of entity dictionaries, including related entities.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Get all service entities including related entities
            >>> all_entities = client.entities.get_all_entities("service")
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "all-entities")

        # Make the request
        response = self._client.make_request('GET', endpoint)

        # Extract and return the entities
        return response.json().get("entities", [])

    # Entity Search and Aggregation Methods

    def search_entities(self, search_data: Dict[str, Any]) -> List[Entity]:
        """
        Search for entities across all blueprints.

        This method searches for entities that match the specified criteria
        across all blueprints.

        Args:
            search_data: A dictionary containing search criteria, which may include:
                - query: A string to search for in entity titles and properties
                - filter: A dictionary of filters to apply to the search
                - sort: A dictionary specifying the sort order
                - page: The page number to retrieve
                - per_page: The number of entities per page

        Returns:
            A list of matching entity dictionaries.

        Raises:
            PortValidationError: If the search criteria are invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Search for entities containing "service" in their title
            >>> results = client.entities.search_entities({"query": "service"})
            >>>
            >>> # Search with filters
            >>> results = client.entities.search_entities({
            ...     "filter": {
            ...         "blueprint": "service",
            ...         "properties.language": "Python"
            ...     }
            ... })
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("entities", "search")

        # Make the request
        response = self._make_request_with_params('POST', endpoint, json=search_data)

        # Extract and return the entities
        return response.get("entities", [])

    def search_blueprint_entities(self, blueprint_identifier: str, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for entities within a specific blueprint.

        This method searches for entities that match the specified criteria
        within the specified blueprint. The returned entities are paginated for improved performance.

        Args:
            blueprint_identifier: The unique identifier of the blueprint.
            search_data: A dictionary containing search criteria, which may include:
                - query: A dictionary with search query parameters
                - include: An array of properties/relations to include (using identifiers)
                - exclude: An array of properties/relations to exclude (using identifiers)
                - limit: Maximum number of entities to return (1-1000, default: 200)
                - from: String hash for pagination (from previous response)

        Returns:
            A dictionary containing:
            - ok: Boolean indicating success
            - entities: List of matching entity dictionaries
            - next: String hash for next page (if more results available)

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortValidationError: If the search criteria are invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Basic search
            >>> result = client.entities.search_blueprint_entities(
            ...     "service", {"query": {"title": {"$contains": "api"}}}
            ... )
            >>> entities = result["entities"]
            >>>
            >>> # Search with pagination
            >>> result = client.entities.search_blueprint_entities(
            ...     "service",
            ...     {
            ...         "query": {"properties.language": "Python"},
            ...         "limit": 50
            ...     }
            ... )
            >>> # Get next page
            >>> if "next" in result:
            ...     next_result = client.entities.search_blueprint_entities(
            ...         "service",
            ...         {
            ...             "query": {"properties.language": "Python"},
            ...             "limit": 50,
            ...             "from": result["next"]
            ...         }
            ...     )
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities", "search")

        # Make the request
        response = self._make_request_with_params('POST', endpoint, json=search_data)

        # Return the full response (includes pagination info)
        return response

    def aggregate_entities(self, aggregation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate entities based on specified criteria.

        This method aggregates entities based on the specified criteria,
        allowing you to perform analytics on your entities.

        Args:
            aggregation_data: A dictionary containing aggregation criteria, which may include:
                - filter: A dictionary of filters to apply to the aggregation
                - aggregation_type: The type of aggregation to perform (e.g., "count", "sum")
                - group_by: A list of properties to group by

        Returns:
            A dictionary containing the aggregation results.

        Raises:
            PortValidationError: If the aggregation criteria are invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Count entities by blueprint
            >>> results = client.entities.aggregate_entities({
            ...     "aggregation_type": "count",
            ...     "group_by": ["blueprint"]
            ... })
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("entities", "aggregate")

        # Make the request
        return self._make_request_with_params('POST', endpoint, json=aggregation_data)

    def aggregate_entities_over_time(self, aggregation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate entities over time based on specified criteria.

        This method aggregates entities over time based on the specified criteria,
        allowing you to perform time-based analytics on your entities.

        Args:
            aggregation_data: A dictionary containing aggregation criteria, which may include:
                - filter: A dictionary of filters to apply to the aggregation
                - aggregation_type: The type of aggregation to perform (e.g., "count", "sum")
                - group_by: A list of properties to group by
                - time_frame: The time frame to aggregate over (e.g., "day", "week", "month")
                - start_time: The start time for the aggregation
                - end_time: The end time for the aggregation

        Returns:
            A dictionary containing the time-based aggregation results.

        Raises:
            PortValidationError: If the aggregation criteria are invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Count entities by blueprint over time
            >>> results = client.entities.aggregate_entities_over_time({
            ...     "aggregation_type": "count",
            ...     "group_by": ["blueprint"],
            ...     "time_frame": "day",
            ...     "start_time": "2023-01-01T00:00:00Z",
            ...     "end_time": "2023-01-31T23:59:59Z"
            ... })
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("entities", "aggregate-over-time")

        # Make the request
        return self._make_request_with_params('POST', endpoint, json=aggregation_data)

    def get_entity_properties_history(self, history_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve the history of entity properties.

        This method retrieves the history of property changes for entities
        that match the specified criteria.

        Args:
            history_data: A dictionary containing criteria for retrieving property history, which may include:
                - filter: A dictionary of filters to apply to the entities
                - properties: A list of properties to retrieve history for
                - start_time: The start time for the history
                - end_time: The end time for the history

        Returns:
            A dictionary containing the property history.

        Raises:
            PortValidationError: If the history criteria are invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Get history of language property for a specific entity
            >>> history = client.entities.get_entity_properties_history({
            ...     "filter": {
            ...         "blueprint": "service",
            ...         "identifier": "payment-service"
            ...     },
            ...     "properties": ["language"],
            ...     "start_time": "2023-01-01T00:00:00Z",
            ...     "end_time": "2023-12-31T23:59:59Z"
            ... })
        """
        # Create the endpoint path
        endpoint = self._build_endpoint("entities", "properties-history")

        # Make the request
        return self._make_request_with_params('POST', endpoint, json=history_data)
