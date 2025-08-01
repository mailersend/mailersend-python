"""Unit tests for SMS Webhooks models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_webhooks import (
    SmsWebhookEvent,
    SmsWebhooksListQueryParams,
    SmsWebhooksListRequest,
    SmsWebhookGetRequest,
    SmsWebhookCreateRequest,
    SmsWebhookUpdateRequest,
    SmsWebhookDeleteRequest,
    SmsWebhook,
)


class TestSmsWebhookEvent:
    """Test SmsWebhookEvent enum."""

    def test_event_values(self):
        """Test SmsWebhookEvent enum values."""
        assert SmsWebhookEvent.SMS_SENT == "sms.sent"
        assert SmsWebhookEvent.SMS_DELIVERED == "sms.delivered"
        assert SmsWebhookEvent.SMS_FAILED == "sms.failed"


class TestSmsWebhooksListQueryParams:
    """Test SmsWebhooksListQueryParams model."""

    def test_valid_query_params(self):
        """Test creating valid query parameters."""
        params = SmsWebhooksListQueryParams(sms_number_id="sms123")

        assert params.sms_number_id == "sms123"

    def test_sms_number_id_trimming(self):
        """Test SMS number ID trimming."""
        params = SmsWebhooksListQueryParams(sms_number_id="  sms123  ")
        assert params.sms_number_id == "sms123"

    def test_empty_sms_number_id_validation(self):
        """Test empty SMS number ID validation."""
        with pytest.raises(ValidationError):
            SmsWebhooksListQueryParams(sms_number_id="")

    def test_whitespace_sms_number_id_validation(self):
        """Test whitespace-only SMS number ID validation."""
        with pytest.raises(ValueError, match="sms_number_id cannot be empty"):
            SmsWebhooksListQueryParams(sms_number_id="   ")

    def test_to_query_params(self):
        """Test converting to query parameters."""
        params = SmsWebhooksListQueryParams(sms_number_id="sms456")
        result = params.to_query_params()

        expected = {"sms_number_id": "sms456"}
        assert result == expected


class TestSmsWebhooksListRequest:
    """Test SmsWebhooksListRequest model."""

    def test_valid_request(self):
        """Test creating valid list request."""
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms123")
        request = SmsWebhooksListRequest(query_params=query_params)

        assert request.query_params.sms_number_id == "sms123"

    def test_to_query_params(self):
        """Test converting to query parameters."""
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms789")
        request = SmsWebhooksListRequest(query_params=query_params)

        result = request.to_query_params()
        expected = {"sms_number_id": "sms789"}
        assert result == expected


class TestSmsWebhookGetRequest:
    """Test SmsWebhookGetRequest model."""

    def test_valid_request(self):
        """Test creating valid get request."""
        request = SmsWebhookGetRequest(sms_webhook_id="webhook123")

        assert request.sms_webhook_id == "webhook123"

    def test_id_trimming(self):
        """Test SMS webhook ID trimming."""
        request = SmsWebhookGetRequest(sms_webhook_id="  webhook123  ")
        assert request.sms_webhook_id == "webhook123"

    def test_empty_id_validation(self):
        """Test empty ID validation."""
        with pytest.raises(ValidationError):
            SmsWebhookGetRequest(sms_webhook_id="")

    def test_whitespace_id_validation(self):
        """Test whitespace-only ID validation."""
        with pytest.raises(ValueError, match="SMS webhook ID cannot be empty"):
            SmsWebhookGetRequest(sms_webhook_id="   ")


class TestSmsWebhookCreateRequest:
    """Test SmsWebhookCreateRequest model."""

    def test_valid_request(self):
        """Test creating valid create request."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED],
            sms_number_id="sms123",
        )

        assert str(request.url) == "https://example.com/webhook"
        assert request.name == "Test Webhook"
        assert len(request.events) == 2
        assert request.sms_number_id == "sms123"
        assert request.enabled is True  # Default value

    def test_request_with_enabled_false(self):
        """Test create request with enabled=False."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_FAILED],
            enabled=False,
            sms_number_id="sms123",
        )

        assert request.enabled is False

    def test_name_trimming(self):
        """Test webhook name trimming."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="  Test Webhook  ",
            events=[SmsWebhookEvent.SMS_SENT],
            sms_number_id="sms123",
        )
        assert request.name == "Test Webhook"

    def test_sms_number_id_trimming(self):
        """Test SMS number ID trimming."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_SENT],
            sms_number_id="  sms123  ",
        )
        assert request.sms_number_id == "sms123"

    def test_empty_name_validation(self):
        """Test empty name validation."""
        with pytest.raises(ValidationError):
            SmsWebhookCreateRequest(
                url="https://example.com/webhook",
                name="",
                events=[SmsWebhookEvent.SMS_SENT],
                sms_number_id="sms123",
            )

    def test_empty_sms_number_id_validation(self):
        """Test empty SMS number ID validation."""
        with pytest.raises(ValidationError):
            SmsWebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test Webhook",
                events=[SmsWebhookEvent.SMS_SENT],
                sms_number_id="",
            )

    def test_empty_events_validation(self):
        """Test empty events validation."""
        with pytest.raises(ValidationError):
            SmsWebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test Webhook",
                events=[],
                sms_number_id="sms123",
            )

    def test_to_request_body(self):
        """Test converting to request body."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED],
            enabled=False,
            sms_number_id="sms123",
        )

        body = request.to_request_body()
        expected = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.sent", "sms.delivered"],
            "enabled": False,
            "sms_number_id": "sms123",
        }
        assert body == expected

    def test_to_request_body_default_enabled(self):
        """Test converting to request body with default enabled."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_SENT],
            sms_number_id="sms123",
        )

        body = request.to_request_body()
        expected = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.sent"],
            "enabled": True,
            "sms_number_id": "sms123",
        }
        assert body == expected


class TestSmsWebhookUpdateRequest:
    """Test SmsWebhookUpdateRequest model."""

    def test_valid_request(self):
        """Test creating valid update request."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook123", name="Updated Webhook", enabled=False
        )

        assert request.sms_webhook_id == "webhook123"
        assert request.name == "Updated Webhook"
        assert request.enabled is False
        assert request.url is None
        assert request.events is None

    def test_id_trimming(self):
        """Test SMS webhook ID trimming."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="  webhook123  ", name="Updated Webhook"
        )
        assert request.sms_webhook_id == "webhook123"

    def test_name_trimming(self):
        """Test webhook name trimming."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook123", name="  Updated Webhook  "
        )
        assert request.name == "Updated Webhook"

    def test_empty_id_validation(self):
        """Test empty ID validation."""
        with pytest.raises(ValidationError):
            SmsWebhookUpdateRequest(sms_webhook_id="")

    def test_empty_name_validation(self):
        """Test empty name validation."""
        with pytest.raises(ValidationError):
            SmsWebhookUpdateRequest(sms_webhook_id="webhook123", name="")

    def test_to_request_body_partial(self):
        """Test converting to request body with partial updates."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook123", name="Updated Webhook", enabled=True
        )

        body = request.to_request_body()
        expected = {"name": "Updated Webhook", "enabled": True}
        assert body == expected

    def test_to_request_body_all_fields(self):
        """Test converting to request body with all fields."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook123",
            url="https://new.example.com/webhook",
            name="New Webhook",
            events=[SmsWebhookEvent.SMS_FAILED],
            enabled=False,
        )

        body = request.to_request_body()
        expected = {
            "url": "https://new.example.com/webhook",
            "name": "New Webhook",
            "events": ["sms.failed"],
            "enabled": False,
        }
        assert body == expected


