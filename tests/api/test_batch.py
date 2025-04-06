"""Tests for batch operations."""
import pytest
from mcp_copper.api.batch import BatchAPI
from mcp_copper.models.opportunities import Opportunity
from mcp_copper.models.people import Person
from mcp_copper.models.companies import Company
from mcp_copper.models.tasks import Task

@pytest.fixture
def batch_api(mock_client):
    """Create a BatchAPI instance with a mock client."""
    return BatchAPI(mock_client)

async def test_batch_create(batch_api, mock_client):
    """Test creating multiple records."""
    # Setup mock response
    mock_client.post.return_value = {"id": 123}

    # Test data
    records = [
        {"name": "Test Opportunity 1", "status": "Open"},
        {"name": "Test Opportunity 2", "status": "Open"}
    ]

    # Execute batch create
    result = await batch_api.create(
        "opportunities",
        records,
        continue_on_error=True,
        return_errors=True
    )

    # Verify results
    assert result["summary"]["total"] == 2
    assert result["summary"]["succeeded"] == 2
    assert result["summary"]["failed"] == 0
    assert len(result["results"]) == 2
    assert all(r["success"] for r in result["results"])
    assert all(r["id"] == 123 for r in result["results"])

    # Verify API calls
    assert mock_client.post.call_count == 2
    for call in mock_client.post.call_args_list:
        assert call[0][0] == "/opportunities"

async def test_batch_create_with_error(batch_api, mock_client):
    """Test batch create with an error."""
    # Setup mock responses
    mock_client.post.side_effect = [
        {"id": 123},
        Exception("API Error")
    ]

    # Test data
    records = [
        {"name": "Test 1", "status": "Open"},
        {"name": "Test 2", "invalid": "data"}
    ]

    # Execute batch create
    result = await batch_api.create(
        "opportunities",
        records,
        continue_on_error=True,
        return_errors=True
    )

    # Verify results
    assert result["summary"]["total"] == 2
    assert result["summary"]["succeeded"] == 1
    assert result["summary"]["failed"] == 1
    assert len(result["results"]) == 2
    assert result["results"][0]["success"]
    assert not result["results"][1]["success"]
    assert "error" in result["results"][1]

async def test_batch_update(batch_api, mock_client):
    """Test updating multiple records."""
    # Setup mock response
    mock_client.put.return_value = {"id": 123}

    # Test data
    records = [
        {"id": 123, "data": {"name": "Updated 1", "status": "Won"}},
        {"id": 456, "data": {"name": "Updated 2", "status": "Lost"}}
    ]

    # Execute batch update
    result = await batch_api.update(
        "opportunities",
        records,
        continue_on_error=True,
        return_errors=True
    )

    # Verify results
    assert result["summary"]["total"] == 2
    assert result["summary"]["succeeded"] == 2
    assert result["summary"]["failed"] == 0
    assert len(result["results"]) == 2
    assert all(r["success"] for r in result["results"])

    # Verify API calls
    assert mock_client.put.call_count == 2
    assert mock_client.put.call_args_list[0][0][0] == "/opportunities/123"
    assert mock_client.put.call_args_list[1][0][0] == "/opportunities/456"

async def test_batch_delete(batch_api, mock_client):
    """Test deleting multiple records."""
    # Setup mock response
    mock_client.delete.return_value = {}

    # Test data
    ids = [123, 456, 789]

    # Execute batch delete
    result = await batch_api.delete(
        "opportunities",
        ids,
        continue_on_error=True,
        return_errors=True
    )

    # Verify results
    assert result["summary"]["total"] == 3
    assert result["summary"]["succeeded"] == 3
    assert result["summary"]["failed"] == 0
    assert len(result["results"]) == 3
    assert all(r["success"] for r in result["results"])

    # Verify API calls
    assert mock_client.delete.call_count == 3
    for i, call in enumerate(mock_client.delete.call_args_list):
        assert call[0][0] == f"/opportunities/{ids[i]}"

async def test_batch_delete_with_error(batch_api, mock_client):
    """Test batch delete with an error."""
    # Setup mock responses
    mock_client.delete.side_effect = [
        {},
        Exception("Not Found"),
        {}
    ]

    # Test data
    ids = [123, 456, 789]

    # Execute batch delete
    result = await batch_api.delete(
        "opportunities",
        ids,
        continue_on_error=True,
        return_errors=True
    )

    # Verify results
    assert result["summary"]["total"] == 3
    assert result["summary"]["succeeded"] == 2
    assert result["summary"]["failed"] == 1
    assert len(result["results"]) == 3
    assert result["results"][0]["success"]
    assert not result["results"][1]["success"]
    assert result["results"][2]["success"]
    assert "error" in result["results"][1]

async def test_batch_operations_stop_on_error(batch_api, mock_client):
    """Test batch operations stopping on error."""
    # Setup mock responses
    mock_client.post.side_effect = [
        {"id": 123},
        Exception("API Error")
    ]

    # Test data
    records = [
        {"name": "Test 1", "status": "Open"},
        {"name": "Test 2", "status": "Open"},
        {"name": "Test 3", "status": "Open"}
    ]

    # Execute batch create with continue_on_error=False
    result = await batch_api.create(
        "opportunities",
        records,
        continue_on_error=False,
        return_errors=True
    )

    # Verify results
    assert result["summary"]["total"] == 3
    assert result["summary"]["succeeded"] == 1
    assert result["summary"]["failed"] == 1
    assert len(result["results"]) == 2  # Only 2 results due to stopping on error
    assert result["results"][0]["success"]
    assert not result["results"][1]["success"]

    # Verify API calls stopped after error
    assert mock_client.post.call_count == 2 