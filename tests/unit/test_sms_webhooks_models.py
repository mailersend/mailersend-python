"""Tests for SMS Webhooks models."""

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
    SmsWebhooksListResponse,
    SmsWebhookGetResponse,
    SmsWebhookCreateResponse,
    SmsWebhookUpdateResponse,
    SmsWebhookDeleteResponse,
)


class TestSmsWebhookEvent:
    """Test SmsWebhookEvent enum."""
    
    def test_sms_webhook_event_values(self):
        """Test SmsWebhookEvent enum values."""
        assert SmsWebhookEvent.SMS_SENT == "sms.sent"
        assert SmsWebhookEvent.SMS_DELIVERED == "sms.delivered"
        assert SmsWebhookEvent.SMS_FAILED == "sms.failed"


class TestSmsWebhooksListQueryParams:
    """Test SmsWebhooksListQueryParams model."""
    
    def test_sms_webhooks_list_query_params_valid(self):
        """Test SmsWebhooksListQueryParams with valid data."""
        params = SmsWebhooksListQueryParams(sms_number_id="sms123")
        
        assert params.sms_number_id == "sms123"
    
    def test_sms_webhooks_list_query_params_whitespace_strip(self):
        """Test sms_number_id whitespace stripping."""
        params = SmsWebhooksListQueryParams(sms_number_id="  sms456  ")
        assert params.sms_number_id == "sms456"
    
    def test_sms_webhooks_list_query_params_validation_empty(self):
        """Test SmsWebhooksListQueryParams validation with empty SMS number ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsWebhooksListQueryParams(sms_number_id="")
    
    def test_sms_webhooks_list_query_params_validation_missing(self):
        """Test SmsWebhooksListQueryParams validation with missing SMS number ID."""
        with pytest.raises(ValidationError):
            SmsWebhooksListQueryParams()
    
    def test_sms_webhooks_list_query_params_to_query_params(self):
        """Test to_query_params method."""
        params = SmsWebhooksListQueryParams(sms_number_id="sms789")
        result = params.to_query_params()
        
        expected = {"sms_number_id": "sms789"}
        assert result == expected


class TestSmsWebhooksListRequest:
    """Test SmsWebhooksListRequest model."""
    
    def test_sms_webhooks_list_request_valid(self):
        """Test SmsWebhooksListRequest with valid data."""
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms123")
        request = SmsWebhooksListRequest(query_params=query_params)
        
        assert request.query_params == query_params
    
    def test_sms_webhooks_list_request_to_query_params(self):
        """Test to_query_params method."""
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms456")
        request = SmsWebhooksListRequest(query_params=query_params)
        result = request.to_query_params()
        
        expected = {"sms_number_id": "sms456"}
        assert result == expected


class TestSmsWebhookGetRequest:
    """Test SmsWebhookGetRequest model."""
    
    def test_sms_webhook_get_request_valid(self):
        """Test SmsWebhookGetRequest with valid data."""
        request = SmsWebhookGetRequest(sms_webhook_id="webhook123")
        assert request.sms_webhook_id == "webhook123"
    
    def test_sms_webhook_get_request_whitespace_strip(self):
        """Test sms_webhook_id whitespace stripping."""
        request = SmsWebhookGetRequest(sms_webhook_id="  webhook456  ")
        assert request.sms_webhook_id == "webhook456"
    
    def test_sms_webhook_get_request_validation_empty(self):
        """Test SmsWebhookGetRequest validation with empty ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsWebhookGetRequest(sms_webhook_id="")
    
    def test_sms_webhook_get_request_validation_missing(self):
        """Test SmsWebhookGetRequest validation with missing ID."""
        with pytest.raises(ValidationError):
            SmsWebhookGetRequest()


