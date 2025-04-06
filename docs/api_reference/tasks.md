# Copper CRM Tasks Tools

## Overview
Tools for managing tasks in Copper CRM through the Model Context Protocol (MCP).

## Example Prompts

```
Create a follow-up task for the meeting with TechCorp:
{
    "name": "Follow up on TechCorp meeting",
    "related_resource": {
        "type": "opportunity",
        "id": 12345
    },
    "assignee_id": 67890,
    "due_date": "2024-03-20",
    "priority": "High"
}
```

```
Show me all overdue high-priority tasks assigned to me.
```

```
Mark the follow-up task for TechCorp as completed and add a note about the outcome.
```

## Tools

### mcp_copper_list_tasks
List tasks with filtering and pagination.

**Input:**
```python
{
    "page_size": int,  # optional, default=20, max=100
    "page_number": int,  # optional, default=1
    "sort_by": str,  # optional, one of ["name", "created_at", "updated_at", "due_date"]
    "sort_direction": str,  # optional, one of ["asc", "desc"]
    "assignee_id": int,  # optional
    "status": str,  # optional, one of ["Open", "Completed"]
    "due_date_start": str,  # optional, ISO format
    "due_date_end": str  # optional, ISO format
}
```

**Output:**
```python
{
    "tasks": [
        {
            "id": int,
            "name": str,
            "status": str,
            "due_date": str,  # ISO format
            # ... other Task fields
        }
    ],
    "total_count": int,
    "page_count": int
}
```

### mcp_copper_get_task
Retrieve a specific task by ID.

**Input:**
```python
{
    "task_id": int  # required
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    "assignee_id": int,
    "due_date": str,  # ISO format
    "reminder_date": str,  # ISO format
    "completed_date": str,  # ISO format
    "status": str,
    # ... full Task object
}
```

### mcp_copper_create_task
Create a new task.

**Input:**
```python
{
    "name": str,  # required
    "assignee_id": int,  # optional
    "due_date": str,  # optional, ISO format
    "reminder_date": str,  # optional, ISO format
    "priority": str,  # optional, one of ["None", "Low", "Medium", "High"]
    "status": str,  # optional, one of ["Open", "Completed"]
    "details": str,  # optional
    "related_resource": {  # optional
        "type": str,  # one of ["opportunity", "person", "company", "lead"]
        "id": int
    },
    "custom_fields": [  # optional
        {
            "custom_field_definition_id": int,
            "value": any
        }
    ]
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    # ... full Task object
}
```

### mcp_copper_update_task
Update an existing task.

**Input:**
```python
{
    "task_id": int,  # required
    "data": {  # required, fields to update
        "name": str,
        "status": str,
        "due_date": str,
        # ... any Task fields
    }
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    # ... full updated Task object
}
```

### mcp_copper_delete_task
Delete a task.

**Input:**
```python
{
    "task_id": int  # required
}
```

**Output:**
```python
{
    "success": bool,
    "message": str
}
```

### mcp_copper_search_tasks
Search for tasks.

**Input:**
```python
{
    "query": str,  # required
    "page_size": int,  # optional, default=20, max=100
    "page_number": int,  # optional, default=1
    "status": str,  # optional, one of ["Open", "Completed"]
    "assignee_id": int  # optional
}
```

**Output:**
```python
{
    "tasks": [
        {
            "id": int,
            "name": str,
            # ... Task fields
        }
    ],
    "total_count": int,
    "page_count": int
}
```

## Data Models

### Task
```python
{
    "id": Optional[int],
    "name": str,  # required
    "assignee_id": Optional[int],
    "due_date": Optional[str],  # ISO format
    "reminder_date": Optional[str],  # ISO format
    "completed_date": Optional[str],  # ISO format
    "priority": Optional[str],  # one of ["None", "Low", "Medium", "High"]
    "status": Optional[str],  # one of ["Open", "Completed"], default="Open"
    "details": Optional[str],
    "tags": List[str],
    "related_resource": Optional[Dict[str, Union[str, int]]],  # {"type": str, "id": int}
    "custom_fields": List[Dict],
    "created_at": Optional[str],  # ISO format
    "updated_at": Optional[str]  # ISO format
}
```

### TaskCustomField
```python
{
    "custom_field_definition_id": int,  # alias="field_id"
    "value": Any
}
``` 