"""
API operations for Copper CRM People endpoints.
"""
from typing import Optional, List, Dict, Any, Union

from ..models.people import Person
from ..config import ENDPOINTS

class PeopleAPI:
    """
    Handler for Copper CRM People API endpoints.
    
    Args:
        client: Initialized CopperClient instance
    """
    
    def __init__(self, client):
        self.client = client
        self.endpoint = ENDPOINTS["people"]
    
    def list(
        self,
        page_size: int = 20,
        page_number: int = 1,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None
    ) -> List[Person]:
        """
        Get a list of people.
        
        Args:
            page_size: Number of records per page
            page_number: Page number to fetch
            sort_by: Field to sort by
            sort_direction: Sort direction ('asc' or 'desc')
            
        Returns:
            List of Person objects
        """
        params = {
            "page_size": page_size,
            "page_number": page_number
        }
        
        if sort_by:
            params["sort_by"] = sort_by
        if sort_direction:
            params["sort_direction"] = sort_direction
            
        return self.client.get(self.endpoint, model=Person, params=params)
    
    def get(self, person_id: int) -> Person:
        """
        Get a specific person by ID.
        
        Args:
            person_id: The ID of the person to retrieve
            
        Returns:
            Person object
        """
        return self.client.get(f"{self.endpoint}/{person_id}", model=Person)
    
    def create(self, person: Union[Person, Dict[str, Any]]) -> Person:
        """
        Create a new person.
        
        Args:
            person: Person object or dictionary with person data
            
        Returns:
            Created Person object
        """
        if isinstance(person, Person):
            data = person.to_api()
        else:
            data = person
            
        return self.client.post(self.endpoint, model=Person, json=data)
    
    def update(
        self,
        person_id: int,
        person: Union[Person, Dict[str, Any]]
    ) -> Person:
        """
        Update an existing person.
        
        Args:
            person_id: The ID of the person to update
            person: Person object or dictionary with updated data
            
        Returns:
            Updated Person object
        """
        if isinstance(person, Person):
            data = person.to_api()
        else:
            data = person
            
        return self.client.put(
            f"{self.endpoint}/{person_id}",
            model=Person,
            json=data
        )
    
    def delete(self, person_id: int) -> None:
        """
        Delete a person.
        
        Args:
            person_id: The ID of the person to delete
        """
        self.client.delete(f"{self.endpoint}/{person_id}")
    
    def search(
        self,
        query: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None,
        page_size: int = 20,
        page_number: int = 1
    ) -> List[Person]:
        """
        Search for people.
        
        Args:
            query: Text to search for across all fields
            fields: Dictionary of field-specific search criteria
            page_size: Number of records per page
            page_number: Page number to fetch
            
        Returns:
            List of matching Person objects
        """
        search_params = {
            "page_size": page_size,
            "page_number": page_number
        }
        
        if query:
            search_params["query"] = query
        if fields:
            search_params.update(fields)
            
        return self.client.search(self.endpoint, search_params, model=Person)
