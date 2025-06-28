"""Tests for Tokens resource."""

import pytest
from unittest.mock import Mock, patch

from mailersend.resources.tokens import Tokens
from mailersend.models.base import APIResponse
from mailersend.models.tokens import (
    TokensListRequest, TokenGetRequest, TokenCreateRequest, TokenUpdateRequest,
    TokenUpdateNameRequest, TokenDeleteRequest, TokensListQueryParams
)


class TestTokensResource:
    """Test cases for Tokens resource."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()

    @pytest.fixture
    def tokens_resource(self, mock_client):
        """Create a Tokens resource with mock client."""
        return Tokens(mock_client)

    def test_list_tokens_basic(self, tokens_resource, mock_client):
        """Test list_tokens basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokensListRequest()
        result = tokens_resource.list_tokens(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/token",
            params={}  # Default values don't get included
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(tokens_resource._create_response.return_value))

    def test_list_tokens_with_pagination(self, tokens_resource, mock_client):
        """Test list_tokens with pagination."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = TokensListQueryParams(page=2, limit=50)
        request = TokensListRequest(query_params=query_params)
        result = tokens_resource.list_tokens(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/token",
            params={"page": 2, "limit": 50}
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(tokens_resource._create_response.return_value))

    @patch('mailersend.resources.tokens.logger')
    def test_list_tokens_logging(self, mock_logger, tokens_resource, mock_client):
        """Test list_tokens logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = TokensListQueryParams(page=2, limit=50)
        request = TokensListRequest(query_params=query_params)
        tokens_resource.list_tokens(request)

        mock_logger.info.assert_called_once_with(
            "Listing tokens with pagination: page=2, limit=50"
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)

    def test_get_token(self, tokens_resource, mock_client):
        """Test get_token functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenGetRequest(token_id="test_token_id")
        result = tokens_resource.get_token(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/token/test_token_id"
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(tokens_resource._create_response.return_value))

    @patch('mailersend.resources.tokens.logger')
    def test_get_token_logging(self, mock_logger, tokens_resource, mock_client):
        """Test get_token logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenGetRequest(token_id="test_token_id")
        tokens_resource.get_token(request)

        mock_logger.info.assert_called_once_with("Getting token: test_token_id")
        tokens_resource._create_response.assert_called_once_with(mock_response)

    def test_create_token(self, tokens_resource, mock_client):
        """Test create_token functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full", "domains_read"]
        )
        result = tokens_resource.create_token(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="POST",
            endpoint="/v1/token",
            json={
                "name": "Test Token",
                "domain_id": "domain123",
                "scopes": ["email_full", "domains_read"]
            }
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(tokens_resource._create_response.return_value))

    @patch('mailersend.resources.tokens.logger')
    def test_create_token_logging(self, mock_logger, tokens_resource, mock_client):
        """Test create_token logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full"]
        )
        tokens_resource.create_token(request)

        mock_logger.info.assert_called_once_with(
            "Creating token: Test Token for domain: domain123"
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)

    def test_update_token(self, tokens_resource, mock_client):
        """Test update_token functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenUpdateRequest(token_id="test_token_id", status="pause")
        result = tokens_resource.update_token(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            endpoint="/v1/token/test_token_id/settings",
            json={"status": "pause"}
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(tokens_resource._create_response.return_value))

    @patch('mailersend.resources.tokens.logger')
    def test_update_token_logging(self, mock_logger, tokens_resource, mock_client):
        """Test update_token logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenUpdateRequest(token_id="test_token_id", status="unpause")
        tokens_resource.update_token(request)

        mock_logger.info.assert_called_once_with(
            "Updating token: test_token_id to status: unpause"
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)

    def test_update_token_name(self, tokens_resource, mock_client):
        """Test update_token_name functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenUpdateNameRequest(token_id="test_token_id", name="New Token Name")
        result = tokens_resource.update_token_name(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            endpoint="/v1/token/test_token_id",
            json={"name": "New Token Name"}
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(tokens_resource._create_response.return_value))

    @patch('mailersend.resources.tokens.logger')
    def test_update_token_name_logging(self, mock_logger, tokens_resource, mock_client):
        """Test update_token_name logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenUpdateNameRequest(token_id="test_token_id", name="New Name")
        tokens_resource.update_token_name(request)

        mock_logger.info.assert_called_once_with(
            "Updating token name: test_token_id to: New Name"
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)

    def test_delete_token(self, tokens_resource, mock_client):
        """Test delete_token functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenDeleteRequest(token_id="test_token_id")
        result = tokens_resource.delete_token(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="DELETE",
            endpoint="/v1/token/test_token_id"
        )
        tokens_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(tokens_resource._create_response.return_value))

    @patch('mailersend.resources.tokens.logger')
    def test_delete_token_logging(self, mock_logger, tokens_resource, mock_client):
        """Test delete_token logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_client.request.return_value = mock_response
        tokens_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = TokenDeleteRequest(token_id="test_token_id")
        tokens_resource.delete_token(request)

        mock_logger.info.assert_called_once_with("Deleting token: test_token_id")
        tokens_resource._create_response.assert_called_once_with(mock_response) 