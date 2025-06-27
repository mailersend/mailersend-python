import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.schedules import Schedules
from mailersend.models.schedules import SchedulesListRequest, ScheduleGetRequest, ScheduleDeleteRequest
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError


class TestSchedules:
    """Test Schedules resource class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_logger = Mock()
        self.schedules = Schedules(self.mock_client, self.mock_logger)
    
    def test_initialization(self):
        """Test Schedules resource initialization."""
        assert self.schedules.client == self.mock_client
        assert self.schedules.logger == self.mock_logger
    
    def test_list_schedules_without_request(self):
        """Test listing schedules without request parameters."""
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.schedules._create_response = Mock(return_value=mock_api_response)
        
        result = self.schedules.list_schedules()
        
        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with("GET", "message-schedules", params={})
        
        # Verify response creation
        self.schedules._create_response.assert_called_once_with(mock_response)
        
        # Verify logging
        self.mock_logger.debug.assert_called()
        self.mock_logger.info.assert_called()
        
        assert result == mock_api_response
    
    def test_list_schedules_with_request(self):
        """Test listing schedules with request parameters."""
        # Create request
        request = SchedulesListRequest(
            domain_id="test-domain",
            status="scheduled",
            page=2,
            limit=50
        )
        
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.schedules._create_response = Mock(return_value=mock_api_response)
        
        # Mock the _build_query_params method
        expected_params = {"domain_id": "test-domain", "status": "scheduled", "page": 2, "limit": 50}
        self.schedules._build_query_params = Mock(return_value=expected_params)
        
        result = self.schedules.list_schedules(request)
        
        # Verify query params were built
        self.schedules._build_query_params.assert_called_once_with(request)
        
        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with("GET", "message-schedules", params=expected_params)
        
        # Verify response creation
        self.schedules._create_response.assert_called_once_with(mock_response)
        
        assert result == mock_api_response
    
    def test_get_schedule_success(self):
        """Test getting a single schedule successfully."""
        # Create request
        request = ScheduleGetRequest(message_id="61e01f471053b349a5478a52")
        
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.schedules._create_response = Mock(return_value=mock_api_response)
        
        result = self.schedules.get_schedule(request)
        
        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with("GET", "message-schedules/61e01f471053b349a5478a52")
        
        # Verify response creation
        self.schedules._create_response.assert_called_once_with(mock_response)
        
        # Verify logging
        self.mock_logger.debug.assert_called()
        self.mock_logger.info.assert_called()
        
        assert result == mock_api_response
    
    def test_get_schedule_without_request(self):
        """Test getting a schedule without request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.schedules.get_schedule(None)
        
        assert "ScheduleGetRequest must be provided" in str(exc_info.value)
        self.mock_logger.error.assert_called_once()
        
        # Verify client was not called
        self.mock_client.request.assert_not_called()
    
    def test_delete_schedule_success(self):
        """Test deleting a schedule successfully."""
        # Create request
        request = ScheduleDeleteRequest(message_id="61e01f471053b349a5478a52")
        
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.schedules._create_response = Mock(return_value=mock_api_response)
        
        result = self.schedules.delete_schedule(request)
        
        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with("DELETE", "message-schedules/61e01f471053b349a5478a52")
        
        # Verify response creation
        self.schedules._create_response.assert_called_once_with(mock_response)
        
        # Verify logging
        self.mock_logger.debug.assert_called()
        self.mock_logger.info.assert_called()
        
        assert result == mock_api_response
    
    def test_delete_schedule_without_request(self):
        """Test deleting a schedule without request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.schedules.delete_schedule(None)
        
        assert "ScheduleDeleteRequest must be provided" in str(exc_info.value)
        self.mock_logger.error.assert_called_once()
        
        # Verify client was not called
        self.mock_client.request.assert_not_called()
    
    def test_build_query_params_all_parameters(self):
        """Test building query parameters with all parameters."""
        request = Mock()
        request.domain_id = "test-domain"
        request.status = "scheduled"
        request.page = 3
        request.limit = 75
        
        result = self.schedules._build_query_params(request)
        
        expected = {
            "domain_id": "test-domain",
            "status": "scheduled",
            "page": 3,
            "limit": 75
        }
        assert result == expected
    
    def test_build_query_params_with_none_values(self):
        """Test building query parameters with None values."""
        request = Mock()
        request.domain_id = None
        request.status = None
        request.page = None
        request.limit = None
        
        result = self.schedules._build_query_params(request)
        
        assert result == {}
    
    def test_build_query_params_with_partial_values(self):
        """Test building query parameters with partial values."""
        request = Mock()
        request.domain_id = "test-domain"
        request.status = None
        request.page = 2
        request.limit = None
        
        result = self.schedules._build_query_params(request)
        
        expected = {"domain_id": "test-domain", "page": 2}
        assert result == expected
    
    def test_build_query_params_without_attributes(self):
        """Test building query parameters with object missing attributes."""
        request = Mock(spec=[])  # Mock without any attributes
        
        result = self.schedules._build_query_params(request)
        
        assert result == {}
    
    def test_list_schedules_logging(self):
        """Test that list_schedules produces correct log messages."""
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.schedules._create_response = Mock(return_value=mock_api_response)
        
        self.schedules.list_schedules()
        
        # Check debug and info calls
        debug_calls = [call[0][0] for call in self.mock_logger.debug.call_args_list]
        info_calls = [call[0][0] for call in self.mock_logger.info.call_args_list]
        
        assert "Retrieving scheduled messages list" in debug_calls
        assert "Requesting scheduled messages list" in info_calls
        assert any("Query params:" in call for call in debug_calls)
    
    def test_get_schedule_logging(self):
        """Test that get_schedule produces correct log messages."""
        request = ScheduleGetRequest(message_id="test-message-id")
        
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.schedules._create_response = Mock(return_value=mock_api_response)
        
        self.schedules.get_schedule(request)
        
        # Check debug and info calls
        debug_calls = [call[0][0] for call in self.mock_logger.debug.call_args_list]
        info_calls = [call[0][0] for call in self.mock_logger.info.call_args_list]
        
        assert any("Retrieving scheduled message: test-message-id" in call for call in debug_calls)
        assert any("Requesting scheduled message information for: test-message-id" in call for call in info_calls)
    
    def test_delete_schedule_logging(self):
        """Test that delete_schedule produces correct log messages."""
        request = ScheduleDeleteRequest(message_id="test-message-id")
        
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.schedules._create_response = Mock(return_value=mock_api_response)
        
        self.schedules.delete_schedule(request)
        
        # Check debug and info calls
        debug_calls = [call[0][0] for call in self.mock_logger.debug.call_args_list]
        info_calls = [call[0][0] for call in self.mock_logger.info.call_args_list]
        
        assert any("Deleting scheduled message: test-message-id" in call for call in debug_calls)
        assert any("Deleting scheduled message: test-message-id" in call for call in info_calls)
    
    def test_get_schedule_error_logging(self):
        """Test error logging when get_schedule is called without request."""
        with pytest.raises(ValidationError):
            self.schedules.get_schedule(None)
        
        # Check error logging
        error_calls = [call[0][0] for call in self.mock_logger.error.call_args_list]
        assert "No ScheduleGetRequest object provided" in error_calls
    
    def test_delete_schedule_error_logging(self):
        """Test error logging when delete_schedule is called without request."""
        with pytest.raises(ValidationError):
            self.schedules.delete_schedule(None)
        
        # Check error logging
        error_calls = [call[0][0] for call in self.mock_logger.error.call_args_list]
        assert "No ScheduleDeleteRequest object provided" in error_calls 