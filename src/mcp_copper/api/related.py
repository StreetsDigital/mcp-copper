"""
Related record operations for the Copper CRM API.
"""
from typing import Dict, List, Optional, Literal
from ..models.base import BaseModel
from ..models.opportunities import Opportunity
from ..models.people import Person
from ..models.companies import Company
from ..models.tasks import Task

EntityType = Literal["opportunities", "people", "companies", "tasks"]
RelatedType = Literal["opportunities", "people", "companies", "tasks", "activities"]

class RelatedAPI:
    """API client for related record operations."""

    def __init__(self, client):
        """Initialize the related records API client.

        Args:
            client: The Copper API client instance
        """
        self.client = client

    def _get_model_class(self, entity_type: EntityType) -> type:
        """Get the model class for an entity type.

        Args:
            entity_type: The type of entity

        Returns:
            The model class for the entity type
        """
        model_map = {
            "opportunities": Opportunity,
            "people": Person,
            "companies": Company,
            "tasks": Task
        }
        return model_map[entity_type]

    async def get_related_records(
        self,
        entity_type: EntityType,
        entity_id: int,
        related_type: RelatedType,
        *,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None
    ) -> Dict:
        """Get records related to a specific entity.

        Args:
            entity_type: Type of the main entity
            entity_id: ID of the main entity
            related_type: Type of related records to fetch
            page_size: Number of records per page
            page_number: Page number (1-based)

        Returns:
            Dict containing related records and pagination metadata
        """
        params = {}
        if page_size is not None:
            params["page_size"] = page_size
        if page_number is not None:
            params["page_number"] = page_number

        # Special handling for activities
        if related_type == "activities":
            response = await self.client.get(
                f"/{entity_type}/{entity_id}/activities",
                params=params
            )
            return {
                "activities": response["data"],
                "metadata": response["metadata"]
            }

        # Get related records
        response = await self.client.get(
            f"/{entity_type}/{entity_id}/related/{related_type}",
            params=params
        )

        # Convert response data to model instances
        model_class = self._get_model_class(related_type)
        data = [
            model_class.from_api(item)
            for item in response["data"]
        ]

        return {
            "data": [item.dict() for item in data],
            "metadata": response["metadata"]
        }

    async def get_entity_activities(
        self,
        entity_type: EntityType,
        entity_id: int,
        *,
        activity_types: Optional[List[str]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None
    ) -> Dict:
        """Get activity history for a specific entity.

        Args:
            entity_type: Type of the entity
            entity_id: ID of the entity
            activity_types: Filter by activity types
            date_from: Start date (ISO format)
            date_to: End date (ISO format)
            page_size: Number of records per page
            page_number: Page number (1-based)

        Returns:
            Dict containing activities and pagination metadata
        """
        params = {}
        if activity_types:
            params["activity_types"] = activity_types
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        if page_size is not None:
            params["page_size"] = page_size
        if page_number is not None:
            params["page_number"] = page_number

        response = await self.client.get(
            f"/{entity_type}/{entity_id}/activities",
            params=params
        )

        return {
            "activities": response["data"],
            "metadata": response["metadata"]
        } 