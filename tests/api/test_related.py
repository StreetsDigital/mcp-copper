"""Tests for related record operations."""
import pytest
from mcp_copper.api.related import RelatedAPI
from mcp_copper.models.opportunities import Opportunity
from mcp_copper.models.people import Person
from mcp_copper.models.companies import Company
from mcp_copper.models.tasks import Task

@pytest.fixture
def related_api(mock_client):
    """Create a RelatedAPI instance with a mock client."""
    return RelatedAPI(mock_client)

async def test_get_related_records(related_api, mock_client):
    """Test getting related records."""
    # Setup mock response
    mock_client.get.return_value = {
        "data": [
            {
                "id": 123,
                "name": "Related Opportunity",
                "status": "Open"
            }
        ],
        "metadata": {
            "total_count": 1,
            "page_count": 1,
            "current_page": 1,
            "per_page": 20,
            "has_more": False
        }
    }

    # Get related opportunities for a company
    result = await related_api.get_related_records(
        "companies",
        456,
        "opportunities",
        page_size=20,
        page_number=1
    )

    # Verify results
    assert "data" in result
    assert "metadata" in result
    assert len(result["data"]) == 1
    assert result["data"][0]["id"] == 123
    assert result["data"][0]["name"] == "Related Opportunity"
    assert result["metadata"]["total_count"] == 1

    # Verify API call
    mock_client.get.assert_called_once_with(
        "/companies/456/related/opportunities",
        params={"page_size": 20, "page_number": 1}
    )

async def test_get_related_activities(related_api, mock_client):
    """Test getting related activities."""
    # Setup mock response
    mock_client.get.return_value = {
        "data": [
            {
                "id": 789,
                "type": "note",
                "action": "created",
                "details": {"content": "Test note"},
                "user_id": 101,
                "occurred_at": "2024-03-15T10:00:00Z"
            }
        ],
        "metadata": {
            "total_count": 1,
            "page_count": 1,
            "current_page": 1,
            "per_page": 20,
            "has_more": False
        }
    }

    # Get activities for an opportunity
    result = await related_api.get_related_records(
        "opportunities",
        123,
        "activities"
    )

    # Verify results
    assert "activities" in result
    assert "metadata" in result
    assert len(result["activities"]) == 1
    assert result["activities"][0]["id"] == 789
    assert result["activities"][0]["type"] == "note"

    # Verify API call
    mock_client.get.assert_called_once_with(
        "/opportunities/123/activities",
        params={}
    )

async def test_get_entity_activities(related_api, mock_client):
    """Test getting entity activities with filters."""
    # Setup mock response
    mock_client.get.return_value = {
        "data": [
            {
                "id": 789,
                "type": "email",
                "action": "sent",
                "details": {"subject": "Test email"},
                "user_id": 101,
                "occurred_at": "2024-03-15T10:00:00Z"
            }
        ],
        "metadata": {
            "total_count": 1,
            "page_count": 1,
            "current_page": 1,
            "per_page": 20,
            "has_more": False
        }
    }

    # Get filtered activities
    result = await related_api.get_entity_activities(
        "people",
        456,
        activity_types=["email"],
        date_from="2024-03-01T00:00:00Z",
        date_to="2024-03-31T23:59:59Z",
        page_size=20,
        page_number=1
    )

    # Verify results
    assert "activities" in result
    assert "metadata" in result
    assert len(result["activities"]) == 1
    assert result["activities"][0]["type"] == "email"

    # Verify API call
    mock_client.get.assert_called_once_with(
        "/people/456/activities",
        params={
            "activity_types": ["email"],
            "date_from": "2024-03-01T00:00:00Z",
            "date_to": "2024-03-31T23:59:59Z",
            "page_size": 20,
            "page_number": 1
        }
    )

async def test_get_related_records_empty(related_api, mock_client):
    """Test getting related records when none exist."""
    # Setup mock response
    mock_client.get.return_value = {
        "data": [],
        "metadata": {
            "total_count": 0,
            "page_count": 0,
            "current_page": 1,
            "per_page": 20,
            "has_more": False
        }
    }

    # Get related tasks for a person
    result = await related_api.get_related_records(
        "people",
        789,
        "tasks"
    )

    # Verify results
    assert "data" in result
    assert "metadata" in result
    assert len(result["data"]) == 0
    assert result["metadata"]["total_count"] == 0

    # Verify API call
    mock_client.get.assert_called_once_with(
        "/people/789/related/tasks",
        params={}
    )

async def test_get_related_records_error_handling(related_api, mock_client):
    """Test error handling for related records."""
    # Setup mock response to raise an exception
    mock_client.get.side_effect = Exception("API Error")

    # Verify that the exception is propagated
    with pytest.raises(Exception) as exc_info:
        await related_api.get_related_records(
            "companies",
            123,
            "opportunities"
        )

    assert str(exc_info.value) == "API Error"
    mock_client.get.assert_called_once_with(
        "/companies/123/related/opportunities",
        params={}
    ) 