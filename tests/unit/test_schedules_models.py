import pytest
from pydantic import ValidationError

from mailersend.models.schedules import (
    SchedulesListRequest,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
    ScheduleDomain,
    ScheduleMessage,
    ScheduledMessage,
    SchedulesListResponse,
    ScheduleResponse
)


class TestSchedulesListRequest:
    """Test SchedulesListRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid schedules list request."""
        request = SchedulesListRequest(
            domain_id="test-domain",
            status="scheduled",
            page=1,
            limit=50
        )
        assert request.domain_id == "test-domain"
        assert request.status == "scheduled"
        assert request.page == 1
        assert request.limit == 50
    
    def test_default_values(self):
        """Test default values."""
        request = SchedulesListRequest()
        assert request.domain_id is None
        assert request.status is None
        assert request.page is None
        assert request.limit == 25
    
    def test_limit_validation_min(self):
        """Test limit validation - minimum value."""
        with pytest.raises(ValidationError) as exc_info:
            SchedulesListRequest(limit=5)
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_limit_validation_max(self):
        """Test limit validation - maximum value."""
        with pytest.raises(ValidationError) as exc_info:
            SchedulesListRequest(limit=150)
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_page_validation(self):
        """Test page validation."""
        with pytest.raises(ValidationError) as exc_info:
            SchedulesListRequest(page=0)
        assert "Page must be greater than 0" in str(exc_info.value)
    
    def test_domain_id_validation_empty(self):
        """Test domain ID validation with empty string."""
        with pytest.raises(ValidationError) as exc_info:
            SchedulesListRequest(domain_id="")
        assert "Domain ID cannot be empty" in str(exc_info.value)
    
    def test_domain_id_validation_whitespace(self):
        """Test domain ID validation with whitespace."""
        with pytest.raises(ValidationError) as exc_info:
            SchedulesListRequest(domain_id="   ")
        assert "Domain ID cannot be empty" in str(exc_info.value)
    
    def test_domain_id_trimming(self):
        """Test domain ID is trimmed."""
        request = SchedulesListRequest(domain_id="  test-domain  ")
        assert request.domain_id == "test-domain"
    
    def test_status_values(self):
        """Test valid status values."""
        for status in ["scheduled", "sent", "error"]:
            request = SchedulesListRequest(status=status)
            assert request.status == status
    
    def test_valid_limits(self):
        """Test valid limit values."""
        request_min = SchedulesListRequest(limit=10)
        assert request_min.limit == 10
        
        request_max = SchedulesListRequest(limit=100)
        assert request_max.limit == 100


class TestScheduleGetRequest:
    """Test ScheduleGetRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid schedule get request."""
        request = ScheduleGetRequest(message_id="61e01f471053b349a5478a52")
        assert request.message_id == "61e01f471053b349a5478a52"
    
    def test_empty_message_id(self):
        """Test validation with empty message ID."""
        with pytest.raises(ValidationError) as exc_info:
            ScheduleGetRequest(message_id="")
        assert "Message ID is required" in str(exc_info.value)
    
    def test_whitespace_message_id(self):
        """Test validation with whitespace-only message ID."""
        with pytest.raises(ValidationError) as exc_info:
            ScheduleGetRequest(message_id="   ")
        assert "Message ID is required" in str(exc_info.value)
    
    def test_message_id_trimming(self):
        """Test message ID is trimmed."""
        request = ScheduleGetRequest(message_id="  61e01f471053b349a5478a52  ")
        assert request.message_id == "61e01f471053b349a5478a52"


class TestScheduleDeleteRequest:
    """Test ScheduleDeleteRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid schedule delete request."""
        request = ScheduleDeleteRequest(message_id="61e01f471053b349a5478a52")
        assert request.message_id == "61e01f471053b349a5478a52"
    
    def test_empty_message_id(self):
        """Test validation with empty message ID."""
        with pytest.raises(ValidationError) as exc_info:
            ScheduleDeleteRequest(message_id="")
        assert "Message ID is required" in str(exc_info.value)
    
    def test_whitespace_message_id(self):
        """Test validation with whitespace-only message ID."""
        with pytest.raises(ValidationError) as exc_info:
            ScheduleDeleteRequest(message_id="   ")
        assert "Message ID is required" in str(exc_info.value)
    
    def test_message_id_trimming(self):
        """Test message ID is trimmed."""
        request = ScheduleDeleteRequest(message_id="  61e01f471053b349a5478a52  ")
        assert request.message_id == "61e01f471053b349a5478a52"


class TestScheduleDomain:
    """Test ScheduleDomain model."""
    
    def test_valid_domain(self):
        """Test creating a valid schedule domain."""
        domain = ScheduleDomain(
            id="7z3m5jgrogdpyo6n",
            name="mailersend.com",
            created_at="2022-01-01T12:00:00.000000Z",
            updated_at="2022-01-01T12:00:00.000000Z"
        )
        assert domain.id == "7z3m5jgrogdpyo6n"
        assert domain.name == "mailersend.com"
        assert domain.created_at == "2022-01-01T12:00:00.000000Z"
        assert domain.updated_at == "2022-01-01T12:00:00.000000Z"


