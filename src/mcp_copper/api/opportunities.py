"""
API operations for Copper CRM Opportunities endpoints.
"""
from typing import Optional, List, Dict, Any, Union

from ..models.opportunities import Opportunity
from ..config import ENDPOINTS

class OpportunitiesAPI:
    """
    Handler for Copper CRM Opportunities API endpoints.
    
    Args:
        client: Initialized CopperClient instance
    """
    
    def __init__(self, client):
        self.client = client
        self.endpoint = ENDPOINTS["opportunities"]
    
    def list(
        self,
        page_size: int = 20,
        page_number: int = 1,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        pipeline_id: Optional[int] = None,
        pipeline_stage_id: Optional[int] = None
    ) -> List[Opportunity]:
        """
        Get a list of opportunities.
        
        Args:
            page_size: Number of records per page
            page_number: Page number to fetch
            sort_by: Field to sort by
            sort_direction: Sort direction ('asc' or 'desc')
            pipeline_id: Filter by pipeline ID
            pipeline_stage_id: Filter by pipeline stage ID
            
        Returns:
            List of Opportunity objects
        """
        params = {
            "page_size": page_size,
            "page_number": page_number
        }
        
        if sort_by:
            params["sort_by"] = sort_by
        if sort_direction:
            params["sort_direction"] = sort_direction
        if pipeline_id:
            params["pipeline_id"] = pipeline_id
        if pipeline_stage_id:
            params["pipeline_stage_id"] = pipeline_stage_id
            
        return self.client.get(self.endpoint, model=Opportunity, params=params)
    
    def get(self, opportunity_id: int) -> Opportunity:
        """
        Get a specific opportunity by ID.
        
        Args:
            opportunity_id: The ID of the opportunity to retrieve
            
        Returns:
            Opportunity object
        """
        return self.client.get(f"{self.endpoint}/{opportunity_id}", model=Opportunity)
    
    def create(self, opportunity: Union[Opportunity, Dict[str, Any]]) -> Opportunity:
        """
        Create a new opportunity.
        
        Args:
            opportunity: Opportunity object or dictionary with opportunity data
            
        Returns:
            Created Opportunity object
        """
        if isinstance(opportunity, Opportunity):
            data = opportunity.to_api()
        else:
            data = opportunity
            
        return self.client.post(self.endpoint, model=Opportunity, json=data)
    
    def update(
        self,
        opportunity_id: int,
        opportunity: Union[Opportunity, Dict[str, Any]]
    ) -> Opportunity:
        """
        Update an existing opportunity.
        
        Args:
            opportunity_id: The ID of the opportunity to update
            opportunity: Opportunity object or dictionary with updated data
            
        Returns:
            Updated Opportunity object
        """
        if isinstance(opportunity, Opportunity):
            data = opportunity.to_api()
        else:
            data = opportunity
            
        return self.client.put(
            f"{self.endpoint}/{opportunity_id}",
            model=Opportunity,
            json=data
        )
    
    def delete(self, opportunity_id: int) -> None:
        """
        Delete an opportunity.
        
        Args:
            opportunity_id: The ID of the opportunity to delete
        """
        self.client.delete(f"{self.endpoint}/{opportunity_id}")
    
    def search(
        self,
        query: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None,
        page_size: int = 20,
        page_number: int = 1,
        pipeline_id: Optional[int] = None,
        pipeline_stage_id: Optional[int] = None
    ) -> List[Opportunity]:
        """
        Search for opportunities.
        
        Args:
            query: Text to search for across all fields
            fields: Dictionary of field-specific search criteria
            page_size: Number of records per page
            page_number: Page number to fetch
            pipeline_id: Filter by pipeline ID
            pipeline_stage_id: Filter by pipeline stage ID
            
        Returns:
            List of matching Opportunity objects
        """
        search_params = {
            "page_size": page_size,
            "page_number": page_number
        }
        
        if query:
            search_params["query"] = query
        if fields:
            search_params.update(fields)
        if pipeline_id:
            search_params["pipeline_id"] = pipeline_id
        if pipeline_stage_id:
            search_params["pipeline_stage_id"] = pipeline_stage_id
            
        return self.client.search(self.endpoint, search_params, model=Opportunity)
