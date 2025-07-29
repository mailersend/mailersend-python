import pytest
from pydantic import ValidationError
import time

from mailersend.models.activity import (
    ActivityRecipient,
    ActivityEmail,
    Activity,
    ActivityQueryParams,
    ActivityRequest,
    SingleActivityRequest,
)


class TestActivityRecipient:
    def test_valid_recipient(self):
        recipient = ActivityRecipient(
            id="recipient-123",
            email="user@example.com",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        assert recipient.id == "recipient-123"
        assert recipient.email == "user@example.com"
        assert recipient.created_at == "2023-01-01T00:00:00Z"
        assert recipient.updated_at == "2023-01-01T00:00:00Z"
        assert recipient.deleted_at is None

    def test_recipient_with_deleted_at(self):
        recipient = ActivityRecipient(
            id="recipient-123",
            email="user@example.com",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            deleted_at="2023-01-02T00:00:00Z",
        )

        assert recipient.deleted_at == "2023-01-02T00:00:00Z"

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            ActivityRecipient()

        errors = exc_info.value.errors()
        required_fields = {"id", "email", "created_at", "updated_at"}
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)

    def test_invalid_email(self):
        with pytest.raises(ValidationError) as exc_info:
            ActivityRecipient(
                id="recipient-123",
                email="invalid-email",
                created_at="2023-01-01T00:00:00Z",
                updated_at="2023-01-01T00:00:00Z",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("email",) for error in errors)


