"""Tests for SMS Inbounds resource."""

import pytest
from unittest.mock import Mock, patch

from mailersend.resources.sms_inbounds import SmsInbounds
from mailersend.models.sms_inbounds import (
    SmsInboundsListRequest,
    SmsInboundsListQueryParams,
    SmsInboundGetRequest,
    SmsInboundCreateRequest,
    SmsInboundUpdateRequest,
    SmsInboundDeleteRequest,
    SmsInboundFilter,
    FilterComparer
)
from mailersend.models.base import APIResponse


class TestSmsInboundsResource:
    """Test cases for SmsInbounds resource."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()
    
    @pytest.fixture
    def sms_inbounds_resource(self, mock_client):
        """Create a SmsInbounds resource with mock client."""
        return SmsInbounds(mock_client)

    def test_list_sms_inbounds_basic(self, sms_inbounds_resource, mock_client):
        """Test list_sms_inbounds basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsInboundsListQueryParams()
        request = SmsInboundsListRequest(query_params=query_params)
        result = sms_inbounds_resource.list_sms_inbounds(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-inbounds",
            params={}
        )
        sms_inbounds_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_inbounds_resource._create_response.return_value))

    def test_list_sms_inbounds_with_filters(self, sms_inbounds_resource, mock_client):
        """Test list_sms_inbounds with filters."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsInboundsListQueryParams(
            sms_number_id="sms123",
            enabled=True,
            page=2,
            limit=50
        )
        request = SmsInboundsListRequest(query_params=query_params)
        result = sms_inbounds_resource.list_sms_inbounds(request)

        # Check the request was made correctly
        expected_params = {
            "sms_number_id": "sms123",
            "enabled": True,
            "page": 2,
            "limit": 50
        }
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-inbounds",
            params=expected_params
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_list_sms_inbounds_logging(self, sms_inbounds_resource, mock_client):
        """Test list_sms_inbounds logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_inbounds_resource.logger = Mock()  # Mock the instance logger
        
        query_params = SmsInboundsListQueryParams(sms_number_id="sms456")
        request = SmsInboundsListRequest(query_params=query_params)
        sms_inbounds_resource.list_sms_inbounds(request)

        # Check that logging was called correctly
        sms_inbounds_resource.logger.info.assert_called_once_with(
            f"Listing SMS inbounds with filters: {{'sms_number_id': 'sms456'}}"
        )

    def test_get_sms_inbound_basic(self, sms_inbounds_resource, mock_client):
        """Test get_sms_inbound basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound123"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsInboundGetRequest(sms_inbound_id="inbound123")
        result = sms_inbounds_resource.get_sms_inbound(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-inbounds/inbound123"
        )
        sms_inbounds_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_inbounds_resource._create_response.return_value))

    def test_get_sms_inbound_logging(self, sms_inbounds_resource, mock_client):
        """Test get_sms_inbound logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound456"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_inbounds_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsInboundGetRequest(sms_inbound_id="inbound456")
        sms_inbounds_resource.get_sms_inbound(request)

        # Check that logging was called correctly
        sms_inbounds_resource.logger.info.assert_called_once_with(
            "Getting SMS inbound: inbound456"
        )

    def test_create_sms_inbound_basic(self, sms_inbounds_resource, mock_client):
        """Test create_sms_inbound basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound789"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Test Inbound",
            forward_url="https://example.com/webhook"
        )
        result = sms_inbounds_resource.create_sms_inbound(request)

        # Check the request was made correctly
        expected_data = {
            "sms_number_id": "sms123",
            "name": "Test Inbound",
            "forward_url": "https://example.com/webhook",
            "enabled": True
        }
        mock_client.request.assert_called_once_with(
            method="POST",
            path="sms-inbounds",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_inbounds_resource._create_response.return_value))

    def test_create_sms_inbound_with_filter(self, sms_inbounds_resource, mock_client):
        """Test create_sms_inbound with filter."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound999"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.STARTS_WITH,
            value="START"
        )
        request = SmsInboundCreateRequest(
            sms_number_id="sms456",
            name="Filtered Inbound",
            forward_url="https://example.com/filtered",
            filter=filter_obj,
            enabled=False
        )
        result = sms_inbounds_resource.create_sms_inbound(request)

        # Check the request was made correctly
        expected_data = {
            "sms_number_id": "sms456",
            "name": "Filtered Inbound",
            "forward_url": "https://example.com/filtered",
            "filter": {
                "comparer": "starts-with",
                "value": "START"
            },
            "enabled": False
        }
        mock_client.request.assert_called_once_with(
            method="POST",
            path="sms-inbounds",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_create_sms_inbound_logging(self, sms_inbounds_resource, mock_client):
        """Test create_sms_inbound logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound777"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_inbounds_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsInboundCreateRequest(
            sms_number_id="sms789",
            name="Logged Inbound",
            forward_url="https://example.com/logged"
        )
        sms_inbounds_resource.create_sms_inbound(request)

        # Check that logging was called correctly
        sms_inbounds_resource.logger.info.assert_called_once_with(
            "Creating SMS inbound: Logged Inbound for SMS number: sms789"
        )

    def test_update_sms_inbound_basic(self, sms_inbounds_resource, mock_client):
        """Test update_sms_inbound basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound123", "name": "Updated"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound123",
            name="Updated Inbound",
            enabled=False
        )
        result = sms_inbounds_resource.update_sms_inbound(request)

        # Check the request was made correctly
        expected_data = {
            "name": "Updated Inbound",
            "enabled": False
        }
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-inbounds/inbound123",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_inbounds_resource._create_response.return_value))

    def test_update_sms_inbound_with_filter(self, sms_inbounds_resource, mock_client):
        """Test update_sms_inbound with filter update."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound456"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.CONTAINS,
            value="STOP"
        )
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound456",
            sms_number_id="sms999",
            name="Updated with Filter",
            forward_url="https://example.com/updated",
            filter=filter_obj,
            enabled=True
        )
        result = sms_inbounds_resource.update_sms_inbound(request)

        # Check the request was made correctly
        expected_data = {
            "sms_number_id": "sms999",
            "name": "Updated with Filter",
            "forward_url": "https://example.com/updated",
            "filter": {
                "comparer": "contains",
                "value": "STOP"
            },
            "enabled": True
        }
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-inbounds/inbound456",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_update_sms_inbound_partial(self, sms_inbounds_resource, mock_client):
        """Test update_sms_inbound with partial update."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound789"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound789",
            forward_url="https://example.com/new-url"
        )
        result = sms_inbounds_resource.update_sms_inbound(request)

        # Check the request was made correctly - only forward URL should be in data
        expected_data = {"forward_url": "https://example.com/new-url"}
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-inbounds/inbound789",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_update_sms_inbound_logging(self, sms_inbounds_resource, mock_client):
        """Test update_sms_inbound logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound888"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_inbounds_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound888",
            name="Log Test"
        )
        sms_inbounds_resource.update_sms_inbound(request)

        # Check that logging was called correctly
        sms_inbounds_resource.logger.info.assert_called_once_with(
            "Updating SMS inbound: inbound888"
        )

    def test_delete_sms_inbound_basic(self, sms_inbounds_resource, mock_client):
        """Test delete_sms_inbound basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Inbound deleted"}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsInboundDeleteRequest(sms_inbound_id="inbound123")
        result = sms_inbounds_resource.delete_sms_inbound(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="DELETE",
            path="sms-inbounds/inbound123"
        )
        sms_inbounds_resource._create_response.assert_called_once()
        assert isinstance(result, type(sms_inbounds_resource._create_response.return_value))

    def test_delete_sms_inbound_logging(self, sms_inbounds_resource, mock_client):
        """Test delete_sms_inbound logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Inbound deleted"}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        sms_inbounds_resource.logger = Mock()  # Mock the instance logger
        
        request = SmsInboundDeleteRequest(sms_inbound_id="inbound999")
        sms_inbounds_resource.delete_sms_inbound(request)

        # Check that logging was called correctly
        sms_inbounds_resource.logger.info.assert_called_once_with(
            "Deleting SMS inbound: inbound999"
        )

    def test_resource_initialization(self, mock_client):
        """Test SmsInbounds resource initialization."""
        resource = SmsInbounds(mock_client)
        
        assert resource.client == mock_client
        assert hasattr(resource, 'logger')

    def test_list_sms_inbounds_with_special_characters(self, sms_inbounds_resource, mock_client):
        """Test list_sms_inbounds with special characters in SMS number ID."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsInboundsListQueryParams(sms_number_id="sms-123_abc")
        request = SmsInboundsListRequest(query_params=query_params)
        result = sms_inbounds_resource.list_sms_inbounds(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-inbounds",
            params={"sms_number_id": "sms-123_abc"}
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_get_sms_inbound_with_special_characters(self, sms_inbounds_resource, mock_client):
        """Test get_sms_inbound with special characters in inbound ID."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound-456_xyz"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsInboundGetRequest(sms_inbound_id="inbound-456_xyz")
        result = sms_inbounds_resource.get_sms_inbound(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-inbounds/inbound-456_xyz"
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_create_sms_inbound_all_filter_comparers(self, sms_inbounds_resource, mock_client):
        """Test create_sms_inbound with all available filter comparers."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound_all_comparers"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        # Test with NOT_CONTAINS comparer
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.NOT_CONTAINS,
            value="SPAM"
        )
        request = SmsInboundCreateRequest(
            sms_number_id="sms_all",
            name="All Comparers Route",
            forward_url="https://example.com/all-comparers",
            filter=filter_obj,
            enabled=True
        )
        result = sms_inbounds_resource.create_sms_inbound(request)

        # Check the request was made correctly
        expected_data = {
            "sms_number_id": "sms_all",
            "name": "All Comparers Route",
            "forward_url": "https://example.com/all-comparers",
            "filter": {
                "comparer": "not-contains",
                "value": "SPAM"
            },
            "enabled": True
        }
        mock_client.request.assert_called_once_with(
            method="POST",
            path="sms-inbounds",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_update_sms_inbound_all_fields(self, sms_inbounds_resource, mock_client):
        """Test update_sms_inbound with all fields updated."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound_full_update"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.ENDS_WITH,
            value="END"
        )
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound_full_update",
            sms_number_id="sms_new",
            name="Fully Updated Route",
            forward_url="https://example.com/fully-updated",
            filter=filter_obj,
            enabled=False
        )
        result = sms_inbounds_resource.update_sms_inbound(request)

        # Check the request was made correctly
        expected_data = {
            "sms_number_id": "sms_new",
            "name": "Fully Updated Route",
            "forward_url": "https://example.com/fully-updated",
            "filter": {
                "comparer": "ends-with",
                "value": "END"
            },
            "enabled": False
        }
        mock_client.request.assert_called_once_with(
            method="PUT",
            path="sms-inbounds/inbound_full_update",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_create_sms_inbound_url_edge_cases(self, sms_inbounds_resource, mock_client):
        """Test create_sms_inbound with various URL formats."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound_url_edge"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmsInboundCreateRequest(
            sms_number_id="sms_url_test",
            name="URL Edge Case",
            forward_url="https://api.example.com/v2/webhooks/sms?token=abc123&source=mailersend"
        )
        result = sms_inbounds_resource.create_sms_inbound(request)

        # Check the request was made correctly with complex URL
        expected_data = {
            "sms_number_id": "sms_url_test",
            "name": "URL Edge Case",
            "forward_url": "https://api.example.com/v2/webhooks/sms?token=abc123&source=mailersend",
            "enabled": True
        }
        mock_client.request.assert_called_once_with(
            method="POST",
            path="sms-inbounds",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_list_sms_inbounds_boolean_enabled_false(self, sms_inbounds_resource, mock_client):
        """Test list_sms_inbounds with enabled=False filter."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmsInboundsListQueryParams(enabled=False)
        request = SmsInboundsListRequest(query_params=query_params)
        result = sms_inbounds_resource.list_sms_inbounds(request)

        # Check the request was made correctly with boolean False
        mock_client.request.assert_called_once_with(
            method="GET",
            path="sms-inbounds",
            params={"enabled": False}
        )
        sms_inbounds_resource._create_response.assert_called_once()

    def test_create_sms_inbound_filter_with_special_chars(self, sms_inbounds_resource, mock_client):
        """Test create_sms_inbound with filter containing special characters."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"id": "inbound_special_filter"}}
        mock_client.request.return_value = mock_response
        sms_inbounds_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.EQUAL,
            value="STOP@2023!"
        )
        request = SmsInboundCreateRequest(
            sms_number_id="sms_special",
            name="Special Filter Route",
            forward_url="https://example.com/special",
            filter=filter_obj
        )
        result = sms_inbounds_resource.create_sms_inbound(request)

        # Check the request handles special characters in filter value
        expected_data = {
            "sms_number_id": "sms_special",
            "name": "Special Filter Route",
            "forward_url": "https://example.com/special",
            "filter": {
                "comparer": "equal",
                "value": "STOP@2023!"
            },
            "enabled": True
        }
        mock_client.request.assert_called_once_with(
            method="POST",
            path="sms-inbounds",
            data=expected_data
        )
        sms_inbounds_resource._create_response.assert_called_once() 