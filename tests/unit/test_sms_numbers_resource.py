import pytest
from unittest.mock import Mock, patch

from mailersend.resources.sms_numbers import SmsNumbers
from mailersend.models.sms_numbers import (
    SmsNumbersListRequest, SmsNumberGetRequest, SmsNumberUpdateRequest, SmsNumberDeleteRequest
)
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError


class TestSmsNumbersResource:
    """Test SMS Numbers resource."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()

    @pytest.fixture
    def sms_numbers_resource(self, mock_client):
        """Create SMS Numbers resource with mock client."""
        return SmsNumbers(mock_client)

    @pytest.fixture
    def valid_list_request(self):
        """Create valid list request."""
        return SmsNumbersListRequest(paused=False, page=1, limit=25)

    @pytest.fixture
    def valid_get_request(self):
        """Create valid get request."""
        return SmsNumberGetRequest(sms_number_id="7z3m5jgrogdpyo6n")

    @pytest.fixture
    def valid_update_request(self):
        """Create valid update request."""
        return SmsNumberUpdateRequest(sms_number_id="7z3m5jgrogdpyo6n", paused=True)

    @pytest.fixture
    def valid_delete_request(self):
        """Create valid delete request."""
        return SmsNumberDeleteRequest(sms_number_id="7z3m5jgrogdpyo6n")

    def test_list_success(self, sms_numbers_resource, valid_list_request, mock_client):
        """Test successful SMS phone numbers listing."""
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
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_numbers_resource.list(valid_list_request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "GET",
            "sms-numbers",
            params={
                "paused": "false",
                "page": 1,
                "limit": 25
            }
        )
        
        # Verify response
        assert isinstance(result, APIResponse)
        assert result.status_code == 200

    def test_list_empty_params(self, sms_numbers_resource, mock_client):
        """Test listing with empty parameters."""
        request = SmsNumbersListRequest()
        
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
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_numbers_resource.list(request)
        
        # Verify API call with empty params
        mock_client.request.assert_called_once_with(
            "GET",
            "sms-numbers",
            params={}
        )

    def test_list_no_request(self, sms_numbers_resource):
        """Test listing without request raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_numbers_resource.list(None)
        
        assert "SmsNumbersListRequest must be provided" in str(exc_info.value)

    def test_list_invalid_request_type(self, sms_numbers_resource):
        """Test listing with invalid request type raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_numbers_resource.list("invalid-request")
        
        assert "SmsNumbersListRequest must be provided" in str(exc_info.value)

    def test_get_success(self, sms_numbers_resource, valid_get_request, mock_client):
        """Test successful SMS phone number retrieval."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": {"id": "7z3m5jgrogdpyo6n"}},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_numbers_resource.get(valid_get_request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "GET",
            "sms-numbers/7z3m5jgrogdpyo6n"
        )
        
        # Verify response
        assert isinstance(result, APIResponse)
        assert result.status_code == 200

    def test_get_no_request(self, sms_numbers_resource):
        """Test getting without request raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_numbers_resource.get(None)
        
        assert "SmsNumberGetRequest must be provided" in str(exc_info.value)

    def test_get_invalid_request_type(self, sms_numbers_resource):
        """Test getting with invalid request type raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_numbers_resource.get("invalid-request")
        
        assert "SmsNumberGetRequest must be provided" in str(exc_info.value)

    def test_update_success(self, sms_numbers_resource, valid_update_request, mock_client):
        """Test successful SMS phone number update."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": {"id": "7z3m5jgrogdpyo6n", "paused": True}},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_numbers_resource.update(valid_update_request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "PUT",
            "sms-numbers/7z3m5jgrogdpyo6n",
            body={"paused": True}
        )
        
        # Verify response
        assert isinstance(result, APIResponse)
        assert result.status_code == 200

    def test_update_no_request(self, sms_numbers_resource):
        """Test updating without request raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_numbers_resource.update(None)
        
        assert "SmsNumberUpdateRequest must be provided" in str(exc_info.value)

    def test_update_invalid_request_type(self, sms_numbers_resource):
        """Test updating with invalid request type raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_numbers_resource.update("invalid-request")
        
        assert "SmsNumberUpdateRequest must be provided" in str(exc_info.value)

    def test_delete_success(self, sms_numbers_resource, valid_delete_request, mock_client):
        """Test successful SMS phone number deletion."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={},
            headers={"Content-Type": "application/json"},
            status_code=204
        )
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_numbers_resource.delete(valid_delete_request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "DELETE",
            "sms-numbers/7z3m5jgrogdpyo6n"
        )
        
        # Verify response
        assert isinstance(result, APIResponse)
        assert result.status_code == 204

    def test_delete_no_request(self, sms_numbers_resource):
        """Test deleting without request raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_numbers_resource.delete(None)
        
        assert "SmsNumberDeleteRequest must be provided" in str(exc_info.value)

    def test_delete_invalid_request_type(self, sms_numbers_resource):
        """Test deleting with invalid request type raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_numbers_resource.delete("invalid-request")
        
        assert "SmsNumberDeleteRequest must be provided" in str(exc_info.value)

    def test_list_logging(self, sms_numbers_resource, valid_list_request, mock_client):
        """Test that appropriate logging occurs during SMS numbers listing."""
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
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        # Test logging using patch.object
        with patch.object(sms_numbers_resource, 'logger') as mock_logger:
            sms_numbers_resource.list(valid_list_request)
            
            # Verify debug logging
            mock_logger.debug.assert_called_with("Preparing to list SMS phone numbers")
            
            # Verify info logging
            mock_logger.info.assert_called_with("Listing SMS phone numbers with params: {'paused': 'false', 'page': 1, 'limit': 25}")

    def test_get_logging(self, sms_numbers_resource, valid_get_request, mock_client):
        """Test that appropriate logging occurs during SMS number retrieval."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": {"id": "7z3m5jgrogdpyo6n"}},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        # Test logging using patch.object
        with patch.object(sms_numbers_resource, 'logger') as mock_logger:
            sms_numbers_resource.get(valid_get_request)
            
            # Verify debug logging
            mock_logger.debug.assert_called_with("Preparing to get SMS phone number")
            
            # Verify info logging
            mock_logger.info.assert_called_with("Getting SMS phone number: 7z3m5jgrogdpyo6n")

    def test_update_logging(self, sms_numbers_resource, valid_update_request, mock_client):
        """Test that appropriate logging occurs during SMS number update."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={"data": {"id": "7z3m5jgrogdpyo6n", "paused": True}},
            headers={"Content-Type": "application/json"},
            status_code=200
        )
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        # Test logging using patch.object
        with patch.object(sms_numbers_resource, 'logger') as mock_logger:
            sms_numbers_resource.update(valid_update_request)
            
            # Verify debug logging
            mock_logger.debug.assert_any_call("Preparing to update SMS phone number")
            
            # Verify info logging
            mock_logger.info.assert_called_with("Updating SMS phone number: 7z3m5jgrogdpyo6n")

    def test_delete_logging(self, sms_numbers_resource, valid_delete_request, mock_client):
        """Test that appropriate logging occurs during SMS number deletion."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={},
            headers={"Content-Type": "application/json"},
            status_code=204
        )
        sms_numbers_resource._create_response = Mock(return_value=expected_response)
        
        # Test logging using patch.object
        with patch.object(sms_numbers_resource, 'logger') as mock_logger:
            sms_numbers_resource.delete(valid_delete_request)
            
            # Verify debug logging
            mock_logger.debug.assert_called_with("Preparing to delete SMS phone number")
            
            # Verify info logging
            mock_logger.info.assert_called_with("Deleting SMS phone number: 7z3m5jgrogdpyo6n")