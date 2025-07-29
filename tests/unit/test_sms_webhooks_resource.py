"""Unit tests for SMS Webhooks resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.sms_webhooks import SmsWebhooks
from mailersend.models.base import APIResponse
from mailersend.models.sms_webhooks import (
    SmsWebhooksListRequest,
    SmsWebhooksListQueryParams,
    SmsWebhookGetRequest,
    SmsWebhookCreateRequest,
    SmsWebhookUpdateRequest,
    SmsWebhookDeleteRequest,
    SmsWebhookEvent,
)
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestSmsWebhooks:
    """Test SMS Webhooks resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = SmsWebhooks(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_sms_webhooks_returns_api_response(self):
        """Test list_sms_webhooks method returns APIResponse."""
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms123")
        request = SmsWebhooksListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_webhooks(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_sms_webhooks_with_parameters(self):
        """Test list_sms_webhooks with query parameters."""
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms456")
        request = SmsWebhooksListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_webhooks(request)

        expected_params = {"sms_number_id": "sms456"}
        self.mock_client.request.assert_called_once_with(
            method="GET", endpoint="sms-webhooks", params=expected_params
        )
        assert result == self.mock_api_response

    def test_get_sms_webhook_returns_api_response(self):
        """Test get_sms_webhook method returns APIResponse."""
        request = SmsWebhookGetRequest(sms_webhook_id="webhook123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_sms_webhook(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", endpoint="sms-webhooks/webhook123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_sms_webhook_returns_api_response(self):
        """Test create_sms_webhook method returns APIResponse."""
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED],
            sms_number_id="sms123",
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_sms_webhook(request)

        expected_body = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.sent", "sms.delivered"],
            "enabled": True,
            "sms_number_id": "sms123",
        }
        self.mock_client.request.assert_called_once_with(
            method="POST", endpoint="sms-webhooks", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_sms_webhook_returns_api_response(self):
        """Test update_sms_webhook method returns APIResponse."""
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook123", name="Updated Webhook", enabled=False
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_sms_webhook(request)

        expected_body = {"name": "Updated Webhook", "enabled": False}
        self.mock_client.request.assert_called_once_with(
            method="PUT", endpoint="sms-webhooks/webhook123", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_sms_webhook_returns_api_response(self):
        """Test delete_sms_webhook method returns APIResponse."""
        request = SmsWebhookDeleteRequest(sms_webhook_id="webhook123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_sms_webhook(request)

        self.mock_client.request.assert_called_once_with(
            method="DELETE", endpoint="sms-webhooks/webhook123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)
