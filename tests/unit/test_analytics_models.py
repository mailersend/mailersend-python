import pytest
import time
from datetime import datetime, timezone

from mailersend.models.analytics import (
    AnalyticsRequest, AnalyticsDateStats, AnalyticsDateResponse,
    AnalyticsCountryStats, AnalyticsCountryResponse,
    AnalyticsUserAgentStats, AnalyticsUserAgentResponse,
    AnalyticsReadingEnvironmentStats, AnalyticsReadingEnvironmentResponse
)
from mailersend.exceptions import ValidationError


class TestAnalyticsRequest:
    """Test AnalyticsRequest model functionality"""
    
    def test_basic_analytics_request(self):
        """Test basic analytics request creation"""
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            tags=["newsletter", "marketing"],
            event=["sent", "delivered", "opened"]
        )
        
        assert request.date_from == 1443651141
        assert request.date_to == 1443661141
        assert request.tags == ["newsletter", "marketing"]
        assert request.event == ["sent", "delivered", "opened"]
        assert request.group_by == "days"  # default value
        assert request.domain_id is None
        assert request.recipient_id is None
    
    def test_analytics_request_with_all_fields(self):
        """Test analytics request with all possible fields"""
        request = AnalyticsRequest(
            domain_id="domain-123",
            recipient_id=["recipient-1", "recipient-2"],
            date_from=1443651141,
            date_to=1443661141,
            tags=["newsletter", "marketing"],
            group_by="weeks",
            event=["sent", "delivered", "opened", "clicked"]
        )
        
        assert request.domain_id == "domain-123"
        assert request.recipient_id == ["recipient-1", "recipient-2"]
        assert request.date_from == 1443651141
        assert request.date_to == 1443661141
        assert request.tags == ["newsletter", "marketing"]
        assert request.group_by == "weeks"
        assert request.event == ["sent", "delivered", "opened", "clicked"]
    
    def test_analytics_request_aliases(self):
        """Test field aliases work correctly"""
        data = {
            "recipient_id[]": ["recipient-1", "recipient-2"],
            "date_from": 1443651141,
            "date_to": 1443661141,
            "tags[]": ["newsletter"],
            "event[]": ["sent", "delivered"]
        }
        
        request = AnalyticsRequest(**data)
        
        assert request.recipient_id == ["recipient-1", "recipient-2"]
        assert request.tags == ["newsletter"]
        assert request.event == ["sent", "delivered"]
    
    def test_model_dump_with_aliases(self):
        """Test model serialization with aliases"""
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            tags=["newsletter"],
            event=["sent", "delivered"]
        )
        
        data = request.model_dump(by_alias=True, exclude_none=True)
        
        assert "tags[]" in data
        assert "event[]" in data
        assert data["tags[]"] == ["newsletter"]
        assert data["event[]"] == ["sent", "delivered"]
    
    def test_date_validation_positive_timestamps(self):
        """Test that timestamps must be positive"""
        with pytest.raises(ValueError, match="Timestamp must be a positive integer"):
            AnalyticsRequest(date_from=-1, date_to=1443661141)
        
        with pytest.raises(ValueError, match="Timestamp must be a positive integer"):
            AnalyticsRequest(date_from=1443651141, date_to=0)
    
    def test_date_range_validation(self):
        """Test that date_from must be before date_to"""
        with pytest.raises(ValueError, match="date_from must be lower than date_to"):
            AnalyticsRequest(date_from=1443661141, date_to=1443651141)
        
        with pytest.raises(ValueError, match="date_from must be lower than date_to"):
            AnalyticsRequest(date_from=1443651141, date_to=1443651141)
    
    def test_recipient_count_validation(self):
        """Test recipient count limit validation"""
        # Should work with 50 recipients
        recipients = [f"recipient-{i}" for i in range(50)]
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            recipient_id=recipients
        )
        assert len(request.recipient_id) == 50
        
        # Should fail with 51 recipients
        recipients = [f"recipient-{i}" for i in range(51)]
        with pytest.raises(ValueError, match="Maximum 50 recipients are allowed"):
            AnalyticsRequest(
                date_from=1443651141,
                date_to=1443661141,
                recipient_id=recipients
            )
    
    def test_tags_validation(self):
        """Test tags validation"""
        # Valid tags
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            tags=["newsletter", "marketing", "campaign"]
        )
        assert request.tags == ["newsletter", "marketing", "campaign"]
        
        # Empty string tags should fail
        with pytest.raises(ValueError, match="All tags must be non-empty strings"):
            AnalyticsRequest(
                date_from=1443651141,
                date_to=1443661141,
                tags=["newsletter", "", "marketing"]
            )
        
        # Whitespace-only tags should fail
        with pytest.raises(ValueError, match="All tags must be non-empty strings"):
            AnalyticsRequest(
                date_from=1443651141,
                date_to=1443661141,
                tags=["newsletter", "   ", "marketing"]
            )
    
    def test_group_by_literal_validation(self):
        """Test group_by field accepts only valid values"""
        # Valid values
        for group_by in ["days", "weeks", "months", "years"]:
            request = AnalyticsRequest(
                date_from=1443651141,
                date_to=1443661141,
                group_by=group_by
            )
            assert request.group_by == group_by
    
    def test_event_literal_validation(self):
        """Test event field accepts only valid values"""
        valid_events = [
            "queued", "sent", "delivered", "soft_bounced", "hard_bounced",
            "opened", "clicked", "unsubscribed", "spam_complaints",
            "survey_opened", "survey_submitted", "opened_unique", "clicked_unique"
        ]
        
        # Test all valid events
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            event=valid_events
        )
        assert request.event == valid_events
        
        # Test subset of valid events
        subset_events = ["sent", "delivered", "opened", "clicked"]
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            event=subset_events
        )
        assert request.event == subset_events


