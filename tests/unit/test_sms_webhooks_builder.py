"""Tests for SMS Webhooks builder."""

import pytest

from mailersend.builders.sms_webhooks import SmsWebhooksBuilder
from mailersend.models.sms_webhooks import (
    SmsWebhooksListRequest,
    SmsWebhookGetRequest,
    SmsWebhookCreateRequest,
    SmsWebhookUpdateRequest,
    SmsWebhookDeleteRequest,
    SmsWebhookEvent,
)


class TestSmsWebhooksBuilderBasicMethods:
    """Test basic SmsWebhooksBuilder methods."""

    def test_initialization(self):
        """Test SmsWebhooksBuilder initialization."""
        builder = SmsWebhooksBuilder()

        assert builder._sms_number_id is None
        assert builder._sms_webhook_id is None
        assert builder._url is None
        assert builder._name is None
        assert builder._events is None
        assert builder._enabled is None

    def test_sms_number_id_method(self):
        """Test sms_number_id method."""
        builder = SmsWebhooksBuilder()
        result = builder.sms_number_id("sms123")

        assert result is builder  # Method chaining
        assert builder._sms_number_id == "sms123"

    def test_sms_webhook_id_method(self):
        """Test sms_webhook_id method."""
        builder = SmsWebhooksBuilder()
        result = builder.sms_webhook_id("webhook456")

        assert result is builder  # Method chaining
        assert builder._sms_webhook_id == "webhook456"

    def test_url_method(self):
        """Test url method."""
        builder = SmsWebhooksBuilder()
        result = builder.url("https://example.com/webhook")

        assert result is builder  # Method chaining
        assert builder._url == "https://example.com/webhook"

    def test_name_method(self):
        """Test name method."""
        builder = SmsWebhooksBuilder()
        result = builder.name("Test Webhook")

        assert result is builder  # Method chaining
        assert builder._name == "Test Webhook"

    def test_events_method(self):
        """Test events method."""
        builder = SmsWebhooksBuilder()
        events = [SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED]
        result = builder.events(events)

        assert result is builder  # Method chaining
        assert builder._events == events

    def test_add_event_method(self):
        """Test add_event method."""
        builder = SmsWebhooksBuilder()
        result = builder.add_event(SmsWebhookEvent.SMS_SENT)

        assert result is builder  # Method chaining
        assert builder._events == [SmsWebhookEvent.SMS_SENT]

    def test_add_event_multiple(self):
        """Test add_event method with multiple events."""
        builder = SmsWebhooksBuilder()
        builder.add_event(SmsWebhookEvent.SMS_SENT)
        builder.add_event(SmsWebhookEvent.SMS_DELIVERED)
        builder.add_event(SmsWebhookEvent.SMS_FAILED)

        assert len(builder._events) == 3
        assert SmsWebhookEvent.SMS_SENT in builder._events
        assert SmsWebhookEvent.SMS_DELIVERED in builder._events
        assert SmsWebhookEvent.SMS_FAILED in builder._events

    def test_add_event_no_duplicates(self):
        """Test add_event method doesn't add duplicates."""
        builder = SmsWebhooksBuilder()
        builder.add_event(SmsWebhookEvent.SMS_SENT)
        builder.add_event(SmsWebhookEvent.SMS_SENT)  # Same event again

        assert len(builder._events) == 1
        assert builder._events == [SmsWebhookEvent.SMS_SENT]

    def test_enabled_method(self):
        """Test enabled method."""
        builder = SmsWebhooksBuilder()
        result = builder.enabled(True)

        assert result is builder  # Method chaining
        assert builder._enabled is True

        # Test with False
        builder.enabled(False)
        assert builder._enabled is False


class TestSmsWebhooksBuilderChaining:
    """Test method chaining functionality."""

    def test_method_chaining_all_parameters(self):
        """Test chaining all methods together."""
        builder = (
            SmsWebhooksBuilder()
            .sms_number_id("sms123")
            .sms_webhook_id("webhook456")
            .url("https://example.com/webhook")
            .name("Chained Webhook")
            .events([SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED])
            .enabled(True)
        )

        assert builder._sms_number_id == "sms123"
        assert builder._sms_webhook_id == "webhook456"
        assert builder._url == "https://example.com/webhook"
        assert builder._name == "Chained Webhook"
        assert builder._events == [
            SmsWebhookEvent.SMS_SENT,
            SmsWebhookEvent.SMS_DELIVERED,
        ]
        assert builder._enabled is True

    def test_method_chaining_with_add_event(self):
        """Test chaining with add_event method."""
        builder = (
            SmsWebhooksBuilder()
            .sms_number_id("sms789")
            .add_event(SmsWebhookEvent.SMS_SENT)
            .add_event(SmsWebhookEvent.SMS_FAILED)
            .name("Event Chain Webhook")
        )

        assert builder._sms_number_id == "sms789"
        assert len(builder._events) == 2
        assert SmsWebhookEvent.SMS_SENT in builder._events
        assert SmsWebhookEvent.SMS_FAILED in builder._events
        assert builder._name == "Event Chain Webhook"


