"""
Tests for the Opportunities API module.
"""
import pytest
from datetime import datetime
from decimal import Decimal

from mcp_copper import CopperClient
from mcp_copper.models.opportunities import Opportunity, OpportunityCustomField

@pytest.fixture
def client():
    """Create a test client instance."""
    return CopperClient(
        api_key="test_key",
        user_email="test@example.com",
        base_url="https://api.copper.com"
    )

@pytest.fixture
def sample_opportunity_data():
    """Create sample opportunity data."""
    return {
        "id": 12345,
        "name": "Big Deal",
        "assignee_id": 67890,
        "close_date": int(datetime.now().timestamp()),
        "company_id": 11111,
        "company_name": "Example Corp",
        "customer_source_id": 1,
        "details": "A promising opportunity",
        "loss_reason_id": None,
        "monetary_value": "50000.00",
        "pipeline_id": 222,
        "pipeline_stage_id": 333,
        "priority": "High",
        "probability": 75,
        "status": "Open",
        "tags": ["Enterprise", "Q2"],
        "win_probability": 80,
        "custom_fields": [{
            "field_id": 444,
            "value": "Custom Value"
        }],
        "date_created": int(datetime.now().timestamp()),
        "date_modified": int(datetime.now().timestamp())
    }

def test_opportunity_model_creation(sample_opportunity_data):
    """Test creating an Opportunity model from API data."""
    opportunity = Opportunity.from_api(sample_opportunity_data)
    
    assert opportunity.id == 12345
    assert opportunity.name == "Big Deal"
    assert opportunity.assignee_id == 67890
    assert opportunity.company_id == 11111
    assert opportunity.company_name == "Example Corp"
    assert opportunity.customer_source_id == 1
    assert opportunity.details == "A promising opportunity"
    assert opportunity.monetary_value == Decimal("50000.00")
    assert opportunity.pipeline_id == 222
    assert opportunity.pipeline_stage_id == 333
    assert opportunity.priority == "High"
    assert opportunity.probability == 75
    assert opportunity.status == "Open"
    assert opportunity.tags == ["Enterprise", "Q2"]
    assert opportunity.win_probability == 80
    assert len(opportunity.custom_fields) == 1
    assert isinstance(opportunity.custom_fields[0], OpportunityCustomField)
    assert opportunity.custom_fields[0].custom_field_definition_id == 444
    assert opportunity.created_at is not None
    assert opportunity.updated_at is not None

def test_opportunity_model_to_api(sample_opportunity_data):
    """Test converting an Opportunity model to API format."""
    opportunity = Opportunity.from_api(sample_opportunity_data)
    api_data = opportunity.to_api()
    
    assert api_data["name"] == "Big Deal"
    assert api_data["monetary_value"] == "50000.00"
    assert isinstance(api_data["close_date"], int)

@pytest.mark.asyncio
async def test_list_opportunities(client, sample_opportunity_data, mocker):
    """Test listing opportunities."""
    mock_response = [sample_opportunity_data]
    mocker.patch.object(
        client,
        "get",
        return_value=[Opportunity.from_api(sample_opportunity_data)]
    )
    
    opportunities = client.opportunities.list()
    assert isinstance(opportunities, list)
    assert isinstance(opportunities[0], Opportunity)
    assert opportunities[0].id == 12345

@pytest.mark.asyncio
async def test_get_opportunity(client, sample_opportunity_data, mocker):
    """Test getting a specific opportunity."""
    mocker.patch.object(
        client,
        "get",
        return_value=Opportunity.from_api(sample_opportunity_data)
    )
    
    opportunity = client.opportunities.get(12345)
    assert isinstance(opportunity, Opportunity)
    assert opportunity.id == 12345

@pytest.mark.asyncio
async def test_create_opportunity(client, sample_opportunity_data, mocker):
    """Test creating a new opportunity."""
    mocker.patch.object(
        client,
        "post",
        return_value=Opportunity.from_api(sample_opportunity_data)
    )
    
    new_opportunity = {
        "name": "New Deal",
        "company_id": 11111,
        "monetary_value": "25000.00",
        "pipeline_id": 222,
        "pipeline_stage_id": 333
    }
    
    opportunity = client.opportunities.create(new_opportunity)
    assert isinstance(opportunity, Opportunity)
    assert opportunity.id == 12345

@pytest.mark.asyncio
async def test_update_opportunity(client, sample_opportunity_data, mocker):
    """Test updating an existing opportunity."""
    mocker.patch.object(
        client,
        "put",
        return_value=Opportunity.from_api(sample_opportunity_data)
    )
    
    updated_data = {
        "name": "Updated Deal",
        "monetary_value": "75000.00",
        "probability": 85
    }
    
    opportunity = client.opportunities.update(12345, updated_data)
    assert isinstance(opportunity, Opportunity)
    assert opportunity.id == 12345

@pytest.mark.asyncio
async def test_delete_opportunity(client, mocker):
    """Test deleting an opportunity."""
    mock_delete = mocker.patch.object(client, "delete")
    
    client.opportunities.delete(12345)
    mock_delete.assert_called_once()

@pytest.mark.asyncio
async def test_search_opportunities(client, sample_opportunity_data, mocker):
    """Test searching for opportunities."""
    mock_response = [sample_opportunity_data]
    mocker.patch.object(
        client,
        "search",
        return_value=[Opportunity.from_api(sample_opportunity_data)]
    )
    
    opportunities = client.opportunities.search(query="Big Deal")
    assert isinstance(opportunities, list)
    assert isinstance(opportunities[0], Opportunity)
    assert opportunities[0].id == 12345

@pytest.mark.asyncio
async def test_list_opportunities_with_pipeline_filters(client, sample_opportunity_data, mocker):
    """Test listing opportunities with pipeline filters."""
    mock_response = [sample_opportunity_data]
    mocker.patch.object(
        client,
        "get",
        return_value=[Opportunity.from_api(sample_opportunity_data)]
    )
    
    opportunities = client.opportunities.list(
        pipeline_id=222,
        pipeline_stage_id=333
    )
    assert isinstance(opportunities, list)
    assert isinstance(opportunities[0], Opportunity)
    assert opportunities[0].pipeline_id == 222
    assert opportunities[0].pipeline_stage_id == 333
