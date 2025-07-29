import pytest
from pydantic import ValidationError

from mailersend.models.schedules import (
    SchedulesListRequest,
    SchedulesListQueryParams,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
    ScheduleDomain,
    ScheduleMessage,
    ScheduledMessage,
)


class TestSchedulesListQueryParams:
    """Test SchedulesListQueryParams model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        query_params = SchedulesListQueryParams()
        assert query_params.domain_id is None
        assert query_params.status is None
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test setting custom values."""
        query_params = SchedulesListQueryParams(
            domain_id="test-domain",
            status="scheduled",
            page=2,
            limit=50
        )
        assert query_params.domain_id == "test-domain"
        assert query_params.status == "scheduled"
        assert query_params.page == 2
        assert query_params.limit == 50

    def test_page_validation(self):
        """Test page validation (must be >= 1)."""
        with pytest.raises(ValidationError):
            SchedulesListQueryParams(page=0)
        
        with pytest.raises(ValidationError):
            SchedulesListQueryParams(page=-1)

    def test_limit_validation(self):
        """Test limit validation (10-100)."""
        with pytest.raises(ValidationError):
            SchedulesListQueryParams(limit=9)
        
        with pytest.raises(ValidationError):
            SchedulesListQueryParams(limit=101)

    def test_domain_id_validation_empty(self):
        """Test domain ID validation with empty string."""
        with pytest.raises(ValidationError) as exc_info:
            SchedulesListQueryParams(domain_id="")
        assert "Domain ID cannot be empty" in str(exc_info.value)

    def test_domain_id_validation_whitespace(self):
        """Test domain ID validation with whitespace."""
        with pytest.raises(ValidationError) as exc_info:
            SchedulesListQueryParams(domain_id="   ")
        assert "Domain ID cannot be empty" in str(exc_info.value)

    def test_domain_id_trimming(self):
        """Test domain ID is trimmed."""
        query_params = SchedulesListQueryParams(domain_id="  test-domain  ")
        assert query_params.domain_id == "test-domain"

    def test_status_values(self):
        """Test valid status values."""
        for status in ["scheduled", "sent", "error"]:
            query_params = SchedulesListQueryParams(status=status)
            assert query_params.status == status

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = SchedulesListQueryParams()
        result = query_params.to_query_params()
        expected = {
            'page': 1,
            'limit': 25
        }
        assert result == expected

    def test_to_query_params_with_custom_values(self):
        """Test to_query_params with custom values."""
        query_params = SchedulesListQueryParams(
            domain_id="test-domain",
            status="scheduled",
            page=3,
            limit=50
        )
        result = query_params.to_query_params()
        expected = {
            'domain_id': 'test-domain',
            'status': 'scheduled',
            'page': 3,
            'limit': 50
        }
        assert result == expected

    def test_to_query_params_excludes_none(self):
        """Test to_query_params excludes None values."""
        query_params = SchedulesListQueryParams(page=2, limit=30)
        result = query_params.to_query_params()
        expected = {
            'page': 2,
            'limit': 30
        }
        assert result == expected
        # domain_id and status should be excluded as they are None


class TestSchedulesListRequest:
    """Test SchedulesListRequest model."""
    
    def test_create_request_with_query_params(self):
        """Test creating request with query params object."""
        query_params = SchedulesListQueryParams(
            domain_id="test-domain",
            status="scheduled",
            page=2,
            limit=50
        )
        request = SchedulesListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_create_request_with_defaults(self):
        """Test creating request with default query params."""
        query_params = SchedulesListQueryParams()
        request = SchedulesListRequest(query_params=query_params)
        assert request.query_params.domain_id is None
        assert request.query_params.status is None
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params object."""
        query_params = SchedulesListQueryParams(
            domain_id="test-domain",
            status="sent",
            page=3,
            limit=75
        )
        request = SchedulesListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {
            'domain_id': 'test-domain',
            'status': 'sent',
            'page': 3,
            'limit': 75
        }
        assert result == expected

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = SchedulesListQueryParams()
        request = SchedulesListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {
            'page': 1,
            'limit': 25
        }
        assert result == expected


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