class TestActivityEmail:
    def test_valid_email(self):
        recipient = ActivityRecipient(
            id="recipient-123",
            email="user@example.com",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        email = ActivityEmail(
            id="email-456",
            **{"from": "sender@example.com"},
            subject="Test Subject",
            text="Test content",
            html="<p>Test content</p>",
            status="sent",
            tags=["newsletter", "marketing"],
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            recipient=recipient
        )

        assert email.id == "email-456"
        assert email.from_email == "sender@example.com"
        assert email.subject == "Test Subject"
        assert email.text == "Test content"
        assert email.html == "<p>Test content</p>"
        assert email.status == "sent"
        assert email.tags == ["newsletter", "marketing"]
        assert email.recipient == recipient

    def test_email_with_alias_from_field(self):
        """Test that 'from' field is properly aliased to 'from_email'."""
        recipient = ActivityRecipient(
            id="recipient-123",
            email="user@example.com",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        # Test with direct field access
        email_data = {
            "id": "email-456",
            "from": "sender@example.com",
            "subject": "Test Subject",
            "status": "sent",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "recipient": recipient,
        }

        email = ActivityEmail(**email_data)
        assert email.from_email == "sender@example.com"

    def test_optional_fields(self):
        recipient = ActivityRecipient(
            id="recipient-123",
            email="user@example.com",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        email = ActivityEmail(
            id="email-456",
            **{"from": "sender@example.com"},
            subject="Test Subject",
            status="sent",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            recipient=recipient
        )

        assert email.text is None
        assert email.html is None
        assert email.tags is None

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            ActivityEmail()

        errors = exc_info.value.errors()
        required_fields = {
            "id",
            "from",
            "subject",
            "status",
            "created_at",
            "updated_at",
            "recipient",
        }
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)


class TestActivity:
    def test_valid_activity(self):
        recipient = ActivityRecipient(
            id="recipient-123",
            email="user@example.com",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        email = ActivityEmail(
            id="email-456",
            **{"from": "sender@example.com"},
            subject="Test Subject",
            status="sent",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            recipient=recipient
        )

        activity = Activity(
            id="activity-789",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            type="sent",
            email=email,
        )

        assert activity.id == "activity-789"
        assert activity.type == "sent"
        assert activity.email == email

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            Activity()

        errors = exc_info.value.errors()
        required_fields = {"id", "created_at", "updated_at", "type", "email"}
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)


class TestActivityQueryParams:
    def test_valid_params(self):
        current_time = int(time.time())
        date_from = current_time - 3600  # 1 hour ago
        date_to = current_time

        params = ActivityQueryParams(
            date_from=date_from,
            date_to=date_to,
            page=1,
            limit=25,
            event=["sent", "delivered"],
        )

        assert params.date_from == date_from
        assert params.date_to == date_to
        assert params.page == 1
        assert params.limit == 25
        assert params.event == ["sent", "delivered"]

    def test_default_values(self):
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        params = ActivityQueryParams(date_from=date_from, date_to=date_to)

        assert params.page == 1
        assert params.limit == 25
        assert params.event is None

    def test_date_range_validation(self):
        current_time = int(time.time())

        # Test date_to <= date_from
        with pytest.raises(
            ValidationError, match="date_to must be greater than date_from"
        ):
            ActivityQueryParams(
                date_from=current_time,
                date_to=current_time - 3600,  # Earlier than date_from
            )

    def test_timeframe_validation(self):
        current_time = int(time.time())
        eight_days_ago = current_time - (8 * 24 * 3600)  # 8 days ago

        # Test timeframe > 7 days
        with pytest.raises(
            ValidationError,
            match="Timeframe between date_from and date_to cannot exceed 7 days",
        ):
            ActivityQueryParams(date_from=eight_days_ago, date_to=current_time)

    def test_page_validation(self):
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        # Test page < 1
        with pytest.raises(ValidationError):
            ActivityQueryParams(date_from=date_from, date_to=date_to, page=0)

    def test_limit_validation(self):
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        # Test limit < 10
        with pytest.raises(ValidationError):
            ActivityQueryParams(date_from=date_from, date_to=date_to, limit=5)

        # Test limit > 100
        with pytest.raises(ValidationError):
            ActivityQueryParams(date_from=date_from, date_to=date_to, limit=150)

    def test_event_validation(self):
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        # Test valid events
        params = ActivityQueryParams(
            date_from=date_from,
            date_to=date_to,
            event=["sent", "delivered", "opened", "clicked"],
        )
        assert params.event == ["sent", "delivered", "opened", "clicked"]

        # Test invalid events
        with pytest.raises(ValidationError, match="Invalid event types"):
            ActivityQueryParams(
                date_from=date_from,
                date_to=date_to,
                event=["sent", "invalid_event", "delivered"],
            )

    def test_to_query_params(self):
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        params = ActivityQueryParams(
            date_from=date_from,
            date_to=date_to,
            page=2,
            limit=50,
            event=["sent", "delivered"],
        )

        query_params = params.to_query_params()

        expected = {
            "page": 2,
            "limit": 50,
            "date_from": date_from,
            "date_to": date_to,
            "event[0]": "sent",
            "event[1]": "delivered",
        }

        assert query_params == expected

    def test_to_query_params_no_events(self):
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        params = ActivityQueryParams(date_from=date_from, date_to=date_to)

        query_params = params.to_query_params()

        expected = {"page": 1, "limit": 25, "date_from": date_from, "date_to": date_to}

        assert query_params == expected

    def test_all_valid_event_types(self):
        """Test that all documented event types are valid."""
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        all_events = [
            "queued",
            "sent",
            "delivered",
            "soft_bounced",
            "hard_bounced",
            "opened",
            "clicked",
            "unsubscribed",
            "spam_complaints",
            "survey_opened",
            "survey_submitted",
        ]

        params = ActivityQueryParams(
            date_from=date_from, date_to=date_to, event=all_events
        )

        assert params.event == all_events


class TestActivityRequest:
    def test_valid_request(self):
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        query_params = ActivityQueryParams(
            date_from=date_from,
            date_to=date_to,
            page=2,
            limit=50,
            event=["sent", "delivered"],
        )

        request = ActivityRequest(domain_id="test-domain", query_params=query_params)

        assert request.domain_id == "test-domain"
        assert request.query_params == query_params

    def test_to_query_params(self):
        current_time = int(time.time())
        date_from = current_time - 3600
        date_to = current_time

        query_params = ActivityQueryParams(
            date_from=date_from,
            date_to=date_to,
            page=2,
            limit=50,
            event=["sent", "delivered"],
        )

        request = ActivityRequest(domain_id="test-domain", query_params=query_params)

        result = request.to_query_params()
        expected = query_params.to_query_params()

        assert result == expected

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            ActivityRequest()

        errors = exc_info.value.errors()
        required_fields = {"domain_id", "query_params"}
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)


class TestSingleActivityRequest:
    """Test cases for SingleActivityRequest model."""

    def test_valid_activity_id(self):
        """Test creating SingleActivityRequest with valid activity_id."""
        activity_id = "5ee0b166b251345e407c9207"
        request = SingleActivityRequest(activity_id=activity_id)

        assert request.activity_id == activity_id

    def test_activity_id_with_whitespace(self):
        """Test that whitespace is stripped from activity_id."""
        activity_id = "  5ee0b166b251345e407c9207  "
        expected_id = "5ee0b166b251345e407c9207"
        request = SingleActivityRequest(activity_id=activity_id)

        assert request.activity_id == expected_id

    def test_empty_activity_id(self):
        """Test that empty activity_id raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            SingleActivityRequest(activity_id="")

        assert "activity_id cannot be empty" in str(exc_info.value)

    def test_whitespace_only_activity_id(self):
        """Test that whitespace-only activity_id raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            SingleActivityRequest(activity_id="   ")

        assert "activity_id cannot be empty" in str(exc_info.value)

    def test_none_activity_id(self):
        """Test that None activity_id is handled by Pydantic validation."""
        with pytest.raises(ValueError):
            SingleActivityRequest(activity_id=None)

    def test_required_fields(self):
        """Test that activity_id is required."""
        with pytest.raises(ValidationError) as exc_info:
            SingleActivityRequest()

        errors = exc_info.value.errors()
        required_fields = {"activity_id"}
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)
