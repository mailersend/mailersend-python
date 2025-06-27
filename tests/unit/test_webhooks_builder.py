"""Unit tests for webhooks builder."""

import pytest

from mailersend.builders.webhooks import WebhooksBuilder
from mailersend.models.webhooks import (
    WebhookCreateRequest,
    WebhookDeleteRequest,
    WebhookGetRequest,
    WebhookUpdateRequest,
    WebhooksListRequest,
)


class TestWebhooksBuilder:
    """Test WebhooksBuilder class."""
    
    def test_init(self):
        """Test builder initialization."""
        builder = WebhooksBuilder()
        assert builder._domain_id is None
        assert builder._webhook_id is None
        assert builder._url is None
        assert builder._name is None
        assert builder._events is None
        assert builder._enabled is None
    
    def test_domain_id(self):
        """Test setting domain_id."""
        builder = WebhooksBuilder()
        result = builder.domain_id("test_domain")
        assert result is builder  # Fluent interface
        assert builder._domain_id == "test_domain"
    
    def test_webhook_id(self):
        """Test setting webhook_id."""
        builder = WebhooksBuilder()
        result = builder.webhook_id("webhook_123")
        assert result is builder  # Fluent interface
        assert builder._webhook_id == "webhook_123"
    
    def test_url(self):
        """Test setting URL."""
        builder = WebhooksBuilder()
        result = builder.url("https://example.com/webhook")
        assert result is builder  # Fluent interface
        assert builder._url == "https://example.com/webhook"
    
    def test_name(self):
        """Test setting name."""
        builder = WebhooksBuilder()
        result = builder.name("Test Webhook")
        assert result is builder  # Fluent interface
        assert builder._name == "Test Webhook"
    
    def test_events(self):
        """Test setting events list."""
        builder = WebhooksBuilder()
        events = ["activity.sent", "activity.delivered"]
        result = builder.events(events)
        assert result is builder  # Fluent interface
        assert builder._events == events
    
    def test_add_event(self):
        """Test adding single event."""
        builder = WebhooksBuilder()
        result = builder.add_event("activity.sent")
        assert result is builder  # Fluent interface
        assert builder._events == ["activity.sent"]
        
        # Add another event
        builder.add_event("activity.delivered")
        assert builder._events == ["activity.sent", "activity.delivered"]
    
    def test_add_event_no_duplicates(self):
        """Test that adding the same event twice doesn't create duplicates."""
        builder = WebhooksBuilder()
        builder.add_event("activity.sent")
        builder.add_event("activity.sent")
        assert builder._events == ["activity.sent"]
    
    def test_enabled(self):
        """Test setting enabled flag."""
        builder = WebhooksBuilder()
        result = builder.enabled(True)
        assert result is builder  # Fluent interface
        assert builder._enabled is True
        
        builder.enabled(False)
        assert builder._enabled is False
    
    def test_activity_events(self):
        """Test adding all activity events."""
        builder = WebhooksBuilder()
        result = builder.activity_events()
        assert result is builder  # Fluent interface
        
        expected_events = [
            "activity.sent",
            "activity.delivered",
            "activity.soft_bounced",
            "activity.hard_bounced",
            "activity.opened",
            "activity.opened_unique",
            "activity.clicked",
            "activity.clicked_unique",
            "activity.unsubscribed",
            "activity.spam_complaint",
            "activity.survey_opened",
            "activity.survey_submitted",
        ]
        assert builder._events == expected_events
    
    def test_system_events(self):
        """Test adding all system events."""
        builder = WebhooksBuilder()
        result = builder.system_events()
        assert result is builder  # Fluent interface
        
        expected_events = [
            "sender_identity.verified",
            "maintenance.start",
            "maintenance.end",
            "inbound_forward.failed",
            "email_single.verified",
            "email_list.verified",
            "bulk_email.completed",
        ]
        assert builder._events == expected_events
    
    def test_all_events(self):
        """Test adding all available events."""
        builder = WebhooksBuilder()
        result = builder.all_events()
        assert result is builder  # Fluent interface
        
        expected_activity_events = [
            "activity.sent",
            "activity.delivered",
            "activity.soft_bounced",
            "activity.hard_bounced",
            "activity.opened",
            "activity.opened_unique",
            "activity.clicked",
            "activity.clicked_unique",
            "activity.unsubscribed",
            "activity.spam_complaint",
            "activity.survey_opened",
            "activity.survey_submitted",
        ]
        expected_system_events = [
            "sender_identity.verified",
            "maintenance.start",
            "maintenance.end",
            "inbound_forward.failed",
            "email_single.verified",
            "email_list.verified",
            "bulk_email.completed",
        ]
        expected_all_events = expected_activity_events + expected_system_events
        assert builder._events == expected_all_events
    
    def test_method_chaining(self):
        """Test fluent interface method chaining."""
        builder = WebhooksBuilder()
        result = (builder
                  .domain_id("test_domain")
                  .url("https://example.com/webhook")
                  .name("Test Webhook")
                  .add_event("activity.sent")
                  .enabled(True))
        
        assert result is builder
        assert builder._domain_id == "test_domain"
        assert builder._url == "https://example.com/webhook"
        assert builder._name == "Test Webhook"
        assert builder._events == ["activity.sent"]
        assert builder._enabled is True


