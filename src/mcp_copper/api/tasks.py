"""
API operations for Copper CRM Tasks endpoints.
"""
from typing import Optional, List, Dict, Any, Union

from ..models.tasks import Task
from ..config import ENDPOINTS

class TasksAPI:
    """
    Handler for Copper CRM Tasks API endpoints.
    
    Args:
        client: Initialized CopperClient instance
    """
    
    def __init__(self, client):
        self.client = client
        self.endpoint = ENDPOINTS["tasks"]
    
    def list(
        self,
        page_size: int = 20,
        page_number: int = 1,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        assignee_id: Optional[int] = None,
        status: Optional[str] = None,
        related_resource_type: Optional[str] = None,
        related_resource_id: Optional[int] = None
    ) -> List[Task]:
        """
        Get a list of tasks.
        
        Args:
            page_size: Number of records per page
            page_number: Page number to fetch
            sort_by: Field to sort by
            sort_direction: Sort direction ('asc' or 'desc')
            assignee_id: Filter by assigned user ID
            status: Filter by task status
            related_resource_type: Filter by related resource type
            related_resource_id: Filter by related resource ID
            
        Returns:
            List of Task objects
        """
        params = {
            "page_size": page_size,
            "page_number": page_number
        }
        
        if sort_by:
            params["sort_by"] = sort_by
        if sort_direction:
            params["sort_direction"] = sort_direction
        if assignee_id:
            params["assignee_id"] = assignee_id
        if status:
            params["status"] = status
        if related_resource_type:
            params["related_resource_type"] = related_resource_type
        if related_resource_id:
            params["related_resource_id"] = related_resource_id
            
        return self.client.get(self.endpoint, model=Task, params=params)
    
    def get(self, task_id: int) -> Task:
        """
        Get a specific task by ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            Task object
        """
        return self.client.get(f"{self.endpoint}/{task_id}", model=Task)
    
    def create(self, task: Union[Task, Dict[str, Any]]) -> Task:
        """
        Create a new task.
        
        Args:
            task: Task object or dictionary with task data
            
        Returns:
            Created Task object
        """
        if isinstance(task, Task):
            data = task.to_api()
        else:
            data = task
            
        return self.client.post(self.endpoint, model=Task, json=data)
    
    def update(
        self,
        task_id: int,
        task: Union[Task, Dict[str, Any]]
    ) -> Task:
        """
        Update an existing task.
        
        Args:
            task_id: The ID of the task to update
            task: Task object or dictionary with updated data
            
        Returns:
            Updated Task object
        """
        if isinstance(task, Task):
            data = task.to_api()
        else:
            data = task
            
        return self.client.put(
            f"{self.endpoint}/{task_id}",
            model=Task,
            json=data
        )
    
    def delete(self, task_id: int) -> None:
        """
        Delete a task.
        
        Args:
            task_id: The ID of the task to delete
        """
        self.client.delete(f"{self.endpoint}/{task_id}")
    
    def search(
        self,
        query: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None,
        page_size: int = 20,
        page_number: int = 1,
        assignee_id: Optional[int] = None,
        status: Optional[str] = None,
        related_resource_type: Optional[str] = None,
        related_resource_id: Optional[int] = None
    ) -> List[Task]:
        """
        Search for tasks.
        
        Args:
            query: Text to search for across all fields
            fields: Dictionary of field-specific search criteria
            page_size: Number of records per page
            page_number: Page number to fetch
            assignee_id: Filter by assigned user ID
            status: Filter by task status
            related_resource_type: Filter by related resource type
            related_resource_id: Filter by related resource ID
            
        Returns:
            List of matching Task objects
        """
        search_params = {
            "page_size": page_size,
            "page_number": page_number
        }
        
        if query:
            search_params["query"] = query
        if fields:
            search_params.update(fields)
        if assignee_id:
            search_params["assignee_id"] = assignee_id
        if status:
            search_params["status"] = status
        if related_resource_type:
            search_params["related_resource_type"] = related_resource_type
        if related_resource_id:
            search_params["related_resource_id"] = related_resource_id
            
        return self.client.search(self.endpoint, search_params, model=Task)
