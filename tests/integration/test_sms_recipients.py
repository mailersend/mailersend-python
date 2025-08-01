import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.sms_recipients import (
    SmsRecipientsListRequest,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsRecipientsListQueryParams,
    SmsRecipientStatus,
)
from mailersend.models.base import APIResponse
from mailersend.builders.sms_recipients import SmsRecipientsBuilder


@pytest.fixture
def test_sms_number_id():
    """Get the test SMS number ID from environment variables"""
    return os.environ.get("SDK_SMS_NUMBER_ID", "test-sms-number-id")


@pytest.fixture
def basic_sms_recipients_list_request():
    """Basic SMS recipients list request"""
    return SmsRecipientsListRequest(
        query_params=SmsRecipientsListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def sms_recipient_get_request():
    """SMS recipient get request with test SMS recipient ID"""
    return SmsRecipientGetRequest(sms_recipient_id="test-sms-recipient-id")


class TestSmsRecipientsIntegration:
    """Integration tests for SMS Recipients API."""

    @vcr.use_cassette("sms_recipients_list_basic.yaml")
    def test_list_sms_recipients_basic(self, email_client, basic_sms_recipients_list_request):
        """Test listing SMS recipients with basic parameters."""
        response = email_client.sms_recipients.list_sms_recipients(basic_sms_recipients_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            recipients = response.data["data"]
            assert isinstance(recipients, list)

            # If we have recipients, check the structure
            if recipients:
                first_recipient = recipients[0]
                assert "id" in first_recipient
                assert "number" in first_recipient
                assert "status" in first_recipient
                assert "created_at" in first_recipient

    @vcr.use_cassette("sms_recipients_list_with_pagination.yaml")
    def test_list_sms_recipients_with_pagination(self, email_client):
        """Test listing SMS recipients with pagination."""
        request = SmsRecipientsListRequest(
            query_params=SmsRecipientsListQueryParams(page=1, limit=25)
        )

        response = email_client.sms_recipients.list_sms_recipients(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta
            assert "per_page" in meta
            assert meta["per_page"] == 25
            assert meta["current_page"] == 1

    @vcr.use_cassette("sms_recipients_list_with_status_filter.yaml")
    def test_list_sms_recipients_with_status_filter(self, email_client):
        """Test listing SMS recipients with status filter."""
        request = SmsRecipientsListRequest(
            query_params=SmsRecipientsListQueryParams(
                status=SmsRecipientStatus.ACTIVE,
                page=1,
                limit=10
            )
        )

        response = email_client.sms_recipients.list_sms_recipients(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that all recipients have active status if any are returned
        if "data" in response.data and response.data["data"]:
            for recipient in response.data["data"]:
                assert recipient["status"] == "active"

    @vcr.use_cassette("sms_recipients_list_with_sms_number_filter.yaml")
    def test_list_sms_recipients_with_sms_number_filter(self, email_client, test_sms_number_id):
        """Test listing SMS recipients with SMS number ID filter."""
        from mailersend.exceptions import BadRequestError
        
        request = SmsRecipientsListRequest(
            query_params=SmsRecipientsListQueryParams(
                sms_number_id=test_sms_number_id,
                page=1,
                limit=10
            )
        )

        try:
            response = email_client.sms_recipients.list_sms_recipients(request)
            assert isinstance(response, APIResponse)
            assert response.status_code == 200
            assert response.data is not None
        except BadRequestError as e:
            # Expected if SMS number ID is invalid in test environment
            assert "sms number" in str(e).lower() or "invalid" in str(e).lower()

    @vcr.use_cassette("sms_recipients_get_not_found.yaml")
    def test_get_sms_recipient_not_found(self, email_client, sms_recipient_get_request):
        """Test getting a non-existent SMS recipient returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_recipients.get_sms_recipient(sms_recipient_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("sms_recipients_update_not_found.yaml")
    def test_update_sms_recipient_not_found(self, email_client):
        """Test updating non-existent SMS recipient returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="test-sms-recipient-id",
            status=SmsRecipientStatus.OPT_OUT
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_recipients.update_sms_recipient(request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("sms_recipients_validation_error.yaml")
    def test_list_sms_recipients_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.sms_recipients.list_sms_recipients("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("sms_recipients_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_sms_recipients_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.sms_recipients.list_sms_recipients(basic_sms_recipients_list_request)

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

    @vcr.use_cassette("sms_recipients_empty_result.yaml")
    def test_list_sms_recipients_empty_result(self, email_client, basic_sms_recipients_list_request):
        """Test listing SMS recipients when no recipients exist."""
        response = email_client.sms_recipients.list_sms_recipients(basic_sms_recipients_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)


class TestSmsRecipientsBuilderIntegration:
    """Integration tests for SmsRecipientsBuilder API."""

    @vcr.use_cassette("sms_recipients_builder_list_basic.yaml")
    def test_builder_list_basic_usage(self, email_client):
        """Test basic SMS recipients list using builder."""
        builder = SmsRecipientsBuilder()
        request = builder.page(1).limit(10).build_list_request()
        
        response = email_client.sms_recipients.list_sms_recipients(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("sms_recipients_builder_list_with_status.yaml")
    def test_builder_list_with_status_filter(self, email_client):
        """Test SMS recipients list with status filter using builder."""
        builder = SmsRecipientsBuilder()
        request = (builder
            .status(SmsRecipientStatus.ACTIVE)
            .page(1)
            .limit(25)
            .build_list_request())
        
        response = email_client.sms_recipients.list_sms_recipients(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("sms_recipients_builder_list_with_sms_number.yaml")
    def test_builder_list_with_sms_number_filter(self, email_client, test_sms_number_id):
        """Test SMS recipients list with SMS number filter using builder."""
        from mailersend.exceptions import BadRequestError
        
        builder = SmsRecipientsBuilder()
        request = (builder
            .sms_number_id(test_sms_number_id)
            .page(1)
            .limit(10)
            .build_list_request())
        
        try:
            response = email_client.sms_recipients.list_sms_recipients(request)
            assert isinstance(response, APIResponse)
            assert response.status_code == 200
        except BadRequestError as e:
            # Expected if SMS number ID is invalid in test environment
            assert "sms number" in str(e).lower() or "invalid" in str(e).lower()

    @vcr.use_cassette("sms_recipients_builder_get_not_found.yaml")
    def test_builder_get_not_found(self, email_client):
        """Test getting non-existent SMS recipient using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = SmsRecipientsBuilder()
        request = builder.sms_recipient_id("test-sms-recipient-id").build_get_request()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.sms_recipients.get_sms_recipient(request)

    @vcr.use_cassette("sms_recipients_builder_update_not_found.yaml")
    def test_builder_update_not_found(self, email_client):
        """Test updating non-existent SMS recipient using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = SmsRecipientsBuilder()
        request = builder.sms_recipient_id("test-sms-recipient-id").build_update_request(
            status=SmsRecipientStatus.OPT_OUT
        )
        
        with pytest.raises(ResourceNotFoundError):
            email_client.sms_recipients.update_sms_recipient(request)

    def test_builder_fluent_interface(self):
        """Test that builder methods return self for chaining."""
        builder = SmsRecipientsBuilder()
        
        # Test method chaining
        result = (builder
            .page(1)
            .limit(10)
            .status(SmsRecipientStatus.ACTIVE)
            .sms_number_id("test-sms-number")
            .sms_recipient_id("test-recipient"))
        
        assert result is builder
        
        # Verify the builder state for different requests
        list_request = builder.build_list_request()
        assert list_request.query_params.page == 1
        assert list_request.query_params.limit == 10
        assert list_request.query_params.status == SmsRecipientStatus.ACTIVE
        assert list_request.query_params.sms_number_id == "test-sms-number"
        
        get_request = builder.build_get_request()
        assert get_request.sms_recipient_id == "test-recipient"
        
        update_request = builder.build_update_request(SmsRecipientStatus.OPT_OUT)
        assert update_request.sms_recipient_id == "test-recipient"
        assert update_request.status == SmsRecipientStatus.OPT_OUT

    def test_builder_validation_errors(self):
        """Test builder validation for missing required fields."""
        builder = SmsRecipientsBuilder()
        
        # Test building get request without SMS recipient ID
        with pytest.raises(ValueError) as exc_info:
            builder.build_get_request()
        assert "sms recipient id is required" in str(exc_info.value).lower()
        
        # Test building update request without SMS recipient ID
        with pytest.raises(ValueError) as exc_info:
            builder.build_update_request(SmsRecipientStatus.ACTIVE)
        assert "sms recipient id is required" in str(exc_info.value).lower()

    @vcr.use_cassette("sms_recipients_comprehensive_workflow.yaml")
    def test_comprehensive_sms_recipients_workflow(self, email_client, test_sms_number_id):
        """Test comprehensive workflow covering list operations, error scenarios, and builder usage."""
        # Test list with different configurations
        list_request = SmsRecipientsListRequest(
            query_params=SmsRecipientsListQueryParams(page=1, limit=10)
        )
        
        response = email_client.sms_recipients.list_sms_recipients(list_request)
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Test builder pattern with different configurations
        builder = SmsRecipientsBuilder()
        
        # Test list with builder and filters
        from mailersend.exceptions import BadRequestError
        
        builder_request = (builder
            .status(SmsRecipientStatus.ACTIVE)
            .page(1)
            .limit(25)
            .build_list_request())
        try:
            builder_response = email_client.sms_recipients.list_sms_recipients(builder_request)
            assert isinstance(builder_response, APIResponse)
            assert builder_response.status_code == 200
        except BadRequestError:
            # Handle potential API errors in test environment
            pass
        
        # Test error scenarios
        from mailersend.exceptions import ResourceNotFoundError
        
        # Test get non-existent SMS recipient
        get_request = SmsRecipientGetRequest(sms_recipient_id="non-existent-id")
        with pytest.raises(ResourceNotFoundError):
            email_client.sms_recipients.get_sms_recipient(get_request)
        
        # Test builder error scenarios
        builder_get_request = builder.sms_recipient_id("another-non-existent-id").build_get_request()
        with pytest.raises(ResourceNotFoundError):
            email_client.sms_recipients.get_sms_recipient(builder_get_request)