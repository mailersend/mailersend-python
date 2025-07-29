import pytest
import os
import time
from datetime import datetime, timedelta
from tests.test_helpers import vcr, email_client

from mailersend.models.activity import ActivityRequest, ActivityQueryParams
from mailersend.models.base import APIResponse
from mailersend.builders.activity import ActivityBuilder, SingleActivityBuilder


@pytest.fixture
def test_domain_id():
    """Get the test domain ID from environment variables"""
    return os.environ.get("SDK_DOMAIN_ID", "test-domain-id")


@pytest.fixture
def base_activity_request(test_domain_id):
    """Basic activity request parameters that are valid for most tests"""
    # Use fixed timestamps for VCR consistency
    # These represent a realistic 24-hour window for testing
    date_from = 1753757734  # Fixed timestamp (now - 12 hours)
    date_to = 1753844134  # Fixed timestamp (now + 12 hours)

    query_params = ActivityQueryParams(
        date_from=date_from, date_to=date_to, page=1, limit=25
    )

    return ActivityRequest(domain_id=test_domain_id, query_params=query_params)


def activity_request_factory(base: ActivityRequest, **overrides) -> ActivityRequest:
    """Create a new ActivityRequest with the same fields, overridden with kwargs"""
    # Extract current values
    domain_id = overrides.get("domain_id", base.domain_id)

    # Build new query params
    query_data = base.query_params.model_dump()
    for key, value in overrides.items():
        if key != "domain_id":  # domain_id is handled separately
            if value is None:
                query_data.pop(key, None)
            else:
                query_data[key] = value

    new_query_params = ActivityQueryParams(**query_data)

    return ActivityRequest(domain_id=domain_id, query_params=new_query_params)


@pytest.fixture(autouse=True)
def inject_common_objects(request, email_client, base_activity_request, test_domain_id):
    if hasattr(request, "cls") and request.cls is not None:
        request.cls.email_client = email_client
        request.cls.base_activity_request = base_activity_request
        request.cls.test_domain_id = test_domain_id
        request.cls.activity_request_factory = staticmethod(activity_request_factory)


