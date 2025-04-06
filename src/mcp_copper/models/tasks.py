"""
Models for Copper CRM Task entities.
"""
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

from pydantic import Field, validator

from .base import CopperModel

class TaskCustomField(CopperModel):
    """
    Custom field information for a task.
    
    Attributes:
        custom_field_definition_id: ID of the custom field definition
        value: Value of the custom field
    """
    custom_field_definition_id: int = Field(..., alias="field_id")
    value: Any

    class Config:
        allow_population_by_field_name = True

class Task(CopperModel):
    """
    Model representing a task in Copper CRM.
    
    Attributes:
        id: Unique identifier for the Task
        name: The name of the Task (required)
        assignee_id: Unique identifier of the User that will be the owner of the Task
        due_date: The date on which the Task is due
        reminder_date: The date on which to receive a reminder about the Task
        priority: The priority of the Task ("None", "Low", "Medium", "High")
        status: The status of the Task ("Open", "Completed")
        details: Description of the Task
        related_resource: The primary related resource for the Task
        related_resource_id: ID of the related resource
        related_resource_type: Type of the related resource
        completed_date: The date on which the Task was completed
        custom_fields: Array of custom field values belonging to the Task
        tags: Array of tags associated with the Task
        date_created: Time at which this Task was created
        date_modified: Time at which this Task was last modified
    """
    id: Optional[int] = None
    name: str
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    priority: Optional[Literal["None", "Low", "Medium", "High"]] = None
    status: Optional[Literal["Open", "Completed"]] = "Open"
    details: Optional[str] = None
    related_resource: Optional[str] = None
    related_resource_id: Optional[int] = None
    related_resource_type: Optional[str] = None
    completed_date: Optional[datetime] = None
    custom_fields: List[TaskCustomField] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    date_created: Optional[datetime] = Field(None, alias="created_at")
    date_modified: Optional[datetime] = Field(None, alias="updated_at")

    class Config:
        allow_population_by_field_name = True

    @validator("priority")
    def validate_priority(cls, v):
        """Validate priority is one of the allowed values."""
        if v and v not in ["None", "Low", "Medium", "High"]:
            raise ValueError('priority must be one of: "None", "Low", "Medium", "High"')
        return v

    @validator("status")
    def validate_status(cls, v):
        """Validate status is one of the allowed values."""
        if v and v not in ["Open", "Completed"]:
            raise ValueError('status must be one of: "Open", "Completed"')
        return v

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "Task":
        """
        Create a Task instance from API response data.
        
        Args:
            data: Dictionary containing the API response data
            
        Returns:
            Task instance
        """
        # Handle custom fields
        if "custom_fields" in data and isinstance(data["custom_fields"], list):
            data["custom_fields"] = [
                TaskCustomField(**field) for field in data["custom_fields"]
            ]

        # Convert timestamps to datetime objects
        for date_field in ["due_date", "reminder_date", "completed_date", "date_created", "date_modified"]:
            if date_field in data and data[date_field]:
                data[date_field] = datetime.fromtimestamp(data[date_field])

        # Map date fields to their aliases
        if "date_created" in data:
            data["created_at"] = data.pop("date_created")
        if "date_modified" in data:
            data["updated_at"] = data.pop("date_modified")

        return super().from_api(data)

    def to_api(self) -> Dict[str, Any]:
        """
        Convert Task model to API request format.
        
        Returns:
            Dictionary in the format expected by the API
        """
        data = super().to_api()

        # Convert datetime fields to timestamps
        for date_field in ["due_date", "reminder_date", "completed_date"]:
            value = getattr(self, date_field)
            if value:
                data[date_field] = int(value.timestamp())

        # Map aliased fields back to API format
        if "created_at" in data:
            data["date_created"] = int(data.pop("created_at").timestamp())
        if "updated_at" in data:
            data["date_modified"] = int(data.pop("updated_at").timestamp())

        return data
