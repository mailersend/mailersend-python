"""Unit tests for Tokens resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.tokens import Tokens
from mailersend.models.base import APIResponse
from mailersend.models.tokens import (
    TokensListRequest,
    TokensListQueryParams,
    TokenGetRequest,
    TokenCreateRequest,
    TokenUpdateRequest,
    TokenUpdateNameRequest,
    TokenDeleteRequest,
)
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestTokens:
    """Test Tokens resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = Tokens(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_tokens_returns_api_response(self):
        """Test list_tokens method returns APIResponse."""
        query_params = TokensListQueryParams()
        request = TokensListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_tokens(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_tokens_uses_query_params(self):
        """Test list_tokens method uses query params correctly."""
        query_params = TokensListQueryParams(page=2, limit=50)
        request = TokensListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_tokens(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="GET", endpoint="token", params={"page": 2, "limit": 50}
        )

        # Verify _create_response was called
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_tokens_with_defaults(self):
        """Test list_tokens with default query params."""
        query_params = TokensListQueryParams()
        request = TokensListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_tokens(request)

        # Verify client was called with empty params (defaults excluded)
        self.mock_client.request.assert_called_once_with(
            method="GET", endpoint="token", params={}
        )

    def test_get_token_returns_api_response(self):
        """Test get_token method returns APIResponse."""
        request = TokenGetRequest(token_id="token123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_token(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_token_endpoint_construction(self):
        """Test get_token constructs endpoint correctly."""
        request = TokenGetRequest(token_id="token123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_token(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method="GET", endpoint="token/token123"
        )

    def test_create_token_returns_api_response(self):
        """Test create_token method returns APIResponse."""
        request = TokenCreateRequest(
            name="Test Token", domain_id="domain123", scopes=["email_full"]
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_token(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_token_with_request_body(self):
        """Test create_token sends correct request body."""
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full", "domains_read"],
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_token(request)

        # Verify client was called with correct body
        self.mock_client.request.assert_called_once_with(
            method="POST",
            endpoint="token",
            body={
                "name": "Test Token",
                "domain_id": "domain123",
                "scopes": ["email_full", "domains_read"],
            },
        )

    def test_update_token_returns_api_response(self):
        """Test update_token method returns APIResponse."""
        request = TokenUpdateRequest(token_id="token123", status="pause")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_token(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_token_with_request_body(self):
        """Test update_token sends correct request body."""
        request = TokenUpdateRequest(token_id="token123", status="unpause")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_token(request)

        # Verify client was called with correct body and endpoint
        self.mock_client.request.assert_called_once_with(
            method="PUT", endpoint="token/token123/settings", body={"status": "unpause"}
        )

    def test_update_token_name_returns_api_response(self):
        """Test update_token_name method returns APIResponse."""
        request = TokenUpdateNameRequest(token_id="token123", name="New Name")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_token_name(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_token_name_with_request_body(self):
        """Test update_token_name sends correct request body."""
        request = TokenUpdateNameRequest(token_id="token123", name="Updated Name")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_token_name(request)

        # Verify client was called with correct body and endpoint
        self.mock_client.request.assert_called_once_with(
            method="PUT", endpoint="token/token123", body={"name": "Updated Name"}
        )

    def test_delete_token_returns_api_response(self):
        """Test delete_token method returns APIResponse."""
        request = TokenDeleteRequest(token_id="token123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_token(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_token_endpoint_construction(self):
        """Test delete_token constructs endpoint correctly."""
        request = TokenDeleteRequest(token_id="token123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_token(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method="DELETE", endpoint="token/token123"
        )

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        query_params = TokensListQueryParams()
        request_list = TokensListRequest(query_params=query_params)
        request_get = TokenGetRequest(token_id="token123")
        request_create = TokenCreateRequest(
            name="Test", domain_id="domain123", scopes=["email_full"]
        )
        request_update = TokenUpdateRequest(token_id="token123", status="pause")
        request_update_name = TokenUpdateNameRequest(
            token_id="token123", name="New Name"
        )
        request_delete = TokenDeleteRequest(token_id="token123")

        # Test that each method returns the expected APIResponse type
        assert isinstance(
            self.resource.list_tokens(request_list), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.get_token(request_get), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.create_token(request_create), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.update_token(request_update), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.update_token_name(request_update_name),
            type(self.mock_api_response),
        )
        assert isinstance(
            self.resource.delete_token(request_delete), type(self.mock_api_response)
        )
