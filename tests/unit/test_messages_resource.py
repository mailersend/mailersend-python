import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.messages import Messages
from mailersend.models.messages import MessagesListRequest, MessageGetRequest
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError


class TestMessages:
    """Test Messages resource class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_logger = Mock()
        self.messages = Messages(self.mock_client, self.mock_logger)
    
    def test_initialization(self):
        """Test Messages resource initialization."""
        assert self.messages.client == self.mock_client
        assert self.messages.logger == self.mock_logger
    
    def test_list_messages_without_request(self):
        """Test listing messages without request parameters."""
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.messages._create_response = Mock(return_value=mock_api_response)
        
        result = self.messages.list_messages()
        
        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with("GET", "messages", params={})
        
        # Verify response creation
        self.messages._create_response.assert_called_once_with(mock_response)
        
        # Verify logging
        self.mock_logger.debug.assert_called()
        self.mock_logger.info.assert_called()
        
        assert result == mock_api_response
    
    def test_list_messages_with_request(self):
        """Test listing messages with request parameters."""
        # Create request
        request = MessagesListRequest(page=2, limit=50)
        
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.messages._create_response = Mock(return_value=mock_api_response)
        
        # Mock the _build_query_params method
        expected_params = {"page": 2, "limit": 50}
        self.messages._build_query_params = Mock(return_value=expected_params)
        
        result = self.messages.list_messages(request)
        
        # Verify query params were built
        self.messages._build_query_params.assert_called_once_with(request)
        
        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with("GET", "messages", params=expected_params)
        
        # Verify response creation
        self.messages._create_response.assert_called_once_with(mock_response)
        
        assert result == mock_api_response
    
    def test_get_message_success(self):
        """Test getting a single message successfully."""
        # Create request
        request = MessageGetRequest(message_id="5ee0b183b251345e407c936a")
        
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.messages._create_response = Mock(return_value=mock_api_response)
        
        result = self.messages.get_message(request)
        
        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with("GET", "messages/5ee0b183b251345e407c936a")
        
        # Verify response creation
        self.messages._create_response.assert_called_once_with(mock_response)
        
        # Verify logging
        self.mock_logger.debug.assert_called()
        self.mock_logger.info.assert_called()
        
        assert result == mock_api_response
    
    def test_get_message_without_request(self):
        """Test getting a message without request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.messages.get_message(None)
        
        assert "MessageGetRequest must be provided" in str(exc_info.value)
        self.mock_logger.error.assert_called_once()
        
        # Verify client was not called
        self.mock_client.request.assert_not_called()
    
    def test_build_query_params_with_page_and_limit(self):
        """Test building query parameters with page and limit."""
        request = Mock()
        request.page = 3
        request.limit = 75
        
        result = self.messages._build_query_params(request)
        
        expected = {"page": 3, "limit": 75}
        assert result == expected
    
    def test_build_query_params_with_none_values(self):
        """Test building query parameters with None values."""
        request = Mock()
        request.page = None
        request.limit = None
        
        result = self.messages._build_query_params(request)
        
        assert result == {}
    
    def test_build_query_params_with_partial_values(self):
        """Test building query parameters with partial values."""
        request = Mock()
        request.page = 2
        request.limit = None
        
        result = self.messages._build_query_params(request)
        
        expected = {"page": 2}
        assert result == expected
    
    def test_build_query_params_without_attributes(self):
        """Test building query parameters with object missing attributes."""
        request = Mock(spec=[])  # Mock without any attributes
        
        result = self.messages._build_query_params(request)
        
        assert result == {}
    
    def test_list_messages_logging(self):
        """Test that list_messages produces correct log messages."""
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.messages._create_response = Mock(return_value=mock_api_response)
        
        self.messages.list_messages()
        
        # Check debug and info calls
        debug_calls = [call[0][0] for call in self.mock_logger.debug.call_args_list]
        info_calls = [call[0][0] for call in self.mock_logger.info.call_args_list]
        
        assert "Retrieving messages list" in debug_calls
        assert "Requesting messages list" in info_calls
        assert any("Query params:" in call for call in debug_calls)
    
    def test_get_message_logging(self):
        """Test that get_message produces correct log messages."""
        request = MessageGetRequest(message_id="test-message-id")
        
        # Mock the client response
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Mock the _create_response method
        mock_api_response = Mock(spec=APIResponse)
        self.messages._create_response = Mock(return_value=mock_api_response)
        
        self.messages.get_message(request)
        
        # Check debug and info calls
        debug_calls = [call[0][0] for call in self.mock_logger.debug.call_args_list]
        info_calls = [call[0][0] for call in self.mock_logger.info.call_args_list]
        
        assert any("Retrieving message: test-message-id" in call for call in debug_calls)
        assert any("Requesting message information for: test-message-id" in call for call in info_calls)
    
    def test_get_message_error_logging(self):
        """Test error logging when get_message is called without request."""
        with pytest.raises(ValidationError):
            self.messages.get_message(None)
        
        # Check error logging
        error_calls = [call[0][0] for call in self.mock_logger.error.call_args_list]
        assert "No MessageGetRequest object provided" in error_calls 