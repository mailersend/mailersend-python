import pytest
import vcr
import os
from datetime import datetime, timezone, timedelta

from mailersend import MailerSendClient, AnalyticsBuilder
from mailersend.models.analytics import (
    AnalyticsRequest, AnalyticsDateResponse, AnalyticsCountryResponse,
    AnalyticsUserAgentResponse, AnalyticsReadingEnvironmentResponse
)
from mailersend.exceptions import ValidationError


class TestAnalyticsIntegration:
    """Integration tests for Analytics API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test client"""
        api_key = os.getenv("MAILERSEND_API_KEY", "test-api-key")
        self.client = MailerSendClient(api_key=api_key)
        
        # Use fixed recent timestamps within the 6-month analytics retention period
        # Using June 1, 2025 as base date for consistency (within 6 months)
        base_date = datetime(2025, 6, 1, tzinfo=timezone.utc)
        self.end_date = int(base_date.timestamp())
        self.start_date = int((base_date - timedelta(days=30)).timestamp())

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_basic.yaml")
    def test_get_activity_by_date_basic(self):
        """Test basic activity by date request"""
        request = (AnalyticsBuilder()
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .events("sent", "delivered", "opened")
            .group_by("days")
            .build())
        
        response = self.client.analytics.get_activity_by_date(request)
        
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
        request = (AnalyticsBuilder()
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .events("sent", "delivered", "opened", "clicked")
            .tags("newsletter", "marketing")
            .group_by("weeks")
            .build())
        
        response = self.client.analytics.get_activity_by_date(request)
        
        assert response.status_code == 200
        assert "data" in response.data
        
        data = response.data["data"]
        assert data["group_by"] == "weeks"

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_with_domain.yaml")
    def test_get_activity_by_date_with_domain(self):
        """Test activity by date with domain filtering"""
        request = (AnalyticsBuilder()
            .domain("your-domain-id")
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .engagement_events()
            .group_by("months")
            .build())
        
        response = self.client.analytics.get_activity_by_date(request)
        
        assert response.status_code == 200
        data = response.data["data"]
        assert data["group_by"] == "months"

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_all_events.yaml")
    def test_get_activity_by_date_all_events(self):
        """Test activity by date with all events"""
        request = (AnalyticsBuilder()
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .all_events()
            .build())
        
        response = self.client.analytics.get_activity_by_date(request)
        
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
        request = (AnalyticsBuilder()
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .build())
        
        response = self.client.analytics.get_opens_by_country(request)
        
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
        request = (AnalyticsBuilder()
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .tags("newsletter")
            .build())
        
        response = self.client.analytics.get_opens_by_country(request)
        
        assert response.status_code == 200
        data = response.data["data"]
        assert "stats" in data

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_user_agent_basic.yaml")
    def test_get_opens_by_user_agent_basic(self):
        """Test basic opens by user agent request"""
        request = (AnalyticsBuilder()
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .build())
        
        response = self.client.analytics.get_opens_by_user_agent(request)
        
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
        request = (AnalyticsBuilder()
            .domain("your-domain-id")
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .build())
        
        response = self.client.analytics.get_opens_by_user_agent(request)
        
        assert response.status_code == 200
        data = response.data["data"]
        assert "stats" in data

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_reading_env_basic.yaml")
    def test_get_opens_by_reading_environment_basic(self):
        """Test basic opens by reading environment request"""
        request = (AnalyticsBuilder()
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .build())
        
        response = self.client.analytics.get_opens_by_reading_environment(request)
        
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

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_reading_env_with_recipients.yaml")
    def test_get_opens_by_reading_environment_with_recipients(self):
        """Test opens by reading environment with recipient filtering"""
        request = (AnalyticsBuilder()
            .recipients("recipient-1", "recipient-2")
            .date_from_timestamp(self.start_date)
            .date_to_timestamp(self.end_date)
            .build())
        
        response = self.client.analytics.get_opens_by_reading_environment(request)
        
        assert response.status_code == 200
        data = response.data["data"]
        assert "stats" in data

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_date_builder_helpers.yaml")
    def test_date_builder_helpers(self):
        """Test Analytics builder date helper methods"""
        # Test last 7 days using fixed date
        base_date = datetime(2025, 6, 1, tzinfo=timezone.utc)
        request = (AnalyticsBuilder()
            .date_range_days(7, base_date)
            .events("sent", "delivered")
            .build())
        
        response = self.client.analytics.get_activity_by_date(request)
        assert response.status_code == 200
        
        # Test with specific end date
        request = (AnalyticsBuilder()
            .date_range_weeks(2, base_date)
            .events("opened", "clicked")
            .build())
        
        response = self.client.analytics.get_activity_by_date(request)
        assert response.status_code == 200

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_error_no_events.yaml")
    def test_activity_by_date_error_no_events(self):
        """Test that activity by date requires events"""
        request = AnalyticsRequest(
            date_from=self.start_date,
            date_to=self.end_date
            # No events specified
        )
        
        with pytest.raises(ValidationError, match="At least one event must be specified"):
            self.client.analytics.get_activity_by_date(request)

    def test_invalid_date_range_error(self):
        """Test error handling for invalid date ranges"""
        from pydantic import ValidationError as PydanticValidationError
        
        with pytest.raises(PydanticValidationError):
            AnalyticsRequest(
                date_from=self.end_date,
                date_to=self.start_date,  # Wrong order
                event=["sent"]
            )

    def test_builder_fluent_interface(self):
        """Test that builder methods can be chained fluently"""
        request = (AnalyticsBuilder()
            .domain("test-domain")
            .recipients("test-recipient")
            .date_range_days(30)
            .tags("newsletter", "marketing")
            .group_by("weeks")
            .engagement_events()
            .build())
        
        # Verify the request was built correctly
        assert request.domain_id == "test-domain"
        assert request.recipient_id == ["test-recipient"]
        assert request.tags == ["newsletter", "marketing"]
        assert request.group_by == "weeks"
        assert request.event == ["opened", "clicked", "opened_unique", "clicked_unique"]

    @vcr.use_cassette("tests/fixtures/cassettes/analytics_comprehensive_test.yaml")
    def test_comprehensive_analytics_workflow(self):
        """Test a comprehensive analytics workflow using all endpoints"""
        # Build a comprehensive request using fixed date
        base_date = datetime(2025, 6, 1, tzinfo=timezone.utc)
        request = (AnalyticsBuilder()
            .date_range_days(30, base_date)
            .tags("integration-test")
            .delivery_events()  # Focus on delivery events for this test
            .group_by("days")
            .build())
        
        # Test activity by date
        date_response = self.client.analytics.get_activity_by_date(request)
        assert date_response.status_code == 200
        
        # Test opens by country (doesn't need events)
        country_request = (AnalyticsBuilder()
            .date_range_days(30, base_date)
            .tags("integration-test")
            .build())
        
        country_response = self.client.analytics.get_opens_by_country(country_request)
        assert country_response.status_code == 200
        
        # Test opens by user agent
        ua_response = self.client.analytics.get_opens_by_user_agent(country_request)
        assert ua_response.status_code == 200
        
        # Test opens by reading environment
        env_response = self.client.analytics.get_opens_by_reading_environment(country_request)
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
        request1 = (builder
            .domain("domain-1")
            .tags("tag-1")
            .date_range_days(7)
            .events("sent")
            .build())
        
        # Reset and build second request
        request2 = (builder
            .reset()
            .domain("domain-2")
            .tags("tag-2")
            .date_range_days(14)
            .events("delivered")
            .build())
        
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
        base_builder = (AnalyticsBuilder()
            .domain("shared-domain")
            .date_range_days(30)
            .events("sent", "delivered"))
        
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