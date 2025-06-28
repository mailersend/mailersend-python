"""Tests for tokens models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.tokens import (
    TOKEN_SCOPES,
    Token,
    TokenCreate,
    TokensListRequest,
    TokenGetRequest,
    TokenCreateRequest,
    TokenUpdateRequest,
    TokenUpdateNameRequest,
    TokenDeleteRequest,
    TokensListResponse,
    TokenResponse,
    TokenCreateResponse,
)


class TestTokensListRequest:
    """Test TokensListRequest model."""

    def test_basic_creation(self):
        """Test basic request creation."""
        request = TokensListRequest()
        assert request.page is None
        assert request.limit == 25  # Default value

    def test_with_pagination(self):
        """Test request with pagination parameters."""
        request = TokensListRequest(page=2, limit=50)
        assert request.page == 2
        assert request.limit == 50

    def test_page_validation(self):
        """Test page validation."""
        with pytest.raises(ValidationError) as exc_info:
            TokensListRequest(page=0)
        assert "Input should be greater than or equal to 1" in str(exc_info.value)

    def test_limit_validation_minimum(self):
        """Test limit minimum validation."""
        with pytest.raises(ValidationError) as exc_info:
            TokensListRequest(limit=5)
        assert "Input should be greater than or equal to 10" in str(exc_info.value)

    def test_limit_validation_maximum(self):
        """Test limit maximum validation."""
        with pytest.raises(ValidationError) as exc_info:
            TokensListRequest(limit=150)
        assert "Input should be less than or equal to 100" in str(exc_info.value)

    def test_limit_boundaries(self):
        """Test limit boundary values."""
        # Minimum allowed
        request = TokensListRequest(limit=10)
        assert request.limit == 10
        
        # Maximum allowed
        request = TokensListRequest(limit=100)
        assert request.limit == 100


class TestTokenGetRequest:
    """Test TokenGetRequest model."""

    def test_basic_creation(self):
        """Test basic request creation."""
        request = TokenGetRequest(token_id="test_token_id")
        assert request.token_id == "test_token_id"

    def test_empty_token_id(self):
        """Test empty token_id."""
        request = TokenGetRequest(token_id="")
        assert request.token_id == ""


class TestTokenCreateRequest:
    """Test TokenCreateRequest model."""

    def test_basic_creation(self):
        """Test basic request creation."""
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="domain123",
            scopes=["email_full"]
        )
        assert request.name == "Test Token"
        assert request.domain_id == "domain123"
        assert request.scopes == ["email_full"]

    def test_name_max_length(self):
        """Test name maximum length validation."""
        # Exactly 50 characters should be valid
        name_50 = "x" * 50
        request = TokenCreateRequest(
            name=name_50,
            domain_id="domain123",
            scopes=["email_full"]
        )
        assert request.name == name_50

        # 51 characters should fail
        name_51 = "x" * 51
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name=name_51,
                domain_id="domain123",
                scopes=["email_full"]
            )
        assert "String should have at most 50 characters" in str(exc_info.value)

    def test_name_trimming(self):
        """Test name trimming."""
        request = TokenCreateRequest(
            name="  Test Token  ",
            domain_id="domain123",
            scopes=["email_full"]
        )
        assert request.name == "Test Token"

    def test_empty_name_validation(self):
        """Test empty name validation."""
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="",
                domain_id="domain123",
                scopes=["email_full"]
            )
        assert "Token name cannot be empty" in str(exc_info.value)

    def test_whitespace_name_validation(self):
        """Test whitespace-only name validation."""
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="   ",
                domain_id="domain123",
                scopes=["email_full"]
            )
        assert "Token name cannot be empty" in str(exc_info.value)

    def test_domain_id_trimming(self):
        """Test domain_id trimming."""
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="  domain123  ",
            scopes=["email_full"]
        )
        assert request.domain_id == "domain123"

    def test_empty_domain_id_validation(self):
        """Test empty domain_id validation."""
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="Test Token",
                domain_id="",
                scopes=["email_full"]
            )
        assert "Domain ID cannot be empty" in str(exc_info.value)

    def test_scopes_validation_empty_list(self):
        """Test scopes validation with empty list."""
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="Test Token",
                domain_id="domain123",
                scopes=[]
            )
        # Could be either min_length or the custom validator
        error_str = str(exc_info.value)
        assert ("List should have at least 1 item" in error_str or 
                "At least one scope is required" in error_str)

    def test_scopes_validation_invalid_scope(self):
        """Test scopes validation with invalid scope."""
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="Test Token",
                domain_id="domain123",
                scopes=["invalid_scope"]
            )
        assert "Invalid scopes: ['invalid_scope']" in str(exc_info.value)

    def test_scopes_validation_mixed_valid_invalid(self):
        """Test scopes validation with mixed valid and invalid scopes."""
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="Test Token",
                domain_id="domain123",
                scopes=["email_full", "invalid_scope", "tokens_full"]
            )
        assert "Invalid scopes: ['invalid_scope']" in str(exc_info.value)

    def test_all_valid_scopes(self):
        """Test all valid scopes."""
        request = TokenCreateRequest(
            name="Test Token",
            domain_id="domain123",
            scopes=TOKEN_SCOPES
        )
        assert set(request.scopes) == set(TOKEN_SCOPES)


class TestTokenUpdateRequest:
    """Test TokenUpdateRequest model."""

    def test_basic_creation_pause(self):
        """Test basic request creation with pause."""
        request = TokenUpdateRequest(
            token_id="token123",
            status="pause"
        )
        assert request.token_id == "token123"
        assert request.status == "pause"

    def test_basic_creation_unpause(self):
        """Test basic request creation with unpause."""
        request = TokenUpdateRequest(
            token_id="token123",
            status="unpause"
        )
        assert request.token_id == "token123"
        assert request.status == "unpause"

    def test_invalid_status(self):
        """Test invalid status validation."""
        with pytest.raises(ValidationError) as exc_info:
            TokenUpdateRequest(
                token_id="token123",
                status="invalid"
            )
        assert "Input should be 'pause' or 'unpause'" in str(exc_info.value)


class TestTokenUpdateNameRequest:
    """Test TokenUpdateNameRequest model."""

    def test_basic_creation(self):
        """Test basic request creation."""
        request = TokenUpdateNameRequest(
            token_id="token123",
            name="New Token Name"
        )
        assert request.token_id == "token123"
        assert request.name == "New Token Name"

    def test_name_validation(self):
        """Test name validation."""
        # Max length
        name_50 = "x" * 50
        request = TokenUpdateNameRequest(
            token_id="token123",
            name=name_50
        )
        assert request.name == name_50

        # Over max length
        with pytest.raises(ValidationError) as exc_info:
            TokenUpdateNameRequest(
                token_id="token123",
                name="x" * 51
            )
        assert "String should have at most 50 characters" in str(exc_info.value)

    def test_name_trimming(self):
        """Test name trimming."""
        request = TokenUpdateNameRequest(
            token_id="token123",
            name="  New Name  "
        )
        assert request.name == "New Name"

    def test_empty_name_validation(self):
        """Test empty name validation."""
        with pytest.raises(ValidationError) as exc_info:
            TokenUpdateNameRequest(
                token_id="token123",
                name=""
            )
        assert "Token name cannot be empty" in str(exc_info.value)


class TestTokenDeleteRequest:
    """Test TokenDeleteRequest model."""

    def test_basic_creation(self):
        """Test basic request creation."""
        request = TokenDeleteRequest(token_id="token123")
        assert request.token_id == "token123"


class TestToken:
    """Test Token model."""

    def test_basic_creation(self):
        """Test basic token creation."""
        token = Token(
            id="token123",
            name="Test Token",
            status="unpause",
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            scopes=["email_full", "domains_read"]
        )
        assert token.id == "token123"
        assert token.name == "Test Token"
        assert token.status == "unpause"
        assert token.created_at == datetime(2024, 1, 1, 12, 0, 0)
        assert token.scopes == ["email_full", "domains_read"]

    def test_empty_scopes_list(self):
        """Test token with empty scopes list."""
        token = Token(
            id="token123",
            name="Test Token",
            status="pause",
            created_at=datetime(2024, 1, 1, 12, 0, 0)
        )
        assert token.scopes == []  # Default empty list

    def test_invalid_status(self):
        """Test invalid status."""
        with pytest.raises(ValidationError) as exc_info:
            Token(
                id="token123",
                name="Test Token",
                status="invalid",
                created_at=datetime(2024, 1, 1, 12, 0, 0)
            )
        assert "Input should be 'pause' or 'unpause'" in str(exc_info.value)


class TestTokenCreate:
    """Test TokenCreate model."""

    def test_basic_creation(self):
        """Test basic token create model."""
        token_create = TokenCreate(
            id="token123",
            accessToken="secret_token_value",
            name="Test Token",
            created_at=datetime(2024, 1, 1, 12, 0, 0)
        )
        assert token_create.id == "token123"
        assert token_create.accessToken == "secret_token_value"
        assert token_create.name == "Test Token"
        assert token_create.created_at == datetime(2024, 1, 1, 12, 0, 0)

    def test_field_access(self):
        """Test field access for accessToken."""
        token_create = TokenCreate(
            id="token123",
            accessToken="secret_token_value",
            name="Test Token",
            created_at=datetime(2024, 1, 1, 12, 0, 0)
        )
        assert token_create.accessToken == "secret_token_value"


class TestResponseModels:
    """Test response models."""

    def test_tokens_list_response(self):
        """Test TokensListResponse model."""
        tokens = [
            Token(
                id="token1",
                name="Token 1",
                status="unpause",
                created_at=datetime(2024, 1, 1, 12, 0, 0)
            ),
            Token(
                id="token2",
                name="Token 2",
                status="pause",
                created_at=datetime(2024, 1, 2, 12, 0, 0)
            )
        ]
        response = TokensListResponse(data=tokens)
        assert len(response.data) == 2
        assert response.data[0].id == "token1"
        assert response.data[1].id == "token2"

    def test_token_response(self):
        """Test TokenResponse model."""
        token = Token(
            id="token123",
            name="Test Token",
            status="unpause",
            created_at=datetime(2024, 1, 1, 12, 0, 0)
        )
        response = TokenResponse(data=token)
        assert response.data.id == "token123"
        assert response.data.name == "Test Token"

    def test_token_create_response(self):
        """Test TokenCreateResponse model."""
        token_create = TokenCreate(
            id="token123",
            accessToken="secret_value",
            name="Test Token",
            created_at=datetime(2024, 1, 1, 12, 0, 0)
        )
        response = TokenCreateResponse(data=token_create)
        assert response.data.id == "token123"
        assert response.data.accessToken == "secret_value"


class TestTokenConstants:
    """Test token constants."""

    def test_token_scopes_count(self):
        """Test that all expected scopes are present."""
        expected_scopes = [
            "email_full",
            "domains_read",
            "domains_full", 
            "activity_read",
            "activity_full",
            "analytics_read",
            "analytics_full",
            "tokens_full",
            "webhooks_full",
            "templates_full",
            "suppressions_read",
            "suppressions_full",
            "sms_full",
            "sms_read",
            "email_verification_read",
            "email_verification_full",
            "inbounds_full",
            "recipients_read",
            "recipients_full",
            "sender_identity_read",
            "sender_identity_full",
            "users_read",
            "users_full",
            "smtp_users_read",
            "smtp_users_full"
        ]
        assert len(TOKEN_SCOPES) == 25
        assert set(TOKEN_SCOPES) == set(expected_scopes)

    def test_token_scopes_uniqueness(self):
        """Test that all scopes are unique."""
        assert len(TOKEN_SCOPES) == len(set(TOKEN_SCOPES)) 