class TestAnalyticsDateStats:
    """Test AnalyticsDateStats model"""
    
    def test_date_stats_creation(self):
        """Test basic date stats creation"""
        stats = AnalyticsDateStats(
            date="1591228800",
            sent=100,
            delivered=95,
            opened=30,
            clicked=10
        )
        
        assert stats.date == "1591228800"
        assert stats.sent == 100
        assert stats.delivered == 95
        assert stats.opened == 30
        assert stats.clicked == 10
        assert stats.queued == 0  # default value
    
    def test_date_stats_with_all_fields(self):
        """Test date stats with all fields"""
        stats = AnalyticsDateStats(
            date="1591228800",
            queued=105,
            sent=100,
            delivered=95,
            opened=30,
            clicked=10,
            soft_bounced=2,
            hard_bounced=3,
            unsubscribed=1,
            spam_complaints=0,
            opened_unique=25,
            clicked_unique=8,
            survey_opened=5,
            survey_submitted=2
        )
        
        assert stats.queued == 105
        assert stats.sent == 100
        assert stats.delivered == 95
        assert stats.opened == 30
        assert stats.clicked == 10
        assert stats.soft_bounced == 2
        assert stats.hard_bounced == 3
        assert stats.unsubscribed == 1
        assert stats.spam_complaints == 0
        assert stats.opened_unique == 25
        assert stats.clicked_unique == 8
        assert stats.survey_opened == 5
        assert stats.survey_submitted == 2


class TestAnalyticsDateResponse:
    """Test AnalyticsDateResponse model"""
    
    def test_date_response_creation(self):
        """Test date response creation"""
        stats = [
            AnalyticsDateStats(date="1591228800", sent=100, delivered=95),
            AnalyticsDateStats(date="1591315200", sent=120, delivered=115)
        ]
        
        response = AnalyticsDateResponse(
            date_from="1591228800",
            date_to="1591401599",
            group_by="days",
            stats=stats
        )
        
        assert response.date_from == "1591228800"
        assert response.date_to == "1591401599"
        assert response.group_by == "days"
        assert len(response.stats) == 2
        assert response.stats[0].sent == 100
        assert response.stats[1].sent == 120


class TestAnalyticsCountryStats:
    """Test AnalyticsCountryStats model"""
    
    def test_country_stats_creation(self):
        """Test country stats creation"""
        stats = AnalyticsCountryStats(name="LT", count=25)
        
        assert stats.name == "LT"
        assert stats.count == 25


class TestAnalyticsCountryResponse:
    """Test AnalyticsCountryResponse model"""
    
    def test_country_response_creation(self):
        """Test country response creation"""
        stats = [
            AnalyticsCountryStats(name="LT", count=25),
            AnalyticsCountryStats(name="US", count=50),
            AnalyticsCountryStats(name="DE", count=30)
        ]
        
        response = AnalyticsCountryResponse(
            date_from=1591228800,
            date_to=1591401599,
            stats=stats
        )
        
        assert response.date_from == 1591228800
        assert response.date_to == 1591401599
        assert len(response.stats) == 3
        assert response.stats[0].name == "LT"
        assert response.stats[1].count == 50