class TestWebhooksBuilderRequests:
    """Test building different request types."""
    
    def test_build_webhooks_list_request(self):
        """Test building WebhooksListRequest."""
        builder = WebhooksBuilder()
        builder.domain_id("test_domain")
        
        request = builder.build_webhooks_list_request()
        assert isinstance(request, WebhooksListRequest)
        assert request.domain_id == "test_domain"
    
    def test_build_webhooks_list_request_missing_domain_id(self):
        """Test building WebhooksListRequest without domain_id."""
        builder = WebhooksBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhooks_list_request()
        assert "domain_id is required" in str(exc_info.value)
    
    def test_build_webhook_get_request(self):
        """Test building WebhookGetRequest."""
        builder = WebhooksBuilder()
        builder.webhook_id("webhook_123")
        
        request = builder.build_webhook_get_request()
        assert isinstance(request, WebhookGetRequest)
        assert request.webhook_id == "webhook_123"
    
    def test_build_webhook_get_request_missing_webhook_id(self):
        """Test building WebhookGetRequest without webhook_id."""
        builder = WebhooksBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhook_get_request()
        assert "webhook_id is required" in str(exc_info.value)
    
    def test_build_webhook_create_request(self):
        """Test building WebhookCreateRequest."""
        builder = WebhooksBuilder()
        builder.url("https://example.com/webhook")
        builder.name("Test Webhook")
        builder.events(["activity.sent", "activity.delivered"])
        builder.domain_id("test_domain")
        builder.enabled(True)
        
        request = builder.build_webhook_create_request()
        assert isinstance(request, WebhookCreateRequest)
        assert request.url == "https://example.com/webhook"
        assert request.name == "Test Webhook"
        assert request.events == ["activity.sent", "activity.delivered"]
        assert request.domain_id == "test_domain"
        assert request.enabled is True
    
    def test_build_webhook_create_request_optional_enabled(self):
        """Test building WebhookCreateRequest without enabled."""
        builder = WebhooksBuilder()
        builder.url("https://example.com/webhook")
        builder.name("Test Webhook")
        builder.events(["activity.sent"])
        builder.domain_id("test_domain")
        
        request = builder.build_webhook_create_request()
        assert request.enabled is None
    
    def test_build_webhook_create_request_missing_url(self):
        """Test building WebhookCreateRequest without URL."""
        builder = WebhooksBuilder()
        builder.name("Test Webhook")
        builder.events(["activity.sent"])
        builder.domain_id("test_domain")
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhook_create_request()
        assert "url is required" in str(exc_info.value)
    
    def test_build_webhook_create_request_missing_name(self):
        """Test building WebhookCreateRequest without name."""
        builder = WebhooksBuilder()
        builder.url("https://example.com/webhook")
        builder.events(["activity.sent"])
        builder.domain_id("test_domain")
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhook_create_request()
        assert "name is required" in str(exc_info.value)
    
    def test_build_webhook_create_request_missing_events(self):
        """Test building WebhookCreateRequest without events."""
        builder = WebhooksBuilder()
        builder.url("https://example.com/webhook")
        builder.name("Test Webhook")
        builder.domain_id("test_domain")
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhook_create_request()
        assert "events are required" in str(exc_info.value)
    
    def test_build_webhook_create_request_missing_domain_id(self):
        """Test building WebhookCreateRequest without domain_id."""
        builder = WebhooksBuilder()
        builder.url("https://example.com/webhook")
        builder.name("Test Webhook")
        builder.events(["activity.sent"])
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhook_create_request()
        assert "domain_id is required" in str(exc_info.value)
    
    def test_build_webhook_update_request(self):
        """Test building WebhookUpdateRequest."""
        builder = WebhooksBuilder()
        builder.webhook_id("webhook_123")
        builder.url("https://example.com/webhook")
        builder.name("Updated Webhook")
        builder.events(["activity.sent"])
        builder.enabled(False)
        
        request = builder.build_webhook_update_request()
        assert isinstance(request, WebhookUpdateRequest)
        assert request.webhook_id == "webhook_123"
        assert request.url == "https://example.com/webhook"
        assert request.name == "Updated Webhook"
        assert request.events == ["activity.sent"]
        assert request.enabled is False
    
    def test_build_webhook_update_request_minimal(self):
        """Test building WebhookUpdateRequest with only webhook_id."""
        builder = WebhooksBuilder()
        builder.webhook_id("webhook_123")
        
        request = builder.build_webhook_update_request()
        assert isinstance(request, WebhookUpdateRequest)
        assert request.webhook_id == "webhook_123"
        assert request.url is None
        assert request.name is None
        assert request.events is None
        assert request.enabled is None
    
    def test_build_webhook_update_request_missing_webhook_id(self):
        """Test building WebhookUpdateRequest without webhook_id."""
        builder = WebhooksBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhook_update_request()
        assert "webhook_id is required" in str(exc_info.value)
    
    def test_build_webhook_delete_request(self):
        """Test building WebhookDeleteRequest."""
        builder = WebhooksBuilder()
        builder.webhook_id("webhook_123")
        
        request = builder.build_webhook_delete_request()
        assert isinstance(request, WebhookDeleteRequest)
        assert request.webhook_id == "webhook_123"
    
    def test_build_webhook_delete_request_missing_webhook_id(self):
        """Test building WebhookDeleteRequest without webhook_id."""
        builder = WebhooksBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhook_delete_request()
        assert "webhook_id is required" in str(exc_info.value)