class TestActivityGet:
    @vcr.use_cassette("activity_get_basic.yaml")
    def test_get_activities_basic(self):
        """Test getting activities with basic parameters"""
        result = self.email_client.activities.get(self.base_activity_request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200
        assert isinstance(result.headers, dict)

        # Check response structure
        assert "data" in result
        assert isinstance(result["data"], list)

        # Check pagination metadata if present
        if "links" in result:
            assert isinstance(result["links"], dict)
        if "meta" in result:
            assert isinstance(result["meta"], dict)

    @vcr.use_cassette("activity_get_with_pagination.yaml")
    def test_get_activities_with_pagination(self):
        """Test getting activities with pagination parameters"""
        request = self.activity_request_factory(
            self.base_activity_request,
            page=2,
            limit=10,
            date_from=1750862844,
            date_to=1750949244,
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        # Verify pagination was applied
        assert "data" in result
        assert isinstance(result["data"], list)

    @vcr.use_cassette("activity_get_with_events.yaml")
    def test_get_activities_with_event_filter(self):
        """Test getting activities filtered by event types"""
        request = self.activity_request_factory(
            self.base_activity_request,
            event=["sent", "delivered", "opened"],
            date_from=1750862861,
            date_to=1750949261,
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        # Check that activities match the requested event types
        assert "data" in result
        activities = result["data"]

        if activities:  # Only check if there are activities
            for activity in activities:
                assert "type" in activity
                assert activity["type"] in ["sent", "delivered", "opened"]

    @vcr.use_cassette("activity_get_single_event.yaml")
    def test_get_activities_single_event(self):
        """Test getting activities for a single event type"""
        request = self.activity_request_factory(
            self.base_activity_request,
            event=["sent"],
            date_from=1750862870,
            date_to=1750949270,
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        # Check that all activities are of the requested type
        assert "data" in result
        activities = result["data"]

        if activities:  # Only check if there are activities
            for activity in activities:
                assert activity["type"] == "sent"

    @vcr.use_cassette("activity_get_delivery_events.yaml")
    def test_get_activities_delivery_events(self):
        """Test getting activities for delivery-related events"""
        request = self.activity_request_factory(
            self.base_activity_request,
            event=["queued", "sent", "delivered", "soft_bounced", "hard_bounced"],
            date_from=1750862891,
            date_to=1750949291,
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        assert "data" in result
        assert isinstance(result["data"], list)

    @vcr.use_cassette("activity_get_engagement_events.yaml")
    def test_get_activities_engagement_events(self):
        """Test getting activities for engagement-related events"""
        request = self.activity_request_factory(
            self.base_activity_request,
            event=["opened", "clicked", "unsubscribed", "spam_complaints"],
            date_from=1750862891,
            date_to=1750949291,
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        assert "data" in result
        assert isinstance(result["data"], list)

    @vcr.use_cassette("activity_get_with_datetime.yaml")
    def test_get_activities_with_datetime_range(self):
        """Test getting activities using datetime objects"""
        # Use fixed timestamps for VCR consistency
        date_from = 1750927692  # Fixed timestamp
        date_to = 1750949292  # Fixed timestamp (6 hours later)

        request = self.activity_request_factory(
            self.base_activity_request, date_from=date_from, date_to=date_to
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        assert "data" in result

    @vcr.use_cassette("activity_get_max_limit.yaml")
    def test_get_activities_max_limit(self):
        """Test getting activities with maximum allowed limit"""
        request = self.activity_request_factory(
            self.base_activity_request,
            limit=100,  # Maximum allowed limit
            date_from=1750862870,
            date_to=1750949270,
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        assert "data" in result
        activities = result["data"]

        # Should return up to 100 activities
        assert len(activities) <= 100

    @vcr.use_cassette("activity_get_min_limit.yaml")
    def test_get_activities_min_limit(self):
        """Test getting activities with minimum allowed limit"""
        request = self.activity_request_factory(
            self.base_activity_request,
            limit=10,  # Minimum allowed limit
            date_from=1750862892,
            date_to=1750949292,
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        assert "data" in result
        activities = result["data"]

        # Should return up to 10 activities
        assert len(activities) <= 10

    @vcr.use_cassette("activity_get_empty_result.yaml")
    def test_get_activities_empty_result(self):
        """Test getting activities when no activities match the criteria"""
        # Use fixed timestamps for VCR consistency - a narrow time range
        date_from = 1750949232  # Fixed timestamp
        date_to = 1750949292  # Fixed timestamp (1 minute later)

        request = self.activity_request_factory(
            self.base_activity_request,
            date_from=date_from,
            date_to=date_to,
            event=["survey_opened"],  # Rare event type
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200

        assert "data" in result
        # Should return empty list if no activities found
        assert isinstance(result["data"], list)


class TestActivityBuilder:
    @vcr.use_cassette("activity_builder_basic.yaml")
    def test_activity_builder_basic_usage(self):
        """Test using ActivityBuilder to construct requests"""
        # Use fixed timestamps for VCR consistency
        date_from = 1750945671  # Fixed timestamp
        date_to = 1750949271  # Fixed timestamp (1 hour later)

        request = (
            ActivityBuilder()
            .domain_id(self.test_domain_id)
            .date_from(date_from)
            .date_to(date_to)
            .page(1)
            .limit(25)
            .build()
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200
        assert "data" in result

    @vcr.use_cassette("activity_builder_with_events.yaml")
    def test_activity_builder_with_events(self):
        """Test using ActivityBuilder with event filtering"""
        # Use fixed timestamps for VCR consistency
        date_from = 1750942092  # Fixed timestamp
        date_to = 1750949292  # Fixed timestamp (2 hours later)

        request = (
            ActivityBuilder()
            .domain_id(self.test_domain_id)
            .date_from(date_from)
            .date_to(date_to)
            .event("sent")
            .event("delivered")
            .event("opened")
            .limit(50)
            .build()
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200
        assert "data" in result

    @vcr.use_cassette("activity_builder_datetime_conversion.yaml")
    def test_activity_builder_datetime_conversion(self):
        """Test ActivityBuilder automatic datetime to timestamp conversion"""
        # Use fixed datetime objects for VCR consistency
        date_from = datetime.fromtimestamp(1750938493)  # Fixed datetime
        date_to = datetime.fromtimestamp(1750949293)  # Fixed datetime (3 hours later)

        request = (
            ActivityBuilder()
            .domain_id(self.test_domain_id)
            .date_from(date_from)  # Pass datetime object
            .date_to(date_to)  # Pass datetime object
            .build()
        )

        result = self.email_client.activities.get(request)

        assert isinstance(result, APIResponse)
        assert result.success is True
        assert result.status_code == 200
        assert "data" in result

        # Verify the builder converted datetime to timestamps
        assert isinstance(request.query_params.date_from, int)
        assert isinstance(request.query_params.date_to, int)


class TestActivityGetSingle:
    @vcr.use_cassette("activity_get_single_not_found.yaml")
    def test_get_single_activity_not_found_with_builder(self):
        """Test getting a single activity by ID that doesn't exist - generates proper VCR cassette"""
        # Use a non-existent activity ID to demonstrate the model-based approach
        activity_id = "5ee0b166b251345e407c9207"  # This ID likely doesn't exist
        request = SingleActivityBuilder().activity_id(activity_id).build()

        from mailersend.exceptions import ResourceNotFoundError

        with pytest.raises(ResourceNotFoundError):
            self.email_client.activities.get_single(request)

    def test_get_single_activity_validation_error(self):
        """Test that validation errors are raised for invalid input at model level"""
        # Test empty activity_id at model level
        with pytest.raises(ValueError) as exc_info:
            SingleActivityBuilder().activity_id("").build()
        assert "activity_id is required" in str(exc_info.value)
        
        # Test whitespace activity_id at model level  
        with pytest.raises(ValueError) as exc_info:
            SingleActivityBuilder().activity_id("   ").build()
        assert "activity_id cannot be empty" in str(exc_info.value)
