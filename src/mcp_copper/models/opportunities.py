"""
Models for Copper CRM Opportunity entities.
"""
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from decimal import Decimal

from pydantic import Field, condecimal, validator

from .base import CopperModel

class OpportunityCustomField(CopperModel):
    """
    Custom field information for an opportunity.
    
    Attributes:
        custom_field_definition_id: ID of the custom field definition
        value: Value of the custom field
    """
    custom_field_definition_id: int = Field(..., alias="field_id")
    value: Any

    class Config:
        allow_population_by_field_name = True

class Opportunity(CopperModel):
    """
    Model representing an opportunity in Copper CRM.
    
    Attributes:
        id: Unique identifier for the Opportunity
        name: Opportunity name (required)
        assignee_id: ID of assigned user
        close_date: Expected close date
        company_id: ID of associated company
        company_name: Name of associated company
        customer_source_id: Source of the opportunity
        details: Additional details
        loss_reason_id: Reason if opportunity was lost
        monetary_value: Value of the opportunity
        pipeline_id: ID of the pipeline
        pipeline_stage_id: ID of the pipeline stage
        priority: Priority level ("None", "Low", "Medium", "High")
        probability: Win probability percentage (0-100)
        status: Current status ("Open", "Won", "Lost", "Abandoned")
        tags: List of tags
        win_probability: Percentage chance of winning (0-100)
        custom_fields: List of custom field values
        date_created: Time at which this Opportunity was created
        date_modified: Time at which this Opportunity was last modified
    """
    id: Optional[int] = None
    name: str
    assignee_id: Optional[int] = None
    close_date: Optional[datetime] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    customer_source_id: Optional[int] = None
    details: Optional[str] = None
    loss_reason_id: Optional[int] = None
    monetary_value: Optional[condecimal(max_digits=15, decimal_places=2)] = Field(default=None)
    pipeline_id: Optional[int] = None
    pipeline_stage_id: Optional[int] = None
    priority: Optional[Literal["None", "Low", "Medium", "High"]] = None
    probability: Optional[int] = Field(default=None, ge=0, le=100)
    status: Optional[Literal["Open", "Won", "Lost", "Abandoned"]] = "Open"
    tags: List[str] = Field(default_factory=list)
    win_probability: Optional[int] = Field(default=None, ge=0, le=100)
    custom_fields: List[OpportunityCustomField] = Field(default_factory=list)
    date_created: Optional[datetime] = Field(None, alias="created_at")
    date_modified: Optional[datetime] = Field(None, alias="updated_at")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            Decimal: str,
            **CopperModel.Config.json_encoders
        }

    @validator("priority")
    def validate_priority(cls, v):
        """Validate priority is one of the allowed values."""
        if v and v not in ["None", "Low", "Medium", "High"]:
            raise ValueError('priority must be one of: "None", "Low", "Medium", "High"')
        return v

    @validator("status")
    def validate_status(cls, v):
        """Validate status is one of the allowed values."""
        if v and v not in ["Open", "Won", "Lost", "Abandoned"]:
            raise ValueError('status must be one of: "Open", "Won", "Lost", "Abandoned"')
        return v

    @validator("probability", "win_probability")
    def validate_probability(cls, v):
        """Validate probability is between 0 and 100."""
        if v is not None and not (0 <= v <= 100):
            raise ValueError("probability must be between 0 and 100")
        return v

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "Opportunity":
        """
        Create an Opportunity instance from API response data.
        
        Args:
            data: Dictionary containing the API response data
            
        Returns:
            Opportunity instance
        """
        # Handle custom fields
        if "custom_fields" in data and isinstance(data["custom_fields"], list):
            data["custom_fields"] = [
                OpportunityCustomField(**field) for field in data["custom_fields"]
            ]

        # Convert monetary value to Decimal
        if "monetary_value" in data and data["monetary_value"] is not None:
            data["monetary_value"] = Decimal(str(data["monetary_value"]))

        # Convert timestamps to datetime objects
        for date_field in ["close_date", "date_created", "date_modified"]:
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
        Convert Opportunity model to API request format.
        
        Returns:
            Dictionary in the format expected by the API
        """
        data = super().to_api()

        # Convert datetime fields to timestamps
        if self.close_date:
            data["close_date"] = int(self.close_date.timestamp())

        # Convert monetary value to string
        if self.monetary_value is not None:
            data["monetary_value"] = str(self.monetary_value)

        # Map aliased fields back to API format
        if "created_at" in data:
            data["date_created"] = int(data.pop("created_at").timestamp())
        if "updated_at" in data:
            data["date_modified"] = int(data.pop("updated_at").timestamp())

        return data
