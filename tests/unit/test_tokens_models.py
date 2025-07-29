"""Tests for Tokens models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.tokens import (
    TOKEN_SCOPES,
    TokenStatus,
    TokensListRequest,
    TokensListQueryParams,
    TokenGetRequest,
    TokenCreateRequest,
    TokenUpdateRequest,
    TokenUpdateNameRequest,
    TokenDeleteRequest,
)


class TestTokenConstants:
    """Test token constants and types."""

    def test_token_scopes_constant(self):
        """Test TOKEN_SCOPES constant."""
        assert isinstance(TOKEN_SCOPES, list)
        assert len(TOKEN_SCOPES) > 0
        assert "email_full" in TOKEN_SCOPES
        assert "domains_read" in TOKEN_SCOPES
        assert "tokens_full" in TOKEN_SCOPES

    def test_token_status_type(self):
        """Test TokenStatus type alias."""
        # This is a type alias, so we just test it's defined
        assert TokenStatus is not None


class TestTokensListQueryParams:
    """Test TokensListQueryParams model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        query_params = TokensListQueryParams()
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test setting custom values."""
        query_params = TokensListQueryParams(page=2, limit=50)
        assert query_params.page == 2
        assert query_params.limit == 50

    def test_page_validation(self):
        """Test page validation (must be >= 1)."""
        with pytest.raises(ValidationError):
            TokensListQueryParams(page=0)

        with pytest.raises(ValidationError):
            TokensListQueryParams(page=-1)

    def test_limit_validation(self):
        """Test limit validation (10-100)."""
        with pytest.raises(ValidationError):
            TokensListQueryParams(limit=9)

        with pytest.raises(ValidationError):
            TokensListQueryParams(limit=101)

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = TokensListQueryParams()
        result = query_params.to_query_params()
        # Default values should not be included
        assert result == {}

    def test_to_query_params_with_custom_values(self):
        """Test to_query_params with custom values."""
        query_params = TokensListQueryParams(page=3, limit=50)
        result = query_params.to_query_params()
        expected = {'page': 3, 'limit': 50}
        assert result == expected

    def test_to_query_params_excludes_defaults(self):
        """Test to_query_params excludes default values."""
        query_params = TokensListQueryParams(page=1, limit=25)
        result = query_params.to_query_params()
        # Should be empty since these are defaults
        assert result == {}


class TestTokensListRequest:
    """Test TokensListRequest model."""

    def test_create_request_with_query_params(self):
        """Test creating request with query params object."""
        query_params = TokensListQueryParams(page=2, limit=50)
        request = TokensListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_create_request_with_defaults(self):
        """Test creating request with default query params."""
        request = TokensListRequest()
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params object."""
        query_params = TokensListQueryParams(page=3, limit=75)
        request = TokensListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {'page': 3, 'limit': 75}
        assert result == expected


class TestTokenGetRequest:
    """Test TokenGetRequest model."""

    def test_valid_token_id(self):
        """Test with valid token ID."""
        request = TokenGetRequest(token_id="token123")
        assert request.token_id == "token123"


class TestTokenCreateRequest:
    """Test TokenCreateRequest model."""

    def test_valid_request(self):
        """Test with valid parameters."""
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full", "domains_read"]
        )
        assert request.name == "Test Token"
        assert request.domain_id == "domain123"
        assert request.scopes == ["email_full", "domains_read"]

    def test_name_validation(self):
        """Test name validation."""
        # Empty name
        with pytest.raises(ValidationError, match="Token name cannot be empty"):
            TokenCreateRequest(
                name="",
                domain_id="domain123",
                scopes=["email_full"]
            )

        # Whitespace-only name
        with pytest.raises(ValidationError, match="Token name cannot be empty"):
            TokenCreateRequest(
                name="   ",
                domain_id="domain123",
                scopes=["email_full"]
            )

    def test_name_trimming(self):
        """Test name is trimmed."""
        request = TokenCreateRequest(
            name="  Test Token  ",
            domain_id="domain123",
            scopes=["email_full"]
        )
        assert request.name == "Test Token"

    def test_domain_id_validation(self):
        """Test domain_id validation."""
        # Empty domain_id
        with pytest.raises(ValidationError, match="Domain ID cannot be empty"):
            TokenCreateRequest(
                name="Test Token",
                domain_id="",
                scopes=["email_full"]
            )

        # Whitespace-only domain_id
        with pytest.raises(ValidationError, match="Domain ID cannot be empty"):
            TokenCreateRequest(
                name="Test Token",
                domain_id="   ",
                scopes=["email_full"]
            )

    def test_domain_id_trimming(self):
        """Test domain_id is trimmed."""
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="  domain123  ",
            scopes=["email_full"]
        )
        assert request.domain_id == "domain123"

    def test_scopes_validation(self):
        """Test scopes validation."""
        # Empty scopes
        with pytest.raises(ValidationError):
            TokenCreateRequest(
                name="Test Token",
                domain_id="domain123",
                scopes=[]
            )

        # Invalid scopes
        with pytest.raises(ValidationError, match="Invalid scopes"):
            TokenCreateRequest(
                name="Test Token",
                domain_id="domain123",
                scopes=["invalid_scope"]
            )

    def test_to_json(self):
        """Test to_json method."""
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full", "domains_read"]
        )
        result = request.to_json()
        expected = {
            "name": "Test Token",
            "domain_id": "domain123",
            "scopes": ["email_full", "domains_read"]
        }
        assert result == expected


class TestTokenUpdateRequest:
    """Test TokenUpdateRequest model."""

    def test_valid_request(self):
        """Test with valid parameters."""
        request = TokenUpdateRequest(token_id="token123", status="pause")
        assert request.token_id == "token123"
        assert request.status == "pause"

    def test_to_json(self):
        """Test to_json method."""
        request = TokenUpdateRequest(token_id="token123", status="unpause")
        result = request.to_json()
        expected = {"status": "unpause"}
        assert result == expected


class TestTokenUpdateNameRequest:
    """Test TokenUpdateNameRequest model."""

    def test_valid_request(self):
        """Test with valid parameters."""
        request = TokenUpdateNameRequest(token_id="token123", name="New Name")
        assert request.token_id == "token123"
        assert request.name == "New Name"

    def test_name_validation(self):
        """Test name validation."""
        # Empty name
        with pytest.raises(ValidationError, match="Token name cannot be empty"):
            TokenUpdateNameRequest(token_id="token123", name="")

        # Whitespace-only name
        with pytest.raises(ValidationError, match="Token name cannot be empty"):
            TokenUpdateNameRequest(token_id="token123", name="   ")

    def test_name_trimming(self):
        """Test name is trimmed."""
        request = TokenUpdateNameRequest(token_id="token123", name="  New Name  ")
        assert request.name == "New Name"

    def test_to_json(self):
        """Test to_json method."""
        request = TokenUpdateNameRequest(token_id="token123", name="Updated Name")
        result = request.to_json()
        expected = {"name": "Updated Name"}
        assert result == expected


class TestTokenDeleteRequest:
    """Test TokenDeleteRequest model."""

    def test_valid_request(self):
        """Test with valid token ID."""
        request = TokenDeleteRequest(token_id="token123")
        assert request.token_id == "token123" 