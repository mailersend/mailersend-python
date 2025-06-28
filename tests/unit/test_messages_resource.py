import pytest
from unittest.mock import Mock

from mailersend.resources.messages import Messages
from mailersend.models.messages import (
    MessagesListRequest,
    MessagesListQueryParams,
    MessageGetRequest,
    MessagesListResponse,
    MessageResponse
)
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestMessages:
    """Test Messages resource class."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        client = Mock()
        client.request = Mock()
        return client

    @pytest.fixture
    def resource(self, mock_client):
        """Create Messages resource with mock client."""
        resource = Messages(mock_client)
        resource._create_response = Mock(return_value=APIResponse(data={}, headers={}, status_code=200))
        return resource
    
    def test_list_messages_returns_api_response(self, resource):
        """Test list_messages method returns APIResponse."""
        query_params = MessagesListQueryParams()
        request = MessagesListRequest(query_params=query_params)
        
        result = resource.list_messages(request)
        assert isinstance(result, APIResponse)

    def test_list_messages_validation_wrong_type(self, resource):
        """Test list_messages method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.list_messages("invalid_request")
        assert "Request must be an instance of MessagesListRequest" in str(exc_info.value)

    def test_list_messages_with_query_params(self, resource):
        """Test list_messages method uses query params correctly."""
        query_params = MessagesListQueryParams(page=2, limit=50)
        request = MessagesListRequest(query_params=query_params)
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.list_messages(request)
        
        # Verify client was called correctly
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='messages',
            params={'page': 2, 'limit': 50}
        )
        
        # Verify _create_response was called with correct params
        resource._create_response.assert_called_once_with(mock_response, MessagesListResponse)

    def test_list_messages_with_default_query_params(self, resource):
        """Test list_messages with default query params."""
        query_params = MessagesListQueryParams()  # Uses defaults
        request = MessagesListRequest(query_params=query_params)
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.list_messages(request)
        
        # Verify client was called with defaults
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='messages',
            params={'page': 1, 'limit': 25}
        )

    def test_get_message_returns_api_response(self, resource):
        """Test get_message method returns APIResponse."""
        request = MessageGetRequest(message_id="test-message-id")
        
        result = resource.get_message(request)
        assert isinstance(result, APIResponse)

    def test_get_message_validation_wrong_type(self, resource):
        """Test get_message method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.get_message("invalid_request")
        assert "Request must be an instance of MessageGetRequest" in str(exc_info.value)

    def test_get_message_with_valid_request(self, resource):
        """Test get_message with valid request."""
        request = MessageGetRequest(message_id="5ee0b183b251345e407c936a")
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.get_message(request)
        
        # Verify client was called correctly
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='messages/5ee0b183b251345e407c936a'
        )
        
        # Verify _create_response was called
        resource._create_response.assert_called_once_with(mock_response, MessageResponse) 