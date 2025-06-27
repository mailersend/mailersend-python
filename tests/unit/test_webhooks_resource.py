"""Unit tests for webhooks resource."""

from unittest.mock import Mock, patch

import pytest
from pydantic import ValidationError

from mailersend.models.base import APIResponse
from mailersend.models.webhooks import (
    WebhookCreateRequest,
    WebhookDeleteRequest,
    WebhookGetRequest,
    WebhookUpdateRequest,
    WebhooksListRequest,
)
from mailersend.resources.webhooks import Webhooks


class TestWebhooks:
    """Test Webhooks resource class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
    
    def test_init(self):
        """Test Webhooks resource initialization."""
        assert self.webhooks.client is self.client


class TestWebhooksListWebhooks:
    """Test list_webhooks method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
        self.mock_response = Mock(spec=APIResponse)
        self.client.request.return_value = self.mock_response
    
    def test_list_webhooks_success(self):
        """Test successful webhook listing."""
        request = WebhooksListRequest(domain_id="test_domain")
        
        result = self.webhooks.list_webhooks(request)
        
        assert result is self.mock_response
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="webhooks",
            params={"domain_id": "test_domain"}
        )
    
    def test_list_webhooks_validation_error(self):
        """Test handling of validation errors."""
        with pytest.raises(ValidationError):
            WebhooksListRequest(domain_id="")  # Invalid empty domain_id


class TestWebhooksGetWebhook:
    """Test get_webhook method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
        self.mock_response = Mock(spec=APIResponse)
        self.client.request.return_value = self.mock_response
    
    def test_get_webhook_success(self):
        """Test successful webhook retrieval."""
        request = WebhookGetRequest(webhook_id="webhook_123")
        
        result = self.webhooks.get_webhook(request)
        
        assert result is self.mock_response
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="webhooks/webhook_123"
        )
    
    def test_get_webhook_validation_error(self):
        """Test handling of validation errors."""
        with pytest.raises(ValidationError):
            WebhookGetRequest(webhook_id="")  # Invalid empty webhook_id


class TestWebhooksCreateWebhook:
    """Test create_webhook method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
        self.mock_response = Mock(spec=APIResponse)
        self.client.request.return_value = self.mock_response
    
    def test_create_webhook_success(self):
        """Test successful webhook creation."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent", "activity.delivered"],
            domain_id="test_domain",
            enabled=True
        )
        
        result = self.webhooks.create_webhook(request)
        
        assert result is self.mock_response
        expected_data = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["activity.sent", "activity.delivered"],
            "domain_id": "test_domain",
            "enabled": True
        }
        self.client.request.assert_called_once_with(
            method="POST",
            endpoint="webhooks",
            json=expected_data
        )
    
    def test_create_webhook_without_enabled(self):
        """Test webhook creation without enabled field."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="test_domain"
        )
        
        result = self.webhooks.create_webhook(request)
        
        assert result is self.mock_response
        expected_data = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["activity.sent"],
            "domain_id": "test_domain"
        }
        self.client.request.assert_called_once_with(
            method="POST",
            endpoint="webhooks",
            json=expected_data
        )
    
    def test_create_webhook_validation_error(self):
        """Test handling of validation errors."""
        with pytest.raises(ValidationError):
            WebhookCreateRequest(
                url="",  # Invalid empty url
                name="Test",
                events=["activity.sent"],
                domain_id="domain_123"
            )


