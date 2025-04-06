# Copper CRM People Tools

## Overview
Tools for managing people (contacts) in Copper CRM through the Model Context Protocol (MCP).

## Example Prompts

```
Create a new contact for John Smith from TechCorp:
{
    "name": "John Smith",
    "first_name": "John",
    "last_name": "Smith",
    "title": "CTO",
    "company_name": "TechCorp",
    "emails": ["john.smith@techcorp.com"],
    "phone_numbers": ["+1-555-123-4567"]
}
```

```
Find all contacts from TechCorp who have interacted with us in the last month.
```

```
Update John Smith's contact information with his new role as CEO.
```

## Tools

### mcp_copper_list_people
List people with filtering and pagination.

**Input:**
```python
{
    "page_size": int,  # optional, default=20, max=100
    "page_number": int,  # optional, default=1
    "sort_by": str,  # optional, one of ["name", "created_at", "updated_at"]
    "sort_direction": str,  # optional, one of ["asc", "desc"]
    "company_id": int,  # optional
    "assignee_id": int,  # optional
    "contact_type_id": int  # optional
}
```

**Output:**
```python
{
    "people": [
        {
            "id": int,
            "name": str,
            "emails": List[str],
            "company_name": str,
            # ... other Person fields
        }
    ],
    "total_count": int,
    "page_count": int
}
```

### mcp_copper_get_person
Retrieve a specific person by ID.

**Input:**
```python
{
    "person_id": int  # required
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    "first_name": str,
    "last_name": str,
    "emails": List[str],
    "phone_numbers": List[str],
    # ... full Person object
}
```

### mcp_copper_create_person
Create a new person.

**Input:**
```python
{
    "name": str,  # required
    "first_name": str,  # optional
    "last_name": str,  # optional
    "prefix": str,  # optional
    "suffix": str,  # optional
    "emails": List[str],  # optional
    "phone_numbers": List[str],  # optional
    "company_id": int,  # optional
    "company_name": str,  # optional
    "title": str,  # optional
    "status": str,  # optional, one of ["Active", "Inactive", "Lead", "Customer"]
    "details": str,  # optional
    "addresses": [  # optional
        {
            "street": str,
            "city": str,
            "state": str,
            "postal_code": str,
            "country": str
        }
    ],
    "social_links": Dict[str, str],  # optional
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
    # ... full Person object
}
```

### mcp_copper_update_person
Update an existing person.

**Input:**
```python
{
    "person_id": int,  # required
    "data": {  # required, fields to update
        "name": str,
        "emails": List[str],
        "title": str,
        # ... any Person fields
    }
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    # ... full updated Person object
}
```

### mcp_copper_delete_person
Delete a person.

**Input:**
```python
{
    "person_id": int  # required
}
```

**Output:**
```python
{
    "success": bool,
    "message": str
}
```

### mcp_copper_search_people
Search for people.

**Input:**
```python
{
    "query": str,  # required
    "page_size": int,  # optional, default=20, max=100
    "page_number": int,  # optional, default=1
    "company_id": int,  # optional
    "status": str  # optional, one of ["Active", "Inactive", "Lead", "Customer"]
}
```

**Output:**
```python
{
    "people": [
        {
            "id": int,
            "name": str,
            # ... Person fields
        }
    ],
    "total_count": int,
    "page_count": int
}
```

## Data Models

### Person
```python
{
    "id": Optional[int],
    "name": str,  # required
    "prefix": Optional[str],
    "first_name": Optional[str],
    "last_name": Optional[str],
    "suffix": Optional[str],
    "emails": List[str],
    "phone_numbers": List[str],
    "addresses": List[Dict],  # List of PersonAddress objects
    "title": Optional[str],
    "company_id": Optional[int],
    "company_name": Optional[str],
    "tags": List[str],
    "social_links": Dict[str, str],
    "details": Optional[str],
    "assignee_id": Optional[int],
    "status": Optional[str],  # one of ["Active", "Inactive", "Lead", "Customer"]
    "contact_type_id": Optional[int],
    "interaction_count": Optional[int],
    "last_interaction": Optional[str],  # ISO format
    "custom_fields": List[Dict],
    "created_at": Optional[str],  # ISO format
    "updated_at": Optional[str]  # ISO format
}
```

### PersonAddress
```python
{
    "street": Optional[str],
    "city": Optional[str],
    "state": Optional[str],
    "postal_code": Optional[str],
    "country": Optional[str]
}
```

### PersonCustomField
```python
{
    "custom_field_definition_id": int,  # alias="field_id"
    "value": Any
}
``` 