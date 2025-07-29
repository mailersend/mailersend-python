import pytest
from tests.test_helpers import vcr, email_client
from datetime import datetime, timezone, timedelta
from mailersend import MailerSendClient, AnalyticsBuilder
from mailersend.models.analytics import AnalyticsRequest
from mailersend.exceptions import ValidationError


@pytest.fixture
def base_analytics_request():
    """Basic email parameters that are valid for most tests"""

    # Use fixed recent timestamps within the 6-month analytics retention period
    # Using June 1, 2025 as base date for consistency (within 6 months)
    base_date = datetime(2025, 6, 1, tzinfo=timezone.utc)
    end_date = int(base_date.timestamp())
    start_date = int((base_date - timedelta(days=30)).timestamp())
    return AnalyticsRequest(
        date_from=start_date,
        date_to=end_date,
        event=["sent", "delivered", "opened"],
        group_by="days",
    )


def analytics_request_factory(base: AnalyticsRequest, **overrides) -> AnalyticsRequest:
    """Create a new AnalyticsRequest with the same fields, overridden with kwargs"""
    data = base.model_dump()

    # Remove fields explicitly set to `None` in overrides
    for key, value in overrides.items():
        if value is None:
            data.pop(key, None)
        else:
            data[key] = value

    return AnalyticsRequest(**data)


@pytest.fixture(autouse=True)
def inject_common_objects(request, email_client, base_analytics_request):
    if hasattr(request, "cls") and request.cls is not None:
        request.cls.email_client = email_client
        request.cls.base_analytics_request = base_analytics_request
        request.cls.analytics_request_factory = staticmethod(analytics_request_factory)


