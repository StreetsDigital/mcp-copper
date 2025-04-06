# MCP Copper CRM

Python client library for the Copper CRM API, designed for use with MCP (Mission Control Protocol).

## Features

- Full support for Copper CRM API v1
- Async/await support
- Type hints and data validation using Pydantic
- Comprehensive test coverage
- Detailed documentation and examples

### Core Features

- CRUD operations for:
  - Opportunities
  - People
  - Companies
  - Tasks
- Search and filtering
- Custom field support
- Rate limiting and error handling

### Advanced Features

- **Batch Operations**
  - Create multiple records in a single request
  - Update multiple records in a single request
  - Delete multiple records in a single request
  - Error handling and continuation options

- **Related Record Operations**
  - Get related records across entities
  - Activity history tracking
  - Filtered activity queries
  - Pagination support

## Installation

```bash
pip install mcp-copper
```

## Quick Start

```python
from mcp_copper import CopperClient

async with CopperClient(api_key="your_key", email="your_email") as client:
    # Create a new opportunity
    opportunity = await client.opportunities.create({
        "name": "New Deal",
        "status": "Open"
    })

    # Batch create multiple contacts
    result = await client.batch.create(
        "people",
        [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"}
        ]
    )

    # Get related opportunities for a company
    related = await client.related.get_related_records(
        "companies",
        company_id=123,
        related_type="opportunities"
    )
```

## Documentation

### Basic Operations

Each entity type (Opportunities, People, Companies, Tasks) supports:

- `list()`: Get a list of records
- `get(id)`: Get a single record
- `create(data)`: Create a new record
- `update(id, data)`: Update an existing record
- `delete(id)`: Delete a record
- `search(query)`: Search for records

### Batch Operations

```python
# Create multiple records
result = await client.batch.create(
    "opportunities",
    records=[
        {"name": "Deal 1", "status": "Open"},
        {"name": "Deal 2", "status": "Open"}
    ],
    continue_on_error=True
)

# Update multiple records
result = await client.batch.update(
    "people",
    records=[
        {"id": 123, "data": {"name": "Updated Name"}},
        {"id": 456, "data": {"email": "new@example.com"}}
    ]
)

# Delete multiple records
result = await client.batch.delete(
    "companies",
    ids=[123, 456, 789]
)
```

### Related Records

```python
# Get opportunities related to a company
opportunities = await client.related.get_related_records(
    "companies",
    company_id=123,
    related_type="opportunities"
)

# Get activity history for a person
activities = await client.related.get_entity_activities(
    "people",
    person_id=456,
    activity_types=["email", "note"],
    date_from="2024-01-01T00:00:00Z"
)
```

### Error Handling

```python
try:
    result = await client.batch.create(
        "opportunities",
        records=[...],
        continue_on_error=True,
        return_errors=True
    )
    
    # Check for partial success
    print(f"Succeeded: {result['summary']['succeeded']}")
    print(f"Failed: {result['summary']['failed']}")
    
    # Handle individual errors
    for item in result["results"]:
        if not item["success"]:
            print(f"Error: {item['error']['message']}")
            
except Exception as e:
    print(f"Operation failed: {str(e)}")
```

## Rate Limiting

The client automatically handles rate limiting and includes rate limit information in responses:

```python
limits = await client.get_rate_limits()
print(f"Remaining requests this hour: {limits['remaining']['requests_this_hour']}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details
