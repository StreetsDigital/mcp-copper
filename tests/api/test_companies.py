"""Tests for the Companies API."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp_copper.client import CopperClient
from mcp_copper.models.companies import Company, CompanyAddress

def create_mock_response(data):
    """Create a mock response object."""
    response = AsyncMock()
    response.raise_for_status.return_value = None
    response.json.return_value = data
    return response

@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    mock = AsyncMock()
    return mock

class TestCompaniesAPI:
    """Test cases for the Companies API."""

    def test_company_model_creation(self):
        """Test creating a Company model instance."""
        company = Company(
            id=1,
            name="Test Company",
            details="Test details",
            email_domain="test.com",
            phone_numbers=[],
            socials=[],
            websites=[],
            addresses=[]
        )
        assert company.id == 1
        assert company.name == "Test Company"

    def test_company_model_to_api(self):
        """Test converting a Company model to API format."""
        company = Company(
            id=1,
            name="Test Company",
            details="Test details",
            email_domain="test.com",
            phone_numbers=[],
            socials=[],
            websites=[],
            addresses=[]
        )
        api_data = company.to_api()
        assert api_data["id"] == 1
        assert api_data["name"] == "Test Company"

    @pytest.mark.asyncio
    async def test_list_companies(self, mock_client):
        """Test listing companies."""
        client = CopperClient(
            api_key="test_key",
            user_email="test@example.com"
        )
        mock_response_data = {
            "data": [
                {
                    "id": 1,
                    "name": "Test Company",
                    "details": "Test details",
                    "email_domain": "test.com",
                    "phone_numbers": [],
                    "socials": [],
                    "websites": [],
                    "addresses": []
                }
            ]
        }
        mock_client.request.return_value = create_mock_response(mock_response_data)
        client.client = mock_client
        companies = await client.companies.list_companies()
        assert isinstance(companies, list)
        assert len(companies) > 0
        assert isinstance(companies[0], Company)

    @pytest.mark.asyncio
    async def test_get_company(self, mock_client):
        """Test getting a single company."""
        client = CopperClient(
            api_key="test_key",
            user_email="test@example.com"
        )
        mock_response_data = {
            "id": 1,
            "name": "Test Company",
            "details": "Test details",
            "email_domain": "test.com",
            "phone_numbers": [],
            "socials": [],
            "websites": [],
            "addresses": []
        }
        mock_client.request.return_value = create_mock_response(mock_response_data)
        client.client = mock_client
        company = await client.companies.get_company(1)
        assert isinstance(company, Company)
        assert company.id == 1

    @pytest.mark.asyncio
    async def test_create_company(self, mock_client):
        """Test creating a company."""
        client = CopperClient(
            api_key="test_key",
            user_email="test@example.com"
        )
        mock_response_data = {
            "id": 1,
            "name": "Test Company",
            "details": "Test details",
            "email_domain": "test.com",
            "phone_numbers": [],
            "socials": [],
            "websites": [],
            "addresses": []
        }
        mock_client.request.return_value = create_mock_response(mock_response_data)
        client.client = mock_client
        data = {
            "name": "Test Company",
            "details": "Test details",
            "email_domain": "test.com"
        }
        company = await client.companies.create_company(data)
        assert isinstance(company, Company)
        assert company.name == "Test Company"

    @pytest.mark.asyncio
    async def test_update_company(self, mock_client):
        """Test updating a company."""
        client = CopperClient(
            api_key="test_key",
            user_email="test@example.com"
        )
        mock_response_data = {
            "id": 1,
            "name": "Updated Company",
            "details": "Updated details",
            "email_domain": "test.com",
            "phone_numbers": [],
            "socials": [],
            "websites": [],
            "addresses": []
        }
        mock_client.request.return_value = create_mock_response(mock_response_data)
        client.client = mock_client
        data = {
            "name": "Updated Company",
            "details": "Updated details"
        }
        company = await client.companies.update_company(1, data)
        assert isinstance(company, Company)
        assert company.id == 1
        assert company.name == "Updated Company"

    @pytest.mark.asyncio
    async def test_delete_company(self, mock_client):
        """Test deleting a company."""
        client = CopperClient(
            api_key="test_key",
            user_email="test@example.com"
        )
        mock_client.request.return_value = create_mock_response(None)
        client.client = mock_client
        result = await client.companies.delete_company(1)
        assert result is None

    @pytest.mark.asyncio
    async def test_search_companies(self, mock_client):
        """Test searching companies."""
        client = CopperClient(
            api_key="test_key",
            user_email="test@example.com"
        )
        mock_response_data = {
            "data": [
                {
                    "id": 1,
                    "name": "Test Company",
                    "details": "Test details",
                    "email_domain": "test.com",
                    "phone_numbers": [],
                    "socials": [],
                    "websites": [],
                    "addresses": []
                }
            ]
        }
        mock_client.request.return_value = create_mock_response(mock_response_data)
        client.client = mock_client
        companies = await client.companies.search_companies("test")
        assert isinstance(companies, list)
        assert len(companies) > 0
        assert isinstance(companies[0], Company)