class TestSmsWebhooksBuilderListRequest:
    """Test build_list_request method."""

    def test_build_list_request_valid(self):
        """Test build_list_request with valid SMS number ID."""
        builder = SmsWebhooksBuilder().sms_number_id("sms123")
        request = builder.build_list_request()

        assert isinstance(request, SmsWebhooksListRequest)
        assert request.query_params.sms_number_id == "sms123"

    def test_build_list_request_without_sms_number_id_raises_error(self):
        """Test build_list_request raises error when SMS number ID is not set."""
        builder = SmsWebhooksBuilder()

        with pytest.raises(
            ValueError, match="SMS number ID is required for list request"
        ):
            builder.build_list_request()

    def test_build_list_request_ignores_other_params(self):
        """Test build_list_request ignores other parameters."""
        builder = (
            SmsWebhooksBuilder()
            .sms_number_id("sms456")
            .sms_webhook_id("webhook123")
            .url("https://example.com/webhook")
            .name("Test Webhook")
        )
        request = builder.build_list_request()

        assert request.query_params.sms_number_id == "sms456"
        assert isinstance(request, SmsWebhooksListRequest)


class TestSmsWebhooksBuilderGetRequest:
    """Test build_get_request method."""

    def test_build_get_request_valid(self):
        """Test build_get_request with valid SMS webhook ID."""
        builder = SmsWebhooksBuilder().sms_webhook_id("webhook123")
        request = builder.build_get_request()

        assert isinstance(request, SmsWebhookGetRequest)
        assert request.sms_webhook_id == "webhook123"

    def test_build_get_request_without_webhook_id_raises_error(self):
        """Test build_get_request raises error when SMS webhook ID is not set."""
        builder = SmsWebhooksBuilder()

        with pytest.raises(
            ValueError, match="SMS webhook ID is required for get request"
        ):
            builder.build_get_request()

    def test_build_get_request_ignores_other_params(self):
        """Test build_get_request ignores other parameters."""
        builder = (
            SmsWebhooksBuilder()
            .sms_webhook_id("webhook456")
            .sms_number_id("sms123")
            .name("Test Webhook")
        )
        request = builder.build_get_request()

        assert request.sms_webhook_id == "webhook456"
        assert isinstance(request, SmsWebhookGetRequest)


