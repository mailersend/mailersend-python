import pytest
from unittest.mock import Mock, patch

from mailersend.resources.sms_activity import SmsActivity
from mailersend.models.sms_activity import (
    SmsActivityListRequest, SmsMessageGetRequest
)
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError


class TestSmsActivityResource:
    """Test SMS Activity resource."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()

    @pytest.fixture
    def sms_activity_resource(self, mock_client):
        """Create SMS Activity resource with mock client."""
        return SmsActivity(mock_client)

    @pytest.fixture
    def valid_list_request(self):
        """Create valid list request."""
        return SmsActivityListRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            date_from=1443651141,
            date_to=1443651200,
            status=["delivered", "sent"],
            page=1,
            limit=25
        )

    @pytest.fixture
    def valid_get_request(self):
        """Create valid get request."""
        return SmsMessageGetRequest(sms_message_id="62134a2d7de3253bf10d6642")

    def test_list_success(self, sms_activity_resource, valid_list_request, mock_client):
        """Test successful SMS activity listing."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": []},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_activity_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_activity_resource.list(valid_list_request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "GET",
            "sms-activity",
            params={
                "sms_number_id": "7z3m5jgrogdpyo6n",
                "date_from": 1443651141,
                "date_to": 1443651200,
                "status[]": ["delivered", "sent"],
                "page": 1,
                "limit": 25
            }
        )
        
        # Verify response
        assert isinstance(result, APIResponse)
        assert result.status_code == 200

    def test_list_empty_params(self, sms_activity_resource, mock_client):
        """Test listing with empty parameters."""
        request = SmsActivityListRequest()
        
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": []},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_activity_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_activity_resource.list(request)
        
        # Verify API call with empty params
        mock_client.request.assert_called_once_with(
            "GET",
            "sms-activity",
            params={}
        )

    def test_list_no_request(self, sms_activity_resource):
        """Test listing without request raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_activity_resource.list(None)
        
        assert "SmsActivityListRequest must be provided" in str(exc_info.value)

    def test_list_invalid_request_type(self, sms_activity_resource):
        """Test listing with invalid request type raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_activity_resource.list("invalid-request")
        
        assert "SmsActivityListRequest must be provided" in str(exc_info.value)

    def test_get_success(self, sms_activity_resource, valid_get_request, mock_client):
        """Test successful SMS message activity retrieval."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": {"id": "62134a2d7de3253bf10d6642"}},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_activity_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_activity_resource.get(valid_get_request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "GET",
            "sms-messages/62134a2d7de3253bf10d6642"
        )
        
        # Verify response
        assert isinstance(result, APIResponse)
        assert result.status_code == 200

    def test_get_no_request(self, sms_activity_resource):
        """Test getting without request raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_activity_resource.get(None)
        
        assert "SmsMessageGetRequest must be provided" in str(exc_info.value)

    def test_get_invalid_request_type(self, sms_activity_resource):
        """Test getting with invalid request type raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_activity_resource.get("invalid-request")
        
        assert "SmsMessageGetRequest must be provided" in str(exc_info.value)

    def test_list_logging(self, sms_activity_resource, valid_list_request, mock_client):
        """Test that appropriate logging occurs during SMS activity listing."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": []},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_activity_resource._create_response = Mock(return_value=expected_response)
        
        # Test logging using patch.object
        with patch.object(sms_activity_resource, 'logger') as mock_logger:
            sms_activity_resource.list(valid_list_request)
            
            # Verify debug logging
            mock_logger.debug.assert_called_with("Preparing to list SMS activities")
            
            # Verify info logging
            expected_params = {
                "sms_number_id": "7z3m5jgrogdpyo6n",
                "date_from": 1443651141,
                "date_to": 1443651200,
                "status[]": ["delivered", "sent"],
                "page": 1,
                "limit": 25
            }
            mock_logger.info.assert_called_with(f"Listing SMS activities with params: {expected_params}")

    def test_get_logging(self, sms_activity_resource, valid_get_request, mock_client):
        """Test that appropriate logging occurs during SMS message activity retrieval."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": {"id": "62134a2d7de3253bf10d6642"}},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_activity_resource._create_response = Mock(return_value=expected_response)
        
        # Test logging using patch.object
        with patch.object(sms_activity_resource, 'logger') as mock_logger:
            sms_activity_resource.get(valid_get_request)
            
            # Verify debug logging
            mock_logger.debug.assert_called_with("Preparing to get SMS message activity")
            
            # Verify info logging
            mock_logger.info.assert_called_with("Getting SMS message activity: 62134a2d7de3253bf10d6642")

    def test_list_with_single_status(self, sms_activity_resource, mock_client):
        """Test listing with single status filter."""
        request = SmsActivityListRequest(status=["delivered"])
        
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": []},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_activity_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_activity_resource.list(request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "GET",
            "sms-activity",
            params={"status[]": ["delivered"]}
        )

    def test_list_with_date_range_only(self, sms_activity_resource, mock_client):
        """Test listing with date range only."""
        request = SmsActivityListRequest(
            date_from=1443651141,
            date_to=1443651200
        )
        
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": []},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_activity_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_activity_resource.list(request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "GET",
            "sms-activity",
            params={
                "date_from": 1443651141,
                "date_to": 1443651200
            }
        )