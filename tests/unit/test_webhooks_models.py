"""Unit tests for webhooks models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from mailersend.models.webhooks import (
    Webhook,
    WebhookCreateRequest,
    WebhookDeleteRequest,
    WebhookGetRequest,
    WebhookResponse,
    WebhookUpdateRequest,
    WebhooksListRequest,
    WebhooksListResponse,
)


class TestWebhooksListRequest:
    """Test WebhooksListRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid WebhooksListRequest."""
        request = WebhooksListRequest(domain_id="test_domain_123")
        assert request.domain_id == "test_domain_123"
    
    def test_domain_id_required(self):
        """Test that domain_id is required."""
        with pytest.raises(ValidationError) as exc_info:
            WebhooksListRequest()
        assert "domain_id" in str(exc_info.value)
    
    def test_empty_domain_id(self):
        """Test validation with empty domain_id."""
        with pytest.raises(ValidationError) as exc_info:
            WebhooksListRequest(domain_id="")
        assert "domain_id cannot be empty" in str(exc_info.value)
    
    def test_whitespace_domain_id(self):
        """Test validation with whitespace-only domain_id."""
        with pytest.raises(ValidationError) as exc_info:
            WebhooksListRequest(domain_id="   ")
        assert "domain_id cannot be empty" in str(exc_info.value)
    
    def test_domain_id_stripped(self):
        """Test that domain_id is stripped of whitespace."""
        request = WebhooksListRequest(domain_id="  test_domain_123  ")
        assert request.domain_id == "test_domain_123"


class TestWebhookGetRequest:
    """Test WebhookGetRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid WebhookGetRequest."""
        request = WebhookGetRequest(webhook_id="webhook_123")
        assert request.webhook_id == "webhook_123"
    
    def test_webhook_id_required(self):
        """Test that webhook_id is required."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookGetRequest()
        assert "webhook_id" in str(exc_info.value)
    
    def test_empty_webhook_id(self):
        """Test validation with empty webhook_id."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookGetRequest(webhook_id="")
        assert "webhook_id cannot be empty" in str(exc_info.value)
    
    def test_whitespace_webhook_id(self):
        """Test validation with whitespace-only webhook_id."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookGetRequest(webhook_id="   ")
        assert "webhook_id cannot be empty" in str(exc_info.value)
    
    def test_webhook_id_stripped(self):
        """Test that webhook_id is stripped of whitespace."""
        request = WebhookGetRequest(webhook_id="  webhook_123  ")
        assert request.webhook_id == "webhook_123"


class TestWebhookCreateRequest:
    """Test WebhookCreateRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid WebhookCreateRequest."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent", "activity.delivered"],
            domain_id="domain_123",
            enabled=True
        )
        assert request.url == "https://example.com/webhook"
        assert request.name == "Test Webhook"
        assert request.events == ["activity.sent", "activity.delivered"]
        assert request.domain_id == "domain_123"
        assert request.enabled is True
    
    def test_enabled_optional(self):
        """Test that enabled is optional."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="domain_123"
        )
        assert request.enabled is None
    
    def test_required_fields(self):
        """Test that all required fields must be provided."""
        with pytest.raises(ValidationError):
            WebhookCreateRequest()
    
    def test_empty_url(self):
        """Test validation with empty URL."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookCreateRequest(
                url="",
                name="Test",
                events=["activity.sent"],
                domain_id="domain_123"
            )
        assert "url cannot be empty" in str(exc_info.value)
    
    def test_url_too_long(self):
        """Test validation with URL that's too long."""
        long_url = "https://example.com/" + "x" * 200
        with pytest.raises(ValidationError) as exc_info:
            WebhookCreateRequest(
                url=long_url,
                name="Test",
                events=["activity.sent"],
                domain_id="domain_123"
            )
        assert "String should have at most 191 characters" in str(exc_info.value)
    
    def test_empty_name(self):
        """Test validation with empty name."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="",
                events=["activity.sent"],
                domain_id="domain_123"
            )
        assert "name cannot be empty" in str(exc_info.value)
    
    def test_name_too_long(self):
        """Test validation with name that's too long."""
        long_name = "x" * 200
        with pytest.raises(ValidationError) as exc_info:
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name=long_name,
                events=["activity.sent"],
                domain_id="domain_123"
            )
        assert "String should have at most 191 characters" in str(exc_info.value)
    
    def test_empty_events(self):
        """Test validation with empty events list."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test",
                events=[],
                domain_id="domain_123"
            )
        assert "events cannot be empty" in str(exc_info.value)
    
    def test_empty_domain_id(self):
        """Test validation with empty domain_id."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test",
                events=["activity.sent"],
                domain_id=""
            )
        assert "domain_id cannot be empty" in str(exc_info.value)
    
    def test_fields_stripped(self):
        """Test that string fields are stripped of whitespace."""
        request = WebhookCreateRequest(
            url="  https://example.com/webhook  ",
            name="  Test Webhook  ",
            events=["activity.sent"],
            domain_id="  domain_123  "
        )
        assert request.url == "https://example.com/webhook"
        assert request.name == "Test Webhook"
        assert request.domain_id == "domain_123"


