import pytest
from pydantic import ValidationError

from mailersend.models.messages import (
    MessagesListRequest,
    MessagesListQueryParams,
    MessageGetRequest,
    Email,
    Message,
    MessagesListResponse,
    MessageResponse
)



class TestMessagesListQueryParams:
    """Test MessagesListQueryParams model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        query_params = MessagesListQueryParams()
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test setting custom values."""
        query_params = MessagesListQueryParams(page=2, limit=50)
        assert query_params.page == 2
        assert query_params.limit == 50

    def test_page_validation(self):
        """Test page validation (must be >= 1)."""
        with pytest.raises(ValidationError):
            MessagesListQueryParams(page=0)
        
        with pytest.raises(ValidationError):
            MessagesListQueryParams(page=-1)

    def test_limit_validation(self):
        """Test limit validation (10-100)."""
        with pytest.raises(ValidationError):
            MessagesListQueryParams(limit=9)
        
        with pytest.raises(ValidationError):
            MessagesListQueryParams(limit=101)

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = MessagesListQueryParams()
        result = query_params.to_query_params()
        expected = {
            'page': 1,
            'limit': 25
        }
        assert result == expected

    def test_to_query_params_with_custom_values(self):
        """Test to_query_params with custom values."""
        query_params = MessagesListQueryParams(page=3, limit=50)
        result = query_params.to_query_params()
        expected = {
            'page': 3,
            'limit': 50
        }
        assert result == expected

    def test_to_query_params_excludes_none(self):
        """Test to_query_params excludes None values."""
        query_params = MessagesListQueryParams(page=2, limit=30)
        result = query_params.to_query_params()
        expected = {
            'page': 2,
            'limit': 30
        }
        assert result == expected
        # No None values in this case but testing the method works correctly


class TestMessagesListRequest:
    """Test MessagesListRequest model."""
    
    def test_create_request_with_query_params(self):
        """Test creating request with query params object."""
        query_params = MessagesListQueryParams(page=2, limit=50)
        request = MessagesListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_create_request_with_defaults(self):
        """Test creating request with default query params."""
        query_params = MessagesListQueryParams()
        request = MessagesListRequest(query_params=query_params)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params object."""
        query_params = MessagesListQueryParams(page=3, limit=75)
        request = MessagesListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {
            'page': 3,
            'limit': 75
        }
        assert result == expected

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = MessagesListQueryParams()
        request = MessagesListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {
            'page': 1,
            'limit': 25
        }
        assert result == expected


class TestMessageGetRequest:
    """Test MessageGetRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid message get request."""
        request = MessageGetRequest(message_id="5ee0b183b251345e407c936a")
        assert request.message_id == "5ee0b183b251345e407c936a"
    
    def test_empty_message_id(self):
        """Test validation with empty message ID."""
        with pytest.raises(ValidationError) as exc_info:
            MessageGetRequest(message_id="")
        assert "Message ID is required" in str(exc_info.value)
    
    def test_whitespace_message_id(self):
        """Test validation with whitespace-only message ID."""
        with pytest.raises(ValidationError) as exc_info:
            MessageGetRequest(message_id="   ")
        assert "Message ID is required" in str(exc_info.value)
    
    def test_message_id_trimming(self):
        """Test message ID is trimmed."""
        request = MessageGetRequest(message_id="  5ee0b183b251345e407c936a  ")
        assert request.message_id == "5ee0b183b251345e407c936a"


class TestEmail:
    """Test Email model."""
    
    def test_empty_email_creation(self):
        """Test creating an empty email object."""
        email = Email()
        assert isinstance(email, Email)


class TestMessage:
    """Test Message model."""
    
    def test_minimal_message_creation(self):
        """Test creating a message with minimal data."""
        message = Message(
            id="5ee0b183b251345e407c936a",
            created_at="2020-06-10T10:10:11.231000Z",
            updated_at="2020-06-10T10:10:11.231000Z"
        )
        assert message.id == "5ee0b183b251345e407c936a"
        assert message.created_at == "2020-06-10T10:10:11.231000Z"
        assert message.updated_at == "2020-06-10T10:10:11.231000Z"
        assert message.emails == []
        assert message.domain is None
    

    
    def test_message_with_emails(self):
        """Test creating a message with emails."""
        emails = [Email(), Email()]
        
        message = Message(
            id="5ee0b183b251345e407c936a",
            created_at="2020-06-10T10:10:11.231000Z",
            updated_at="2020-06-10T10:10:11.231000Z",
            emails=emails
        )
        
        assert len(message.emails) == 2
        assert all(isinstance(email, Email) for email in message.emails)


class TestMessagesListResponse:
    """Test MessagesListResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid messages list response."""
        messages = [
            Message(
                id="5ee0b182b251345e407c935a",
                created_at="2020-06-10T10:10:10.377000Z",
                updated_at="2020-06-10T10:10:10.377000Z"
            ),
            Message(
                id="5ee0b182b251345e407c935c",
                created_at="2020-06-10T10:10:10.385000Z",
                updated_at="2020-06-10T10:10:10.385000Z"
            )
        ]
        
        response = MessagesListResponse(
            data=messages,
            links={"first": "https://api.mailersend.com/v1/messages?page=1"},
            meta={"current_page": 1, "total": 2}
        )
        
        assert len(response.data) == 2
        assert response.data[0].id == "5ee0b182b251345e407c935a"
        assert response.data[1].id == "5ee0b182b251345e407c935c"
        assert response.links["first"] == "https://api.mailersend.com/v1/messages?page=1"
        assert response.meta["total"] == 2


class TestMessageResponse:
    """Test MessageResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid message response."""
        message = Message(
            id="5ee0b183b251345e407c936a",
            created_at="2020-06-10T10:10:11.231000Z",
            updated_at="2020-06-10T10:10:11.231000Z"
        )
        
        response = MessageResponse(data=message)
        
        assert response.data.id == "5ee0b183b251345e407c936a"
        assert response.data.created_at == "2020-06-10T10:10:11.231000Z" 