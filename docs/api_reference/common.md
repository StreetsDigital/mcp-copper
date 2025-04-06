# Copper CRM Common Patterns

## Overview
Common patterns, error handling, and shared functionality across all Copper CRM MCP tools.

## Error Responses
All tools may return these standard error responses:

```python
{
    "error": {
        "code": str,  # Error code
        "message": str,  # Human-readable error message
        "details": Optional[Dict],  # Additional error context
        "request_id": str  # Unique identifier for the request
    }
}
```

### Common Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `unauthorized` | Invalid or missing API credentials | 401 |
| `forbidden` | Insufficient permissions | 403 |
| `not_found` | Requested resource doesn't exist | 404 |
| `invalid_input` | Invalid request parameters | 400 |
| `rate_limited` | Too many requests | 429 |
| `server_error` | Internal server error | 500 |
| `service_unavailable` | Service temporarily unavailable | 503 |

### Error Examples

```python
# Resource not found
{
    "error": {
        "code": "not_found",
        "message": "Opportunity with ID 12345 not found",
        "details": {
            "resource_type": "opportunity",
            "resource_id": 12345
        },
        "request_id": "req_abc123"
    }
}

# Invalid input
{
    "error": {
        "code": "invalid_input",
        "message": "Invalid opportunity status",
        "details": {
            "field": "status",
            "value": "pending",
            "allowed_values": ["Open", "Won", "Lost", "Abandoned"]
        },
        "request_id": "req_def456"
    }
}

# Rate limited
{
    "error": {
        "code": "rate_limited",
        "message": "Rate limit exceeded",
        "details": {
            "retry_after": 60,
            "limit": 100,
            "remaining": 0,
            "reset_at": "2024-03-15T10:00:00Z"
        },
        "request_id": "req_ghi789"
    }
}
```

## Pagination
All list operations support standard pagination parameters:

```python
{
    "page_size": int,  # Number of records per page (default: 20, max: 100)
    "page_number": int,  # Page number (1-based)
    "sort_by": str,  # Field to sort by
    "sort_direction": str  # "asc" or "desc"
}
```

### Pagination Response Format

```python
{
    "data": List[Dict],  # Array of records
    "metadata": {
        "total_count": int,  # Total number of records
        "page_count": int,  # Total number of pages
        "current_page": int,  # Current page number
        "per_page": int,  # Records per page
        "has_more": bool  # Whether there are more pages
    }
}
```

## Rate Limiting
Rate limits are included in all response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1678892400
```

### Rate Limit Tool

```python
mcp_copper_get_rate_limits

Input: None

Output:
{
    "limits": {
        "requests_per_second": int,
        "requests_per_hour": int,
        "remaining": {
            "requests_this_second": int,
            "requests_this_hour": int
        },
        "reset_at": str  # ISO format timestamp
    }
}
```

## Batch Operations

### mcp_copper_batch_create
Create multiple records of the same type in a single request.

**Input:**
```python
{
    "entity_type": str,  # "opportunities", "people", "companies", or "tasks"
    "records": List[Dict],  # Array of records to create
    "options": {  # optional
        "continue_on_error": bool,  # Whether to continue if some records fail
        "return_errors": bool  # Whether to return error details for failed records
    }
}
```

**Output:**
```python
{
    "results": [
        {
            "success": bool,
            "id": Optional[int],
            "error": Optional[Dict]  # Error details if success is false
        }
    ],
    "summary": {
        "total": int,
        "succeeded": int,
        "failed": int
    }
}
```

### mcp_copper_batch_update
Update multiple records of the same type in a single request.

**Input:**
```python
{
    "entity_type": str,  # "opportunities", "people", "companies", or "tasks"
    "records": [
        {
            "id": int,
            "data": Dict  # Fields to update
        }
    ],
    "options": {  # optional
        "continue_on_error": bool,
        "return_errors": bool
    }
}
```

**Output:**
```python
{
    "results": [
        {
            "success": bool,
            "id": int,
            "error": Optional[Dict]
        }
    ],
    "summary": {
        "total": int,
        "succeeded": int,
        "failed": int
    }
}
```

### mcp_copper_batch_delete
Delete multiple records of the same type in a single request.

**Input:**
```python
{
    "entity_type": str,  # "opportunities", "people", "companies", or "tasks"
    "ids": List[int],  # Array of record IDs to delete
    "options": {  # optional
        "continue_on_error": bool,
        "return_errors": bool
    }
}
```

**Output:**
```python
{
    "results": [
        {
            "success": bool,
            "id": int,
            "error": Optional[Dict]
        }
    ],
    "summary": {
        "total": int,
        "succeeded": int,
        "failed": int
    }
}
```

## Related Resource Operations

### mcp_copper_get_related_records
Get records related to a specific entity.

**Input:**
```python
{
    "entity_type": str,  # "opportunities", "people", "companies", or "tasks"
    "entity_id": int,
    "related_type": str,  # Type of related records to fetch
    "page_size": int,  # optional
    "page_number": int  # optional
}
```

**Output:**
```python
{
    "data": List[Dict],  # Array of related records
    "metadata": {
        "total_count": int,
        "page_count": int,
        "current_page": int,
        "per_page": int,
        "has_more": bool
    }
}
```

### Example Related Resource Queries

```python
# Get all opportunities for a company
{
    "entity_type": "companies",
    "entity_id": 12345,
    "related_type": "opportunities"
}

# Get all tasks for a person
{
    "entity_type": "people",
    "entity_id": 67890,
    "related_type": "tasks"
}

# Get all people from a company
{
    "entity_type": "companies",
    "entity_id": 12345,
    "related_type": "people"
}
```

## Activity Tracking

### mcp_copper_get_entity_activities
Get activity history for a specific entity.

**Input:**
```python
{
    "entity_type": str,  # "opportunities", "people", "companies", or "tasks"
    "entity_id": int,
    "activity_types": Optional[List[str]],  # Filter by activity types
    "date_from": Optional[str],  # ISO format
    "date_to": Optional[str],  # ISO format
    "page_size": int,  # optional
    "page_number": int  # optional
}
```

**Output:**
```python
{
    "activities": [
        {
            "id": int,
            "type": str,
            "action": str,
            "details": Dict,
            "user_id": int,
            "occurred_at": str  # ISO format
        }
    ],
    "metadata": {
        "total_count": int,
        "page_count": int,
        "current_page": int,
        "per_page": int,
        "has_more": bool
    }
}
``` 