import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.messages import Messages
from mailersend.models.messages import (
    MessagesListRequest,
    MessagesListQueryParams,
    MessageGetRequest,
)
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestMessages:
    """Test Messages resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = Messages(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_messages_returns_api_response(self):
        """Test list_messages method returns APIResponse."""
        query_params = MessagesListQueryParams()
        request = MessagesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_messages(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_messages_uses_query_params(self):
        """Test list_messages method uses query params correctly."""
        query_params = MessagesListQueryParams(page=2, limit=50)
        request = MessagesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_messages(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="GET", path="messages", params={"page": 2, "limit": 50}
        )

        # Verify _create_response was called
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_messages_with_defaults(self):
        """Test list_messages with default query params."""
        query_params = MessagesListQueryParams()
        request = MessagesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_messages(request)

        # Verify client was called with defaults
        self.mock_client.request.assert_called_once_with(
            method="GET", path="messages", params={"page": 1, "limit": 25}
        )

    def test_list_messages_excludes_none_values(self):
        """Test list_messages excludes None values from params."""
        query_params = MessagesListQueryParams(page=1, limit=25)
        request = MessagesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_messages(request)

        # Verify None values are excluded from params
        call_args = self.mock_client.request.call_args
        params = call_args[1]["params"]
        for key, value in params.items():
            assert value is not None

    def test_get_message_returns_api_response(self):
        """Test get_message method returns APIResponse."""
        request = MessageGetRequest(message_id="message123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_message(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_message_with_valid_request(self):
        """Test get_message with valid request."""
        request = MessageGetRequest(message_id="message123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_message(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="GET", path="messages/message123"
        )

    def test_get_message_endpoint_construction(self):
        """Test get_message constructs endpoint correctly."""
        request = MessageGetRequest(message_id="5ee0b183b251345e407c936a")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_message(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method="GET", path="messages/5ee0b183b251345e407c936a"
        )

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        query_params = MessagesListQueryParams()
        request_list = MessagesListRequest(query_params=query_params)
        request_get = MessageGetRequest(message_id="message123")

        # Test that each method returns the expected APIResponse type
        assert isinstance(
            self.resource.list_messages(request_list), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.get_message(request_get), type(self.mock_api_response)
        )
