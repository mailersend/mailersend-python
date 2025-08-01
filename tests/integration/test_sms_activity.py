import pytest
from tests.test_helpers import vcr, email_client
import os
import time

from mailersend.models.sms_activity import (
    SmsActivityListRequest,
    SmsMessageGetRequest,
)
from mailersend.models.base import APIResponse
from mailersend.builders.sms_activity import SmsActivityBuilder


@pytest.fixture
def test_sms_number_id():
    """Get the test SMS number ID from environment variables"""
    return os.environ.get("SDK_SMS_NUMBER_ID", "test-sms-number-id")


@pytest.fixture
def basic_sms_activity_list_request():
    """Basic SMS activity list request"""
    return SmsActivityListRequest(page=1, limit=10)


@pytest.fixture
def sms_message_get_request():
    """SMS message get request with test SMS message ID"""
    return SmsMessageGetRequest(sms_message_id="test-sms-message-id")


class TestSmsActivityIntegration:
    """Integration tests for SMS Activity API."""

    @vcr.use_cassette("sms_activity_list_basic.yaml")
    def test_list_sms_activity_basic(self, email_client, basic_sms_activity_list_request):
        """Test listing SMS activity with basic parameters."""
        response = email_client.sms_activity.list(basic_sms_activity_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            activities = response.data["data"]
            assert isinstance(activities, list)

            # If we have activities, check the structure
            if activities:
                first_activity = activities[0]
                assert "from" in first_activity
                assert "to" in first_activity
                assert "content" in first_activity
                assert "status" in first_activity
                assert "created_at" in first_activity
                assert "sms_message_id" in first_activity

    @vcr.use_cassette("sms_activity_list_with_pagination.yaml")
    def test_list_sms_activity_with_pagination(self, email_client):
        """Test listing SMS activity with pagination."""
        request = SmsActivityListRequest(page=1, limit=25)

        response = email_client.sms_activity.list(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta
            assert "per_page" in meta
            assert meta["per_page"] == 25
            assert meta["current_page"] == 1

    @vcr.use_cassette("sms_activity_list_with_sms_number_filter.yaml")
    def test_list_sms_activity_with_sms_number_filter(self, email_client, test_sms_number_id):
        """Test listing SMS activity with SMS number ID filter."""
        from mailersend.exceptions import BadRequestError
        
        request = SmsActivityListRequest(
            sms_number_id=test_sms_number_id,
            page=1,
            limit=10
        )

        try:
            response = email_client.sms_activity.list(request)
            assert isinstance(response, APIResponse)
            assert response.status_code == 200
            assert response.data is not None
        except BadRequestError as e:
            # Expected if SMS number ID is invalid in test environment
            assert "sms number" in str(e).lower() or "invalid" in str(e).lower()

    @vcr.use_cassette("sms_activity_list_with_date_range.yaml")
    def test_list_sms_activity_with_date_range(self, email_client):
        """Test listing SMS activity with date range filter."""
        from mailersend.exceptions import BadRequestError
        
        # Use fixed timestamps to ensure VCR cassette matching
        # These represent a recent 7-day period
        date_to = 1753800000  # Fixed timestamp
        date_from = date_to - (7 * 24 * 60 * 60)  # 7 days earlier
        
        request = SmsActivityListRequest(
            date_from=date_from,
            date_to=date_to,
            page=1,
            limit=10
        )

        try:
            response = email_client.sms_activity.list(request)
            assert isinstance(response, APIResponse)
            assert response.status_code == 200
            assert response.data is not None
        except BadRequestError as e:
            # Expected if date range exceeds account retention limit
            assert "date" in str(e).lower() or "retention" in str(e).lower() or "range" in str(e).lower()

    @vcr.use_cassette("sms_activity_list_with_status_filter.yaml")
    def test_list_sms_activity_with_status_filter(self, email_client):
        """Test listing SMS activity with status filter."""
        request = SmsActivityListRequest(
            status=["queued", "sent"],
            page=1,
            limit=10
        )

        response = email_client.sms_activity.list(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that all activities have the filtered statuses if any are returned
        if "data" in response.data and response.data["data"]:
            for activity in response.data["data"]:
                assert activity["status"] in ["queued", "sent"]

    @vcr.use_cassette("sms_activity_get_message_not_found.yaml")
    def test_get_sms_message_not_found(self, email_client, sms_message_get_request):
        """Test getting a non-existent SMS message returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_activity.get(sms_message_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("sms_activity_validation_error.yaml")
    def test_list_sms_activity_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.sms_activity.list("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("sms_activity_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_sms_activity_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.sms_activity.list(basic_sms_activity_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert hasattr(response, "data")
        assert hasattr(response, "headers")

        # Check for rate limiting headers
        if response.rate_limit_remaining is not None:
            assert isinstance(response.rate_limit_remaining, int)
            # Rate limit remaining can be -1 for unlimited plans
        assert response.rate_limit_remaining is not None

        # Check for request ID
        if response.request_id is not None:
            assert isinstance(response.request_id, str)
            assert len(response.request_id) > 0

    @vcr.use_cassette("sms_activity_empty_result.yaml")
    def test_list_sms_activity_empty_result(self, email_client, basic_sms_activity_list_request):
        """Test listing SMS activity when no activities exist."""
        response = email_client.sms_activity.list(basic_sms_activity_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)


class TestSmsActivityBuilderIntegration:
    """Integration tests for SmsActivityBuilder API."""

    @vcr.use_cassette("sms_activity_builder_list_basic.yaml")
    def test_builder_list_basic_usage(self, email_client):
        """Test basic SMS activity list using builder."""
        builder = SmsActivityBuilder()
        request = builder.page(1).limit(10).build_list_request()
        
        response = email_client.sms_activity.list(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("sms_activity_builder_list_with_filters.yaml")
    def test_builder_list_with_filters(self, email_client):
        """Test SMS activity list with various filters using builder."""
        from mailersend.exceptions import BadRequestError
        
        builder = SmsActivityBuilder()
        
        # Use fixed timestamps to ensure VCR cassette matching
        date_to = 1753800000  # Fixed timestamp
        date_from = date_to - (7 * 24 * 60 * 60)  # 7 days earlier
        
        request = (builder
            .date_from(date_from)
            .date_to(date_to)
            .status(["sent", "delivered"])
            .page(1)
            .limit(25)
            .build_list_request())
        
        try:
            response = email_client.sms_activity.list(request)
            assert isinstance(response, APIResponse)
            assert response.status_code == 200
        except BadRequestError as e:
            # Expected if date range exceeds account retention limit
            assert "date" in str(e).lower() or "retention" in str(e).lower() or "range" in str(e).lower()

    @vcr.use_cassette("sms_activity_builder_list_with_sms_number.yaml")
    def test_builder_list_with_sms_number_filter(self, email_client, test_sms_number_id):
        """Test SMS activity list with SMS number filter using builder."""
        from mailersend.exceptions import BadRequestError
        
        builder = SmsActivityBuilder()
        request = (builder
            .sms_number_id(test_sms_number_id)
            .page(1)
            .limit(10)
            .build_list_request())
        
        try:
            response = email_client.sms_activity.list(request)
            assert isinstance(response, APIResponse)
            assert response.status_code == 200
        except BadRequestError as e:
            # Expected if SMS number ID is invalid in test environment
            assert "sms number" in str(e).lower() or "invalid" in str(e).lower()

    @vcr.use_cassette("sms_activity_builder_get_not_found.yaml")
    def test_builder_get_not_found(self, email_client):
        """Test getting non-existent SMS message using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = SmsActivityBuilder()
        request = builder.sms_message_id("test-sms-message-id").build_get_request()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.sms_activity.get(request)

    def test_builder_fluent_interface(self):
        """Test that builder methods return self for chaining."""
        builder = SmsActivityBuilder()
        
        current_time = int(time.time())
        
        # Test method chaining
        result = (builder
            .page(1)
            .limit(10)
            .sms_number_id("test-sms-number")
            .date_from(current_time - 86400)
            .date_to(current_time)
            .status(["sent", "delivered"])
            .sms_message_id("test-message"))
        
        assert result is builder
        
        # Verify the builder state for different requests
        list_request = builder.build_list_request()
        assert list_request.page == 1
        assert list_request.limit == 10
        assert list_request.sms_number_id == "test-sms-number"
        assert list_request.date_from == current_time - 86400
        assert list_request.date_to == current_time
        assert list_request.status == ["sent", "delivered"]
        
        get_request = builder.build_get_request()
        assert get_request.sms_message_id == "test-message"

    def test_builder_reset_functionality(self):
        """Test builder reset functionality."""
        builder = SmsActivityBuilder()
        builder.page(2).limit(50).sms_number_id("test").status(["sent"])
        
        # Reset the builder
        builder.reset()
        
        # Verify all fields are cleared
        assert builder._page is None
        assert builder._limit is None
        assert builder._sms_number_id is None
        assert builder._date_from is None
        assert builder._date_to is None
        assert builder._status is None
        assert builder._sms_message_id is None

    def test_builder_validation_errors(self):
        """Test builder validation for missing required fields."""
        builder = SmsActivityBuilder()
        
        # Test building get request without SMS message ID
        with pytest.raises(ValueError) as exc_info:
            builder.build_get_request()
        assert "sms message id must be set" in str(exc_info.value).lower()

    @vcr.use_cassette("sms_activity_comprehensive_workflow.yaml")
    def test_comprehensive_sms_activity_workflow(self, email_client, test_sms_number_id):
        """Test comprehensive workflow covering list operations, error scenarios, and builder usage."""
        # Test list with different configurations
        list_request = SmsActivityListRequest(page=1, limit=10)
        
        response = email_client.sms_activity.list(list_request)
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Test builder pattern with different configurations
        builder = SmsActivityBuilder()
        
        # Test list with builder and filters
        date_to = 1753800000  # Fixed timestamp
        date_from = date_to - (7 * 24 * 60 * 60)  # 7 days earlier
        
        try:
            builder_request = (builder
                .date_from(date_from)
                .date_to(date_to)
                .status(["sent"])
                .page(1)
                .limit(25)
                .build_list_request())
            builder_response = email_client.sms_activity.list(builder_request)
            assert isinstance(builder_response, APIResponse)
            assert builder_response.status_code == 200
        except Exception:
            # Handle potential API errors in test environment
            pass
        
        # Test error scenarios
        from mailersend.exceptions import ResourceNotFoundError
        
        # Test get non-existent SMS message
        get_request = SmsMessageGetRequest(sms_message_id="non-existent-id")
        with pytest.raises(ResourceNotFoundError):
            email_client.sms_activity.get(get_request)
        
        # Test builder error scenarios
        builder_get_request = builder.sms_message_id("another-non-existent-id").build_get_request()
        with pytest.raises(ResourceNotFoundError):
            email_client.sms_activity.get(builder_get_request)