class TestWebhooksUpdateWebhook:
    """Test update_webhook method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
        self.mock_response = Mock(spec=APIResponse)
        self.client.request.return_value = self.mock_response
    
    def test_update_webhook_success(self):
        """Test successful webhook update."""
        request = WebhookUpdateRequest(
            webhook_id="webhook_123",
            url="https://example.com/webhook",
            name="Updated Webhook",
            events=["activity.sent"],
            enabled=False
        )
        
        result = self.webhooks.update_webhook(request)
        
        assert result is self.mock_response
        expected_data = {
            "url": "https://example.com/webhook",
            "name": "Updated Webhook",
            "events": ["activity.sent"],
            "enabled": False
        }
        self.client.request.assert_called_once_with(
            method="PUT",
            endpoint="webhooks/webhook_123",
            json=expected_data
        )
    
    def test_update_webhook_partial(self):
        """Test partial webhook update."""
        request = WebhookUpdateRequest(
            webhook_id="webhook_123",
            name="Updated Name"
        )
        
        result = self.webhooks.update_webhook(request)
        
        assert result is self.mock_response
        expected_data = {
            "name": "Updated Name"
        }
        self.client.request.assert_called_once_with(
            method="PUT",
            endpoint="webhooks/webhook_123",
            json=expected_data
        )
    
    def test_update_webhook_minimal(self):
        """Test minimal webhook update (only webhook_id)."""
        request = WebhookUpdateRequest(webhook_id="webhook_123")
        
        result = self.webhooks.update_webhook(request)
        
        assert result is self.mock_response
        self.client.request.assert_called_once_with(
            method="PUT",
            endpoint="webhooks/webhook_123",
            json={}
        )
    
    def test_update_webhook_validation_error(self):
        """Test handling of validation errors."""
        with pytest.raises(ValidationError):
            WebhookUpdateRequest(webhook_id="")  # Invalid empty webhook_id


class TestWebhooksDeleteWebhook:
    """Test delete_webhook method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
        self.mock_response = Mock(spec=APIResponse)
        self.client.request.return_value = self.mock_response
    
    def test_delete_webhook_success(self):
        """Test successful webhook deletion."""
        request = WebhookDeleteRequest(webhook_id="webhook_123")
        
        result = self.webhooks.delete_webhook(request)
        
        assert result is self.mock_response
        self.client.request.assert_called_once_with(
            method="DELETE",
            endpoint="webhooks/webhook_123"
        )
    
    def test_delete_webhook_validation_error(self):
        """Test handling of validation errors."""
        with pytest.raises(ValidationError):
            WebhookDeleteRequest(webhook_id="")  # Invalid empty webhook_id


class TestWebhooksLogging:
    """Test logging behavior."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
        self.mock_response = Mock(spec=APIResponse)
        self.client.request.return_value = self.mock_response
    
    def test_list_webhooks_logs_info(self):
        """Test that list_webhooks logs info message."""
        request = WebhooksListRequest(domain_id="test_domain")
        
        with patch("mailersend.resources.webhooks.logger") as mock_logger:
            self.webhooks.list_webhooks(request)
            mock_logger.info.assert_called_once_with(
                "Listing webhooks for domain: %s", "test_domain"
            )
    
    def test_get_webhook_logs_info(self):
        """Test that get_webhook logs info message."""
        request = WebhookGetRequest(webhook_id="webhook_123")
        
        with patch("mailersend.resources.webhooks.logger") as mock_logger:
            self.webhooks.get_webhook(request)
            mock_logger.info.assert_called_once_with(
                "Getting webhook: %s", "webhook_123"
            )
    
    def test_create_webhook_logs_info(self):
        """Test that create_webhook logs info message."""
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="test_domain"
        )
        
        with patch("mailersend.resources.webhooks.logger") as mock_logger:
            self.webhooks.create_webhook(request)
            mock_logger.info.assert_called_once_with(
                "Creating webhook: %s", "Test Webhook"
            )
    
    def test_update_webhook_logs_info(self):
        """Test that update_webhook logs info message."""
        request = WebhookUpdateRequest(webhook_id="webhook_123")
        
        with patch("mailersend.resources.webhooks.logger") as mock_logger:
            self.webhooks.update_webhook(request)
            mock_logger.info.assert_called_once_with(
                "Updating webhook: %s", "webhook_123"
            )
    
    def test_delete_webhook_logs_info(self):
        """Test that delete_webhook logs info message."""
        request = WebhookDeleteRequest(webhook_id="webhook_123")
        
        with patch("mailersend.resources.webhooks.logger") as mock_logger:
            self.webhooks.delete_webhook(request)
            mock_logger.info.assert_called_once_with(
                "Deleting webhook: %s", "webhook_123"
            )
    
    def test_validation_error_logs_error(self):
        """Test that validation errors are raised for invalid requests."""
        with pytest.raises(ValidationError):
            WebhooksListRequest(domain_id="")  # Invalid empty domain_id 