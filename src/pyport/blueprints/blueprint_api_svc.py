from typing import Dict, List, Any, Optional, cast

from ..services.base_api_service import BaseAPIService
from ..types import Blueprint


class Blueprints(BaseAPIService):
    """Blueprints API category for managing blueprint definitions.

    Blueprints define the structure of entities in Port. They specify the properties,
    relations, and other metadata that entities of a particular type should have.

    Examples:
        >>> client = PortClient(client_id="your-client-id", client_secret="your-client-secret")
        >>> # Get all blueprints
        >>> blueprints = client.blueprints.get_blueprints()
        >>> # Get a specific blueprint
        >>> service_blueprint = client.blueprints.get_blueprint("service")
        >>> # Create a new blueprint
        >>> new_blueprint = client.blueprints.create_blueprint({
        ...     "identifier": "microservice",
        ...     "title": "Microservice",
        ...     "properties": {
        ...         "language": {
        ...             "type": "string",
        ...             "title": "Language",
        ...             "enum": ["Python", "JavaScript", "Java", "Go"]
        ...         }
        ...     }
        ... })
    """

    def __init__(self, client):
        """Initialize the Blueprints API service.

        Args:
            client: The API client to use for requests.
        """
        super().__init__(client, resource_name="blueprints", response_key="blueprint")

    def get_blueprints(self, page: Optional[int] = None, per_page: Optional[int] = None) -> List[Blueprint]:
        """
        Get all blueprints with pagination support.

        This method retrieves a list of all blueprints defined in Port.
        The results can be paginated using the page and per_page parameters.

        Args:
            page: The page number to retrieve (default: None).
            per_page: The number of blueprints per page (default: None, max: 1000).

        Returns:
            A list of blueprint dictionaries. Each blueprint contains:
            - identifier: The unique identifier of the blueprint
            - title: The display name of the blueprint
            - properties: The property definitions for entities of this blueprint
            - relations: The relation definitions for entities of this blueprint
            - and other metadata

        Examples:
            >>> # Get all blueprints
            >>> blueprints = client.blueprints.get_blueprints()
            >>> # Get the second page of blueprints, 50 per page
            >>> page2 = client.blueprints.get_blueprints(page=2, per_page=50)
        """
        # Use the base class get_all method which handles pagination
        blueprints = self.get_all(page=page, per_page=per_page)
        return cast(List[Blueprint], blueprints)

    def get_blueprint(self, blueprint_identifier: str) -> Blueprint:
        """
        Get a specific blueprint by its identifier.

        This method retrieves detailed information about a specific blueprint.

        Args:
            blueprint_identifier: The unique identifier of the blueprint to retrieve.

        Returns:
            A dictionary containing the blueprint details:
            - identifier: The unique identifier of the blueprint
            - title: The display name of the blueprint
            - properties: The property definitions for entities of this blueprint
            - relations: The relation definitions for entities of this blueprint
            - and other metadata

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Get the 'service' blueprint
            >>> service_blueprint = client.blueprints.get_blueprint("service")
            >>> print(service_blueprint["title"])
            'Service'
        """
        # Use the base class get_by_id method which handles response extraction
        return cast(Blueprint, self.get_by_id(blueprint_identifier))

    def create_blueprint(self, blueprint_data: Dict[str, Any]) -> Blueprint:
        """
        Create a new blueprint.

        This method creates a new blueprint with the specified data.

        Args:
            blueprint_data: A dictionary containing the data for the new blueprint.
                Must include at minimum:
                - identifier: A unique identifier for the blueprint (string)
                - title: A display name for the blueprint (string)

                May also include:
                - description: A description of the blueprint (string)
                - icon: An icon for the blueprint (string)
                - properties: Property definitions for entities of this blueprint (dict)
                - relations: Relation definitions for entities of this blueprint (dict)
                - calculationProperties: Calculated property definitions (dict)

        Returns:
            A dictionary representing the created blueprint.

        Raises:
            PortValidationError: If the blueprint data is invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Create a simple blueprint
            >>> new_blueprint = client.blueprints.create_blueprint({
            ...     "identifier": "microservice",
            ...     "title": "Microservice",
            ...     "properties": {
            ...         "language": {
            ...             "type": "string",
            ...             "title": "Language",
            ...             "enum": ["Python", "JavaScript", "Java", "Go"]
            ...         }
            ...     }
            ... })
        """
        # Use the base class create_resource method which handles response extraction
        return cast(Blueprint, self.create_resource(blueprint_data))

    def update_blueprint(self, blueprint_identifier: str, blueprint_data: Dict[str, Any]) -> Blueprint:
        """
        Update an existing blueprint.

        This method updates an existing blueprint with the specified data.

        Args:
            blueprint_identifier: The unique identifier of the blueprint to update.
            blueprint_data: A dictionary containing the updated data for the blueprint.
                May include any of the fields mentioned in create_blueprint.

        Returns:
            A dictionary representing the updated blueprint.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortValidationError: If the blueprint data is invalid.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Update a blueprint's title
            >>> updated_blueprint = client.blueprints.update_blueprint(
            ...     "microservice",
            ...     {"title": "Cloud Microservice"}
            ... )
        """
        # Use the base class update_resource method which handles response extraction
        return cast(Blueprint, self.update_resource(blueprint_identifier, blueprint_data))

    def delete_blueprint(self, blueprint_identifier: str) -> bool:
        """
        Delete a blueprint.

        This method deletes a blueprint with the specified identifier.
        Note that deleting a blueprint will also delete all entities of that blueprint.

        Args:
            blueprint_identifier: The unique identifier of the blueprint to delete.

        Returns:
            True if deletion was successful, otherwise False.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Delete a blueprint
            >>> success = client.blueprints.delete_blueprint("microservice")
            >>> if success:
            ...     print("Blueprint deleted successfully")
        """
        # Use the base class delete_resource method
        return self.delete_resource(blueprint_identifier)

    # Blueprint Permissions Methods

    def get_blueprint_permissions(self, blueprint_identifier: str) -> Dict:
        """
        Retrieve permissions for a specific blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.

        Returns:
            A dictionary representing the blueprint permissions.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.
        """
        # Use the _build_endpoint method to create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "permissions")
        response = self._client.make_request('GET', endpoint)
        return response.json().get("permissions", {})

    def update_blueprint_permissions(self, blueprint_identifier: str, permissions_data: Dict) -> Dict:
        """
        Update permissions for a specific blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.
            permissions_data: A dictionary containing updated permissions data.

        Returns:
            A dictionary representing the updated blueprint permissions.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortValidationError: If the permissions data is invalid.
            PortApiError: If another API error occurs.
        """
        # Use the _build_endpoint method to create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "permissions")
        response = self._make_request_with_params('PUT', endpoint, json=permissions_data)
        return response.json()

    # Blueprint Property Operations Methods

    def rename_blueprint_property(self, blueprint_identifier: str, property_name: str, rename_data: Dict) -> Dict:
        """
        Rename a property in a blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.
            property_name: The name of the property to rename.
            rename_data: A dictionary containing the new name for the property.

        Returns:
            A dictionary representing the result of the rename operation.

        Raises:
            PortResourceNotFoundError: If the blueprint or property does not exist.
            PortValidationError: If the rename data is invalid.
            PortApiError: If another API error occurs.
        """
        # Use the _build_endpoint method to create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "properties", property_name, "rename")
        response = self._make_request_with_params('POST', endpoint, json=rename_data)
        return response.json()

    def rename_blueprint_mirror(self, blueprint_identifier: str, mirror_name: str, rename_data: Dict) -> Dict:
        """
        Rename a mirror in a blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.
            mirror_name: The name of the mirror to rename.
            rename_data: A dictionary containing the new name for the mirror.

        Returns:
            A dictionary representing the result of the rename operation.

        Raises:
            PortResourceNotFoundError: If the blueprint or mirror does not exist.
            PortValidationError: If the rename data is invalid.
            PortApiError: If another API error occurs.
        """
        # Use the _build_endpoint method to create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "mirror", mirror_name, "rename")
        response = self._make_request_with_params('POST', endpoint, json=rename_data)
        return response.json()

    def rename_blueprint_relation(self, blueprint_identifier: str, relation_identifier: str, rename_data: Dict) -> Dict:
        """
        Rename a relation in a blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.
            relation_identifier: The identifier of the relation to rename.
            rename_data: A dictionary containing the new name for the relation.

        Returns:
            A dictionary representing the result of the rename operation.

        Raises:
            PortResourceNotFoundError: If the blueprint or relation does not exist.
            PortValidationError: If the rename data is invalid.
            PortApiError: If another API error occurs.
        """
        # Use the _build_endpoint method to create the endpoint path
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "relations", relation_identifier, "rename")
        response = self._make_request_with_params('POST', endpoint, json=rename_data)
        return response.json()

    def get_blueprint_system_structure(self, blueprint_identifier: str) -> Dict:
        """
        Retrieve the system structure for a specific blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.

        Returns:
            A dictionary representing the blueprint system structure.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.
        """
        # Use the _build_endpoint method to create the endpoint path
        endpoint = self._build_endpoint("blueprints", "system", blueprint_identifier, "structure")
        response = self._client.make_request('GET', endpoint)
        return response.json()

    def get_blueprint_entities(
        self,
        blueprint_identifier: str,
        exclude_calculated_properties: Optional[bool] = None,
        include: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
        compact: Optional[bool] = None,
        attach_title_to_relation: Optional[bool] = None,
        attach_identifier_to_title_mirror_properties: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get all entities of a blueprint.

        This route allows you to fetch all entities in your software catalog based on a given blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint to operate on.
            exclude_calculated_properties: If true, calculated properties will be excluded from the entities.
            include: An array of values from the entity JSON. Only these values will be returned in the response.
                For example: ["properties.propertyIdentifier", "identifier"]
            exclude: An array of values from the entity JSON to be omitted from the response.
                For example: ["properties.propertyIdentifier", "identifier"]
            compact: Compact response format.
            attach_title_to_relation: Attach title to relation.
            attach_identifier_to_title_mirror_properties: Attach identifier to title mirror properties.

        Returns:
            A dictionary containing:
            - ok: Boolean indicating success
            - entities: List of entity dictionaries

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.

        Examples:
            >>> # Get all entities for a blueprint
            >>> result = client.blueprints.get_blueprint_entities("service")
            >>> entities = result["entities"]

            >>> # Get entities with specific fields only
            >>> result = client.blueprints.get_blueprint_entities(
            ...     "service",
            ...     include=["identifier", "title", "properties.language"]
            ... )

            >>> # Get entities excluding calculated properties
            >>> result = client.blueprints.get_blueprint_entities(
            ...     "service",
            ...     exclude_calculated_properties=True
            ... )
        """
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities")

        # Build query parameters
        params = {}
        if exclude_calculated_properties is not None:
            params["exclude_calculated_properties"] = exclude_calculated_properties
        if include is not None:
            params["include"] = include
        if exclude is not None:
            params["exclude"] = exclude
        if compact is not None:
            params["compact"] = compact
        if attach_title_to_relation is not None:
            params["attach_title_to_relation"] = attach_title_to_relation
        if attach_identifier_to_title_mirror_properties is not None:
            params["attach_identifier_to_title_mirror_properties"] = attach_identifier_to_title_mirror_properties

        response = self._client.make_request('GET', endpoint, params=params)
        return response.json()

    def get_blueprint_entities_count(self, blueprint_identifier: str) -> Dict[str, Any]:
        """
        Get the entity count for a specific blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.

        Returns:
            A dictionary containing the entity count information.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.
        """
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "entities-count")
        response = self._client.make_request('GET', endpoint)
        return response.json()

    def delete_all_blueprint_entities(self, blueprint_identifier: str) -> Dict[str, Any]:
        """
        Delete all entities of a specific blueprint.

        Args:
            blueprint_identifier: The identifier of the blueprint.

        Returns:
            A dictionary containing the deletion result.

        Raises:
            PortResourceNotFoundError: If the blueprint does not exist.
            PortApiError: If another API error occurs.
        """
        endpoint = self._build_endpoint("blueprints", blueprint_identifier, "all-entities")
        response = self._client.make_request('DELETE', endpoint)
        return response.json().get("structure", {})
