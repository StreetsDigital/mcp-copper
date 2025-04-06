"""
Configuration settings for the Copper CRM client.
"""
from typing import Optional
from pydantic import BaseSettings, HttpUrl

class Settings(BaseSettings):
    """
    Configuration settings for the Copper CRM client.
    
    Attributes:
        api_key: Your Copper API key
        user_email: Your Copper user email
        base_url: The base URL for the Copper API
        api_version: The API version to use
        timeout: Request timeout in seconds
    """
    api_key: Optional[str] = None
    user_email: Optional[str] = None
    base_url: HttpUrl = "https://api.copper.com"
    api_version: str = "v1"
    timeout: int = 30

    class Config:
        env_prefix = "COPPER_"
        case_sensitive = False

# Default settings instance
settings = Settings()

# API endpoints
ENDPOINTS = {
    "people": "/people",
    "companies": "/companies",
    "opportunities": "/opportunities",
    "tasks": "/tasks",
    "activities": "/activities",
    "projects": "/projects",
    "custom_fields": "/custom_field_definitions",
}

# Rate limiting settings
RATE_LIMIT = {
    "max_retries": 3,
    "min_seconds": 1,
    "max_seconds": 60,
    "factor": 2,
}

# HTTP headers
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "X-PW-Application": "developer_api",
}