class TestWebhookUpdateRequest:
    """Test WebhookUpdateRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid WebhookUpdateRequest."""
        request = WebhookUpdateRequest(
            webhook_id="webhook_123",
            url="https://example.com/webhook",
            name="Updated Webhook",
            events=["activity.sent", "activity.delivered"],
            enabled=False
        )
        assert request.webhook_id == "webhook_123"
        assert request.url == "https://example.com/webhook"
        assert request.name == "Updated Webhook"
        assert request.events == ["activity.sent", "activity.delivered"]
        assert request.enabled is False
    
    def test_webhook_id_required(self):
        """Test that webhook_id is required."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookUpdateRequest()
        assert "webhook_id" in str(exc_info.value)
    
    def test_optional_fields(self):
        """Test that other fields are optional."""
        request = WebhookUpdateRequest(webhook_id="webhook_123")
        assert request.webhook_id == "webhook_123"
        assert request.url is None
        assert request.name is None
        assert request.events is None
        assert request.enabled is None
    
    def test_empty_webhook_id(self):
        """Test validation with empty webhook_id."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookUpdateRequest(webhook_id="")
        assert "webhook_id cannot be empty" in str(exc_info.value)
    
    def test_empty_url_when_provided(self):
        """Test validation with empty URL when provided."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookUpdateRequest(webhook_id="webhook_123", url="")
        assert "url cannot be empty when provided" in str(exc_info.value)
    
    def test_url_too_long_when_provided(self):
        """Test validation with URL that's too long when provided."""
        long_url = "https://example.com/" + "x" * 200
        with pytest.raises(ValidationError) as exc_info:
            WebhookUpdateRequest(webhook_id="webhook_123", url=long_url)
        assert "String should have at most 191 characters" in str(exc_info.value)
    
    def test_empty_name_when_provided(self):
        """Test validation with empty name when provided."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookUpdateRequest(webhook_id="webhook_123", name="")
        assert "name cannot be empty when provided" in str(exc_info.value)
    
    def test_name_too_long_when_provided(self):
        """Test validation with name that's too long when provided."""
        long_name = "x" * 200
        with pytest.raises(ValidationError) as exc_info:
            WebhookUpdateRequest(webhook_id="webhook_123", name=long_name)
        assert "String should have at most 191 characters" in str(exc_info.value)
    
    def test_empty_events_when_provided(self):
        """Test validation with empty events list when provided."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookUpdateRequest(webhook_id="webhook_123", events=[])
        assert "events cannot be empty when provided" in str(exc_info.value)
    
    def test_fields_stripped(self):
        """Test that string fields are stripped of whitespace."""
        request = WebhookUpdateRequest(
            webhook_id="  webhook_123  ",
            url="  https://example.com/webhook  ",
            name="  Updated Webhook  "
        )
        assert request.webhook_id == "webhook_123"
        assert request.url == "https://example.com/webhook"
        assert request.name == "Updated Webhook"


class TestWebhookDeleteRequest:
    """Test WebhookDeleteRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid WebhookDeleteRequest."""
        request = WebhookDeleteRequest(webhook_id="webhook_123")
        assert request.webhook_id == "webhook_123"
    
    def test_webhook_id_required(self):
        """Test that webhook_id is required."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookDeleteRequest()
        assert "webhook_id" in str(exc_info.value)
    
    def test_empty_webhook_id(self):
        """Test validation with empty webhook_id."""
        with pytest.raises(ValidationError) as exc_info:
            WebhookDeleteRequest(webhook_id="")
        assert "webhook_id cannot be empty" in str(exc_info.value)
    
    def test_webhook_id_stripped(self):
        """Test that webhook_id is stripped of whitespace."""
        request = WebhookDeleteRequest(webhook_id="  webhook_123  ")
        assert request.webhook_id == "webhook_123"


class TestWebhook:
    """Test Webhook response model."""
    
    def test_valid_webhook(self):
        """Test creating a valid Webhook."""
        webhook = Webhook(
            id="webhook_123",
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent", "activity.delivered"],
            enabled=True,
            domain_id="domain_123",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            updated_at=datetime(2023, 1, 2, 12, 0, 0)
        )
        assert webhook.id == "webhook_123"
        assert webhook.url == "https://example.com/webhook"
        assert webhook.name == "Test Webhook"
        assert webhook.events == ["activity.sent", "activity.delivered"]
        assert webhook.enabled is True
        assert webhook.domain_id == "domain_123"
        assert webhook.created_at == datetime(2023, 1, 1, 12, 0, 0)
        assert webhook.updated_at == datetime(2023, 1, 2, 12, 0, 0)


class TestWebhooksListResponse:
    """Test WebhooksListResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid WebhooksListResponse."""
        webhook = Webhook(
            id="webhook_123",
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            enabled=True,
            domain_id="domain_123",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            updated_at=datetime(2023, 1, 2, 12, 0, 0)
        )
        response = WebhooksListResponse(data=[webhook])
        assert len(response.data) == 1
        assert response.data[0] == webhook
    
    def test_empty_list(self):
        """Test response with empty webhook list."""
        response = WebhooksListResponse(data=[])
        assert response.data == []


class TestWebhookResponse:
    """Test WebhookResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid WebhookResponse."""
        webhook = Webhook(
            id="webhook_123",
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            enabled=True,
            domain_id="domain_123",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            updated_at=datetime(2023, 1, 2, 12, 0, 0)
        )
        response = WebhookResponse(data=webhook)
        assert response.data == webhook 