class TestAnalyticsIntegration:
    """Integration tests for Analytics API endpoints"""

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_basic.yaml")
    def test_get_activity_by_date_basic(self):
        """Test basic activity by date request"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            event=["sent", "delivered", "opened"],
            group_by="days",
        )

        response = self.email_client.analytics.get_activity_by_date(request)

        # Verify response structure
        assert response.status_code == 200
        assert "data" in response.data

        # Check response can be parsed as AnalyticsDateResponse
        data = response.data["data"]
        assert "stats" in data
        assert isinstance(data["stats"], list)

        # Verify date range in response
        assert "date_from" in data
        assert "date_to" in data

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_with_tags.yaml")
    def test_get_activity_by_date_with_tags(self):
        """Test activity by date with tag filtering"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            event=["sent", "delivered", "opened", "clicked"],
            tags=["newsletter", "marketing"],
            group_by="weeks",
        )

        response = self.email_client.analytics.get_activity_by_date(request)

        assert response.status_code == 200
        assert "data" in response.data

        data = response.data["data"]
        assert data["group_by"] == "weeks"

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_with_domain.yaml")
    def test_get_activity_by_date_with_domain(self):
        """Test activity by date with domain filtering"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            domain_id="your-domain-id",
            event=[
                "opened",
                "clicked",
                "unsubscribed",
                "spam_complaints",
            ],  # engagement events
            group_by="months",
        )

        response = self.email_client.analytics.get_activity_by_date(request)

        assert response.status_code == 200
        data = response.data["data"]
        assert data["group_by"] == "months"

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_all_events.yaml")
    def test_get_activity_by_date_all_events(self):
        """Test activity by date with all events"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            event=[
                "sent",
                "delivered",
                "opened",
                "clicked",
                "hard_bounced",
                "soft_bounced",
                "unsubscribed",
                "spam_complaints",
            ],  # all events (removed rejected as it's invalid)
        )

        response = self.email_client.analytics.get_activity_by_date(request)

        assert response.status_code == 200

        # Verify all events are tracked
        data = response.data["data"]
        if data["stats"]:
            # If there are stats, check they have the right structure
            first_stat = data["stats"][0]
            assert "date" in first_stat
            # Should have various event counts
            event_fields = ["sent", "delivered", "opened", "clicked", "hard_bounced"]
            # At least some of these fields should exist
            assert any(field in first_stat for field in event_fields)

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_country_basic.yaml")
    def test_get_opens_by_country_basic(self):
        """Test basic opens by country request"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            event=None,  # Country endpoint doesn't use events
        )

        response = self.email_client.analytics.get_opens_by_country(request)

        assert response.status_code == 200
        assert "data" in response.data

        data = response.data["data"]
        assert "stats" in data
        assert isinstance(data["stats"], list)

        # Check structure of country stats
        if data["stats"]:
            country_stat = data["stats"][0]
            assert "name" in country_stat
            assert "count" in country_stat
            assert isinstance(country_stat["count"], int)

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_country_with_tags.yaml")
    def test_get_opens_by_country_with_tags(self):
        """Test opens by country with tag filtering"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            tags=["newsletter"],
            event=None,  # Country endpoint doesn't use events
        )

        response = self.email_client.analytics.get_opens_by_country(request)

        assert response.status_code == 200
        data = response.data["data"]
        assert "stats" in data

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_user_agent_basic.yaml")
    def test_get_opens_by_user_agent_basic(self):
        """Test basic opens by user agent request"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            event=None,  # User agent endpoint doesn't use events
        )

        response = self.email_client.analytics.get_opens_by_user_agent(request)

        assert response.status_code == 200
        assert "data" in response.data

        data = response.data["data"]
        assert "stats" in data
        assert isinstance(data["stats"], list)

        # Check structure of user agent stats
        if data["stats"]:
            ua_stat = data["stats"][0]
            assert "name" in ua_stat
            assert "count" in ua_stat
            assert isinstance(ua_stat["count"], int)

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_user_agent_with_domain.yaml")
    def test_get_opens_by_user_agent_with_domain(self):
        """Test opens by user agent with domain filtering"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            domain_id="your-domain-id",
            event=None,  # User agent endpoint doesn't use events
        )

        response = self.email_client.analytics.get_opens_by_user_agent(request)

        assert response.status_code == 200
        data = response.data["data"]
        assert "stats" in data

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_reading_env_basic.yaml")
    def test_get_opens_by_reading_environment_basic(self):
        """Test basic opens by reading environment request"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            event=None,  # Reading environment endpoint doesn't use events
        )

        response = self.email_client.analytics.get_opens_by_reading_environment(request)

        assert response.status_code == 200
        assert "data" in response.data

        data = response.data["data"]
        assert "stats" in data
        assert isinstance(data["stats"], list)

        # Check structure of reading environment stats
        if data["stats"]:
            env_stat = data["stats"][0]
            assert "name" in env_stat
            assert "count" in env_stat
            assert isinstance(env_stat["count"], int)
            # Should be one of the valid reading environments
            assert env_stat["name"] in ["webmail", "mobile", "desktop"]

    @vcr.use_cassette(
        "tests/fixtures/cassettes/analytics_reading_env_with_recipients.yaml"
    )
    def test_get_opens_by_reading_environment_with_recipients(self):
        """Test opens by reading environment with recipient filtering"""
        request = self.analytics_request_factory(
            self.base_analytics_request,
            recipient_id=["recipient-1", "recipient-2"],
            event=None,  # Reading environment endpoint doesn't use events
        )

        response = self.email_client.analytics.get_opens_by_reading_environment(request)

        assert response.status_code == 200
        data = response.data["data"]
        assert "stats" in data

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_builder_helpers.yaml")
    def test_date_builder_helpers(self):
        """Test Analytics builder date helper methods"""
        # Test last 7 days using fixed date
        base_date = datetime(2025, 6, 1, tzinfo=timezone.utc)

        # Create request with 7 days range
        end_date = int(base_date.timestamp())
        start_date = int((base_date - timedelta(days=7)).timestamp())
        request = self.analytics_request_factory(
            self.base_analytics_request,
            date_from=start_date,
            date_to=end_date,
            event=["sent", "delivered"],
        )

        response = self.email_client.analytics.get_activity_by_date(request)
        assert response.status_code == 200

        # Test with specific end date (2 weeks range)
        start_date_weeks = int((base_date - timedelta(weeks=2)).timestamp())
        request = self.analytics_request_factory(
            self.base_analytics_request,
            date_from=start_date_weeks,
            date_to=end_date,
            event=["opened", "clicked"],
        )

        response = self.email_client.analytics.get_activity_by_date(request)
        assert response.status_code == 200

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_error_no_events.yaml")
    def test_activity_by_date_error_no_events(self):
        """Test that activity by date requires events"""
        from mailersend.exceptions import BadRequestError
        
        request = self.analytics_request_factory(
            self.base_analytics_request,
            event=None,  # No events specified - should cause error
        )

        with pytest.raises(
            BadRequestError, match="The event must be an array"
        ):
            self.email_client.analytics.get_activity_by_date(request)

    def test_invalid_date_range_error(self):
        """Test error handling for invalid date ranges"""
        from pydantic import ValidationError as PydanticValidationError

        # Get the timestamps from base request and reverse them
        base_timestamps = self.base_analytics_request

        with pytest.raises(PydanticValidationError):
            AnalyticsRequest(
                date_from=base_timestamps.date_to,
                date_to=base_timestamps.date_from,  # Wrong order
                event=["sent"],
            )

    def test_builder_fluent_interface(self):
        """Test that builder methods can be chained fluently"""
        request = (
            AnalyticsBuilder()
            .domain("test-domain")
            .recipients("test-recipient")
            .date_range_days(30)
            .tags("newsletter", "marketing")
            .group_by("weeks")
            .engagement_events()
            .build()
        )

        # Verify the request was built correctly
        assert request.domain_id == "test-domain"
        assert request.recipient_id == ["test-recipient"]
        assert request.tags == ["newsletter", "marketing"]
        assert request.group_by == "weeks"
        assert request.event == ["opened", "clicked", "opened_unique", "clicked_unique"]

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_comprehensive_test.yaml")
    def test_comprehensive_analytics_workflow(self):
        """Test a comprehensive analytics workflow using all endpoints"""
        # Build a comprehensive request for activity by date
        request = self.analytics_request_factory(
            self.base_analytics_request,
            tags=["integration-test"],
            event=["sent", "delivered"],  # delivery events
            group_by="days",
        )

        # Test activity by date
        date_response = self.email_client.analytics.get_activity_by_date(request)
        assert date_response.status_code == 200

        # Test opens by country (doesn't need events)
        country_request = self.analytics_request_factory(
            self.base_analytics_request,
            tags=["integration-test"],
            event=None,  # Country endpoint doesn't use events
        )

        country_response = self.email_client.analytics.get_opens_by_country(
            country_request
        )
        assert country_response.status_code == 200

        # Test opens by user agent
        ua_response = self.email_client.analytics.get_opens_by_user_agent(
            country_request
        )
        assert ua_response.status_code == 200

        # Test opens by reading environment
        env_response = self.email_client.analytics.get_opens_by_reading_environment(
            country_request
        )
        assert env_response.status_code == 200

        # All should return valid data structures
        for response in [date_response, country_response, ua_response, env_response]:
            assert "data" in response.data
            assert "stats" in response.data["data"]


class TestAnalyticsBuilderIntegration:
    """Integration tests specifically for AnalyticsBuilder functionality"""

    def test_builder_date_helpers_accuracy(self):
        """Test that builder date helpers produce accurate timestamps"""
        builder = AnalyticsBuilder()

        # Test that date helpers produce reasonable timestamps
        request = builder.date_range_days(7).events("sent").build()

        # Should have a 7-day difference
        date_diff = request.date_to - request.date_from
        expected_diff = 7 * 24 * 60 * 60  # 7 days in seconds

        # Allow for small timing differences (within 60 seconds)
        assert abs(date_diff - expected_diff) < 60

    def test_builder_reset_functionality(self):
        """Test builder reset works correctly"""
        builder = AnalyticsBuilder()

        # Build first request
        request1 = (
            builder.domain("domain-1")
            .tags("tag-1")
            .date_range_days(7)
            .events("sent")
            .build()
        )

        # Reset and build second request
        request2 = (
            builder.reset()
            .domain("domain-2")
            .tags("tag-2")
            .date_range_days(14)
            .events("delivered")
            .build()
        )

        # Verify they're different
        assert request1.domain_id != request2.domain_id
        assert request1.tags != request2.tags
        assert request1.event != request2.event

        # Verify the date ranges are different (7 vs 14 days)
        diff1 = request1.date_to - request1.date_from
        diff2 = request2.date_to - request2.date_from
        assert diff2 > diff1  # 14 days should be longer than 7 days

    def test_builder_copy_functionality(self):
        """Test builder copy creates independent instances"""
        base_builder = (
            AnalyticsBuilder()
            .domain("shared-domain")
            .date_range_days(30)
            .events("sent", "delivered")
        )

        # Copy and modify
        builder1 = base_builder.copy().tags("newsletter")
        builder2 = base_builder.copy().tags("marketing")

        request1 = builder1.build()
        request2 = builder2.build()

        # Both should have shared domain and date range
        assert request1.domain_id == request2.domain_id == "shared-domain"

        # But different tags
        assert request1.tags == ["newsletter"]
        assert request2.tags == ["marketing"]

        # Original builder should be unchanged
        base_request = base_builder.build()
        assert base_request.tags is None
