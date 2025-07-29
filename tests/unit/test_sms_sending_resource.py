"""Unit tests for SMS Sending resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.sms_sending import SmsSending
from mailersend.models.base import APIResponse
from mailersend.models.sms_sending import SmsSendRequest, SmsPersonalization
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestSmsSending:
    """Test SMS Sending resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = SmsSending(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_send_returns_api_response(self):
        """Test send method returns APIResponse."""
        request = SmsSendRequest(
            from_number="+1234567890", to=["+1987654321"], text="Hello world!"
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.send(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_send_with_basic_request(self):
        """Test send with basic SMS request."""
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello world!",
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.send(request)

        expected_body = {
            "from": "+1234567890",
            "to": ["+1987654321", "+1111111111"],
            "text": "Hello world!",
        }
        self.mock_client.request.assert_called_once_with(
            method="POST", endpoint="sms", body=expected_body
        )
        assert result == self.mock_api_response

    def test_send_with_personalization(self):
        """Test send with personalization."""
        personalization = [
            SmsPersonalization(phone_number="+1987654321", data={"name": "John"})
        ]

        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321"],
            text="Hello {{name}}!",
            personalization=personalization,
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.send(request)

        expected_body = {
            "from": "+1234567890",
            "to": ["+1987654321"],
            "text": "Hello {{name}}!",
            "personalization": [
                {"phone_number": "+1987654321", "data": {"name": "John"}}
            ],
        }
        self.mock_client.request.assert_called_once_with(
            method="POST", endpoint="sms", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)
