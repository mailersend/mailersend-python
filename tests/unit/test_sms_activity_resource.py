"""Unit tests for SMS Activity resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.sms_activity import SmsActivity
from mailersend.models.base import APIResponse
from mailersend.models.sms_activity import (
    SmsActivityListRequest,
    SmsMessageGetRequest,
)
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestSmsActivity:
    """Test SMS Activity resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = SmsActivity(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_returns_api_response(self):
        """Test list method returns APIResponse."""
        request = SmsActivityListRequest()

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_with_full_parameters(self):
        """Test list with all parameters."""
        request = SmsActivityListRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            date_from=1443651141,
            date_to=1443651200,
            status=["delivered", "sent"],
            page=1,
            limit=25,
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        expected_params = {
            "sms_number_id": "7z3m5jgrogdpyo6n",
            "date_from": 1443651141,
            "date_to": 1443651200,
            "status[]": ["delivered", "sent"],
            "page": 1,
            "limit": 25,
        }

        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-activity", params=expected_params
        )
        assert result == self.mock_api_response

    def test_list_with_partial_parameters(self):
        """Test list with some parameters."""
        request = SmsActivityListRequest(
            sms_number_id="7z3m5jgrogdpyo6n", status=["delivered"]
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        expected_params = {
            "sms_number_id": "7z3m5jgrogdpyo6n",
            "status[]": ["delivered"],
        }

        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-activity", params=expected_params
        )
        assert result == self.mock_api_response

    def test_get_returns_api_response(self):
        """Test get method returns APIResponse."""
        request = SmsMessageGetRequest(sms_message_id="62134a2d7de3253bf10d6642")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-messages/62134a2d7de3253bf10d6642"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)