class TestSmsWebhookCreateRequest:
    """Test SmsWebhookCreateRequest model."""
    
    def test_sms_webhook_create_request_valid(self):
        """Test SmsWebhookCreateRequest with valid data."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED],
            enabled=True,
            sms_number_id="sms123"
        )
        
        assert str(request.url) == "https://example.com/webhook"
        assert request.name == "Test Webhook"
        assert request.events == [SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED]
        assert request.enabled is True
        assert request.sms_number_id == "sms123"
    
    def test_sms_webhook_create_request_default_enabled(self):
        """Test SmsWebhookCreateRequest with default enabled value."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_FAILED],
            sms_number_id="sms456"
        )
        
        assert request.enabled is True  # Default value
    
    def test_sms_webhook_create_request_validation_empty_name(self):
        """Test SmsWebhookCreateRequest validation with empty name."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsWebhookCreateRequest(
                url="https://example.com/webhook",
                name="",
                events=[SmsWebhookEvent.SMS_SENT],
                sms_number_id="sms123"
            )
    
    def test_sms_webhook_create_request_validation_empty_events(self):
        """Test SmsWebhookCreateRequest validation with empty events list."""
        with pytest.raises(ValidationError):
            SmsWebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test Webhook",
                events=[],
                sms_number_id="sms123"
            )
    
    def test_sms_webhook_create_request_validation_invalid_url(self):
        """Test SmsWebhookCreateRequest validation with invalid URL."""
        with pytest.raises(ValidationError):
            SmsWebhookCreateRequest(
                url="not-a-url",
                name="Test Webhook",
                events=[SmsWebhookEvent.SMS_SENT],
                sms_number_id="sms123"
            )
    
    def test_sms_webhook_create_request_validation_missing_fields(self):
        """Test SmsWebhookCreateRequest validation with missing required fields."""
        with pytest.raises(ValidationError):
            SmsWebhookCreateRequest()
    
    def test_sms_webhook_create_request_to_request_body(self):
        """Test to_request_body method."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED],
            enabled=False,
            sms_number_id="sms789"
        )
        result = request.to_request_body()
        
        expected = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.sent", "sms.delivered"],
            "enabled": False,
            "sms_number_id": "sms789"
        }
        assert result == expected
    
    def test_sms_webhook_create_request_to_request_body_default_enabled(self):
        """Test to_request_body method with default enabled value."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_FAILED],
            sms_number_id="sms999"
        )
        result = request.to_request_body()
        
        expected = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.failed"],
            "enabled": True,
            "sms_number_id": "sms999"
        }
        assert result == expected


class TestSmsWebhookUpdateRequest:
    """Test SmsWebhookUpdateRequest model."""
    
    def test_sms_webhook_update_request_valid(self):
        """Test SmsWebhookUpdateRequest with valid data."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook123",
            url="https://example.com/new-webhook",
            name="Updated Webhook",
            events=[SmsWebhookEvent.SMS_SENT],
            enabled=False
        )
        
        assert request.sms_webhook_id == "webhook123"
        assert str(request.url) == "https://example.com/new-webhook"
        assert request.name == "Updated Webhook"
        assert request.events == [SmsWebhookEvent.SMS_SENT]
        assert request.enabled is False
    
    def test_sms_webhook_update_request_partial_update(self):
        """Test SmsWebhookUpdateRequest with partial fields."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook456",
            name="New Name Only"
        )
        
        assert request.sms_webhook_id == "webhook456"
        assert request.name == "New Name Only"
        assert request.url is None
        assert request.events is None
        assert request.enabled is None
    
    def test_sms_webhook_update_request_validation_empty_id(self):
        """Test SmsWebhookUpdateRequest validation with empty ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsWebhookUpdateRequest(
                sms_webhook_id="",
                name="Test"
            )
    
    def test_sms_webhook_update_request_validation_missing_id(self):
        """Test SmsWebhookUpdateRequest validation with missing ID."""
        with pytest.raises(ValidationError):
            SmsWebhookUpdateRequest(name="Test")
    
    def test_sms_webhook_update_request_to_request_body_full(self):
        """Test to_request_body method with all fields."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook789",
            url="https://example.com/updated",
            name="Updated Name",
            events=[SmsWebhookEvent.SMS_FAILED, SmsWebhookEvent.SMS_DELIVERED],
            enabled=True
        )
        result = request.to_request_body()
        
        expected = {
            "url": "https://example.com/updated",
            "name": "Updated Name",
            "events": ["sms.failed", "sms.delivered"],
            "enabled": True
        }
        assert result == expected
    
    def test_sms_webhook_update_request_to_request_body_partial(self):
        """Test to_request_body method with partial fields."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook999",
            name="Only Name"
        )
        result = request.to_request_body()
        
        expected = {"name": "Only Name"}
        assert result == expected


