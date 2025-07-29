import pytest
from pydantic import ValidationError

from mailersend.models.schedules import (
    SchedulesListRequest,
    SchedulesListQueryParams,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
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

    def test_domain_id_validation(self):
        """Test domain_id validation."""
        # Empty domain_id should raise error
        with pytest.raises(ValidationError, match="Domain ID cannot be empty"):
            SchedulesListQueryParams(domain_id="")

        with pytest.raises(ValidationError, match="Domain ID cannot be empty"):
            SchedulesListQueryParams(domain_id="   ")

    def test_domain_id_trimming(self):
        """Test domain_id is trimmed."""
        query_params = SchedulesListQueryParams(domain_id="  test-domain  ")
        assert query_params.domain_id == "test-domain"

    def test_status_validation(self):
        """Test status validation."""
        # Valid statuses
        for status in ["scheduled", "sent", "error"]:
            query_params = SchedulesListQueryParams(status=status)
            assert query_params.status == status

        # Invalid status should raise error
        with pytest.raises(ValidationError):
            SchedulesListQueryParams(status="invalid")

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

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = SchedulesListQueryParams()
        result = query_params.to_query_params()
        expected = {'page': 1, 'limit': 25}
        assert result == expected

    def test_to_query_params_with_all_values(self):
        """Test to_query_params with all values set."""
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
        expected = {'page': 2, 'limit': 30}
        assert result == expected
        # Verify no None values are included
        assert 'domain_id' not in result
        assert 'status' not in result


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
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.query_params.domain_id is None
        assert request.query_params.status is None

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
        expected = {'page': 1, 'limit': 25}
        assert result == expected


class TestScheduleGetRequest:
    """Test ScheduleGetRequest model."""

    def test_valid_message_id(self):
        """Test with valid message ID."""
        request = ScheduleGetRequest(message_id="message123")
        assert request.message_id == "message123"

    def test_message_id_validation(self):
        """Test message ID validation."""
        # Empty message ID
        with pytest.raises(ValidationError, match="Message ID is required"):
            ScheduleGetRequest(message_id="")

        # Whitespace-only message ID
        with pytest.raises(ValidationError, match="Message ID is required"):
            ScheduleGetRequest(message_id="   ")

    def test_message_id_trimming(self):
        """Test message ID is trimmed."""
        request = ScheduleGetRequest(message_id="  message123  ")
        assert request.message_id == "message123"


class TestScheduleDeleteRequest:
    """Test ScheduleDeleteRequest model."""

    def test_valid_message_id(self):
        """Test with valid message ID."""
        request = ScheduleDeleteRequest(message_id="message123")
        assert request.message_id == "message123"

    def test_message_id_validation(self):
        """Test message ID validation."""
        # Empty message ID
        with pytest.raises(ValidationError, match="Message ID is required"):
            ScheduleDeleteRequest(message_id="")

        # Whitespace-only message ID
        with pytest.raises(ValidationError, match="Message ID is required"):
            ScheduleDeleteRequest(message_id="   ")

    def test_message_id_trimming(self):
        """Test message ID is trimmed."""
        request = ScheduleDeleteRequest(message_id="  message123  ")
        assert request.message_id == "message123"