class TestSmsWebhookDeleteRequest:
    """Test SmsWebhookDeleteRequest model."""

    def test_valid_request(self):
        """Test creating valid delete request."""
        request = SmsWebhookDeleteRequest(sms_webhook_id="webhook123")

        assert request.sms_webhook_id == "webhook123"

    def test_id_trimming(self):
        """Test SMS webhook ID trimming."""
        request = SmsWebhookDeleteRequest(sms_webhook_id="  webhook123  ")
        assert request.sms_webhook_id == "webhook123"

    def test_empty_id_validation(self):
        """Test empty ID validation."""
        with pytest.raises(ValidationError):
            SmsWebhookDeleteRequest(sms_webhook_id="")


class TestSmsWebhook:
    """Test SmsWebhook model."""

    def test_valid_webhook(self):
        """Test creating valid SMS webhook."""
        data = {
            "id": "webhook123",
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.sent", "sms.delivered"],
            "enabled": True,
            "sms_number_id": "sms456",
            "signing_secret": "secret123",
            "created_at": "2023-01-01T12:00:00.000000Z",
            "updated_at": "2023-01-02T12:00:00.000000Z",
        }

        webhook = SmsWebhook.model_validate(data)

        assert webhook.id == "webhook123"
        assert webhook.url == "https://example.com/webhook"
        assert webhook.name == "Test Webhook"
        assert webhook.events == ["sms.sent", "sms.delivered"]
        assert webhook.enabled is True
        assert webhook.sms_number_id == "sms456"
        assert webhook.signing_secret == "secret123"
        assert isinstance(webhook.created_at, datetime)
        assert isinstance(webhook.updated_at, datetime)

    def test_webhook_without_optional_fields(self):
        """Test webhook without optional fields."""
        data = {
            "id": "webhook789",
            "url": "https://example.com/webhook",
            "name": "Simple Webhook",
            "events": ["sms.failed"],
            "enabled": False,
            "sms_number_id": "sms789",
            "created_at": "2023-01-01T12:00:00.000000Z",
        }

        webhook = SmsWebhook.model_validate(data)

        assert webhook.signing_secret is None
        assert webhook.updated_at is None
