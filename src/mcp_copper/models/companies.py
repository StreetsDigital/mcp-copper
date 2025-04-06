"""
Models for Copper CRM Company entities.
"""
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

from pydantic import Field, EmailStr, HttpUrl, validator

from .base import CopperModel

class CompanyCustomField(CopperModel):
    """
    Custom field information for a company.
    
    Attributes:
        custom_field_definition_id: ID of the custom field definition
        value: Value of the custom field
    """
    custom_field_definition_id: int = Field(..., alias="field_id")
    value: Any

    class Config:
        allow_population_by_field_name = True

class CompanyAddress(CopperModel):
    """
    Address information for a company.
    
    Attributes:
        street: Street address
        city: City name
        state: State/province name
        postal_code: ZIP/postal code
        country: Country name
    """
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

class Company(CopperModel):
    """
    Model representing a company in Copper CRM.
    
    Attributes:
        id: Unique identifier for the Company
        name: Company name (required)
        assignee_id: ID of assigned user
        contact_type_id: Type of contact
        details: Additional details
        email_domain: Company email domain
        phone_numbers: List of phone numbers
        socials: Social media profile links
        tags: List of tags
        websites: List of website URLs
        addresses: List of addresses
        parent_company_id: ID of parent company
        interaction_count: Number of interactions
        last_interaction: Date of last interaction
        custom_fields: List of custom field values
        date_created: Time at which this Company was created
        date_modified: Time at which this Company was last modified
    """
    id: Optional[int] = None
    name: str
    assignee_id: Optional[int] = None
    contact_type_id: Optional[int] = None
    details: Optional[str] = None
    email_domain: Optional[str] = None
    phone_numbers: List[str] = Field(default_factory=list)
    socials: Dict[str, HttpUrl] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    websites: List[HttpUrl] = Field(default_factory=list)
    addresses: List[CompanyAddress] = Field(default_factory=list)
    parent_company_id: Optional[int] = None
    interaction_count: Optional[int] = None
    last_interaction: Optional[datetime] = None
    custom_fields: List[CompanyCustomField] = Field(default_factory=list)
    date_created: Optional[datetime] = Field(None, alias="created_at")
    date_modified: Optional[datetime] = Field(None, alias="updated_at")

    class Config:
        allow_population_by_field_name = True

    @validator("interaction_count")
    def validate_interaction_count(cls, v):
        """Validate interaction count is non-negative."""
        if v is not None and v < 0:
            raise ValueError("interaction_count must be non-negative")
        return v

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "Company":
        """
        Create a Company instance from API response data.
        
        Args:
            data: Dictionary containing the API response data
            
        Returns:
            Company instance
        """
        # Handle nested address objects
        if "addresses" in data:
            data["addresses"] = [
                CompanyAddress(**addr) for addr in data["addresses"]
            ]

        # Handle custom fields
        if "custom_fields" in data and isinstance(data["custom_fields"], list):
            data["custom_fields"] = [
                CompanyCustomField(**field) for field in data["custom_fields"]
            ]

        # Handle phone numbers
        if "phone_numbers" in data and isinstance(data["phone_numbers"], list):
            data["phone_numbers"] = [
                phone["number"] for phone in data["phone_numbers"]
                if isinstance(phone, dict) and "number" in phone
            ]

        # Handle websites
        if "websites" in data and isinstance(data["websites"], list):
            data["websites"] = [
                website["url"] for website in data["websites"]
                if isinstance(website, dict) and "url" in website
            ]

        # Convert timestamps to datetime objects
        for date_field in ["last_interaction", "date_created", "date_modified"]:
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
        Convert Company model to API request format.
        
        Returns:
            Dictionary in the format expected by the API
        """
        data = super().to_api()

        # Format phone numbers
        if self.phone_numbers:
            data["phone_numbers"] = [{"number": phone} for phone in self.phone_numbers]

        # Format websites
        if self.websites:
            data["websites"] = [{"url": str(url)} for url in self.websites]

        # Convert datetime fields to timestamps
        if self.last_interaction:
            data["last_interaction"] = int(self.last_interaction.timestamp())

        # Map aliased fields back to API format
        if "created_at" in data:
            data["date_created"] = int(data.pop("created_at").timestamp())
        if "updated_at" in data:
            data["date_modified"] = int(data.pop("updated_at").timestamp())

        return data
