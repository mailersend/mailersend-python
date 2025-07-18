"""Tests for SMS Messages resource."""

import pytest
from unittest.mock import Mock, patch

from mailersend.resources.sms_messages import SmsMessages
from mailersend.models.sms_messages import (
    SmsMessagesListRequest, SmsMessagesListQueryParams, SmsMessageGetRequest
)
from mailersend.models.base import APIResponse


class TestSmsMessagesResource:
    """Test cases for SmsMessages resource."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()
    
    @pytest.fixture
    def sms_messages_resource(self, mock_client):
        """Create a SmsMessages resource with mock client."""
        return SmsMessages(mock_client)

    def test_list_sms_messages_basic(self, sms_messages_resource, mock_client):
        """Test list_sms_messages basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_messages_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsMessagesListRequest()
        result = sms_messages_resource.list_sms_messages(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/sms-messages",
            params={}  # Default values don't get included
        )
        sms_messages_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_messages_resource._create_response.return_value))

    def test_list_sms_messages_with_params(self, sms_messages_resource, mock_client):
        """Test list_sms_messages with custom parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_messages_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsMessagesListQueryParams(page=2, limit=50)
        request = SmsMessagesListRequest(query_params=query_params)
        result = sms_messages_resource.list_sms_messages(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/sms-messages",
            params={"page": 2, "limit": 50}
        )
        sms_messages_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_messages_resource._create_response.return_value))

    @patch('mailersend.resources.sms_messages.logger')
    def test_list_sms_messages_logging(self, mock_logger, sms_messages_resource, mock_client):
        """Test list_sms_messages logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_messages_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsMessagesListQueryParams(page=3, limit=30)
        request = SmsMessagesListRequest(query_params=query_params)
        sms_messages_resource.list_sms_messages(request)

        mock_logger.info.assert_called_once_with(
            "Listing SMS messages with page: 3, limit: 30"
        )
        sms_messages_resource._create_response.assert_called_once()

    def test_get_sms_message(self, sms_messages_resource, mock_client):
        """Test get_sms_message functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        sms_messages_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsMessageGetRequest(sms_message_id="msg123")
        result = sms_messages_resource.get_sms_message(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/sms-messages/msg123"
        )
        sms_messages_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_messages_resource._create_response.return_value))

    @patch('mailersend.resources.sms_messages.logger')
    def test_get_sms_message_logging(self, mock_logger, sms_messages_resource, mock_client):
        """Test get_sms_message logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        sms_messages_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsMessageGetRequest(sms_message_id="msg456")
        sms_messages_resource.get_sms_message(request)

        mock_logger.info.assert_called_once_with(
            "Getting SMS message: msg456"
        )
        sms_messages_resource._create_response.assert_called_once()
