# MCP-Copper Project Planning

## Project Overview
Modern Copper CRM integration package for Python, providing a clean and efficient way to interact with the Copper CRM API.

## Architecture

### Directory Structure
```
mcp-copper/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── client.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── people.py
│   │   ├── companies.py
│   │   ├── opportunities.py
│   │   └── tasks.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── people.py
│   │   ├── companies.py
│   │   ├── opportunities.py
│   │   └── tasks.py
│   └── utils/
│       ├── __init__.py
│       ├── auth.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_client.py
│   └── api/
│       ├── test_people.py
│       ├── test_companies.py
│       ├── test_opportunities.py
│       └── test_tasks.py
├── docs/
│   ├── api.md
│   └── examples.md
├── README.md
├── PLANNING.md
├── TASK.md
└── requirements.txt
```

### Core Components

1. **Client (`client.py`)**
   - Main client class for interacting with Copper API
   - Handles authentication and session management
   - Provides access to all API endpoints

2. **Models (`models/`)**
   - Pydantic models for data validation
   - Represents Copper CRM entities (People, Companies, Opportunities, Tasks)
   - Handles data serialization/deserialization

3. **API Modules (`api/`)**
   - Individual modules for each Copper API endpoint
   - Implements CRUD operations
   - Handles pagination and filtering

4. **Utils (`utils/`)**
   - Authentication helpers
   - Common utility functions
   - Error handling

## Style Guide

### Python Standards
- Python 3.8+
- PEP 8 compliant
- Type hints required
- Black for formatting
- Docstrings in Google style

### Naming Conventions
- Classes: PascalCase
- Functions/Variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Private methods/variables: _leading_underscore

### Testing
- pytest for unit tests
- Coverage requirement: 80%+
- Mock external API calls
- Test both success and error cases

## API Design

### Authentication
- API Token based authentication
- Environment variables for credentials
- Secure token storage

### Rate Limiting
- Implement rate limiting as per Copper API guidelines
- Retry mechanism for failed requests
- Exponential backoff

### Error Handling
- Custom exception classes
- Detailed error messages
- Proper HTTP status codes

## Future Enhancements
1. Async support
2. Webhook handling
3. Bulk operations
4. Caching layer
5. CLI tool

## Dependencies
- fastapi
- pydantic
- httpx
- python-dotenv
- pytest (dev)
- black (dev)
- mypy (dev)
