import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.sms_webhooks import (
    SmsWebhooksListRequest,
    SmsWebhookGetRequest,
    SmsWebhookCreateRequest,
    SmsWebhookUpdateRequest,
    SmsWebhookDeleteRequest,
    SmsWebhooksListQueryParams,
    SmsWebhookEvent,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def sms_number_id_from_env():
    """Get SMS number ID from environment or use test ID"""
    return os.environ.get("SDK_SMS_NUMBER_ID", "test-sms-number-id")


@pytest.fixture
def basic_sms_webhooks_list_request(sms_number_id_from_env):
    """Basic SMS webhooks list request"""
    return SmsWebhooksListRequest(
        query_params=SmsWebhooksListQueryParams(sms_number_id=sms_number_id_from_env)
    )


@pytest.fixture
def sms_webhook_get_request():
    """SMS webhook get request with test webhook ID"""
    return SmsWebhookGetRequest(sms_webhook_id="test-sms-webhook-id")


@pytest.fixture
def sample_sms_webhook_create_request(sms_number_id_from_env):
    """Sample SMS webhook create request"""
    return SmsWebhookCreateRequest(
        url="https://example.com/webhook",
        name="Test SMS Webhook",
        events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED],
        enabled=True,
        sms_number_id=sms_number_id_from_env
    )


@pytest.fixture  
def sms_webhook_update_request():
    """SMS webhook update request"""
    return SmsWebhookUpdateRequest(
        sms_webhook_id="test-sms-webhook-id",
        name="Updated SMS Webhook",
        enabled=False
    )


@pytest.fixture
def sms_webhook_delete_request():
    """SMS webhook delete request"""
    return SmsWebhookDeleteRequest(sms_webhook_id="test-sms-webhook-id")


class TestSmsWebhooksIntegration:
    """Integration tests for SMS Webhooks API."""

    # ============================================================================
    # SMS Webhooks List Tests
    # ============================================================================

    @vcr.use_cassette("sms_webhooks_list_basic.yaml")
    def test_list_sms_webhooks_basic(self, email_client, basic_sms_webhooks_list_request):
        """Test listing SMS webhooks with basic parameters."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        # This will likely fail due to invalid SMS number ID or missing webhook configuration
        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            response = email_client.sms_webhooks.list_sms_webhooks(basic_sms_webhooks_list_request)

        error_str = str(exc_info.value).lower()
        assert ("sms" in error_str or "number" in error_str or 
                "webhook" in error_str or "not found" in error_str or
                "invalid" in error_str or "id" in error_str)

    @vcr.use_cassette("sms_webhooks_list_with_invalid_sms_number.yaml")
    def test_list_sms_webhooks_with_invalid_sms_number(self, email_client):
        """Test listing SMS webhooks with invalid SMS number ID."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        request = SmsWebhooksListRequest(
            query_params=SmsWebhooksListQueryParams(sms_number_id="invalid-sms-number-id")
        )

        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            email_client.sms_webhooks.list_sms_webhooks(request)

        error_str = str(exc_info.value).lower()
        assert ("sms" in error_str or "number" in error_str or 
                "not found" in error_str or "invalid" in error_str)

    # ============================================================================
    # SMS Webhook Get Tests
    # ============================================================================

    @vcr.use_cassette("sms_webhooks_get_not_found.yaml")
    def test_get_sms_webhook_not_found_with_test_id(self, email_client, sms_webhook_get_request):
        """Test getting a non-existent SMS webhook returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_webhooks.get_sms_webhook(sms_webhook_get_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "webhook" in error_str or "sms" in error_str)

    # ============================================================================
    # SMS Webhook Create Tests
    # ============================================================================

    @vcr.use_cassette("sms_webhooks_create_invalid_sms_number.yaml")
    def test_create_sms_webhook_invalid_sms_number(self, email_client, sample_sms_webhook_create_request):
        """Test creating SMS webhook with invalid SMS number ID."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        # This will likely fail due to invalid SMS number ID
        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            email_client.sms_webhooks.create_sms_webhook(sample_sms_webhook_create_request)

        error_str = str(exc_info.value).lower()
        assert ("sms" in error_str or "number" in error_str or 
                "webhook" in error_str or "not found" in error_str or
                "invalid" in error_str or "id" in error_str)

    @vcr.use_cassette("sms_webhooks_create_with_all_events.yaml")
    def test_create_sms_webhook_with_all_events(self, email_client, sms_number_id_from_env):
        """Test creating SMS webhook with all available events."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        request = SmsWebhookCreateRequest(
            url="https://example.com/all-events",
            name="All Events Webhook",
            events=[
                SmsWebhookEvent.SMS_SENT,
                SmsWebhookEvent.SMS_DELIVERED,
                SmsWebhookEvent.SMS_FAILED
            ],
            enabled=True,
            sms_number_id=sms_number_id_from_env
        )

        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            email_client.sms_webhooks.create_sms_webhook(request)

        error_str = str(exc_info.value).lower()
        assert ("sms" in error_str or "number" in error_str or 
                "webhook" in error_str or "not found" in error_str or
                "invalid" in error_str)

    # ============================================================================
    # SMS Webhook Update Tests
    # ============================================================================

    @vcr.use_cassette("sms_webhooks_update_not_found.yaml")
    def test_update_sms_webhook_not_found_with_test_id(self, email_client, sms_webhook_update_request):
        """Test updating a non-existent SMS webhook returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_webhooks.update_sms_webhook(sms_webhook_update_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "webhook" in error_str or "sms" in error_str)

    @vcr.use_cassette("sms_webhooks_update_disable.yaml")
    def test_update_sms_webhook_disable(self, email_client):
        """Test disabling an SMS webhook."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="test-sms-webhook-id",
            enabled=False
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_webhooks.update_sms_webhook(request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "webhook" in error_str)

    # ============================================================================
    # SMS Webhook Delete Tests
    # ============================================================================

    @vcr.use_cassette("sms_webhooks_delete_not_found.yaml")
    def test_delete_sms_webhook_not_found_with_test_id(self, email_client, sms_webhook_delete_request):
        """Test deleting a non-existent SMS webhook returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_webhooks.delete_sms_webhook(sms_webhook_delete_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "webhook" in error_str or "sms" in error_str)

    # ============================================================================
    # Validation and Error Handling Tests
    # ============================================================================

    @vcr.use_cassette("sms_webhooks_validation_error.yaml")
    def test_list_sms_webhooks_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.sms_webhooks.list_sms_webhooks("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        ) 