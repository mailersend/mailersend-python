import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from mailersend.builders.analytics import AnalyticsBuilder
from mailersend.models.analytics import AnalyticsRequest
from mailersend.exceptions import ValidationError


class TestAnalyticsBuilder:
    """Test AnalyticsBuilder functionality"""

    def test_basic_analytics_builder(self):
        """Test basic analytics builder construction"""
        request = (
            AnalyticsBuilder()
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert isinstance(request, AnalyticsRequest)
        assert request.date_from == 1443651141
        assert request.date_to == 1443661141
        assert request.group_by == "days"  # default

    def test_domain_filtering(self):
        """Test domain filtering"""
        request = (
            AnalyticsBuilder()
            .domain("domain-123")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.domain_id == "domain-123"

    def test_recipient_filtering(self):
        """Test recipient filtering"""
        request = (
            AnalyticsBuilder()
            .recipient("recipient-1")
            .recipient("recipient-2")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.recipient_id == ["recipient-1", "recipient-2"]

    def test_recipients_multiple(self):
        """Test adding multiple recipients at once"""
        request = (
            AnalyticsBuilder()
            .recipients("recipient-1", "recipient-2", "recipient-3")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.recipient_id == ["recipient-1", "recipient-2", "recipient-3"]

    def test_recipient_limit_validation(self):
        """Test recipient limit validation"""
        builder = AnalyticsBuilder()

        # Add 50 recipients (should work)
        for i in range(50):
            builder.recipient(f"recipient-{i}")

        # Try to add the 51st recipient (should fail)
        with pytest.raises(ValidationError, match="Maximum 50 recipients are allowed"):
            builder.recipient("recipient-51")

    def test_timestamp_date_methods(self):
        """Test timestamp-based date methods"""
        request = (
            AnalyticsBuilder()
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.date_from == 1443651141
        assert request.date_to == 1443661141

    def test_timestamp_validation(self):
        """Test timestamp validation"""
        builder = AnalyticsBuilder()

        with pytest.raises(
            ValidationError, match="Timestamp must be a positive integer"
        ):
            builder.date_from_timestamp(-1)

        with pytest.raises(
            ValidationError, match="Timestamp must be a positive integer"
        ):
            builder.date_to_timestamp(0)

    def test_datetime_date_methods(self):
        """Test datetime-based date methods"""
        dt_from = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        dt_to = datetime(2024, 1, 7, 12, 0, 0, tzinfo=timezone.utc)

        request = (
            AnalyticsBuilder()
            .date_from_datetime(dt_from)
            .date_to_datetime(dt_to)
            .build()
        )

        assert request.date_from == int(dt_from.timestamp())
        assert request.date_to == int(dt_to.timestamp())

    def test_datetime_without_timezone(self):
        """Test datetime without timezone (should default to UTC)"""
        dt_from = datetime(2024, 1, 1, 12, 0, 0)
        dt_to = datetime(2024, 1, 7, 12, 0, 0)

        request = (
            AnalyticsBuilder()
            .date_from_datetime(dt_from)
            .date_to_datetime(dt_to)
            .build()
        )

        # Should be treated as UTC
        expected_from = int(dt_from.replace(tzinfo=timezone.utc).timestamp())
        expected_to = int(dt_to.replace(tzinfo=timezone.utc).timestamp())

        assert request.date_from == expected_from
        assert request.date_to == expected_to

    def test_date_range_method(self):
        """Test date range method"""
        dt_from = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        dt_to = datetime(2024, 1, 7, 12, 0, 0, tzinfo=timezone.utc)

        request = AnalyticsBuilder().date_range(dt_from, dt_to).build()

        assert request.date_from == int(dt_from.timestamp())
        assert request.date_to == int(dt_to.timestamp())

    @patch("mailersend.builders.analytics.datetime")
    def test_date_range_days(self, mock_datetime):
        """Test date range days helper"""
        now = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now

        request = AnalyticsBuilder().date_range_days(7).build()

        start = now - timedelta(days=7)

        assert request.date_from == int(start.timestamp())
        assert request.date_to == int(now.timestamp())

    def test_date_range_days_with_end_date(self):
        """Test date range days with custom end date"""
        end_date = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)

        request = AnalyticsBuilder().date_range_days(7, end_date).build()

        start = end_date - timedelta(days=7)

        assert request.date_from == int(start.timestamp())
        assert request.date_to == int(end_date.timestamp())

    @patch("mailersend.builders.analytics.datetime")
    def test_date_range_weeks(self, mock_datetime):
        """Test date range weeks helper"""
        now = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now

        request = AnalyticsBuilder().date_range_weeks(2).build()

        start = now - timedelta(days=14)  # 2 weeks = 14 days

        assert request.date_from == int(start.timestamp())
        assert request.date_to == int(now.timestamp())

    @patch("mailersend.builders.analytics.datetime")
    def test_date_range_months(self, mock_datetime):
        """Test date range months helper"""
        now = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now

        request = AnalyticsBuilder().date_range_months(2).build()

        start = now - timedelta(days=60)  # 2 months = 60 days (approximate)

        assert request.date_from == int(start.timestamp())
        assert request.date_to == int(now.timestamp())

    @patch("mailersend.builders.analytics.datetime")
    def test_today_helper(self, mock_datetime):
        """Test today helper"""
        now = datetime(2024, 1, 15, 14, 30, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now

        request = AnalyticsBuilder().today().build()

        start_of_day = datetime(2024, 1, 15, 0, 0, 0, tzinfo=timezone.utc)

        assert request.date_from == int(start_of_day.timestamp())
        assert request.date_to == int(now.timestamp())

    @patch("mailersend.builders.analytics.datetime")
    def test_yesterday_helper(self, mock_datetime):
        """Test yesterday helper"""
        now = datetime(2024, 1, 15, 14, 30, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now

        request = AnalyticsBuilder().yesterday().build()

        start_of_yesterday = datetime(2024, 1, 14, 0, 0, 0, tzinfo=timezone.utc)
        end_of_yesterday = datetime(2024, 1, 15, 0, 0, 0, tzinfo=timezone.utc)

        assert request.date_from == int(start_of_yesterday.timestamp())
        assert request.date_to == int(end_of_yesterday.timestamp())

    @patch("mailersend.builders.analytics.datetime")
    def test_this_week_helper(self, mock_datetime):
        """Test this week helper"""
        now = datetime(2024, 1, 15, 14, 30, 0, tzinfo=timezone.utc)  # Monday
        mock_datetime.now.return_value = now

        request = AnalyticsBuilder().this_week().build()

        start_of_week = datetime(2024, 1, 15, 0, 0, 0, tzinfo=timezone.utc)  # Monday

        assert request.date_from == int(start_of_week.timestamp())
        assert request.date_to == int(now.timestamp())

    @patch("mailersend.builders.analytics.datetime")
    def test_this_month_helper(self, mock_datetime):
        """Test this month helper"""
        now = datetime(2024, 1, 15, 14, 30, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now

        request = AnalyticsBuilder().this_month().build()

        start_of_month = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        assert request.date_from == int(start_of_month.timestamp())
        assert request.date_to == int(now.timestamp())

    def test_tag_methods(self):
        """Test tag methods"""
        request = (
            AnalyticsBuilder()
            .tag("newsletter", "marketing")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.tags == ["newsletter", "marketing"]

    def test_tags_alias(self):
        """Test tags alias method"""
        request = (
            AnalyticsBuilder()
            .tags("newsletter", "marketing", "campaign")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.tags == ["newsletter", "marketing", "campaign"]

    def test_tag_validation(self):
        """Test tag validation"""
        builder = AnalyticsBuilder()

        with pytest.raises(ValidationError, match="Tags cannot be empty"):
            builder.tag("")

        with pytest.raises(ValidationError, match="Tags cannot be empty"):
            builder.tag("   ")

    def test_tag_deduplication(self):
        """Test tag deduplication"""
        request = (
            AnalyticsBuilder()
            .tag("newsletter")
            .tag("newsletter")  # duplicate
            .tag("marketing")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.tags == ["newsletter", "marketing"]

    def test_group_by_method(self):
        """Test group_by method"""
        for group_by in ["days", "weeks", "months", "years"]:
            request = (
                AnalyticsBuilder()
                .group_by(group_by)
                .date_from_timestamp(1443651141)
                .date_to_timestamp(1443661141)
                .build()
            )

            assert request.group_by == group_by

    def test_group_by_validation(self):
        """Test group_by validation"""
        builder = AnalyticsBuilder()

        with pytest.raises(ValidationError, match="group_by must be one of"):
            builder.group_by("invalid")

    def test_event_methods(self):
        """Test event methods"""
        request = (
            AnalyticsBuilder()
            .event("sent", "delivered", "opened")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.event == ["sent", "delivered", "opened"]

    def test_events_alias(self):
        """Test events alias method"""
        request = (
            AnalyticsBuilder()
            .events("sent", "delivered", "opened", "clicked")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.event == ["sent", "delivered", "opened", "clicked"]

    def test_event_validation(self):
        """Test event validation"""
        builder = AnalyticsBuilder()

        with pytest.raises(ValidationError, match="Invalid event: invalid"):
            builder.event("invalid")

    def test_event_deduplication(self):
        """Test event deduplication"""
        request = (
            AnalyticsBuilder()
            .event("sent")
            .event("sent")  # duplicate
            .event("delivered")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request.event == ["sent", "delivered"]

    def test_all_events_helper(self):
        """Test all events helper"""
        request = (
            AnalyticsBuilder()
            .all_events()
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        expected_events = [
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

        assert request.event == expected_events

    def test_delivery_events_helper(self):
        """Test delivery events helper"""
        request = (
            AnalyticsBuilder()
            .delivery_events()
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        expected_events = [
            "queued",
            "sent",
            "delivered",
            "soft_bounced",
            "hard_bounced",
        ]
        assert request.event == expected_events

    def test_engagement_events_helper(self):
        """Test engagement events helper"""
        request = (
            AnalyticsBuilder()
            .engagement_events()
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        expected_events = ["opened", "clicked", "opened_unique", "clicked_unique"]
        assert request.event == expected_events

    def test_negative_events_helper(self):
        """Test negative events helper"""
        request = (
            AnalyticsBuilder()
            .negative_events()
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        expected_events = ["unsubscribed", "spam_complaints"]
        assert request.event == expected_events

    def test_build_validation_missing_dates(self):
        """Test build validation for missing dates"""
        builder = AnalyticsBuilder()

        with pytest.raises(ValidationError, match="date_from is required"):
            builder.build()

        with pytest.raises(ValidationError, match="date_to is required"):
            builder.date_from_timestamp(1443651141).build()

    def test_complex_builder_chain(self):
        """Test complex builder chain"""
        request = (
            AnalyticsBuilder()
            .domain("domain-123")
            .recipients("recipient-1", "recipient-2")
            .date_range_days(30)
            .tags("newsletter", "marketing")
            .group_by("weeks")
            .engagement_events()
            .build()
        )

        assert request.domain_id == "domain-123"
        assert request.recipient_id == ["recipient-1", "recipient-2"]
        assert request.tags == ["newsletter", "marketing"]
        assert request.group_by == "weeks"
        assert request.event == ["opened", "clicked", "opened_unique", "clicked_unique"]

    def test_builder_reset(self):
        """Test builder reset functionality"""
        builder = (
            AnalyticsBuilder()
            .domain("domain-123")
            .tags("newsletter")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
        )

        # Build first request
        request1 = builder.build()
        assert request1.domain_id == "domain-123"
        assert request1.tags == ["newsletter"]

        # Reset and build new request
        request2 = (
            builder.reset()
            .domain("domain-456")
            .tags("marketing")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request2.domain_id == "domain-456"
        assert request2.tags == ["marketing"]
        assert request2.domain_id != request1.domain_id

    def test_builder_copy(self):
        """Test builder copy functionality"""
        base_builder = (
            AnalyticsBuilder()
            .domain("domain-123")
            .tags("newsletter")
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
        )

        # Copy and modify
        copied_builder = base_builder.copy()
        request1 = copied_builder.tags("marketing").build()

        # Original builder should be unchanged
        request2 = base_builder.build()

        assert request1.tags == ["newsletter", "marketing"]
        assert request2.tags == ["newsletter"]
        assert request1.domain_id == request2.domain_id  # Same base data

    def test_builder_fluent_interface(self):
        """Test that all methods return builder instance for chaining"""
        builder = AnalyticsBuilder()

        # Test all methods return self
        assert builder.domain("test") is builder
        assert builder.recipient("test") is builder
        assert builder.recipients("test") is builder
        assert builder.date_from_timestamp(1443651141) is builder
        assert builder.date_to_timestamp(1443661141) is builder
        assert builder.tag("test") is builder
        assert builder.tags("test") is builder
        assert builder.group_by("days") is builder
        assert builder.event("sent") is builder
        assert builder.events("sent") is builder
        assert builder.all_events() is builder
        assert builder.delivery_events() is builder
        assert builder.engagement_events() is builder
        assert builder.negative_events() is builder
        assert builder.reset() is builder


class TestAnalyticsBuilderEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_lists_in_build(self):
        """Test handling of empty lists in build"""
        request = (
            AnalyticsBuilder()
            .date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        # Empty lists should be None in the final request
        assert request.recipient_id is None
        assert request.tags is None
        assert request.event is None

    def test_date_helpers_with_timezone_naive_datetime(self):
        """Test date helpers with timezone-naive datetime"""
        end_date = datetime(2024, 1, 15, 12, 0, 0)  # No timezone

        request = AnalyticsBuilder().date_range_days(7, end_date).build()

        # Should be treated as UTC
        expected_end = end_date.replace(tzinfo=timezone.utc)
        expected_start = expected_end - timedelta(days=7)

        assert request.date_from == int(expected_start.timestamp())
        assert request.date_to == int(expected_end.timestamp())

    def test_builder_state_isolation(self):
        """Test that builder instances don't interfere with each other"""
        builder1 = AnalyticsBuilder().domain("domain-1").tags("tag-1")
        builder2 = AnalyticsBuilder().domain("domain-2").tags("tag-2")

        request1 = (
            builder1.date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        request2 = (
            builder2.date_from_timestamp(1443651141)
            .date_to_timestamp(1443661141)
            .build()
        )

        assert request1.domain_id == "domain-1"
        assert request1.tags == ["tag-1"]
        assert request2.domain_id == "domain-2"
        assert request2.tags == ["tag-2"]
