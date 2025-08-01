"""Unit tests for SMS Messages resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.sms_messages import SmsMessages
from mailersend.models.base import APIResponse
from mailersend.models.sms_messages import (
    SmsMessagesListRequest,
    SmsMessagesListQueryParams,
    SmsMessageGetRequest,
)
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestSmsMessages:
    """Test SMS Messages resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = SmsMessages(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_sms_messages_returns_api_response(self):
        """Test list_sms_messages method returns APIResponse."""
        request = SmsMessagesListRequest()

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_messages(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_sms_messages_with_default_params(self):
        """Test list_sms_messages with default parameters."""
        request = SmsMessagesListRequest()

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_messages(request)

        # Default values should not be sent as params
        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-messages", params={}
        )
        assert result == self.mock_api_response

    def test_list_sms_messages_with_custom_params(self):
        """Test list_sms_messages with custom parameters."""
        query_params = SmsMessagesListQueryParams(page=2, limit=50)
        request = SmsMessagesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_messages(request)

        expected_params = {"page": 2, "limit": 50}
        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-messages", params=expected_params
        )
        assert result == self.mock_api_response

    def test_get_sms_message_returns_api_response(self):
        """Test get_sms_message method returns APIResponse."""
        request = SmsMessageGetRequest(sms_message_id="msg123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_sms_message(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-messages/msg123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)
