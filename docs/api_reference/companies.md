# Copper CRM Companies Tools

## Overview
Tools for managing companies in Copper CRM through the Model Context Protocol (MCP).

## Example Prompts

```
Create a new company profile for TechCorp:
{
    "name": "TechCorp",
    "email_domain": "techcorp.com",
    "details": "Enterprise software solutions provider",
    "websites": ["https://techcorp.com"],
    "industry": "Technology",
    "tags": ["Enterprise", "Software"]
}
```

```
Find all companies in the technology sector that we've interacted with in the last quarter.
```

```
Update TechCorp's information with their new headquarters address in San Francisco.
```

## Tools

### mcp_copper_list_companies
List companies with filtering and pagination.

**Input:**
```python
{
    "page_size": int,  # optional, default=20, max=100
    "page_number": int,  # optional, default=1
    "sort_by": str,  # optional, one of ["name", "created_at", "updated_at"]
    "sort_direction": str,  # optional, one of ["asc", "desc"]
    "assignee_id": int,  # optional
    "contact_type_id": int  # optional
}
```

**Output:**
```python
{
    "companies": [
        {
            "id": int,
            "name": str,
            "email_domain": str,
            "websites": List[str],
            # ... other Company fields
        }
    ],
    "total_count": int,
    "page_count": int
}
```

### mcp_copper_get_company
Retrieve a specific company by ID.

**Input:**
```python
{
    "company_id": int  # required
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    "email_domain": str,
    "websites": List[str],
    "phone_numbers": List[str],
    "addresses": List[Dict],
    # ... full Company object
}
```

### mcp_copper_create_company
Create a new company.

**Input:**
```python
{
    "name": str,  # required
    "assignee_id": int,  # optional
    "contact_type_id": int,  # optional
    "details": str,  # optional
    "email_domain": str,  # optional
    "phone_numbers": List[str],  # optional
    "websites": List[str],  # optional
    "addresses": [  # optional
        {
            "street": str,
            "city": str,
            "state": str,
            "postal_code": str,
            "country": str
        }
    ],
    "tags": List[str],  # optional
    "socials": Dict[str, str],  # optional
    "parent_company_id": int,  # optional
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
    # ... full Company object
}
```

### mcp_copper_update_company
Update an existing company.

**Input:**
```python
{
    "company_id": int,  # required
    "data": {  # required, fields to update
        "name": str,
        "email_domain": str,
        "websites": List[str],
        # ... any Company fields
    }
}
```

**Output:**
```python
{
    "id": int,
    "name": str,
    # ... full updated Company object
}
```

### mcp_copper_delete_company
Delete a company.

**Input:**
```python
{
    "company_id": int  # required
}
```

**Output:**
```python
{
    "success": bool,
    "message": str
}
```

### mcp_copper_search_companies
Search for companies.

**Input:**
```python
{
    "query": str,  # required
    "page_size": int,  # optional, default=20, max=100
    "page_number": int,  # optional, default=1
    "contact_type_id": int  # optional
}
```

**Output:**
```python
{
    "companies": [
        {
            "id": int,
            "name": str,
            # ... Company fields
        }
    ],
    "total_count": int,
    "page_count": int
}
```

## Data Models

### Company
```python
{
    "id": Optional[int],
    "name": str,  # required
    "assignee_id": Optional[int],
    "contact_type_id": Optional[int],
    "details": Optional[str],
    "email_domain": Optional[str],
    "phone_numbers": List[str],
    "socials": Dict[str, str],
    "tags": List[str],
    "websites": List[str],
    "addresses": List[Dict],  # List of CompanyAddress objects
    "parent_company_id": Optional[int],
    "interaction_count": Optional[int],
    "last_interaction": Optional[str],  # ISO format
    "custom_fields": List[Dict],
    "created_at": Optional[str],  # ISO format
    "updated_at": Optional[str]  # ISO format
}
```

### CompanyAddress
```python
{
    "street": Optional[str],
    "city": Optional[str],
    "state": Optional[str],
    "postal_code": Optional[str],
    "country": Optional[str]
}
```

### CompanyCustomField
```python
{
    "custom_field_definition_id": int,  # alias="field_id"
    "value": Any
}
``` 