class TestSmsWebhookDeleteRequest:
    """Test SmsWebhookDeleteRequest model."""
    
    def test_sms_webhook_delete_request_valid(self):
        """Test SmsWebhookDeleteRequest with valid data."""
        request = SmsWebhookDeleteRequest(sms_webhook_id="webhook123")
        assert request.sms_webhook_id == "webhook123"
    
    def test_sms_webhook_delete_request_validation_empty(self):
        """Test SmsWebhookDeleteRequest validation with empty ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsWebhookDeleteRequest(sms_webhook_id="")
    
    def test_sms_webhook_delete_request_validation_missing(self):
        """Test SmsWebhookDeleteRequest validation with missing ID."""
        with pytest.raises(ValidationError):
            SmsWebhookDeleteRequest()


class TestSmsWebhook:
    """Test SmsWebhook model."""
    
    def test_sms_webhook_creation(self):
        """Test SmsWebhook creation with all fields."""
        data = {
            "id": "webhook123",
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.sent", "sms.delivered"],
            "enabled": True,
            "sms_number_id": "sms456",
            "signing_secret": "secret123",
            "created_at": "2023-01-01T12:00:00.000000Z",
            "updated_at": "2023-01-02T12:00:00.000000Z"
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
    
    def test_sms_webhook_creation_without_optional_fields(self):
        """Test SmsWebhook creation without optional fields."""
        data = {
            "id": "webhook789",
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.failed"],
            "enabled": False,
            "sms_number_id": "sms789",
            "created_at": "2023-01-01T12:00:00.000000Z"
        }
        
        webhook = SmsWebhook.model_validate(data)
        
        assert webhook.id == "webhook789"
        assert webhook.signing_secret is None
        assert webhook.updated_at is None


class TestSmsWebhooksListResponse:
    """Test SmsWebhooksListResponse model."""
    
    def test_sms_webhooks_list_response_creation(self):
        """Test SmsWebhooksListResponse creation."""
        data = {
            "data": [
                {
                    "id": "webhook1",
                    "url": "https://example.com/webhook1",
                    "name": "Webhook 1",
                    "events": ["sms.sent"],
                    "enabled": True,
                    "sms_number_id": "sms123",
                    "created_at": "2023-01-01T12:00:00.000000Z"
                },
                {
                    "id": "webhook2",
                    "url": "https://example.com/webhook2",
                    "name": "Webhook 2",
                    "events": ["sms.delivered", "sms.failed"],
                    "enabled": False,
                    "sms_number_id": "sms456",
                    "created_at": "2023-01-01T13:00:00.000000Z"
                }
            ]
        }
        
        response = SmsWebhooksListResponse.model_validate(data)
        
        assert len(response.data) == 2
        assert all(isinstance(webhook, SmsWebhook) for webhook in response.data)
        assert response.data[0].id == "webhook1"
        assert response.data[1].id == "webhook2"


class TestSmsWebhookGetResponse:
    """Test SmsWebhookGetResponse model."""
    
    def test_sms_webhook_get_response_creation(self):
        """Test SmsWebhookGetResponse creation."""
        data = {
            "data": {
                "id": "webhook123",
                "url": "https://example.com/webhook",
                "name": "Test Webhook",
                "events": ["sms.sent", "sms.delivered"],
                "enabled": True,
                "sms_number_id": "sms789",
                "created_at": "2023-01-01T12:00:00.000000Z"
            }
        }
        
        response = SmsWebhookGetResponse.model_validate(data)
        
        assert isinstance(response.data, SmsWebhook)
        assert response.data.id == "webhook123"


class TestSmsWebhookCreateResponse:
    """Test SmsWebhookCreateResponse model."""
    
    def test_sms_webhook_create_response_creation(self):
        """Test SmsWebhookCreateResponse creation."""
        data = {
            "data": {
                "id": "webhook456",
                "url": "https://example.com/new-webhook",
                "name": "New Webhook",
                "events": ["sms.failed"],
                "enabled": True,
                "sms_number_id": "sms999",
                "signing_secret": "new_secret",
                "created_at": "2023-01-01T12:00:00.000000Z"
            }
        }
        
        response = SmsWebhookCreateResponse.model_validate(data)
        
        assert isinstance(response.data, SmsWebhook)
        assert response.data.id == "webhook456"
        assert response.data.signing_secret == "new_secret"


class TestSmsWebhookUpdateResponse:
    """Test SmsWebhookUpdateResponse model."""
    
    def test_sms_webhook_update_response_creation(self):
        """Test SmsWebhookUpdateResponse creation."""
        data = {
            "data": {
                "id": "webhook789",
                "url": "https://example.com/updated-webhook",
                "name": "Updated Webhook",
                "events": ["sms.sent", "sms.delivered", "sms.failed"],
                "enabled": False,
                "sms_number_id": "sms111",
                "created_at": "2023-01-01T12:00:00.000000Z",
                "updated_at": "2023-01-02T12:00:00.000000Z"
            }
        }
        
        response = SmsWebhookUpdateResponse.model_validate(data)
        
        assert isinstance(response.data, SmsWebhook)
        assert response.data.id == "webhook789"
        assert response.data.enabled is False


class TestSmsWebhookDeleteResponse:
    """Test SmsWebhookDeleteResponse model."""
    
    def test_sms_webhook_delete_response_creation(self):
        """Test SmsWebhookDeleteResponse creation."""
        data = {
            "message": "SMS webhook deleted successfully"
        }
        
        response = SmsWebhookDeleteResponse.model_validate(data)
        
        assert response.message == "SMS webhook deleted successfully"