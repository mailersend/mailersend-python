"""Unit tests for SMS Numbers resource."""
from unittest.mock import Mock, MagicMock

from mailersend.resources.sms_numbers import SmsNumbers
from mailersend.models.base import APIResponse
from mailersend.models.sms_numbers import (
    SmsNumbersListRequest,
    SmsNumberGetRequest,
    SmsNumberUpdateRequest,
    SmsNumberDeleteRequest,
)


class TestSmsNumbers:
    """Test SMS Numbers resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = SmsNumbers(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_returns_api_response(self):
        """Test list method returns APIResponse."""
        request = SmsNumbersListRequest()

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_with_parameters(self):
        """Test list with query parameters."""
        request = SmsNumbersListRequest(paused=True, page=2, limit=50)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        expected_params = {"paused": "true", "page": 2, "limit": 50}
        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-numbers", params=expected_params
        )
        assert result == self.mock_api_response

    def test_list_with_empty_parameters(self):
        """Test list with empty query parameters."""
        request = SmsNumbersListRequest()

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-numbers", params={}
        )
        assert result == self.mock_api_response

    def test_get_returns_api_response(self):
        """Test get method returns APIResponse."""
        request = SmsNumberGetRequest(sms_number_id="7z3m5jgrogdpyo6n")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-numbers/7z3m5jgrogdpyo6n"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_returns_api_response(self):
        """Test update method returns APIResponse."""
        request = SmsNumberUpdateRequest(sms_number_id="7z3m5jgrogdpyo6n", paused=True)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update(request)

        expected_body = {"paused": True}
        self.mock_client.request.assert_called_once_with(
            method="PUT", path="sms-numbers/7z3m5jgrogdpyo6n", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_with_empty_payload(self):
        """Test update with empty payload."""
        request = SmsNumberUpdateRequest(sms_number_id="7z3m5jgrogdpyo6n")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update(request)

        expected_body = {}
        self.mock_client.request.assert_called_once_with(
            method="PUT", path="sms-numbers/7z3m5jgrogdpyo6n", body=expected_body
        )
        assert result == self.mock_api_response

    def test_delete_returns_api_response(self):
        """Test delete method returns APIResponse."""
        request = SmsNumberDeleteRequest(sms_number_id="7z3m5jgrogdpyo6n")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete(request)

        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="sms-numbers/7z3m5jgrogdpyo6n"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)
