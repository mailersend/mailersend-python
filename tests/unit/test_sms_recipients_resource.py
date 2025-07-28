"""Tests for SMS Recipients resource."""

import pytest
from unittest.mock import Mock, patch

from mailersend.resources.sms_recipients import SmsRecipients
from mailersend.models.sms_recipients import (
    SmsRecipientsListRequest,
    SmsRecipientsListQueryParams,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsRecipientStatus
)
from mailersend.models.base import APIResponse


class TestSmsRecipientsResource:
    """Test cases for SmsRecipients resource."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()
    
    @pytest.fixture
    def sms_recipients_resource(self, mock_client):
        """Create a SmsRecipients resource with mock client."""
        return SmsRecipients(mock_client)

    def test_list_sms_recipients_basic(self, sms_recipients_resource, mock_client):
        """Test list_sms_recipients basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsRecipientsListRequest()
        result = sms_recipients_resource.list_sms_recipients(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-recipients",
            params={}  # Default values don't get included
        )
        sms_recipients_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_recipients_resource._create_response.return_value))

    def test_list_sms_recipients_with_params(self, sms_recipients_resource, mock_client):
        """Test list_sms_recipients with custom parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.ACTIVE,
            sms_number_id="sms123",
            page=2,
            limit=50
        )
        request = SmsRecipientsListRequest(query_params=query_params)
        result = sms_recipients_resource.list_sms_recipients(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-recipients",
            params={
                "status": "active",
                "sms_number_id": "sms123",
                "page": 2,
                "limit": 50
            }
        )
        sms_recipients_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_recipients_resource._create_response.return_value))

    def test_list_sms_recipients_logging(self, sms_recipients_resource, mock_client):
        """Test list_sms_recipients logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_recipients_resource.logger = Mock()  # Mock the instance logger
        
        query_params = SmsRecipientsListQueryParams(page=3, limit=30)
        request = SmsRecipientsListRequest(query_params=query_params)
        sms_recipients_resource.list_sms_recipients(request)

        # Check that logging was called correctly
        sms_recipients_resource.logger.info.assert_called_once_with(
            "Listing SMS recipients with page: 3, limit: 30"
        )

    def test_list_sms_recipients_with_status_filter(self, sms_recipients_resource, mock_client):
        """Test list_sms_recipients with status filter."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsRecipientsListQueryParams(status=SmsRecipientStatus.OPT_OUT)
        request = SmsRecipientsListRequest(query_params=query_params)
        result = sms_recipients_resource.list_sms_recipients(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-recipients",
            params={"status": "opt_out"}
        )
        sms_recipients_resource._create_response.assert_called_once()

    def test_get_sms_recipient_basic(self, sms_recipients_resource, mock_client):
        """Test get_sms_recipient basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "recipient123"}}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsRecipientGetRequest(sms_recipient_id="recipient123")
        result = sms_recipients_resource.get_sms_recipient(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-recipients/recipient123"
        )
        sms_recipients_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_recipients_resource._create_response.return_value))

    def test_get_sms_recipient_logging(self, sms_recipients_resource, mock_client):
        """Test get_sms_recipient logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "recipient456"}}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_recipients_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsRecipientGetRequest(sms_recipient_id="recipient456")
        sms_recipients_resource.get_sms_recipient(request)

        # Check that logging was called correctly
        sms_recipients_resource.logger.info.assert_called_once_with(
            "Getting SMS recipient: recipient456"
        )

    def test_update_sms_recipient_basic(self, sms_recipients_resource, mock_client):
        """Test update_sms_recipient basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "recipient123", "status": "opt_out"}}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient123",
            status=SmsRecipientStatus.OPT_OUT
        )
        result = sms_recipients_resource.update_sms_recipient(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-recipients/recipient123",
            data={"status": "opt_out"}
        )
        sms_recipients_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_recipients_resource._create_response.return_value))

    def test_update_sms_recipient_to_active(self, sms_recipients_resource, mock_client):
        """Test update_sms_recipient to active status."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "recipient789", "status": "active"}}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient789",
            status=SmsRecipientStatus.ACTIVE
        )
        result = sms_recipients_resource.update_sms_recipient(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-recipients/recipient789",
            data={"status": "active"}
        )
        sms_recipients_resource._create_response.assert_called_once()

    def test_update_sms_recipient_logging(self, sms_recipients_resource, mock_client):
        """Test update_sms_recipient logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "recipient999", "status": "opt_out"}}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_recipients_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient999",
            status=SmsRecipientStatus.OPT_OUT
        )
        sms_recipients_resource.update_sms_recipient(request)

        # Check that logging was called correctly
        sms_recipients_resource.logger.info.assert_called_once_with(
            "Updating SMS recipient: recipient999 to status: SmsRecipientStatus.OPT_OUT"
        )

    def test_resource_initialization(self, mock_client):
        """Test SmsRecipients resource initialization."""
        resource = SmsRecipients(mock_client)
        
        assert resource.client == mock_client
        assert hasattr(resource, 'logger')

    def test_list_sms_recipients_partial_params(self, sms_recipients_resource, mock_client):
        """Test list_sms_recipients with partial parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        # Only set sms_number_id, leave other params as defaults
        query_params = SmsRecipientsListQueryParams(sms_number_id="sms999")
        request = SmsRecipientsListRequest(query_params=query_params)
        result = sms_recipients_resource.list_sms_recipients(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-recipients",
            params={"sms_number_id": "sms999"}  # Only non-default values included
        )
        sms_recipients_resource._create_response.assert_called_once()

    def test_get_sms_recipient_with_special_characters(self, sms_recipients_resource, mock_client):
        """Test get_sms_recipient with special characters in ID."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "recipient-123_abc"}}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsRecipientGetRequest(sms_recipient_id="recipient-123_abc")
        result = sms_recipients_resource.get_sms_recipient(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-recipients/recipient-123_abc"
        )
        sms_recipients_resource._create_response.assert_called_once()

    def test_update_sms_recipient_with_special_characters(self, sms_recipients_resource, mock_client):
        """Test update_sms_recipient with special characters in ID."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "recipient-456_xyz", "status": "active"}}
        mock_client.request.return_value = mock_response
        sms_recipients_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient-456_xyz",
            status=SmsRecipientStatus.ACTIVE
        )
        result = sms_recipients_resource.update_sms_recipient(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-recipients/recipient-456_xyz",
            data={"status": "active"}
        )
        sms_recipients_resource._create_response.assert_called_once() 