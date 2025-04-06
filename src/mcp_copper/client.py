"""
Main client for interacting with the Copper CRM API.
"""
from typing import Optional, Dict, Any, Type
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
import aiohttp

from .config import settings, ENDPOINTS, RATE_LIMIT, DEFAULT_HEADERS
from .utils.auth import get_auth_headers
from .models.base import CopperModel
from .api.people import PeopleAPI
from .api.companies import CompaniesAPI
from .api.opportunities import OpportunitiesAPI
from .api.tasks import TasksAPI
from .api.batch import BatchAPI
from .api.related import RelatedAPI

class CopperClient:
    """
    Client for interacting with the Copper CRM API.
    
    Args:
        api_key: Your Copper API key
        user_email: Your Copper user email
        base_url: Optional base URL override
        timeout: Optional request timeout override
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        user_email: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        self.api_key = api_key
        self.user_email = user_email
        self.base_url = base_url or str(settings.base_url)
        self.timeout = timeout or settings.timeout
        
        # Initialize HTTP client
        self.client = httpx.Client(
            base_url=f"{self.base_url}/api/{settings.api_version}",
            timeout=self.timeout,
            headers={**DEFAULT_HEADERS, **get_auth_headers(api_key, user_email)}
        )
        
        # Initialize API handlers
        self.people = PeopleAPI(self)
        self.companies = CompaniesAPI(self)
        self.opportunities = OpportunitiesAPI(self)
        self.tasks = TasksAPI(self)
        self.batch = BatchAPI(self)
        self.related = RelatedAPI(self)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Close the HTTP client session."""
        self.client.close()
    
    @retry(
        stop=stop_after_attempt(RATE_LIMIT["max_retries"]),
        wait=wait_exponential(
            multiplier=RATE_LIMIT["min_seconds"],
            max=RATE_LIMIT["max_seconds"],
            exp_base=RATE_LIMIT["factor"]
        ),
        reraise=True
    )
    def _request(
        self,
        method: str,
        endpoint: str,
        model: Optional[Type[CopperModel]] = None,
        **kwargs
    ) -> Any:
        """
        Make an HTTP request to the Copper API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            model: Optional Pydantic model for response parsing
            **kwargs: Additional arguments to pass to httpx
            
        Returns:
            Parsed response data
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        response = self.client.request(method, endpoint, **kwargs)
        response.raise_for_status()
        
        data = response.json()
        
        if model and isinstance(data, dict):
            return model.from_api(data)
        elif model and isinstance(data, list):
            return [model.from_api(item) for item in data]
        
        return data
    
    def get(self, endpoint: str, model: Optional[Type[CopperModel]] = None, **kwargs) -> Any:
        """Send GET request."""
        return self._request("GET", endpoint, model, **kwargs)
    
    def post(self, endpoint: str, model: Optional[Type[CopperModel]] = None, **kwargs) -> Any:
        """Send POST request."""
        return self._request("POST", endpoint, model, **kwargs)
    
    def put(self, endpoint: str, model: Optional[Type[CopperModel]] = None, **kwargs) -> Any:
        """Send PUT request."""
        return self._request("PUT", endpoint, model, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> None:
        """Send DELETE request."""
        self._request("DELETE", endpoint, **kwargs)
    
    def search(self, endpoint: str, query: Dict[str, Any], model: Optional[Type[CopperModel]] = None) -> Any:
        """
        Search entities using Copper's search endpoint.
        
        Args:
            endpoint: API endpoint to search
            query: Search query parameters
            model: Optional Pydantic model for response parsing
            
        Returns:
            Search results
        """
        search_endpoint = f"{endpoint}/search"
        return self.post(search_endpoint, model=model, json=query)

    async def connect(self):
        """Create aiohttp session."""
        if self.client is None:
            self.client = httpx.Client(
                base_url=f"{self.base_url}/api/{settings.api_version}",
                timeout=self.timeout,
                headers={**DEFAULT_HEADERS, **get_auth_headers(self.api_key, self.user_email)}
            )

    async def close(self):
        """Close the HTTP client session."""
        await self.client.aclose()
        self.client = None

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Dict:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method
            path: API endpoint path
            params: Query parameters (optional)
            json: Request body (optional)

        Returns:
            API response data

        Raises:
            httpx.HTTPError: If the request fails
        """
        if self.client is None:
            await self.connect()

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.request(
            method,
            url,
            params=params,
            json=json
        )
        response.raise_for_status()
        return await response.json()

    async def get(self, path: str, *, params: Optional[Dict] = None) -> Dict:
        """Make a GET request.

        Args:
            path: API endpoint path
            params: Query parameters (optional)

        Returns:
            API response data
        """
        return await self._request("GET", path, params=params)

    async def post(self, path: str, *, json: Dict) -> Dict:
        """Make a POST request.

        Args:
            path: API endpoint path
            json: Request body

        Returns:
            API response data
        """
        return await self._request("POST", path, json=json)

    async def put(self, path: str, *, json: Dict) -> Dict:
        """Make a PUT request.

        Args:
            path: API endpoint path
            json: Request body

        Returns:
            API response data
        """
        return await self._request("PUT", path, json=json)

    async def delete(self, path: str) -> Dict:
        """Make a DELETE request.

        Args:
            path: API endpoint path

        Returns:
            API response data
        """
        return await self._request("DELETE", path)

    async def get_rate_limits(self) -> Dict:
        """Get current rate limit information.

        Returns:
            Dict containing rate limit details
        """
        response = await self.get("/rate_limits")
        return {
            "limits": {
                "requests_per_second": response["per_second"],
                "requests_per_hour": response["per_hour"],
                "remaining": {
                    "requests_this_second": response["remaining_this_second"],
                    "requests_this_hour": response["remaining_this_hour"]
                },
                "reset_at": response["reset_at"]
            }
        }
