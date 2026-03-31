"""Unit tests for WhatsApp resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.whatsapp import WhatsApp
from mailersend.models.base import APIResponse
from mailersend.models.whatsapp import (
    WhatsAppPersonalization,
    WhatsAppPersonalizationData,
    WhatsAppSendRequest,
)


class TestWhatsApp:
    """Test WhatsApp resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = WhatsApp(self.mock_client)
        self.resource.logger = Mock()

        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_send_returns_api_response(self):
        """Test send method returns APIResponse."""
        request = WhatsAppSendRequest(
            from_number="12345678901",
            to=["19191234567"],
            template_id="abc123",
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.send(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_send_with_basic_request(self):
        """Test send with basic WhatsApp request."""
        request = WhatsAppSendRequest(
            from_number="12345678901",
            to=["19191234567", "19199876543"],
            template_id="abc123",
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.send(request)

        expected_body = {
            "from": "12345678901",
            "to": ["19191234567", "19199876543"],
            "template_id": "abc123",
        }
        self.mock_client.request.assert_called_once_with(
            method="POST", path="whatsapp/send", body=expected_body
        )
        assert result == self.mock_api_response

    def test_send_with_personalization(self):
        """Test send with personalization."""
        personalization = [
            WhatsAppPersonalization(
                to="19191234567",
                data=WhatsAppPersonalizationData(
                    header=["John"],
                    body=["order #1234", "tomorrow"],
                ),
            )
        ]

        request = WhatsAppSendRequest(
            from_number="12345678901",
            to=["19191234567"],
            template_id="abc123",
            personalization=personalization,
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.send(request)

        expected_body = {
            "from": "12345678901",
            "to": ["19191234567"],
            "template_id": "abc123",
            "personalization": [
                {
                    "to": "19191234567",
                    "data": {
                        "header": ["John"],
                        "body": ["order #1234", "tomorrow"],
                    },
                }
            ],
        }
        self.mock_client.request.assert_called_once_with(
            method="POST", path="whatsapp/send", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)