class TestWebhooksBuilderStateManagement:
    """Test builder state management."""
    
    def test_reset(self):
        """Test resetting builder state."""
        builder = WebhooksBuilder()
        builder.domain_id("test_domain")
        builder.webhook_id("webhook_123")
        builder.url("https://example.com/webhook")
        builder.name("Test Webhook")
        builder.events(["activity.sent"])
        builder.enabled(True)
        
        result = builder.reset()
        assert result is builder  # Fluent interface
        assert builder._domain_id is None
        assert builder._webhook_id is None
        assert builder._url is None
        assert builder._name is None
        assert builder._events is None
        assert builder._enabled is None
    
    def test_copy(self):
        """Test copying builder state."""
        builder = WebhooksBuilder()
        builder.domain_id("test_domain")
        builder.webhook_id("webhook_123")
        builder.url("https://example.com/webhook")
        builder.name("Test Webhook")
        builder.events(["activity.sent", "activity.delivered"])
        builder.enabled(True)
        
        copy_builder = builder.copy()
        
        # Verify it's a different instance
        assert copy_builder is not builder
        
        # Verify state is copied
        assert copy_builder._domain_id == "test_domain"
        assert copy_builder._webhook_id == "webhook_123"
        assert copy_builder._url == "https://example.com/webhook"
        assert copy_builder._name == "Test Webhook"
        assert copy_builder._events == ["activity.sent", "activity.delivered"]
        assert copy_builder._enabled is True
        
        # Verify events list is a copy, not reference
        copy_builder._events.append("activity.opened")
        assert len(builder._events) == 2  # Original unchanged
        assert len(copy_builder._events) == 3  # Copy modified
    
    def test_copy_empty_builder(self):
        """Test copying an empty builder."""
        builder = WebhooksBuilder()
        copy_builder = builder.copy()
        
        assert copy_builder is not builder
        assert copy_builder._domain_id is None
        assert copy_builder._webhook_id is None
        assert copy_builder._url is None
        assert copy_builder._name is None
        assert copy_builder._events is None
        assert copy_builder._enabled is None
    
    def test_builder_reuse(self):
        """Test reusing builder for multiple requests."""
        builder = WebhooksBuilder()
        builder.domain_id("test_domain")
        
        # Build list request
        list_request = builder.build_webhooks_list_request()
        assert list_request.domain_id == "test_domain"
        
        # Add webhook_id and build get request
        builder.webhook_id("webhook_123")
        get_request = builder.build_webhook_get_request()
        assert get_request.webhook_id == "webhook_123"
        
        # Add more fields and build create request
        builder.url("https://example.com/webhook")
        builder.name("Test Webhook")
        builder.events(["activity.sent"])
        create_request = builder.build_webhook_create_request()
        assert create_request.url == "https://example.com/webhook"
        assert create_request.name == "Test Webhook"
        assert create_request.events == ["activity.sent"]
        assert create_request.domain_id == "test_domain" 