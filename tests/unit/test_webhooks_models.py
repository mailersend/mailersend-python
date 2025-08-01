"""Tests for Webhooks models."""

import pytest
from pydantic import ValidationError

from mailersend.models.webhooks import (
    WebhooksListQueryParams,
    WebhooksListRequest,
    WebhookGetRequest,
    WebhookCreateRequest,
    WebhookUpdateRequest,
    WebhookDeleteRequest,
)


class TestWebhooksListQueryParams:
    """Test WebhooksListQueryParams model."""

    def test_valid_domain_id(self):
        """Test with valid domain ID."""
        query_params = WebhooksListQueryParams(domain_id="domain123")
        assert query_params.domain_id == "domain123"

    def test_domain_id_validation(self):
        """Test domain_id validation."""
        # Empty domain_id
        with pytest.raises(ValidationError, match="domain_id cannot be empty"):
            WebhooksListQueryParams(domain_id="")

        # Whitespace-only domain_id
        with pytest.raises(ValidationError, match="domain_id cannot be empty"):
            WebhooksListQueryParams(domain_id="   ")

    def test_domain_id_trimming(self):
        """Test domain_id is trimmed."""
        query_params = WebhooksListQueryParams(domain_id="  domain123  ")
        assert query_params.domain_id == "domain123"

    def test_to_query_params(self):
        """Test to_query_params method."""
        query_params = WebhooksListQueryParams(domain_id="domain123")
        result = query_params.to_query_params()
        expected = {"domain_id": "domain123"}
        assert result == expected


