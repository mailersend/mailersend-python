"""Tests for tokens resource."""

import pytest
from unittest.mock import Mock, patch

from mailersend.resources.tokens import Tokens
from mailersend.models.base import APIResponse


class TestTokensResource:
    """Test Tokens resource."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        client = Mock()
        client.request = Mock()
        return client

    @pytest.fixture
    def tokens_resource(self, mock_client):
        """Create a Tokens resource with mock client."""
        return Tokens(mock_client)

    def test_list_tokens_basic(self, tokens_resource, mock_client):
        """Test list_tokens basic functionality."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.list_tokens()

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/token",
            params={"limit": 25}  # Default limit is included
        )
        assert result is mock_response

    def test_list_tokens_with_pagination(self, tokens_resource, mock_client):
        """Test list_tokens with pagination."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.list_tokens(page=2, limit=50)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/token",
            params={"page": 2, "limit": 50}
        )
        assert result is mock_response

    def test_list_tokens_with_partial_pagination(self, tokens_resource, mock_client):
        """Test list_tokens with only some pagination params."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.list_tokens(page=3)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/token",
            params={"page": 3, "limit": 25}  # Default limit is included
        )
        assert result is mock_response

    @patch('mailersend.resources.tokens.logger')
    def test_list_tokens_logging(self, mock_logger, tokens_resource, mock_client):
        """Test list_tokens logs correctly."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        tokens_resource.list_tokens()

        mock_logger.info.assert_called_once_with("Listing API tokens")

    def test_get_token(self, tokens_resource, mock_client):
        """Test get_token functionality."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.get_token("test_token_id")

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/token/test_token_id"
        )
        assert result is mock_response

    @patch('mailersend.resources.tokens.logger')
    def test_get_token_logging(self, mock_logger, tokens_resource, mock_client):
        """Test get_token logs correctly."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        tokens_resource.get_token("test_token_id")

        mock_logger.info.assert_called_once_with("Getting token: test_token_id")

    def test_create_token(self, tokens_resource, mock_client):
        """Test create_token functionality."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.create_token(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full", "domains_read"]
        )

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
        assert result is mock_response

    @patch('mailersend.resources.tokens.logger')
    def test_create_token_logging(self, mock_logger, tokens_resource, mock_client):
        """Test create_token logs correctly."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        tokens_resource.create_token(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full"]
        )

        mock_logger.info.assert_called_once_with(
            "Creating token: Test Token for domain: domain123"
        )

    def test_update_token(self, tokens_resource, mock_client):
        """Test update_token functionality."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.update_token("test_token_id", "pause")

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            endpoint="/v1/token/test_token_id/settings",
            json={"status": "pause"}
        )
        assert result is mock_response

    @patch('mailersend.resources.tokens.logger')
    def test_update_token_logging(self, mock_logger, tokens_resource, mock_client):
        """Test update_token logs correctly."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        tokens_resource.update_token("test_token_id", "unpause")

        mock_logger.info.assert_called_once_with(
            "Updating token: test_token_id to status: unpause"
        )

    def test_update_token_name(self, tokens_resource, mock_client):
        """Test update_token_name functionality."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.update_token_name("test_token_id", "New Token Name")

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            endpoint="/v1/token/test_token_id",
            json={"name": "New Token Name"}
        )
        assert result is mock_response

    @patch('mailersend.resources.tokens.logger')
    def test_update_token_name_logging(self, mock_logger, tokens_resource, mock_client):
        """Test update_token_name logs correctly."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        tokens_resource.update_token_name("test_token_id", "New Name")

        mock_logger.info.assert_called_once_with(
            "Updating token name: test_token_id to: New Name"
        )

    def test_delete_token(self, tokens_resource, mock_client):
        """Test delete_token functionality."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.delete_token("test_token_id")

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="DELETE",
            endpoint="/v1/token/test_token_id"
        )
        assert result is mock_response

    @patch('mailersend.resources.tokens.logger')
    def test_delete_token_logging(self, mock_logger, tokens_resource, mock_client):
        """Test delete_token logs correctly."""
        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        tokens_resource.delete_token("test_token_id")

        mock_logger.info.assert_called_once_with("Deleting token: test_token_id")


