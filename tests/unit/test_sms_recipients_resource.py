"""Unit tests for SMS Recipients resource."""
from unittest.mock import Mock, MagicMock

from mailersend.resources.sms_recipients import SmsRecipients
from mailersend.models.base import APIResponse
from mailersend.models.sms_recipients import (
    SmsRecipientsListRequest,
    SmsRecipientsListQueryParams,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsRecipientStatus,
)


class TestSmsRecipients:
    """Test SMS Recipients resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = SmsRecipients(self.mock_client)
        self.resource.logger = Mock()
        
        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_sms_recipients_returns_api_response(self):
        """Test list_sms_recipients method returns APIResponse."""
        request = SmsRecipientsListRequest()
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_recipients(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_sms_recipients_with_parameters(self):
        """Test list_sms_recipients with query parameters."""
        query_params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.ACTIVE,
            sms_number_id="sms123",
            page=2,
            limit=50
        )
        request = SmsRecipientsListRequest(query_params=query_params)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_recipients(request)

        expected_params = {
            "status": "active",
            "sms_number_id": "sms123",
            "page": 2,
            "limit": 50
        }
        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="sms-recipients",
            params=expected_params
        )
        assert result == self.mock_api_response

    def test_list_sms_recipients_with_empty_parameters(self):
        """Test list_sms_recipients with empty query parameters."""
        request = SmsRecipientsListRequest()
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_recipients(request)

        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="sms-recipients",
            params={}
        )
        assert result == self.mock_api_response

    def test_get_sms_recipient_returns_api_response(self):
        """Test get_sms_recipient method returns APIResponse."""
        request = SmsRecipientGetRequest(sms_recipient_id="recipient123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_sms_recipient(request)

        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="sms-recipients/recipient123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_sms_recipient_returns_api_response(self):
        """Test update_sms_recipient method returns APIResponse."""
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient123",
            status=SmsRecipientStatus.OPT_OUT
        )
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_sms_recipient(request)

        expected_body = {"status": "opt_out"}
        self.mock_client.request.assert_called_once_with(
            method="PUT",
            endpoint="sms-recipients/recipient123",
            body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response) 