class TestSmsWebhooksBuilderCreateRequest:
    """Test build_create_request method."""

    def test_build_create_request_valid(self):
        """Test build_create_request with all required fields."""
        builder = (
            SmsWebhooksBuilder()
            .url("https://example.com/webhook")
            .name("Test Webhook")
            .events([SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED])
            .enabled(True)
            .sms_number_id("sms123")
        )
        request = builder.build_create_request()

        assert isinstance(request, SmsWebhookCreateRequest)
        assert str(request.url) == "https://example.com/webhook"
        assert request.name == "Test Webhook"
        assert request.events == [
            SmsWebhookEvent.SMS_SENT,
            SmsWebhookEvent.SMS_DELIVERED,
        ]
        assert request.enabled is True
        assert request.sms_number_id == "sms123"

    def test_build_create_request_default_enabled(self):
        """Test build_create_request with default enabled value."""
        builder = (
            SmsWebhooksBuilder()
            .url("https://example.com/webhook")
            .name("Default Enabled Webhook")
            .events([SmsWebhookEvent.SMS_FAILED])
            .sms_number_id("sms456")
        )
        request = builder.build_create_request()

        # enabled should be None in builder but default to True in request
        assert builder._enabled is None
        assert request.enabled is True  # Default value from model

    def test_build_create_request_missing_url_raises_error(self):
        """Test build_create_request raises error when URL is not set."""
        builder = (
            SmsWebhooksBuilder()
            .name("Test Webhook")
            .events([SmsWebhookEvent.SMS_SENT])
            .sms_number_id("sms123")
        )

        with pytest.raises(ValueError, match="URL is required for create request"):
            builder.build_create_request()

    def test_build_create_request_missing_name_raises_error(self):
        """Test build_create_request raises error when name is not set."""
        builder = (
            SmsWebhooksBuilder()
            .url("https://example.com/webhook")
            .events([SmsWebhookEvent.SMS_SENT])
            .sms_number_id("sms123")
        )

        with pytest.raises(ValueError, match="Name is required for create request"):
            builder.build_create_request()

    def test_build_create_request_missing_events_raises_error(self):
        """Test build_create_request raises error when events are not set."""
        builder = (
            SmsWebhooksBuilder()
            .url("https://example.com/webhook")
            .name("Test Webhook")
            .sms_number_id("sms123")
        )

        with pytest.raises(
            ValueError, match="Events list is required for create request"
        ):
            builder.build_create_request()

    def test_build_create_request_empty_events_raises_error(self):
        """Test build_create_request raises error when events list is empty."""
        builder = (
            SmsWebhooksBuilder()
            .url("https://example.com/webhook")
            .name("Test Webhook")
            .events([])
            .sms_number_id("sms123")
        )

        with pytest.raises(
            ValueError, match="Events list is required for create request"
        ):
            builder.build_create_request()

    def test_build_create_request_missing_sms_number_id_raises_error(self):
        """Test build_create_request raises error when SMS number ID is not set."""
        builder = (
            SmsWebhooksBuilder()
            .url("https://example.com/webhook")
            .name("Test Webhook")
            .events([SmsWebhookEvent.SMS_SENT])
        )

        with pytest.raises(
            ValueError, match="SMS number ID is required for create request"
        ):
            builder.build_create_request()


class TestSmsWebhooksBuilderUpdateRequest:
    """Test build_update_request method."""

    def test_build_update_request_valid_full(self):
        """Test build_update_request with all fields set."""
        builder = (
            SmsWebhooksBuilder()
            .sms_webhook_id("webhook123")
            .url("https://example.com/updated")
            .name("Updated Webhook")
            .events([SmsWebhookEvent.SMS_DELIVERED])
            .enabled(False)
        )
        request = builder.build_update_request()

        assert isinstance(request, SmsWebhookUpdateRequest)
        assert request.sms_webhook_id == "webhook123"
        assert str(request.url) == "https://example.com/updated"
        assert request.name == "Updated Webhook"
        assert request.events == [SmsWebhookEvent.SMS_DELIVERED]
        assert request.enabled is False

    def test_build_update_request_partial(self):
        """Test build_update_request with only some fields set."""
        builder = (
            SmsWebhooksBuilder()
            .sms_webhook_id("webhook456")
            .name("Partially Updated Webhook")
        )
        request = builder.build_update_request()

        assert isinstance(request, SmsWebhookUpdateRequest)
        assert request.sms_webhook_id == "webhook456"
        assert request.name == "Partially Updated Webhook"
        assert request.url is None
        assert request.events is None
        assert request.enabled is None

    def test_build_update_request_without_webhook_id_raises_error(self):
        """Test build_update_request raises error when SMS webhook ID is not set."""
        builder = SmsWebhooksBuilder().name("Test Webhook")

        with pytest.raises(
            ValueError, match="SMS webhook ID is required for update request"
        ):
            builder.build_update_request()


class TestSmsWebhooksBuilderDeleteRequest:
    """Test build_delete_request method."""

    def test_build_delete_request_valid(self):
        """Test build_delete_request with valid SMS webhook ID."""
        builder = SmsWebhooksBuilder().sms_webhook_id("webhook123")
        request = builder.build_delete_request()

        assert isinstance(request, SmsWebhookDeleteRequest)
        assert request.sms_webhook_id == "webhook123"

    def test_build_delete_request_without_webhook_id_raises_error(self):
        """Test build_delete_request raises error when SMS webhook ID is not set."""
        builder = SmsWebhooksBuilder()

        with pytest.raises(
            ValueError, match="SMS webhook ID is required for delete request"
        ):
            builder.build_delete_request()

    def test_build_delete_request_ignores_other_params(self):
        """Test build_delete_request ignores other parameters."""
        builder = (
            SmsWebhooksBuilder()
            .sms_webhook_id("webhook789")
            .url("https://example.com/webhook")
            .name("To Be Deleted")
            .enabled(True)
        )
        request = builder.build_delete_request()

        assert request.sms_webhook_id == "webhook789"
        assert isinstance(request, SmsWebhookDeleteRequest)