class TestAnalyticsUserAgentStats:
    """Test AnalyticsUserAgentStats model"""
    
    def test_user_agent_stats_creation(self):
        """Test user agent stats creation"""
        stats = AnalyticsUserAgentStats(name="Chrome", count=75)
        
        assert stats.name == "Chrome"
        assert stats.count == 75


class TestAnalyticsUserAgentResponse:
    """Test AnalyticsUserAgentResponse model"""
    
    def test_user_agent_response_creation(self):
        """Test user agent response creation"""
        stats = [
            AnalyticsUserAgentStats(name="Chrome", count=75),
            AnalyticsUserAgentStats(name="Firefox", count=20),
            AnalyticsUserAgentStats(name="Safari", count=15)
        ]
        
        response = AnalyticsUserAgentResponse(
            date_from=1591228800,
            date_to=1591401599,
            stats=stats
        )
        
        assert response.date_from == 1591228800
        assert response.date_to == 1591401599
        assert len(response.stats) == 3
        assert response.stats[0].name == "Chrome"
        assert response.stats[2].count == 15


class TestAnalyticsReadingEnvironmentStats:
    """Test AnalyticsReadingEnvironmentStats model"""
    
    def test_reading_environment_stats_creation(self):
        """Test reading environment stats creation"""
        stats = AnalyticsReadingEnvironmentStats(name="webmail", count=45)
        
        assert stats.name == "webmail"
        assert stats.count == 45
    
    def test_reading_environment_literal_validation(self):
        """Test reading environment name validation"""
        # Valid values
        for env in ["webmail", "mobile", "desktop"]:
            stats = AnalyticsReadingEnvironmentStats(name=env, count=10)
            assert stats.name == env


class TestAnalyticsReadingEnvironmentResponse:
    """Test AnalyticsReadingEnvironmentResponse model"""
    
    def test_reading_environment_response_creation(self):
        """Test reading environment response creation"""
        stats = [
            AnalyticsReadingEnvironmentStats(name="webmail", count=45),
            AnalyticsReadingEnvironmentStats(name="mobile", count=30),
            AnalyticsReadingEnvironmentStats(name="desktop", count=25)
        ]
        
        response = AnalyticsReadingEnvironmentResponse(
            date_from=1591228800,
            date_to=1591401599,
            stats=stats
        )
        
        assert response.date_from == 1591228800
        assert response.date_to == 1591401599
        assert len(response.stats) == 3
        assert response.stats[0].name == "webmail"
        assert response.stats[1].name == "mobile"
        assert response.stats[2].name == "desktop"


class TestAnalyticsModelIntegration:
    """Test integration between analytics models"""
    
    def test_from_api_creation(self):
        """Test creating models from API response data"""
        api_data = {
            "date_from": 1591228800,
            "date_to": 1591401599,
            "tags[]": ["newsletter", "marketing"],
            "event[]": ["sent", "delivered", "opened"]
        }
        
        request = AnalyticsRequest.from_api(api_data)
        
        assert request.date_from == 1591228800
        assert request.date_to == 1591401599
        assert request.tags == ["newsletter", "marketing"]
        assert request.event == ["sent", "delivered", "opened"]
    
    def test_complex_validation_scenarios(self):
        """Test complex validation scenarios"""
        # Test with current timestamp
        current_time = int(time.time())
        future_time = current_time + 3600  # 1 hour later
        
        request = AnalyticsRequest(
            date_from=current_time,
            date_to=future_time,
            event=["sent", "delivered"]
        )
        
        assert request.date_from == current_time
        assert request.date_to == future_time
        
        # Test edge case: exactly 50 recipients
        recipients = [f"recipient-{i}@example.com" for i in range(50)]
        request = AnalyticsRequest(
            date_from=current_time,
            date_to=future_time,
            recipient_id=recipients
        )
        
        assert len(request.recipient_id) == 50
        assert request.recipient_id[0] == "recipient-0@example.com"
        assert request.recipient_id[49] == "recipient-49@example.com" 