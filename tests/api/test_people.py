"""
Tests for the People API module.
"""
import pytest
from datetime import datetime

from mcp_copper import CopperClient, Person
from mcp_copper.models.people import PersonAddress

@pytest.fixture
def client():
    """Create a test client instance."""
    return CopperClient(
        api_key="test_key",
        user_email="test@example.com",
        base_url="https://api.copper.com"
    )

@pytest.fixture
def sample_person_data():
    """Create sample person data."""
    return {
        "id": 12345,
        "name": "John Doe",
        "first_name": "John",
        "last_name": "Doe",
        "emails": [{"email": "john@example.com"}],
        "phone_numbers": [{"number": "+1234567890"}],
        "addresses": [{
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "postal_code": "12345",
            "country": "USA"
        }],
        "title": "CEO",
        "company_name": "Example Corp",
        "tags": ["VIP", "Customer"],
        "date_created": int(datetime.now().timestamp()),
        "date_modified": int(datetime.now().timestamp())
    }

def test_person_model_creation(sample_person_data):
    """Test creating a Person model from API data."""
    person = Person.from_api(sample_person_data)
    
    assert person.id == 12345
    assert person.name == "John Doe"
    assert person.first_name == "John"
    assert person.last_name == "Doe"
    assert person.emails == ["john@example.com"]
    assert person.phone_numbers == ["+1234567890"]
    assert len(person.addresses) == 1
    assert isinstance(person.addresses[0], PersonAddress)
    assert person.addresses[0].street == "123 Main St"
    assert person.title == "CEO"
    assert person.company_name == "Example Corp"
    assert person.tags == ["VIP", "Customer"]
    assert person.created_at is not None
    assert person.updated_at is not None

def test_person_model_to_api(sample_person_data):
    """Test converting a Person model to API format."""
    person = Person.from_api(sample_person_data)
    api_data = person.to_api()
    
    assert api_data["name"] == "John Doe"
    assert api_data["emails"] == [{"email": "john@example.com"}]
    assert api_data["phone_numbers"] == [{"number": "+1234567890"}]
    assert "addresses" in api_data
    assert api_data["addresses"][0]["street"] == "123 Main St"

@pytest.mark.asyncio
async def test_list_people(client, sample_person_data, mocker):
    """Test listing people."""
    mock_response = [sample_person_data]
    mocker.patch.object(
        client,
        "get",
        return_value=[Person.from_api(sample_person_data)]
    )
    
    people = client.people.list()
    assert len(people) == 1
    assert isinstance(people[0], Person)
    assert people[0].name == "John Doe"

@pytest.mark.asyncio
async def test_get_person(client, sample_person_data, mocker):
    """Test getting a specific person."""
    mocker.patch.object(
        client,
        "get",
        return_value=Person.from_api(sample_person_data)
    )
    
    person = client.people.get(12345)
    assert isinstance(person, Person)
    assert person.id == 12345
    assert person.name == "John Doe"

@pytest.mark.asyncio
async def test_create_person(client, sample_person_data, mocker):
    """Test creating a new person."""
    mocker.patch.object(
        client,
        "post",
        return_value=Person.from_api(sample_person_data)
    )
    
    new_person = {
        "name": "John Doe",
        "emails": [{"email": "john@example.com"}]
    }
    
    person = client.people.create(new_person)
    assert isinstance(person, Person)
    assert person.name == "John Doe"
    assert person.emails == ["john@example.com"]

@pytest.mark.asyncio
async def test_update_person(client, sample_person_data, mocker):
    """Test updating an existing person."""
    mocker.patch.object(
        client,
        "put",
        return_value=Person.from_api(sample_person_data)
    )
    
    updated_data = {
        "name": "John Doe Jr.",
        "title": "CTO"
    }
    
    person = client.people.update(12345, updated_data)
    assert isinstance(person, Person)
    assert person.id == 12345

@pytest.mark.asyncio
async def test_delete_person(client, mocker):
    """Test deleting a person."""
    mock_delete = mocker.patch.object(client, "delete")
    
    client.people.delete(12345)
    mock_delete.assert_called_once_with("/people/12345")

@pytest.mark.asyncio
async def test_search_people(client, sample_person_data, mocker):
    """Test searching for people."""
    mock_response = [sample_person_data]
    mocker.patch.object(
        client,
        "search",
        return_value=[Person.from_api(sample_person_data)]
    )
    
    people = client.people.search(query="John")
    assert len(people) == 1
    assert isinstance(people[0], Person)
    assert people[0].name == "John Doe"