class TestSmsWebhooksBuilderEdgeCases:
    """Test edge cases and special scenarios."""

    def test_builder_state_persistence(self):
        """Test that builder state persists across multiple build calls."""
        builder = (
            SmsWebhooksBuilder()
            .sms_number_id("sms123")
            .sms_webhook_id("webhook456")
            .url("https://example.com/webhook")
            .name("Persistent Webhook")
            .events([SmsWebhookEvent.SMS_SENT])
            .enabled(True)
        )

        # Build list request
        list_request = builder.build_list_request()
        assert list_request.query_params.sms_number_id == "sms123"

        # Build get request - should still work with same builder
        get_request = builder.build_get_request()
        assert get_request.sms_webhook_id == "webhook456"

        # Build create request - should still work with same builder
        create_request = builder.build_create_request()
        assert create_request.name == "Persistent Webhook"

        # Build update request - should still work with same builder
        update_request = builder.build_update_request()
        assert update_request.sms_webhook_id == "webhook456"
        assert update_request.enabled is True

        # Build delete request - should still work with same builder
        delete_request = builder.build_delete_request()
        assert delete_request.sms_webhook_id == "webhook456"

    def test_builder_parameter_override(self):
        """Test that parameters can be overridden."""
        builder = SmsWebhooksBuilder().name("Original Name")

        # Override with different name
        builder.name("New Name")
        create_request = (
            builder.url("https://example.com/webhook")
            .events([SmsWebhookEvent.SMS_SENT])
            .sms_number_id("sms123")
            .build_create_request()
        )

        assert create_request.name == "New Name"

    def test_builder_events_override_vs_add(self):
        """Test the difference between events() and add_event()."""
        builder = SmsWebhooksBuilder()

        # Use add_event to build up events list
        builder.add_event(SmsWebhookEvent.SMS_SENT)
        builder.add_event(SmsWebhookEvent.SMS_DELIVERED)
        assert len(builder._events) == 2

        # Use events() to replace entire list
        builder.events([SmsWebhookEvent.SMS_FAILED])
        assert len(builder._events) == 1
        assert builder._events == [SmsWebhookEvent.SMS_FAILED]

    def test_builder_with_all_events(self):
        """Test builder with all available SMS webhook events."""
        builder = (
            SmsWebhooksBuilder()
            .add_event(SmsWebhookEvent.SMS_SENT)
            .add_event(SmsWebhookEvent.SMS_DELIVERED)
            .add_event(SmsWebhookEvent.SMS_FAILED)
        )

        assert len(builder._events) == 3
        assert SmsWebhookEvent.SMS_SENT in builder._events
        assert SmsWebhookEvent.SMS_DELIVERED in builder._events
        assert SmsWebhookEvent.SMS_FAILED in builder._events

    def test_builder_reuse_for_different_operations(self):
        """Test that same builder can be used for different operations."""
        builder = SmsWebhooksBuilder()

        # Use for list operation
        list_request = builder.sms_number_id("sms123").build_list_request()
        assert list_request.query_params.sms_number_id == "sms123"

        # Modify for create operation
        create_request = (
            builder.url("https://example.com/webhook")
            .name("Reused Builder Webhook")
            .events([SmsWebhookEvent.SMS_SENT])
            .build_create_request()
        )
        assert create_request.name == "Reused Builder Webhook"
        assert create_request.sms_number_id == "sms123"  # Preserved from list operation

        # Use for get operation
        get_request = builder.sms_webhook_id("webhook789").build_get_request()
        assert get_request.sms_webhook_id == "webhook789"

        # Use for update operation
        update_request = builder.enabled(False).build_update_request()
        assert update_request.sms_webhook_id == "webhook789"
        assert update_request.enabled is False

        # Use for delete operation
        delete_request = builder.build_delete_request()
        assert delete_request.sms_webhook_id == "webhook789"

    def test_multiple_calls_to_same_build_method(self):
        """Test that multiple calls to the same build method work correctly."""
        builder = (
            SmsWebhooksBuilder()
            .sms_webhook_id("webhook123")
            .url("https://example.com/webhook")
            .name("Multi-call Webhook")
            .events([SmsWebhookEvent.SMS_DELIVERED])
            .enabled(True)
        )

        # Multiple calls should create separate request instances
        request1 = builder.build_update_request()
        request2 = builder.build_update_request()

        # Both should have same values but be different instances
        assert request1.sms_webhook_id == request2.sms_webhook_id == "webhook123"
        assert request1.name == request2.name == "Multi-call Webhook"
        assert request1 is not request2
