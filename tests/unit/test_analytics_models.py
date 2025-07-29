import pytest
import time
from datetime import datetime, timezone

from mailersend.models.analytics import (
    AnalyticsRequest,
)
from mailersend.exceptions import ValidationError


class TestAnalyticsRequest:
    """Test AnalyticsRequest model functionality"""

    def test_valid_analytics_request(self):
        """Test creation of valid analytics request"""
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            domain_id="test-domain",
            recipient_id=["recipient1@example.com", "recipient2@example.com"],
            tags=["newsletter", "marketing"],
            group_by="days",
            event=["sent", "delivered", "opened"],
        )

        assert request.date_from == 1443651141
        assert request.date_to == 1443661141
        assert request.domain_id == "test-domain"
        assert request.recipient_id == [
            "recipient1@example.com",
            "recipient2@example.com",
        ]
        assert request.tags == ["newsletter", "marketing"]
        assert request.group_by == "days"
        assert request.event == ["sent", "delivered", "opened"]

    def test_required_fields_only(self):
        """Test creation with only required fields"""
        request = AnalyticsRequest(date_from=1443651141, date_to=1443661141)

        assert request.date_from == 1443651141
        assert request.date_to == 1443661141
        assert request.domain_id is None
        assert request.recipient_id is None
        assert request.tags is None
        assert request.group_by == "days"  # default value
        assert request.event is None

    def test_invalid_date_range(self):
        """Test validation when date_from >= date_to"""
        with pytest.raises(ValueError) as exc_info:
            AnalyticsRequest(
                date_from=1443661141,  # later timestamp
                date_to=1443651141,  # earlier timestamp
            )
        assert "date_from must be lower than date_to" in str(exc_info.value)

    def test_invalid_timestamps(self):
        """Test validation of timestamp values"""
        with pytest.raises(ValueError) as exc_info:
            AnalyticsRequest(date_from=0, date_to=1443661141)  # invalid timestamp
        assert "Timestamp must be a positive integer" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            AnalyticsRequest(date_from=1443651141, date_to=-1)  # invalid timestamp
        assert "Timestamp must be a positive integer" in str(exc_info.value)

    def test_recipient_count_validation(self):
        """Test recipient count limit validation"""
        # Test with exactly 50 recipients (should be valid)
        recipients_50 = [f"user{i}@example.com" for i in range(50)]
        request = AnalyticsRequest(
            date_from=1443651141, date_to=1443661141, recipient_id=recipients_50
        )
        assert len(request.recipient_id) == 50

        # Test with 51 recipients (should fail)
        recipients_51 = [f"user{i}@example.com" for i in range(51)]
        with pytest.raises(ValueError) as exc_info:
            AnalyticsRequest(
                date_from=1443651141, date_to=1443661141, recipient_id=recipients_51
            )
        assert "Maximum 50 recipients are allowed" in str(exc_info.value)

    def test_tags_validation(self):
        """Test tags validation"""
        # Valid tags
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            tags=["newsletter", "marketing", "promo"],
        )
        assert request.tags == ["newsletter", "marketing", "promo"]

        # Invalid tags - empty string
        with pytest.raises(ValueError) as exc_info:
            AnalyticsRequest(
                date_from=1443651141,
                date_to=1443661141,
                tags=["newsletter", "", "marketing"],
            )
        assert "All tags must be non-empty strings" in str(exc_info.value)

        # Invalid tags - whitespace only
        with pytest.raises(ValueError) as exc_info:
            AnalyticsRequest(
                date_from=1443651141,
                date_to=1443661141,
                tags=["newsletter", "   ", "marketing"],
            )
        assert "All tags must be non-empty strings" in str(exc_info.value)

    def test_group_by_validation(self):
        """Test group_by field validation"""
        valid_values = ["days", "weeks", "months", "years"]

        for value in valid_values:
            request = AnalyticsRequest(
                date_from=1443651141, date_to=1443661141, group_by=value
            )
            assert request.group_by == value

    def test_event_validation(self):
        """Test event field validation"""
        valid_events = [
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
            "opened_unique",
            "clicked_unique",
        ]

        # Test all valid events
        request = AnalyticsRequest(
            date_from=1443651141, date_to=1443661141, event=valid_events
        )
        assert request.event == valid_events

        # Test subset of valid events
        subset_events = ["sent", "delivered", "opened", "clicked"]
        request = AnalyticsRequest(
            date_from=1443651141, date_to=1443661141, event=subset_events
        )
        assert request.event == subset_events