class TestWebhooksListRequest:
    """Test WebhooksListRequest model."""

    def test_create_request_with_query_params(self):
        """Test creating request with query params object."""
        query_params = WebhooksListQueryParams(domain_id="domain123")
        request = WebhooksListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params object."""
        query_params = WebhooksListQueryParams(domain_id="domain123")
        request = WebhooksListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {"domain_id": "domain123"}
        assert result == expected


class TestWebhookGetRequest:
    """Test WebhookGetRequest model."""

    def test_valid_webhook_id(self):
        """Test with valid webhook ID."""
        request = WebhookGetRequest(webhook_id="webhook123")
        assert request.webhook_id == "webhook123"

    def test_webhook_id_validation(self):
        """Test webhook_id validation."""
        # Empty webhook_id
        with pytest.raises(ValidationError, match="webhook_id cannot be empty"):
            WebhookGetRequest(webhook_id="")

        # Whitespace-only webhook_id
        with pytest.raises(ValidationError, match="webhook_id cannot be empty"):
            WebhookGetRequest(webhook_id="   ")

    def test_webhook_id_trimming(self):
        """Test webhook_id is trimmed."""
        request = WebhookGetRequest(webhook_id="  webhook123  ")
        assert request.webhook_id == "webhook123"


class TestWebhookCreateRequest:
    """Test WebhookCreateRequest model."""

    def test_valid_request(self):
        """Test with valid parameters."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent", "activity.delivered"],
            domain_id="domain123",
        )
        assert request.url == "https://example.com/webhook"
        assert request.name == "Test Webhook"
        assert request.events == ["activity.sent", "activity.delivered"]
        assert request.domain_id == "domain123"
        assert request.enabled is None

    def test_with_enabled_flag(self):
        """Test with enabled flag set."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="domain123",
            enabled=True,
        )
        assert request.enabled is True

    def test_url_validation(self):
        """Test URL validation."""
        # Empty URL
        with pytest.raises(ValidationError, match="url cannot be empty"):
            WebhookCreateRequest(
                url="",
                name="Test Webhook",
                events=["activity.sent"],
                domain_id="domain123",
            )

        # URL too long
        long_url = "https://example.com/" + "x" * 200
        with pytest.raises(ValidationError):
            WebhookCreateRequest(
                url=long_url,
                name="Test Webhook",
                events=["activity.sent"],
                domain_id="domain123",
            )

    def test_url_trimming(self):
        """Test URL is trimmed."""
        request = WebhookCreateRequest(
            url="  https://example.com/webhook  ",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="domain123",
        )
        assert request.url == "https://example.com/webhook"

    def test_name_validation(self):
        """Test name validation."""
        # Empty name
        with pytest.raises(ValidationError, match="name cannot be empty"):
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="",
                events=["activity.sent"],
                domain_id="domain123",
            )

        # Name too long
        long_name = "x" * 200
        with pytest.raises(ValidationError):
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name=long_name,
                events=["activity.sent"],
                domain_id="domain123",
            )

    def test_name_trimming(self):
        """Test name is trimmed."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="  Test Webhook  ",
            events=["activity.sent"],
            domain_id="domain123",
        )
        assert request.name == "Test Webhook"

    def test_events_validation(self):
        """Test events validation."""
        # Empty events
        with pytest.raises(ValidationError, match="events cannot be empty"):
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test Webhook",
                events=[],
                domain_id="domain123",
            )

    def test_domain_id_validation(self):
        """Test domain_id validation."""
        # Empty domain_id
        with pytest.raises(ValidationError, match="domain_id cannot be empty"):
            WebhookCreateRequest(
                url="https://example.com/webhook",
                name="Test Webhook",
                events=["activity.sent"],
                domain_id="",
            )

    def test_domain_id_trimming(self):
        """Test domain_id is trimmed."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="  domain123  ",
        )
        assert request.domain_id == "domain123"


class TestWebhookUpdateRequest:
    """Test WebhookUpdateRequest model."""

    def test_valid_request_minimal(self):
        """Test with minimal valid parameters."""
        request = WebhookUpdateRequest(webhook_id="webhook123")
        assert request.webhook_id == "webhook123"
        assert request.url is None
        assert request.name is None
        assert request.events is None
        assert request.enabled is None

    def test_valid_request_full(self):
        """Test with all parameters."""
        request = WebhookUpdateRequest(
            webhook_id="webhook123",
            url="https://example.com/webhook",
            name="Updated Webhook",
            events=["activity.opened"],
            enabled=False,
        )
        assert request.webhook_id == "webhook123"
        assert request.url == "https://example.com/webhook"
        assert request.name == "Updated Webhook"
        assert request.events == ["activity.opened"]
        assert request.enabled is False

    def test_webhook_id_validation(self):
        """Test webhook_id validation."""
        # Empty webhook_id
        with pytest.raises(ValidationError, match="webhook_id cannot be empty"):
            WebhookUpdateRequest(webhook_id="")

    def test_webhook_id_trimming(self):
        """Test webhook_id is trimmed."""
        request = WebhookUpdateRequest(webhook_id="  webhook123  ")
        assert request.webhook_id == "webhook123"

    def test_url_validation(self):
        """Test URL validation when provided."""
        # Empty URL when provided
        with pytest.raises(ValidationError, match="url cannot be empty when provided"):
            WebhookUpdateRequest(webhook_id="webhook123", url="")

        # URL too long
        long_url = "https://example.com/" + "x" * 200
        with pytest.raises(ValidationError):
            WebhookUpdateRequest(webhook_id="webhook123", url=long_url)

    def test_url_trimming(self):
        """Test URL is trimmed when provided."""
        request = WebhookUpdateRequest(
            webhook_id="webhook123", url="  https://example.com/webhook  "
        )
        assert request.url == "https://example.com/webhook"

    def test_name_validation(self):
        """Test name validation when provided."""
        # Empty name when provided
        with pytest.raises(ValidationError, match="name cannot be empty when provided"):
            WebhookUpdateRequest(webhook_id="webhook123", name="")

        # Name too long
        long_name = "x" * 200
        with pytest.raises(ValidationError):
            WebhookUpdateRequest(webhook_id="webhook123", name=long_name)

    def test_name_trimming(self):
        """Test name is trimmed when provided."""
        request = WebhookUpdateRequest(
            webhook_id="webhook123", name="  Updated Webhook  "
        )
        assert request.name == "Updated Webhook"

    def test_events_validation(self):
        """Test events validation when provided."""
        # Empty events when provided
        with pytest.raises(
            ValidationError, match="events cannot be empty when provided"
        ):
            WebhookUpdateRequest(webhook_id="webhook123", events=[])


class TestWebhookDeleteRequest:
    """Test WebhookDeleteRequest model."""

    def test_valid_webhook_id(self):
        """Test with valid webhook ID."""
        request = WebhookDeleteRequest(webhook_id="webhook123")
        assert request.webhook_id == "webhook123"

    def test_webhook_id_validation(self):
        """Test webhook_id validation."""
        # Empty webhook_id
        with pytest.raises(ValidationError, match="webhook_id cannot be empty"):
            WebhookDeleteRequest(webhook_id="")

        # Whitespace-only webhook_id
        with pytest.raises(ValidationError, match="webhook_id cannot be empty"):
            WebhookDeleteRequest(webhook_id="   ")

    def test_webhook_id_trimming(self):
        """Test webhook_id is trimmed."""
        request = WebhookDeleteRequest(webhook_id="  webhook123  ")
        assert request.webhook_id == "webhook123"
