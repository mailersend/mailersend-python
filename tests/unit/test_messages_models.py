import pytest
from pydantic import ValidationError

from mailersend.models.messages import (
    MessagesListRequest,
    MessageGetRequest,
    Email,
    Message,
    MessagesListResponse,
    MessageResponse
)
from mailersend.models.domains import Domain, DomainSettings


class TestMessagesListRequest:
    """Test MessagesListRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid messages list request."""
        request = MessagesListRequest(page=1, limit=50)
        assert request.page == 1
        assert request.limit == 50
    
    def test_default_values(self):
        """Test default values."""
        request = MessagesListRequest()
        assert request.page is None
        assert request.limit == 25
    
    def test_limit_validation_min(self):
        """Test limit validation - minimum value."""
        with pytest.raises(ValidationError) as exc_info:
            MessagesListRequest(limit=5)
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_limit_validation_max(self):
        """Test limit validation - maximum value."""
        with pytest.raises(ValidationError) as exc_info:
            MessagesListRequest(limit=150)
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_page_validation(self):
        """Test page validation."""
        with pytest.raises(ValidationError) as exc_info:
            MessagesListRequest(page=0)
        assert "Page must be greater than 0" in str(exc_info.value)
    
    def test_valid_limits(self):
        """Test valid limit values."""
        request_min = MessagesListRequest(limit=10)
        assert request_min.limit == 10
        
        request_max = MessagesListRequest(limit=100)
        assert request_max.limit == 100


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
    
    def test_message_with_domain(self):
        """Test creating a message with domain data."""
        domain_settings = DomainSettings(
            send_paused=False,
            track_clicks=True,
            track_opens=True,
            track_unsubscribe=True
        )
        
        domain = Domain(
            id="zo8zdo",
            name="example.net",
            is_verified=True,
            is_dns_active=True,
            domain_settings=domain_settings,
            created_at="2020-06-10 10:10:11",
            updated_at="2020-06-10 10:10:11"
        )
        
        message = Message(
            id="5ee0b183b251345e407c936a",
            created_at="2020-06-10T10:10:11.231000Z",
            updated_at="2020-06-10T10:10:11.231000Z",
            emails=[],
            domain=domain
        )
        
        assert message.domain.id == "zo8zdo"
        assert message.domain.name == "example.net"
        assert message.domain.is_verified is True
    
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