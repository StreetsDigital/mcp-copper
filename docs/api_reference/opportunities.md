# Copper CRM Opportunities Tools

## Overview
Tools for managing opportunities in Copper CRM through the Model Context Protocol (MCP).

## Example Prompts

```
Create a new opportunity for the company TechCorp with a value of $50,000:
{
    "name": "TechCorp Q2 Deal",
    "company_name": "TechCorp",
    "monetary_value": 50000,
    "status": "Open",
    "priority": "High"
}
```

```
Show me all high-priority opportunities in the sales pipeline that are closing this quarter.
```

## Tools

### mcp_copper_list_opportunities
List opportunities with filtering and pagination.

**Input:**
```python
{
    "page_size": int,  # optional, default=20, max=100
    "page_number": int,  # optional, default=1
    "sort_by": str,  # optional, one of ["name", "created_at", "updated_at", "close_date", "monetary_value"]
    "sort_direction": str,  # optional, one of ["asc", "desc"]
    "pipeline_id": int,  # optional
    "pipeline_stage_id": int  # optional
}
```

**Output:**
```python
{
    "opportunities": [
        {
            "id": int,
            "name": str,
            "monetary_value": float,
            "status": str,
            # ... other Opportunity fields
        }
    ],
    "total_count": int,
    "page_count": int
}
```

### mcp_copper_get_opportunity
Retrieve a specific opportunity by ID.

**Input:**
```python
{
    "opportunity_id": int  # required
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    "assignee_id": int,
    "close_date": str,  # ISO format
    "company_id": int,
    "company_name": str,
    "monetary_value": float,
    "status": str,
    # ... full Opportunity object
}
```

### mcp_copper_create_opportunity
Create a new opportunity.

**Input:**
```python
{
    "name": str,  # required
    "company_id": int,  # optional
    "company_name": str,  # optional
    "monetary_value": float,  # optional
    "pipeline_id": int,  # optional
    "pipeline_stage_id": int,  # optional
    "priority": str,  # optional, one of ["None", "Low", "Medium", "High"]
    "status": str,  # optional, one of ["Open", "Won", "Lost", "Abandoned"]
    "close_date": str,  # optional, ISO format
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
    # ... full Opportunity object
}
```

### mcp_copper_update_opportunity
Update an existing opportunity.

**Input:**
```python
{
    "opportunity_id": int,  # required
    "data": {  # required, fields to update
        "name": str,
        "monetary_value": float,
        "status": str,
        # ... any Opportunity fields
    }
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    # ... full updated Opportunity object
}
```

### mcp_copper_delete_opportunity
Delete an opportunity.

**Input:**
```python
{
    "opportunity_id": int  # required
}
```

**Output:**
```python
{
    "success": bool,
    "message": str
}
```

### mcp_copper_search_opportunities
Search for opportunities.

**Input:**
```python
{
    "query": str,  # required
    "page_size": int,  # optional, default=20, max=100
    "page_number": int  # optional, default=1
}
```

**Output:**
```python
{
    "opportunities": [
        {
            "id": int,
            "name": str,
            # ... Opportunity fields
        }
    ],
    "total_count": int,
    "page_count": int
}
```

## Data Models

### Opportunity
```python
{
    "id": Optional[int],
    "name": str,  # required
    "assignee_id": Optional[int],
    "close_date": Optional[str],  # ISO format
    "company_id": Optional[int],
    "company_name": Optional[str],
    "customer_source_id": Optional[int],
    "details": Optional[str],
    "loss_reason_id": Optional[int],
    "monetary_value": Optional[float],
    "pipeline_id": Optional[int],
    "pipeline_stage_id": Optional[int],
    "priority": Optional[str],  # one of ["None", "Low", "Medium", "High"]
    "probability": Optional[int],  # 0-100
    "status": Optional[str],  # one of ["Open", "Won", "Lost", "Abandoned"]
    "tags": List[str],
    "win_probability": Optional[int],  # 0-100
    "custom_fields": List[Dict],
    "created_at": Optional[str],  # ISO format
    "updated_at": Optional[str]  # ISO format
}
```

### OpportunityCustomField Model

```python
class OpportunityCustomField:
    custom_field_definition_id: int  # alias="field_id"
    value: Any
``` 