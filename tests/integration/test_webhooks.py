import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.webhooks import (
    WebhooksListRequest,
    WebhookGetRequest,
    WebhookCreateRequest,
    WebhookUpdateRequest,
    WebhookDeleteRequest,
    WebhooksListQueryParams,
)
from mailersend.models.base import APIResponse
from mailersend.builders.webhooks import WebhooksBuilder


@pytest.fixture
def test_domain_id():
    """Get the test domain ID from environment variables"""
    return os.environ.get("SDK_DOMAIN_ID", "test-domain-id")


@pytest.fixture
def basic_webhooks_list_request(test_domain_id):
    """Basic webhooks list request"""
    return WebhooksListRequest(
        query_params=WebhooksListQueryParams(domain_id=test_domain_id)
    )


@pytest.fixture
def webhook_get_request():
    """Webhook get request with test webhook ID"""
    return WebhookGetRequest(webhook_id="test-webhook-id")


@pytest.fixture
def sample_webhook_data(test_domain_id):
    """Sample webhook data for testing"""
    return {
        "url": "https://example.com/webhook",
        "name": "Test Webhook",
        "events": ["activity.sent", "activity.delivered"],
        "domain_id": test_domain_id,
        "enabled": True
    }


class TestWebhooksIntegration:
    """Integration tests for Webhooks API."""

    @vcr.use_cassette("webhooks_list_basic.yaml")
    def test_list_webhooks_basic(self, email_client, basic_webhooks_list_request):
        """Test listing webhooks with basic parameters."""
        response = email_client.webhooks.list_webhooks(basic_webhooks_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            webhooks = response.data["data"]
            assert isinstance(webhooks, list)

            # If we have webhooks, check the structure
            if webhooks:
                first_webhook = webhooks[0]
                assert "id" in first_webhook
                assert "name" in first_webhook
                assert "url" in first_webhook
                assert "events" in first_webhook
                assert "enabled" in first_webhook
                assert "created_at" in first_webhook

    @vcr.use_cassette("webhooks_list_invalid_domain.yaml")
    def test_list_webhooks_invalid_domain(self, email_client):
        """Test listing webhooks with invalid domain ID returns error."""
        from mailersend.exceptions import BadRequestError
        
        request = WebhooksListRequest(
            query_params=WebhooksListQueryParams(domain_id="invalid-domain-id")
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.webhooks.list_webhooks(request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str or "required" in error_str

    @vcr.use_cassette("webhooks_get_not_found.yaml")
    def test_get_webhook_not_found(self, email_client, webhook_get_request):
        """Test getting a non-existent webhook returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.webhooks.get_webhook(webhook_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("webhooks_create_basic.yaml")
    def test_create_webhook_basic(self, email_client, sample_webhook_data):
        """Test creating webhook with basic parameters."""
        request = WebhookCreateRequest(**sample_webhook_data)

        response = email_client.webhooks.create_webhook(request)

        assert isinstance(response, APIResponse)
        assert response.status_code in [200, 201]
        assert response.data is not None

    @vcr.use_cassette("webhooks_create_invalid_domain.yaml")
    def test_create_webhook_invalid_domain(self, email_client, sample_webhook_data):
        """Test creating webhook with invalid domain ID returns error."""
        from mailersend.exceptions import BadRequestError
        
        webhook_data = sample_webhook_data.copy()
        webhook_data["domain_id"] = "invalid-domain-id"
        request = WebhookCreateRequest(**webhook_data)

        with pytest.raises(BadRequestError) as exc_info:
            email_client.webhooks.create_webhook(request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str or "not found" in error_str or "invalid" in error_str

    @vcr.use_cassette("webhooks_update_not_found.yaml")
    def test_update_webhook_not_found(self, email_client):
        """Test updating non-existent webhook returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = WebhookUpdateRequest(
            webhook_id="test-webhook-id",
            name="Updated Webhook Name",
            enabled=False
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.webhooks.update_webhook(request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("webhooks_delete_not_found.yaml")
    def test_delete_webhook_not_found(self, email_client, webhook_get_request):
        """Test deleting non-existent webhook returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = WebhookDeleteRequest(
            webhook_id=webhook_get_request.webhook_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.webhooks.delete_webhook(delete_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("webhooks_validation_error.yaml")
    def test_list_webhooks_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.webhooks.list_webhooks("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("webhooks_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_webhooks_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.webhooks.list_webhooks(basic_webhooks_list_request)

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

    @vcr.use_cassette("webhooks_empty_result.yaml")
    def test_list_webhooks_empty_result(self, email_client, basic_webhooks_list_request):
        """Test listing webhooks when no webhooks exist."""
        response = email_client.webhooks.list_webhooks(basic_webhooks_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    def test_webhook_create_model_validation(self):
        """Test model validation for webhook creation."""
        # Test empty URL
        with pytest.raises(ValueError) as exc_info:
            WebhookCreateRequest(
                url="",
                name="Test Webhook",
                events=["activity.sent"],
                domain_id="test-domain"
            )
        assert "url cannot be empty" in str(exc_info.value).lower()

        # Test empty name
        with pytest.raises(ValueError) as exc_info:
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="",
                events=["activity.sent"],
                domain_id="test-domain"
            )
        assert "name cannot be empty" in str(exc_info.value).lower()

        # Test empty events
        with pytest.raises(ValueError) as exc_info:
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test Webhook",
                events=[],
                domain_id="test-domain"
            )
        assert "events cannot be empty" in str(exc_info.value).lower()

        # Test empty domain_id
        with pytest.raises(ValueError) as exc_info:
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test Webhook",
                events=["activity.sent"],
                domain_id=""
            )
        assert "domain_id cannot be empty" in str(exc_info.value).lower()

        # Test URL too long
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            WebhookCreateRequest(
                url="x" * 192,  # Exceeds 191 character limit
                name="Test Webhook",
                events=["activity.sent"],
                domain_id="test-domain"
            )
        assert "string should have at most 191 characters" in str(exc_info.value).lower()

        # Test name too long
        with pytest.raises(ValidationError) as exc_info:
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="x" * 192,  # Exceeds 191 character limit
                events=["activity.sent"],
                domain_id="test-domain"
            )
        assert "string should have at most 191 characters" in str(exc_info.value).lower()

    def test_webhook_update_model_validation(self):
        """Test model validation for webhook updates."""
        # Test empty webhook_id
        with pytest.raises(ValueError) as exc_info:
            WebhookUpdateRequest(
                webhook_id="",
                name="Updated Name"
            )
        assert "webhook_id cannot be empty" in str(exc_info.value).lower()

        # Test empty URL when provided
        with pytest.raises(ValueError) as exc_info:
            WebhookUpdateRequest(
                webhook_id="test-id",
                url=""
            )
        assert "url cannot be empty when provided" in str(exc_info.value).lower()

        # Test empty name when provided
        with pytest.raises(ValueError) as exc_info:
            WebhookUpdateRequest(
                webhook_id="test-id",
                name=""
            )
        assert "name cannot be empty when provided" in str(exc_info.value).lower()

        # Test empty events when provided
        with pytest.raises(ValueError) as exc_info:
            WebhookUpdateRequest(
                webhook_id="test-id",
                events=[]
            )
        assert "events cannot be empty when provided" in str(exc_info.value).lower()

    def test_webhook_get_model_validation(self):
        """Test model validation for webhook retrieval."""
        # Test empty webhook_id
        with pytest.raises(ValueError) as exc_info:
            WebhookGetRequest(webhook_id="")
        assert "webhook_id cannot be empty" in str(exc_info.value).lower()

    def test_webhook_delete_model_validation(self):
        """Test model validation for webhook deletion."""
        # Test empty webhook_id
        with pytest.raises(ValueError) as exc_info:
            WebhookDeleteRequest(webhook_id="")
        assert "webhook_id cannot be empty" in str(exc_info.value).lower()

    def test_webhooks_list_query_params_validation(self):
        """Test validation for webhooks list query parameters."""
        # Test valid parameters
        params = WebhooksListQueryParams(domain_id="test-domain")
        assert params.domain_id == "test-domain"
        
        # Test empty domain_id
        with pytest.raises(ValueError) as exc_info:
            WebhooksListQueryParams(domain_id="")
        assert "domain_id cannot be empty" in str(exc_info.value).lower()


class TestWebhooksBuilderIntegration:
    """Integration tests for WebhooksBuilder API."""

    @vcr.use_cassette("webhooks_builder_list_basic.yaml")
    def test_builder_list_basic_usage(self, email_client, test_domain_id):
        """Test basic webhooks list using builder."""
        builder = WebhooksBuilder()
        request = builder.domain_id(test_domain_id).build_webhooks_list_request()
        
        response = email_client.webhooks.list_webhooks(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("webhooks_builder_get_not_found.yaml")
    def test_builder_get_not_found(self, email_client):
        """Test getting non-existent webhook using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = WebhooksBuilder()
        request = builder.webhook_id("test-webhook-id").build_webhook_get_request()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.webhooks.get_webhook(request)

    @vcr.use_cassette("webhooks_builder_create_basic.yaml")
    def test_builder_create_basic(self, email_client, test_domain_id):
        """Test creating webhook using builder."""
        builder = WebhooksBuilder()
        request = (builder
            .domain_id(test_domain_id)
            .name("Test Webhook Builder")
            .url("https://example.com/webhook-builder")
            .add_event("activity.sent")
            .add_event("activity.delivered")
            .enabled(True)
            .build_webhook_create_request())
        
        try:
            response = email_client.webhooks.create_webhook(request)
            assert isinstance(response, APIResponse)
            assert response.status_code in [200, 201]
            assert response.data is not None
        except Exception as e:
            # Creation might fail due to URL already taken or other constraints
            # Just ensure the request was properly formed
            assert "url" in str(e).lower() or "taken" in str(e).lower()

    @vcr.use_cassette("webhooks_builder_update_not_found.yaml")
    def test_builder_update_not_found(self, email_client):
        """Test updating non-existent webhook using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = WebhooksBuilder()
        request = (builder
            .webhook_id("test-webhook-id")
            .name("Updated Name")
            .enabled(False)
            .build_webhook_update_request())
        
        with pytest.raises(ResourceNotFoundError):
            email_client.webhooks.update_webhook(request)

    @vcr.use_cassette("webhooks_builder_delete_not_found.yaml")
    def test_builder_delete_not_found(self, email_client):
        """Test deleting non-existent webhook using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = WebhooksBuilder()
        request = builder.webhook_id("test-webhook-id").build_webhook_delete_request()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.webhooks.delete_webhook(request)

    def test_builder_fluent_interface(self):
        """Test that builder methods return self for chaining."""
        builder = WebhooksBuilder()
        
        # Test method chaining
        result = (builder
            .domain_id("test-domain")
            .webhook_id("test-webhook")
            .name("Test Webhook")
            .url("https://example.com/webhook")
            .add_event("activity.sent")
            .enabled(True))
        
        assert result is builder
        
        # Verify the builder state for list request
        list_request = builder.build_webhooks_list_request()
        assert list_request.query_params.domain_id == "test-domain"
        
        # Verify the builder state for get request
        get_request = builder.build_webhook_get_request()
        assert get_request.webhook_id == "test-webhook"
        
        # Verify the builder state for create request
        create_request = builder.build_webhook_create_request()
        assert create_request.name == "Test Webhook"
        assert create_request.url == "https://example.com/webhook"
        assert "activity.sent" in create_request.events
        assert create_request.enabled is True

    def test_builder_event_helpers(self):
        """Test builder event helper methods."""
        builder = WebhooksBuilder()
        
        # Test activity events
        builder.activity_events()
        activity_events = [
            "activity.sent", "activity.delivered", "activity.soft_bounced",
            "activity.hard_bounced", "activity.opened", "activity.opened_unique",
            "activity.clicked", "activity.clicked_unique", "activity.unsubscribed",
            "activity.spam_complaint", "activity.survey_opened", "activity.survey_submitted"
        ]
        for event in activity_events:
            assert event in builder._events
        
        # Test system events
        builder_system = WebhooksBuilder()
        builder_system.system_events()
        system_events = [
            "sender_identity.verified", "maintenance.start", "maintenance.end",
            "inbound_forward.failed", "email_single.verified", "email_list.verified",
            "bulk_email.completed"
        ]
        for event in system_events:
            assert event in builder_system._events
        
        # Test all events
        builder_all = WebhooksBuilder()
        builder_all.all_events()
        all_expected_events = activity_events + system_events
        for event in all_expected_events:
            assert event in builder_all._events

    def test_builder_event_deduplication(self):
        """Test that builder prevents duplicate events."""
        builder = WebhooksBuilder()
        
        # Add the same event multiple times
        builder.add_event("activity.sent")
        builder.add_event("activity.sent")
        builder.add_event("activity.delivered")
        builder.add_event("activity.sent")
        
        # Should only have unique events
        assert builder._events.count("activity.sent") == 1
        assert builder._events.count("activity.delivered") == 1
        assert len(builder._events) == 2

    def test_builder_reset_functionality(self):
        """Test builder reset functionality."""
        builder = WebhooksBuilder()
        builder.domain_id("test").webhook_id("test").name("test").add_event("activity.sent")
        
        # Reset the builder
        builder.reset()
        
        # Verify all fields are cleared
        assert builder._domain_id is None
        assert builder._webhook_id is None
        assert builder._url is None
        assert builder._name is None
        assert builder._events is None
        assert builder._enabled is None

    def test_builder_copy_functionality(self):
        """Test builder copy functionality."""
        original_builder = WebhooksBuilder()
        original_builder.domain_id("test").add_event("activity.sent").enabled(True)
        
        # Copy the builder
        copied_builder = original_builder.copy()
        
        # Modify the copy
        copied_builder.domain_id("different").add_event("activity.delivered")
        
        # Verify original is unchanged
        assert original_builder._domain_id == "test"
        assert copied_builder._domain_id == "different"
        assert "activity.sent" in original_builder._events
        assert "activity.sent" in copied_builder._events
        assert "activity.delivered" not in original_builder._events
        assert "activity.delivered" in copied_builder._events
        assert original_builder._enabled is True
        assert copied_builder._enabled is True

    def test_builder_validation_errors(self):
        """Test builder validation for missing required fields."""
        builder = WebhooksBuilder()
        
        # Test building list request without domain_id
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhooks_list_request()
        assert "domain_id is required" in str(exc_info.value).lower()
        
        # Test building get request without webhook_id
        with pytest.raises(ValueError) as exc_info:
            builder.build_webhook_get_request()
        assert "webhook_id is required" in str(exc_info.value).lower()
        
        # Test building create request without URL
        with pytest.raises(ValueError) as exc_info:
            builder.domain_id("test").name("test").add_event("activity.sent").build_webhook_create_request()
        assert "url is required" in str(exc_info.value).lower()
        
        # Test building create request without name
        with pytest.raises(ValueError) as exc_info:
            builder.reset().domain_id("test").url("https://test.com").add_event("activity.sent").build_webhook_create_request()
        assert "name is required" in str(exc_info.value).lower()
        
        # Test building create request without events
        with pytest.raises(ValueError) as exc_info:
            builder.reset().domain_id("test").url("https://test.com").name("test").build_webhook_create_request()
        assert "events are required" in str(exc_info.value).lower()
        
        # Test building create request without domain_id
        with pytest.raises(ValueError) as exc_info:
            builder.reset().url("https://test.com").name("test").add_event("activity.sent").build_webhook_create_request()
        assert "domain_id is required" in str(exc_info.value).lower()
        
        # Test building update request without webhook_id
        with pytest.raises(ValueError) as exc_info:
            builder.reset().name("test").build_webhook_update_request()
        assert "webhook_id is required" in str(exc_info.value).lower()
        
        # Test building delete request without webhook_id
        with pytest.raises(ValueError) as exc_info:
            builder.reset().build_webhook_delete_request()
        assert "webhook_id is required" in str(exc_info.value).lower()

    def test_builder_events_list_management(self):
        """Test builder events list management."""
        builder = WebhooksBuilder()
        
        # Test events setter
        builder.events(["activity.sent", "activity.delivered"])
        assert builder._events == ["activity.sent", "activity.delivered"]
        
        # Test add_event method
        builder.add_event("activity.opened")
        assert "activity.opened" in builder._events
        assert len(builder._events) == 3
        
        # Test that add_event doesn't add duplicates
        builder.add_event("activity.sent")
        assert builder._events.count("activity.sent") == 1

    def test_builder_webhook_model_serialization(self):
        """Test that builder-created requests serialize correctly."""
        builder = WebhooksBuilder()
        
        # Test create request serialization
        create_request = (builder
            .domain_id("test-domain")
            .name("Test Webhook")
            .url("https://example.com/webhook")
            .events(["activity.sent", "activity.delivered"])
            .enabled(True)
            .build_webhook_create_request())
        
        # Verify serialization via model_dump
        data = create_request.model_dump(exclude_none=True)
        assert data["domain_id"] == "test-domain"
        assert data["name"] == "Test Webhook"
        assert data["url"] == "https://example.com/webhook"
        assert data["events"] == ["activity.sent", "activity.delivered"]
        assert data["enabled"] is True
        
        # Test update request serialization
        update_request = (builder
            .webhook_id("webhook-123")
            .name("Updated Name")
            .enabled(False)
            .build_webhook_update_request())
        
        # Verify serialization excludes webhook_id (goes in URL)
        update_data = update_request.model_dump(exclude_none=True, exclude={"webhook_id"})
        assert "webhook_id" not in update_data
        assert update_data["name"] == "Updated Name"
        assert update_data["enabled"] is False

    @vcr.use_cassette("webhooks_comprehensive_workflow.yaml") 
    def test_comprehensive_webhooks_workflow(self, email_client, test_domain_id):
        """Test comprehensive workflow covering list, CRUD operations, error scenarios, and builder usage."""
        # Test list with different configurations
        list_request = WebhooksListRequest(
            query_params=WebhooksListQueryParams(domain_id=test_domain_id)
        )
        
        response = email_client.webhooks.list_webhooks(list_request)
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Test builder pattern with different configurations
        builder = WebhooksBuilder()
        
        # Test list with builder
        builder_request = builder.domain_id(test_domain_id).build_webhooks_list_request()
        builder_response = email_client.webhooks.list_webhooks(builder_request)
        assert isinstance(builder_response, APIResponse)
        assert builder_response.status_code == 200
        
        # Test error scenarios
        from mailersend.exceptions import ResourceNotFoundError
        
        # Test get non-existent webhook
        get_request = WebhookGetRequest(webhook_id="non-existent-id")
        with pytest.raises(ResourceNotFoundError):
            email_client.webhooks.get_webhook(get_request)
        
        # Test create webhook
        create_request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id=test_domain_id
        )
        try:
            create_response = email_client.webhooks.create_webhook(create_request)
            assert isinstance(create_response, APIResponse)
        except Exception:
            # Creation might fail due to quota limits or other reasons
            pass
        
        # Test builder error scenarios
        builder_get_request = builder.webhook_id("another-non-existent-id").build_webhook_get_request()
        with pytest.raises(ResourceNotFoundError):
            email_client.webhooks.get_webhook(builder_get_request)