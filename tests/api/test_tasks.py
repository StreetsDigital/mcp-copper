"""
Tests for the Tasks API module.
"""
import pytest
from datetime import datetime

from mcp_copper import CopperClient
from mcp_copper.models.tasks import Task, TaskCustomField

@pytest.fixture
def client():
    """Create a test client instance."""
    return CopperClient(
        api_key="test_key",
        user_email="test@example.com",
        base_url="https://api.copper.com"
    )

@pytest.fixture
def sample_task_data():
    """Create sample task data."""
    return {
        "id": 12345,
        "name": "Follow up with client",
        "assignee_id": 67890,
        "due_date": int(datetime.now().timestamp()),
        "reminder_date": int(datetime.now().timestamp()),
        "priority": "High",
        "status": "Open",
        "details": "Schedule a meeting to discuss proposal",
        "related_resource": "opportunity",
        "related_resource_id": 11111,
        "related_resource_type": "opportunity",
        "completed_date": None,
        "custom_fields": [{
            "field_id": 444,
            "value": "Custom Value"
        }],
        "tags": ["Follow-up", "Q2"],
        "date_created": int(datetime.now().timestamp()),
        "date_modified": int(datetime.now().timestamp())
    }

def test_task_model_creation(sample_task_data):
    """Test creating a Task model from API data."""
    task = Task.from_api(sample_task_data)
    
    assert task.id == 12345
    assert task.name == "Follow up with client"
    assert task.assignee_id == 67890
    assert task.priority == "High"
    assert task.status == "Open"
    assert task.details == "Schedule a meeting to discuss proposal"
    assert task.related_resource == "opportunity"
    assert task.related_resource_id == 11111
    assert task.related_resource_type == "opportunity"
    assert task.completed_date is None
    assert task.tags == ["Follow-up", "Q2"]
    assert len(task.custom_fields) == 1
    assert isinstance(task.custom_fields[0], TaskCustomField)
    assert task.custom_fields[0].custom_field_definition_id == 444
    assert task.created_at is not None
    assert task.updated_at is not None

def test_task_model_to_api(sample_task_data):
    """Test converting a Task model to API format."""
    task = Task.from_api(sample_task_data)
    api_data = task.to_api()
    
    assert api_data["name"] == "Follow up with client"
    assert api_data["priority"] == "High"
    assert isinstance(api_data["due_date"], int)
    assert isinstance(api_data["reminder_date"], int)

@pytest.mark.asyncio
async def test_list_tasks(client, sample_task_data, mocker):
    """Test listing tasks."""
    mock_response = [sample_task_data]
    mocker.patch.object(
        client,
        "get",
        return_value=[Task.from_api(sample_task_data)]
    )
    
    tasks = client.tasks.list()
    assert isinstance(tasks, list)
    assert isinstance(tasks[0], Task)
    assert tasks[0].id == 12345

@pytest.mark.asyncio
async def test_get_task(client, sample_task_data, mocker):
    """Test getting a specific task."""
    mocker.patch.object(
        client,
        "get",
        return_value=Task.from_api(sample_task_data)
    )
    
    task = client.tasks.get(12345)
    assert isinstance(task, Task)
    assert task.id == 12345

@pytest.mark.asyncio
async def test_create_task(client, sample_task_data, mocker):
    """Test creating a new task."""
    mocker.patch.object(
        client,
        "post",
        return_value=Task.from_api(sample_task_data)
    )
    
    new_task = {
        "name": "New Task",
        "assignee_id": 67890,
        "priority": "High",
        "status": "Open"
    }
    
    task = client.tasks.create(new_task)
    assert isinstance(task, Task)
    assert task.id == 12345

@pytest.mark.asyncio
async def test_update_task(client, sample_task_data, mocker):
    """Test updating an existing task."""
    mocker.patch.object(
        client,
        "put",
        return_value=Task.from_api(sample_task_data)
    )
    
    updated_data = {
        "name": "Updated Task",
        "status": "Completed",
        "completed_date": int(datetime.now().timestamp())
    }
    
    task = client.tasks.update(12345, updated_data)
    assert isinstance(task, Task)
    assert task.id == 12345

@pytest.mark.asyncio
async def test_delete_task(client, mocker):
    """Test deleting a task."""
    mock_delete = mocker.patch.object(client, "delete")
    
    client.tasks.delete(12345)
    mock_delete.assert_called_once()

@pytest.mark.asyncio
async def test_search_tasks(client, sample_task_data, mocker):
    """Test searching for tasks."""
    mock_response = [sample_task_data]
    mocker.patch.object(
        client,
        "search",
        return_value=[Task.from_api(sample_task_data)]
    )
    
    tasks = client.tasks.search(query="Follow up")
    assert isinstance(tasks, list)
    assert isinstance(tasks[0], Task)
    assert tasks[0].id == 12345

@pytest.mark.asyncio
async def test_list_tasks_with_filters(client, sample_task_data, mocker):
    """Test listing tasks with filters."""
    mock_response = [sample_task_data]
    mocker.patch.object(
        client,
        "get",
        return_value=[Task.from_api(sample_task_data)]
    )
    
    tasks = client.tasks.list(
        assignee_id=67890,
        status="Open",
        related_resource_type="opportunity"
    )
    assert isinstance(tasks, list)
    assert isinstance(tasks[0], Task)
    assert tasks[0].assignee_id == 67890
    assert tasks[0].status == "Open"
    assert tasks[0].related_resource_type == "opportunity"
