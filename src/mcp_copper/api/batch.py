"""
Batch operations for the Copper CRM API.
"""
from typing import Dict, List, Optional, Union, Literal
from ..models.base import BaseModel
from ..models.opportunities import Opportunity
from ..models.people import Person
from ..models.companies import Company
from ..models.tasks import Task

EntityType = Literal["opportunities", "people", "companies", "tasks"]

class BatchAPI:
    """API client for batch operations."""

    def __init__(self, client):
        """Initialize the batch API client.

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

    async def create(
        self,
        entity_type: EntityType,
        records: List[Dict],
        *,
        continue_on_error: bool = True,
        return_errors: bool = True
    ) -> Dict:
        """Create multiple records in a single request.

        Args:
            entity_type: Type of entities to create
            records: List of records to create
            continue_on_error: Whether to continue if some records fail
            return_errors: Whether to return error details for failed records

        Returns:
            Dict containing results and summary
        """
        model_class = self._get_model_class(entity_type)
        results = []
        succeeded = 0
        failed = 0

        for record in records:
            try:
                # Convert to model instance
                instance = model_class(**record)
                # Create via API
                api_data = instance.to_api()
                response = await self.client.post(f"/{entity_type}", json=api_data)
                # Add success result
                results.append({
                    "success": True,
                    "id": response["id"]
                })
                succeeded += 1
            except Exception as e:
                failed += 1
                if return_errors:
                    results.append({
                        "success": False,
                        "error": {
                            "message": str(e),
                            "details": record
                        }
                    })
                if not continue_on_error:
                    break

        return {
            "results": results,
            "summary": {
                "total": len(records),
                "succeeded": succeeded,
                "failed": failed
            }
        }

    async def update(
        self,
        entity_type: EntityType,
        records: List[Dict[str, Union[int, Dict]]],
        *,
        continue_on_error: bool = True,
        return_errors: bool = True
    ) -> Dict:
        """Update multiple records in a single request.

        Args:
            entity_type: Type of entities to update
            records: List of records to update, each containing id and data
            continue_on_error: Whether to continue if some records fail
            return_errors: Whether to return error details for failed records

        Returns:
            Dict containing results and summary
        """
        model_class = self._get_model_class(entity_type)
        results = []
        succeeded = 0
        failed = 0

        for record in records:
            try:
                record_id = record["id"]
                data = record["data"]
                # Convert to model instance
                instance = model_class(**data)
                # Update via API
                api_data = instance.to_api()
                response = await self.client.put(
                    f"/{entity_type}/{record_id}",
                    json=api_data
                )
                # Add success result
                results.append({
                    "success": True,
                    "id": record_id
                })
                succeeded += 1
            except Exception as e:
                failed += 1
                if return_errors:
                    results.append({
                        "success": False,
                        "id": record.get("id"),
                        "error": {
                            "message": str(e),
                            "details": record
                        }
                    })
                if not continue_on_error:
                    break

        return {
            "results": results,
            "summary": {
                "total": len(records),
                "succeeded": succeeded,
                "failed": failed
            }
        }

    async def delete(
        self,
        entity_type: EntityType,
        ids: List[int],
        *,
        continue_on_error: bool = True,
        return_errors: bool = True
    ) -> Dict:
        """Delete multiple records in a single request.

        Args:
            entity_type: Type of entities to delete
            ids: List of record IDs to delete
            continue_on_error: Whether to continue if some records fail
            return_errors: Whether to return error details for failed records

        Returns:
            Dict containing results and summary
        """
        results = []
        succeeded = 0
        failed = 0

        for record_id in ids:
            try:
                # Delete via API
                await self.client.delete(f"/{entity_type}/{record_id}")
                # Add success result
                results.append({
                    "success": True,
                    "id": record_id
                })
                succeeded += 1
            except Exception as e:
                failed += 1
                if return_errors:
                    results.append({
                        "success": False,
                        "id": record_id,
                        "error": {
                            "message": str(e)
                        }
                    })
                if not continue_on_error:
                    break

        return {
            "results": results,
            "summary": {
                "total": len(ids),
                "succeeded": succeeded,
                "failed": failed
            }
        } 