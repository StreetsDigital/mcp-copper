"""
Authentication utilities for Copper CRM API.
"""
from typing import Dict, Optional
import base64

from ..config import settings

def get_auth_headers(api_key: Optional[str] = None, user_email: Optional[str] = None) -> Dict[str, str]:
    """
    Get authentication headers for Copper API requests.
    
    Args:
        api_key: Optional API key override
        user_email: Optional user email override
        
    Returns:
        Dictionary containing authentication headers
        
    Raises:
        ValueError: If API key or user email is not provided
    """
    # Use provided credentials or fall back to settings
    final_api_key = api_key or settings.api_key
    final_user_email = user_email or settings.user_email
    
    if not final_api_key or not final_user_email:
        raise ValueError(
            "API key and user email are required. "
            "Set them via environment variables COPPER_API_KEY and COPPER_USER_EMAIL "
            "or pass them directly to the client."
        )
    
    # Create authentication token
    auth_string = f"{final_user_email}:{final_api_key}"
    auth_bytes = auth_string.encode("ascii")
    auth_b64 = base64.b64encode(auth_bytes).decode("ascii")
    
    return {
        "X-PW-AccessToken": final_api_key,
        "X-PW-UserEmail": final_user_email,
        "Authorization": f"Basic {auth_b64}"
    }
