import pytest
from unittest.mock import Mock

from mailersend.resources.schedules import Schedules
from mailersend.models.schedules import (
    SchedulesListRequest,
    SchedulesListQueryParams,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
    SchedulesListResponse,
    ScheduleResponse
)
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestSchedules:
    """Test Schedules resource class."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        client = Mock()
        client.request = Mock()
        return client

    @pytest.fixture
    def resource(self, mock_client):
        """Create Schedules resource with mock client."""
        resource = Schedules(mock_client)
        resource._create_response = Mock(return_value=APIResponse(data={}, headers={}, status_code=200))
        return resource
    
    def test_list_schedules_returns_api_response(self, resource):
        """Test list_schedules method returns APIResponse."""
        query_params = SchedulesListQueryParams()
        request = SchedulesListRequest(query_params=query_params)
        
        result = resource.list_schedules(request)
        assert isinstance(result, APIResponse)

    def test_list_schedules_validation_wrong_type(self, resource):
        """Test list_schedules method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.list_schedules("invalid_request")
        assert "Request must be an instance of SchedulesListRequest" in str(exc_info.value)

    def test_list_schedules_with_query_params(self, resource):
        """Test list_schedules method uses query params correctly."""
        query_params = SchedulesListQueryParams(
            domain_id="test-domain",
            status="scheduled",
            page=2,
            limit=50
        )
        request = SchedulesListRequest(query_params=query_params)
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.list_schedules(request)
        
        # Verify client was called correctly
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='message-schedules',
            params={
                'domain_id': 'test-domain',
                'status': 'scheduled',
                'page': 2,
                'limit': 50
            }
        )
        
        # Verify _create_response was called with correct params
        resource._create_response.assert_called_once_with(mock_response, SchedulesListResponse)

    def test_list_schedules_with_default_query_params(self, resource):
        """Test list_schedules with default query params."""
        query_params = SchedulesListQueryParams()  # Uses defaults
        request = SchedulesListRequest(query_params=query_params)
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.list_schedules(request)
        
        # Verify client was called with defaults
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='message-schedules',
            params={'page': 1, 'limit': 25}
        )

    def test_list_schedules_with_partial_params(self, resource):
        """Test list_schedules with partial query params."""
        query_params = SchedulesListQueryParams(domain_id="test-domain", page=3)
        request = SchedulesListRequest(query_params=query_params)
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.list_schedules(request)
        
        # Verify client was called with partial params
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='message-schedules',
            params={'domain_id': 'test-domain', 'page': 3, 'limit': 25}
        )

    def test_get_schedule_returns_api_response(self, resource):
        """Test get_schedule method returns APIResponse."""
        request = ScheduleGetRequest(message_id="test-message-id")
        
        result = resource.get_schedule(request)
        assert isinstance(result, APIResponse)

    def test_get_schedule_validation_wrong_type(self, resource):
        """Test get_schedule method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.get_schedule("invalid_request")
        assert "Request must be an instance of ScheduleGetRequest" in str(exc_info.value)

    def test_get_schedule_with_valid_request(self, resource):
        """Test get_schedule with valid request."""
        request = ScheduleGetRequest(message_id="61e01f471053b349a5478a52")
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.get_schedule(request)
        
        # Verify client was called correctly
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='message-schedules/61e01f471053b349a5478a52'
        )
        
        # Verify _create_response was called
        resource._create_response.assert_called_once_with(mock_response, ScheduleResponse)

    def test_delete_schedule_returns_api_response(self, resource):
        """Test delete_schedule method returns APIResponse."""
        request = ScheduleDeleteRequest(message_id="test-message-id")
        
        result = resource.delete_schedule(request)
        assert isinstance(result, APIResponse)

    def test_delete_schedule_validation_wrong_type(self, resource):
        """Test delete_schedule method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.delete_schedule("invalid_request")
        assert "Request must be an instance of ScheduleDeleteRequest" in str(exc_info.value)

    def test_delete_schedule_with_valid_request(self, resource):
        """Test delete_schedule with valid request."""
        request = ScheduleDeleteRequest(message_id="61e01f471053b349a5478a52")
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.delete_schedule(request)
        
        # Verify client was called correctly
        resource.client.request.assert_called_once_with(
            method='DELETE',
            endpoint='message-schedules/61e01f471053b349a5478a52'
        )
        
        # Verify _create_response was called (no response model for delete)
        resource._create_response.assert_called_once_with(mock_response) 