class TestScheduleMessage:
    """Test ScheduleMessage model."""
    
    def test_valid_message(self):
        """Test creating a valid schedule message."""
        message = ScheduleMessage(
            id="61e01f471053b349a5478a52",
            created_at="2022-01-01T12:00:00.000000Z",
            updated_at="2022-01-01T12:00:00.000000Z"
        )
        assert message.id == "61e01f471053b349a5478a52"
        assert message.created_at == "2022-01-01T12:00:00.000000Z"
        assert message.updated_at == "2022-01-01T12:00:00.000000Z"


class TestScheduledMessage:
    """Test ScheduledMessage model."""
    
    def test_minimal_scheduled_message(self):
        """Test creating a scheduled message with minimal data."""
        scheduled_msg = ScheduledMessage(
            message_id="61e01c6a7f97913a17075262",
            subject="Hello from Company",
            send_at="2022-01-01T12:00:00.000000Z",
            status="scheduled",
            created_at="2022-01-17:00:00.000000Z"
        )
        assert scheduled_msg.message_id == "61e01c6a7f97913a17075262"
        assert scheduled_msg.subject == "Hello from Company"
        assert scheduled_msg.send_at == "2022-01-01T12:00:00.000000Z"
        assert scheduled_msg.status == "scheduled"
        assert scheduled_msg.status_message is None
        assert scheduled_msg.created_at == "2022-01-17:00:00.000000Z"
        assert scheduled_msg.domain is None
        assert scheduled_msg.message is None
    
    def test_scheduled_message_with_domain_and_message(self):
        """Test creating a scheduled message with domain and message data."""
        domain = ScheduleDomain(
            id="7z3m5jgrogdpyo6n",
            name="mailersend.com",
            created_at="2022-01-01T12:00:00.000000Z",
            updated_at="2022-01-01T12:00:00.000000Z"
        )
        
        message = ScheduleMessage(
            id="61e01f471053b349a5478a52",
            created_at="2022-01-01T12:00:00.000000Z",
            updated_at="2022-01-01T12:00:00.000000Z"
        )
        
        scheduled_msg = ScheduledMessage(
            message_id="61e01f471053b349a5478a52",
            subject="Hello from Company",
            send_at="2022-01-01T12:00:00.000000Z",
            status="scheduled",
            created_at="2022-01-01T17:00:00.000000Z",
            domain=domain,
            message=message
        )
        
        assert scheduled_msg.domain.id == "7z3m5jgrogdpyo6n"
        assert scheduled_msg.domain.name == "mailersend.com"
        assert scheduled_msg.message.id == "61e01f471053b349a5478a52"
    
    def test_status_values(self):
        """Test valid status values for scheduled message."""
        for status in ["scheduled", "sent", "error"]:
            scheduled_msg = ScheduledMessage(
                message_id="test-id",
                subject="Test Subject",
                send_at="2022-01-01T12:00:00.000000Z",
                status=status,
                created_at="2022-01-01T12:00:00.000000Z"
            )
            assert scheduled_msg.status == status


class TestSchedulesListResponse:
    """Test SchedulesListResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid schedules list response."""
        scheduled_messages = [
            ScheduledMessage(
                message_id="61e01c6a7f97913a17075262",
                subject="Hello from Company",
                send_at="2022-01-01T12:00:00.000000Z",
                status="scheduled",
                created_at="2022-01-17:00:00.000000Z"
            ),
            ScheduledMessage(
                message_id="61e01c6a7f97913a17075263",
                subject="Another Message",
                send_at="2022-01-02T12:00:00.000000Z",
                status="sent",
                created_at="2022-01-18:00:00.000000Z"
            )
        ]
        
        response = SchedulesListResponse(
            data=scheduled_messages,
            links={"first": "https://api.mailersend.com/v1/message-schedules?page=1"},
            meta={"current_page": 1, "total": 2}
        )
        
        assert len(response.data) == 2
        assert response.data[0].message_id == "61e01c6a7f97913a17075262"
        assert response.data[1].message_id == "61e01c6a7f97913a17075263"
        assert response.links["first"] == "https://api.mailersend.com/v1/message-schedules?page=1"
        assert response.meta["total"] == 2


class TestScheduleResponse:
    """Test ScheduleResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid schedule response."""
        scheduled_msg = ScheduledMessage(
            message_id="61e01f471053b349a5478a52",
            subject="Hello from Company",
            send_at="2022-01-01T12:00:00.000000Z",
            status="scheduled",
            created_at="2022-01-01T17:00:00.000000Z"
        )
        
        response = ScheduleResponse(data=scheduled_msg)
        
        assert response.data.message_id == "61e01f471053b349a5478a52"
        assert response.data.subject == "Hello from Company"
        assert response.data.status == "scheduled" 