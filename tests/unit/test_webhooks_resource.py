"""Unit tests for Webhooks resource."""
from unittest.mock import Mock, MagicMock

from mailersend.resources.webhooks import Webhooks
from mailersend.models.base import APIResponse
from mailersend.models.webhooks import (
    WebhooksListQueryParams,
    WebhooksListRequest,
    WebhookGetRequest,
    WebhookCreateRequest,
    WebhookUpdateRequest,
    WebhookDeleteRequest,
)


class TestWebhooks:
    """Test Webhooks resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = Webhooks(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_webhooks_returns_api_response(self):
        """Test list_webhooks method returns APIResponse."""
        query_params = WebhooksListQueryParams(domain_id="domain123")
        request = WebhooksListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_webhooks(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_webhooks_uses_query_params(self):
        """Test list_webhooks method uses query params correctly."""
        query_params = WebhooksListQueryParams(domain_id="domain123")
        request = WebhooksListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_webhooks(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="GET", path="webhooks", params={"domain_id": "domain123"}
        )

        # Verify _create_response was called
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_webhook_returns_api_response(self):
        """Test get_webhook method returns APIResponse."""
        request = WebhookGetRequest(webhook_id="webhook123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_webhook(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_webhook_endpoint_construction(self):
        """Test get_webhook constructs endpoint correctly."""
        request = WebhookGetRequest(webhook_id="webhook123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_webhook(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method="GET", path="webhooks/webhook123"
        )

    def test_create_webhook_returns_api_response(self):
        """Test create_webhook method returns APIResponse."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="domain123",
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_webhook(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_webhook_with_request_body(self):
        """Test create_webhook sends correct request body."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent", "activity.delivered"],
            domain_id="domain123",
            enabled=True,
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_webhook(request)

        expected_body = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["activity.sent", "activity.delivered"],
            "domain_id": "domain123",
            "enabled": True,
        }

        # Verify client was called with correct body
        self.mock_client.request.assert_called_once_with(
            method="POST", path="webhooks", body=expected_body
        )

    def test_update_webhook_returns_api_response(self):
        """Test update_webhook method returns APIResponse."""
        request = WebhookUpdateRequest(webhook_id="webhook123", name="Updated Webhook")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_webhook(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_webhook_with_request_body(self):
        """Test update_webhook sends correct request body."""
        request = WebhookUpdateRequest(
            webhook_id="webhook123",
            url="https://new.example.com/webhook",
            name="Updated Webhook",
            enabled=False,
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_webhook(request)

        expected_body = {
            "url": "https://new.example.com/webhook",
            "name": "Updated Webhook",
            "enabled": False,
        }

        # Verify client was called with correct body and endpoint
        self.mock_client.request.assert_called_once_with(
            method="PUT", path="webhooks/webhook123", body=expected_body
        )

    def test_update_webhook_excludes_webhook_id_from_body(self):
        """Test update_webhook excludes webhook_id from request body."""
        request = WebhookUpdateRequest(webhook_id="webhook123", name="Updated Webhook")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_webhook(request)

        expected_body = {"name": "Updated Webhook"}

        # Verify webhook_id is not in body but is in endpoint
        self.mock_client.request.assert_called_once_with(
            method="PUT", path="webhooks/webhook123", body=expected_body
        )

    def test_delete_webhook_returns_api_response(self):
        """Test delete_webhook method returns APIResponse."""
        request = WebhookDeleteRequest(webhook_id="webhook123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_webhook(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_webhook_endpoint_construction(self):
        """Test delete_webhook constructs endpoint correctly."""
        request = WebhookDeleteRequest(webhook_id="webhook123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_webhook(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="webhooks/webhook123"
        )

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        query_params = WebhooksListQueryParams(domain_id="domain123")
        request_list = WebhooksListRequest(query_params=query_params)
        request_get = WebhookGetRequest(webhook_id="webhook123")
        request_create = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="domain123",
        )
        request_update = WebhookUpdateRequest(webhook_id="webhook123", name="Updated")
        request_delete = WebhookDeleteRequest(webhook_id="webhook123")

        # Test that each method returns the expected APIResponse type
        assert isinstance(
            self.resource.list_webhooks(request_list), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.get_webhook(request_get), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.create_webhook(request_create), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.update_webhook(request_update), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.delete_webhook(request_delete), type(self.mock_api_response)
        )
