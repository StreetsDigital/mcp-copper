"""
Models for Copper CRM People entities.
"""
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

from pydantic import Field, EmailStr, validator

from .base import CopperModel

class PersonCustomField(CopperModel):
    """
    Custom field information for a person.
    
    Attributes:
        custom_field_definition_id: ID of the custom field definition
        value: Value of the custom field
    """
    custom_field_definition_id: int = Field(..., alias="field_id")
    value: Any

    class Config:
        allow_population_by_field_name = True

class PersonAddress(CopperModel):
    """
    Address information for a person.
    
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

class Person(CopperModel):
    """
    Model representing a person in Copper CRM.
    
    Attributes:
        id: Unique identifier for the Person
        name: Person's full name (required)
        prefix: Name prefix (e.g., Mr., Mrs., Dr.)
        first_name: First name
        last_name: Last name
        suffix: Name suffix
        emails: List of email addresses
        phone_numbers: List of phone numbers
        addresses: List of addresses
        title: Job title
        company_id: ID of associated company
        company_name: Name of associated company
        tags: List of tags
        social_links: Social media profile links
        details: Additional details
        assignee_id: ID of assigned user
        status: Contact status (one of: "Active", "Inactive", "Lead", "Customer")
        contact_type_id: Type of contact
        interaction_count: Number of interactions
        last_interaction: Date of last interaction
        custom_fields: List of custom field values
        date_created: Time at which this Person was created
        date_modified: Time at which this Person was last modified
    """
    id: Optional[int] = None
    name: str
    prefix: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    suffix: Optional[str] = None
    
    emails: List[EmailStr] = Field(default_factory=list)
    phone_numbers: List[str] = Field(default_factory=list)
    addresses: List[PersonAddress] = Field(default_factory=list)
    
    title: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    
    tags: List[str] = Field(default_factory=list)
    social_links: Dict[str, str] = Field(default_factory=dict)
    details: Optional[str] = None
    
    assignee_id: Optional[int] = None
    status: Optional[Literal["Active", "Inactive", "Lead", "Customer"]] = "Active"
    contact_type_id: Optional[int] = None
    
    interaction_count: Optional[int] = None
    last_interaction: Optional[datetime] = None
    custom_fields: List[PersonCustomField] = Field(default_factory=list)
    date_created: Optional[datetime] = Field(None, alias="created_at")
    date_modified: Optional[datetime] = Field(None, alias="updated_at")
    
    class Config:
        allow_population_by_field_name = True
    
    @validator("interaction_count", allow_reuse=True)
    def validate_interaction_count(cls, v):
        """Validate interaction count is non-negative."""
        if v is not None and v < 0:
            raise ValueError("interaction_count must be non-negative")
        return v
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "Person":
        """
        Create a Person instance from API response data.
        
        Args:
            data: Dictionary containing the API response data
            
        Returns:
            Person instance
        """
        # Handle nested address objects
        if "addresses" in data:
            data["addresses"] = [
                PersonAddress(**addr) for addr in data["addresses"]
            ]
            
        # Handle email addresses
        if "emails" in data and isinstance(data["emails"], list):
            data["emails"] = [
                email["email"] for email in data["emails"]
                if isinstance(email, dict) and "email" in email
            ]
            
        # Handle phone numbers
        if "phone_numbers" in data and isinstance(data["phone_numbers"], list):
            data["phone_numbers"] = [
                phone["number"] for phone in data["phone_numbers"]
                if isinstance(phone, dict) and "number" in phone
            ]

        # Handle custom fields
        if "custom_fields" in data and isinstance(data["custom_fields"], list):
            data["custom_fields"] = [
                PersonCustomField(**field) for field in data["custom_fields"]
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
        Convert Person model to API request format.
        
        Returns:
            Dictionary in the format expected by the API
        """
        data = super().to_api()
        
        # Format email addresses
        if self.emails:
            data["emails"] = [{"email": email} for email in self.emails]
            
        # Format phone numbers
        if self.phone_numbers:
            data["phone_numbers"] = [{"number": phone} for phone in self.phone_numbers]

        # Convert datetime fields to timestamps
        if self.last_interaction:
            data["last_interaction"] = int(self.last_interaction.timestamp())

        # Map aliased fields back to API format
        if "created_at" in data:
            data["date_created"] = int(data.pop("created_at").timestamp())
        if "updated_at" in data:
            data["date_modified"] = int(data.pop("updated_at").timestamp())
            
        return data
