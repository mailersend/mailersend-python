"""Unit tests for SMS Inbounds resource."""
from unittest.mock import Mock, MagicMock

from mailersend.resources.sms_inbounds import SmsInbounds
from mailersend.models.base import APIResponse
from mailersend.models.sms_inbounds import (
    SmsInboundsListRequest,
    SmsInboundsListQueryParams,
    SmsInboundGetRequest,
    SmsInboundCreateRequest,
    SmsInboundUpdateRequest,
    SmsInboundDeleteRequest,
    SmsInboundFilter,
    FilterComparer,
)


class TestSmsInbounds:
    """Test SMS Inbounds resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = SmsInbounds(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_sms_inbounds_returns_api_response(self):
        """Test list_sms_inbounds method returns APIResponse."""
        request = SmsInboundsListRequest()

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_inbounds(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_sms_inbounds_with_parameters(self):
        """Test list_sms_inbounds with query parameters."""
        query_params = SmsInboundsListQueryParams(
            sms_number_id="sms123", enabled=True, page=2, limit=50
        )
        request = SmsInboundsListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_sms_inbounds(request)

        expected_params = {
            "sms_number_id": "sms123",
            "enabled": True,
            "page": 2,
            "limit": 50,
        }

        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-inbounds", params=expected_params
        )
        assert result == self.mock_api_response

    def test_get_sms_inbound_returns_api_response(self):
        """Test get_sms_inbound method returns APIResponse."""
        request = SmsInboundGetRequest(sms_inbound_id="inbound123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_sms_inbound(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", path="sms-inbounds/inbound123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_sms_inbound_returns_api_response(self):
        """Test create_sms_inbound method returns APIResponse."""
        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Test Route",
            forward_url="https://example.com/webhook",
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_sms_inbound(request)

        expected_body = {
            "sms_number_id": "sms123",
            "name": "Test Route",
            "forward_url": "https://example.com/webhook",
            "enabled": True,
        }

        self.mock_client.request.assert_called_once_with(
            method="POST", path="sms-inbounds", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_sms_inbound_with_filter(self):
        """Test create_sms_inbound with filter."""
        filter_obj = SmsInboundFilter(comparer=FilterComparer.STARTS_WITH, value="STOP")
        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Filtered Route",
            forward_url="https://example.com/webhook",
            filter=filter_obj,
            enabled=False,
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_sms_inbound(request)

        expected_body = {
            "sms_number_id": "sms123",
            "name": "Filtered Route",
            "forward_url": "https://example.com/webhook",
            "enabled": False,
            "filter": {"comparer": "starts-with", "value": "STOP"},
        }

        self.mock_client.request.assert_called_once_with(
            method="POST", path="sms-inbounds", body=expected_body
        )
        assert result == self.mock_api_response

    def test_update_sms_inbound_returns_api_response(self):
        """Test update_sms_inbound method returns APIResponse."""
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound123", name="Updated Route", enabled=False
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_sms_inbound(request)

        expected_body = {"name": "Updated Route", "enabled": False}

        self.mock_client.request.assert_called_once_with(
            method="PUT", path="sms-inbounds/inbound123", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_sms_inbound_returns_api_response(self):
        """Test delete_sms_inbound method returns APIResponse."""
        request = SmsInboundDeleteRequest(sms_inbound_id="inbound123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_sms_inbound(request)

        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="sms-inbounds/inbound123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)
