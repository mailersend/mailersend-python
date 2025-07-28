"""Tests for tokens builder."""

import pytest

from mailersend.builders.tokens import TokensBuilder
from mailersend.models.tokens import (
    TOKEN_SCOPES,
    TokensListRequest,
    TokenGetRequest,
    TokenCreateRequest,
    TokenUpdateRequest,
    TokenUpdateNameRequest,
    TokenDeleteRequest,
)


class TestTokensBuilderBasicMethods:
    """Test basic TokensBuilder methods."""

    def test_initialization(self):
        """Test builder initialization."""
        builder = TokensBuilder()
        assert builder._page is None
        assert builder._limit is None
        assert builder._token_id is None
        assert builder._name is None
        assert builder._domain_id is None
        assert builder._scopes == []
        assert builder._status is None

    def test_page_method(self):
        """Test page method."""
        builder = TokensBuilder()
        result = builder.page(2)
        assert result is builder  # Method chaining
        assert builder._page == 2

    def test_token_id_method(self):
        """Test token_id method."""
        builder = TokensBuilder()
        result = builder.token_id("test_token")
        assert result is builder  # Method chaining
        assert builder._token_id == "test_token"

    def test_add_scope_method(self):
        """Test add_scope method."""
        builder = TokensBuilder()
        result = builder.add_scope("email_full")
        assert result is builder  # Method chaining
        assert builder._scopes == ["email_full"]


class TestTokensBuilderBuildMethods:
    """Test build methods."""

    def test_build_tokens_list_basic(self):
        """Test build_tokens_list method."""
        builder = TokensBuilder()
        request = builder.build_tokens_list()
        
        assert isinstance(request, TokensListRequest)
        assert request.query_params.page == 1  # Default from model
        assert request.query_params.limit == 25  # Default from model

    def test_build_token_get_success(self):
        """Test build_token_get method success."""
        builder = TokensBuilder()
        request = builder.token_id("test_token").build_token_get()
        
        assert isinstance(request, TokenGetRequest)
        assert request.token_id == "test_token"

    def test_build_token_create_success(self):
        """Test build_token_create method success."""
        builder = TokensBuilder()
        request = (builder
                  .name("Test Token")
                  .domain_id("domain123")
                  .add_scope("email_full")
                  .build_token_create())
        
        assert isinstance(request, TokenCreateRequest)
        assert request.name == "Test Token"
        assert request.domain_id == "domain123"
        assert request.scopes == ["email_full"]

    def test_build_token_create_missing_name(self):
        """Test build_token_create with missing name."""
        builder = TokensBuilder()
        builder.domain_id("domain123").add_scope("email_full")
        
        with pytest.raises(ValueError, match="name is required for creating a token"):
            builder.build_token_create()

    def test_build_token_delete_success(self):
        """Test build_token_delete method success."""
        builder = TokensBuilder()
        request = builder.token_id("test_token").build_token_delete()
        
        assert isinstance(request, TokenDeleteRequest)
        assert request.token_id == "test_token" 