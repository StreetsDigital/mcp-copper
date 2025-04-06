"""
API operations for Copper CRM Companies endpoints.
"""
from typing import Optional, List, Dict, Any, Union

from ..models.companies import Company

class CompaniesAPI:
    """
    Handler for Copper CRM Companies API endpoints.
    
    Args:
        client: Initialized CopperClient instance
    """
    
    def __init__(self, client):
        """Initialize the companies API client.

        Args:
            client: The Copper API client instance
        """
        self.client = client
        self.endpoint = "/companies"
    
    async def list_companies(
        self,
        *,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None
    ) -> List[Company]:
        """List companies with optional filtering and pagination.

        Args:
            page_size: Number of records per page
            page_number: Page number (1-based)
            sort_by: Field to sort by
            sort_direction: Sort direction ("asc" or "desc")

        Returns:
            List of Company instances
        """
        params = {}
        if page_size is not None:
            params["page_size"] = page_size
        if page_number is not None:
            params["page_number"] = page_number
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_direction is not None:
            params["sort_direction"] = sort_direction

        response = await self.client.get(self.endpoint, params=params)
        return [Company.from_api(item) for item in response["data"]]
    
    async def get_company(self, company_id: int) -> Company:
        """Get a specific company by ID.

        Args:
            company_id: The company ID

        Returns:
            Company instance
        """
        response = await self.client.get(f"{self.endpoint}/{company_id}")
        return Company.from_api(response)
    
    async def create_company(self, data: Dict) -> Company:
        """Create a new company.

        Args:
            data: Company data

        Returns:
            Created Company instance
        """
        company = Company(**data)
        response = await self.client.post(self.endpoint, json=company.to_api())
        return Company.from_api(response)
    
    async def update_company(self, company_id: int, data: Dict) -> Company:
        """Update an existing company.

        Args:
            company_id: The company ID
            data: Updated company data

        Returns:
            Updated Company instance
        """
        company = Company(**data)
        response = await self.client.put(
            f"{self.endpoint}/{company_id}",
            json=company.to_api()
        )
        return Company.from_api(response)
    
    async def delete_company(self, company_id: int) -> None:
        """Delete a company.

        Args:
            company_id: The company ID
        """
        await self.client.delete(f"{self.endpoint}/{company_id}")
    
    async def search_companies(self, query: str) -> List[Company]:
        """Search for companies.

        Args:
            query: Search query string

        Returns:
            List of matching Company instances
        """
        response = await self.client.get(
            f"{self.endpoint}/search",
            params={"query": query}
        )
        return [Company.from_api(item) for item in response["data"]]
