"""
Base model for Copper CRM entities.
"""
from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

class CopperModel(BaseModel):
    """
    Base model for all Copper CRM entities.
    
    Attributes:
        id: The unique identifier of the entity
        created_at: Timestamp when the entity was created
        updated_at: Timestamp when the entity was last updated
        custom_fields: Dictionary of custom field values
    """
    id: Optional[int] = None
    created_at: Optional[datetime] = Field(None, alias="date_created")
    updated_at: Optional[datetime] = Field(None, alias="date_modified")
    custom_fields: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: int(v.timestamp()) if v else None
        }

    def dict(self, *args, **kwargs):
        """Convert model to dictionary, excluding None values."""
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "CopperModel":
        """
        Create a model instance from API response data.
        
        Args:
            data: Dictionary containing the API response data
            
        Returns:
            An instance of the model
        """
        # Convert timestamp strings to datetime objects
        if "date_created" in data and data["date_created"]:
            data["date_created"] = datetime.fromtimestamp(data["date_created"])
        if "date_modified" in data and data["date_modified"]:
            data["date_modified"] = datetime.fromtimestamp(data["date_modified"])
            
        return cls(**data)

    def to_api(self) -> Dict[str, Any]:
        """
        Convert model to API request format.
        
        Returns:
            Dictionary in the format expected by the API
        """
        data = self.dict(by_alias=True)
        
        # Convert datetime objects to timestamps
        if self.created_at:
            data["date_created"] = int(self.created_at.timestamp())
        if self.updated_at:
            data["date_modified"] = int(self.updated_at.timestamp())
            
        return data