class TestTokensResourceBuilderUsage:
    """Test that Tokens resource uses builders correctly."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        client = Mock()
        client.request = Mock()
        return client

    @pytest.fixture
    def tokens_resource(self, mock_client):
        """Create a Tokens resource with mock client."""
        return Tokens(mock_client)

    @patch('mailersend.resources.tokens.TokensBuilder')
    def test_list_tokens_uses_builder(self, mock_builder_class, tokens_resource, mock_client):
        """Test that list_tokens uses TokensBuilder correctly."""
        mock_builder = Mock()
        mock_builder_class.return_value = mock_builder
        mock_builder.page.return_value = mock_builder
        mock_builder.limit.return_value = mock_builder
        mock_builder.build_tokens_list.return_value = Mock(page=2, limit=50)

        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.list_tokens(page=2, limit=50)

        # Check builder was used correctly
        mock_builder_class.assert_called_once()
        mock_builder.page.assert_called_once_with(2)
        mock_builder.limit.assert_called_once_with(50)
        mock_builder.build_tokens_list.assert_called_once()

    @patch('mailersend.resources.tokens.TokensBuilder')
    def test_get_token_uses_builder(self, mock_builder_class, tokens_resource, mock_client):
        """Test that get_token uses TokensBuilder correctly."""
        mock_builder = Mock()
        mock_builder_class.return_value = mock_builder
        mock_builder.token_id.return_value = mock_builder
        mock_builder.build_token_get.return_value = Mock(token_id="test_id")

        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.get_token("test_id")

        # Check builder was used correctly
        mock_builder_class.assert_called_once()
        mock_builder.token_id.assert_called_once_with("test_id")
        mock_builder.build_token_get.assert_called_once()

    @patch('mailersend.resources.tokens.TokensBuilder')
    def test_create_token_uses_builder(self, mock_builder_class, tokens_resource, mock_client):
        """Test that create_token uses TokensBuilder correctly."""
        mock_builder = Mock()
        mock_builder_class.return_value = mock_builder
        mock_builder.name.return_value = mock_builder
        mock_builder.domain_id.return_value = mock_builder
        mock_builder.scopes.return_value = mock_builder
        mock_builder.build_token_create.return_value = Mock(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full"]
        )

        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.create_token(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full"]
        )

        # Check builder was used correctly
        mock_builder_class.assert_called_once()
        mock_builder.name.assert_called_once_with("Test Token")
        mock_builder.domain_id.assert_called_once_with("domain123")
        mock_builder.scopes.assert_called_once_with(["email_full"])
        mock_builder.build_token_create.assert_called_once()

    @patch('mailersend.resources.tokens.TokensBuilder')
    def test_update_token_uses_builder(self, mock_builder_class, tokens_resource, mock_client):
        """Test that update_token uses TokensBuilder correctly."""
        mock_builder = Mock()
        mock_builder_class.return_value = mock_builder
        mock_builder.token_id.return_value = mock_builder
        mock_builder.status.return_value = mock_builder
        mock_builder.build_token_update.return_value = Mock(
            token_id="test_id",
            status="pause"
        )

        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.update_token("test_id", "pause")

        # Check builder was used correctly
        mock_builder_class.assert_called_once()
        mock_builder.token_id.assert_called_once_with("test_id")
        mock_builder.status.assert_called_once_with("pause")
        mock_builder.build_token_update.assert_called_once()

    @patch('mailersend.resources.tokens.TokensBuilder')
    def test_delete_token_uses_builder(self, mock_builder_class, tokens_resource, mock_client):
        """Test that delete_token uses TokensBuilder correctly."""
        mock_builder = Mock()
        mock_builder_class.return_value = mock_builder
        mock_builder.token_id.return_value = mock_builder
        mock_builder.build_token_delete.return_value = Mock(token_id="test_id")

        mock_response = Mock(spec=APIResponse)
        mock_client.request.return_value = mock_response

        result = tokens_resource.delete_token("test_id")

        # Check builder was used correctly
        mock_builder_class.assert_called_once()
        mock_builder.token_id.assert_called_once_with("test_id")
        mock_builder.build_token_delete.assert_called_once() 