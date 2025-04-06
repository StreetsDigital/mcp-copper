"""Test fixtures for MCP Copper."""
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    client = MagicMock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.put = AsyncMock()
    client.delete = AsyncMock()
    return client
