"""Tests for SMS Webhooks resource."""

import pytest
from unittest.mock import Mock, patch

from mailersend.resources.sms_webhooks import SmsWebhooks
from mailersend.models.sms_webhooks import (
    SmsWebhooksListRequest,
    SmsWebhooksListQueryParams,
    SmsWebhookGetRequest,
    SmsWebhookCreateRequest,
    SmsWebhookUpdateRequest,
    SmsWebhookDeleteRequest,
    SmsWebhookEvent
)
from mailersend.models.base import APIResponse


class TestSmsWebhooksResource:
    """Test cases for SmsWebhooks resource."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()
    
    @pytest.fixture
    def sms_webhooks_resource(self, mock_client):
        """Create a SmsWebhooks resource with mock client."""
        return SmsWebhooks(mock_client)

    def test_list_sms_webhooks_basic(self, sms_webhooks_resource, mock_client):
        """Test list_sms_webhooks basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms123")
        request = SmsWebhooksListRequest(query_params=query_params)
        result = sms_webhooks_resource.list_sms_webhooks(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-webhooks",
            params={"sms_number_id": "sms123"}
        )
        sms_webhooks_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_webhooks_resource._create_response.return_value))

    def test_list_sms_webhooks_logging(self, sms_webhooks_resource, mock_client):
        """Test list_sms_webhooks logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_webhooks_resource.logger = Mock()  # Mock the instance logger
        
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms456")
        request = SmsWebhooksListRequest(query_params=query_params)
        sms_webhooks_resource.list_sms_webhooks(request)

        # Check that logging was called correctly
        sms_webhooks_resource.logger.info.assert_called_once_with(
            "Listing SMS webhooks for SMS number: sms456"
        )

    def test_get_sms_webhook_basic(self, sms_webhooks_resource, mock_client):
        """Test get_sms_webhook basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook123"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsWebhookGetRequest(sms_webhook_id="webhook123")
        result = sms_webhooks_resource.get_sms_webhook(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-webhooks/webhook123"
        )
        sms_webhooks_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_webhooks_resource._create_response.return_value))

    def test_get_sms_webhook_logging(self, sms_webhooks_resource, mock_client):
        """Test get_sms_webhook logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook456"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_webhooks_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsWebhookGetRequest(sms_webhook_id="webhook456")
        sms_webhooks_resource.get_sms_webhook(request)

        # Check that logging was called correctly
        sms_webhooks_resource.logger.info.assert_called_once_with(
            "Getting SMS webhook: webhook456"
        )

    def test_create_sms_webhook_basic(self, sms_webhooks_resource, mock_client):
        """Test create_sms_webhook basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook789"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED],
            enabled=True,
            sms_number_id="sms123"
        )
        result = sms_webhooks_resource.create_sms_webhook(request)

        # Check the request was made correctly
        expected_data = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["sms.sent", "sms.delivered"],
            "enabled": True,
            "sms_number_id": "sms123"
        }
        mock_client.request.assert_called_once_with(
            method="POST",
            path="sms-webhooks",
            data=expected_data
        )
        sms_webhooks_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_webhooks_resource._create_response.return_value))

    def test_create_sms_webhook_logging(self, sms_webhooks_resource, mock_client):
        """Test create_sms_webhook logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook999"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_webhooks_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsWebhookCreateRequest(
            url="https://example.com/new-webhook",
            name="New Webhook",
            events=[SmsWebhookEvent.SMS_FAILED],
            sms_number_id="sms789"
        )
        sms_webhooks_resource.create_sms_webhook(request)

        # Check that logging was called correctly
        sms_webhooks_resource.logger.info.assert_called_once_with(
            "Creating SMS webhook: New Webhook for SMS number: sms789"
        )

    def test_update_sms_webhook_basic(self, sms_webhooks_resource, mock_client):
        """Test update_sms_webhook basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook123", "name": "Updated"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook123",
            name="Updated Webhook",
            enabled=False
        )
        result = sms_webhooks_resource.update_sms_webhook(request)

        # Check the request was made correctly
        expected_data = {
            "name": "Updated Webhook",
            "enabled": False
        }
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-webhooks/webhook123",
            data=expected_data
        )
        sms_webhooks_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_webhooks_resource._create_response.return_value))

    def test_update_sms_webhook_partial(self, sms_webhooks_resource, mock_client):
        """Test update_sms_webhook with partial update."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook456"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook456",
            url="https://example.com/updated-url"
        )
        result = sms_webhooks_resource.update_sms_webhook(request)

        # Check the request was made correctly - only URL should be in data
        expected_data = {"url": "https://example.com/updated-url"}
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-webhooks/webhook456",
            data=expected_data
        )
        sms_webhooks_resource._create_response.assert_called_once()

    def test_update_sms_webhook_logging(self, sms_webhooks_resource, mock_client):
        """Test update_sms_webhook logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook777"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_webhooks_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook777",
            events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_FAILED]
        )
        sms_webhooks_resource.update_sms_webhook(request)

        # Check that logging was called correctly
        sms_webhooks_resource.logger.info.assert_called_once_with(
            "Updating SMS webhook: webhook777"
        )

    def test_delete_sms_webhook_basic(self, sms_webhooks_resource, mock_client):
        """Test delete_sms_webhook basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Webhook deleted"}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsWebhookDeleteRequest(sms_webhook_id="webhook123")
        result = sms_webhooks_resource.delete_sms_webhook(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="DELETE",
            path="sms-webhooks/webhook123"
        )
        sms_webhooks_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_webhooks_resource._create_response.return_value))

    def test_delete_sms_webhook_logging(self, sms_webhooks_resource, mock_client):
        """Test delete_sms_webhook logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Webhook deleted"}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_webhooks_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsWebhookDeleteRequest(sms_webhook_id="webhook888")
        sms_webhooks_resource.delete_sms_webhook(request)

        # Check that logging was called correctly
        sms_webhooks_resource.logger.info.assert_called_once_with(
            "Deleting SMS webhook: webhook888"
        )

    def test_resource_initialization(self, mock_client):
        """Test SmsWebhooks resource initialization."""
        resource = SmsWebhooks(mock_client)
        
        assert resource.client == mock_client
        assert hasattr(resource, 'logger')

    def test_list_sms_webhooks_with_special_characters(self, sms_webhooks_resource, mock_client):
        """Test list_sms_webhooks with special characters in SMS number ID."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsWebhooksListQueryParams(sms_number_id="sms-123_abc")
        request = SmsWebhooksListRequest(query_params=query_params)
        result = sms_webhooks_resource.list_sms_webhooks(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-webhooks",
            params={"sms_number_id": "sms-123_abc"}
        )
        sms_webhooks_resource._create_response.assert_called_once()

    def test_get_sms_webhook_with_special_characters(self, sms_webhooks_resource, mock_client):
        """Test get_sms_webhook with special characters in webhook ID."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook-456_xyz"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsWebhookGetRequest(sms_webhook_id="webhook-456_xyz")
        result = sms_webhooks_resource.get_sms_webhook(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-webhooks/webhook-456_xyz"
        )
        sms_webhooks_resource._create_response.assert_called_once()

    def test_create_sms_webhook_all_events(self, sms_webhooks_resource, mock_client):
        """Test create_sms_webhook with all available events."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook_all_events"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsWebhookCreateRequest(
            url="https://example.com/all-events",
            name="All Events Webhook",
            events=[SmsWebhookEvent.SMS_SENT, SmsWebhookEvent.SMS_DELIVERED, SmsWebhookEvent.SMS_FAILED],
            enabled=False,
            sms_number_id="sms_all"
        )
        result = sms_webhooks_resource.create_sms_webhook(request)

        # Check the request was made correctly
        expected_data = {
            "url": "https://example.com/all-events",
            "name": "All Events Webhook",
            "events": ["sms.sent", "sms.delivered", "sms.failed"],
            "enabled": False,
            "sms_number_id": "sms_all"
        }
        mock_client.request.assert_called_once_with(
            method="POST",
            path="sms-webhooks",
            data=expected_data
        )
        sms_webhooks_resource._create_response.assert_called_once()

    def test_update_sms_webhook_all_fields(self, sms_webhooks_resource, mock_client):
        """Test update_sms_webhook with all fields updated."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "webhook_full_update"}}
        mock_client.request.return_value = mock_response
        sms_webhooks_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsWebhookUpdateRequest(
            sms_webhook_id="webhook_full_update",
            url="https://example.com/fully-updated",
            name="Fully Updated Webhook",
            events=[SmsWebhookEvent.SMS_DELIVERED],
            enabled=True
        )
        result = sms_webhooks_resource.update_sms_webhook(request)

        # Check the request was made correctly
        expected_data = {
            "url": "https://example.com/fully-updated",
            "name": "Fully Updated Webhook",
            "events": ["sms.delivered"],
            "enabled": True
        }
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-webhooks/webhook_full_update",
            data=expected_data
        )
        sms_webhooks_resource._create_response.assert_called_once() 