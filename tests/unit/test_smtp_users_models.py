"""Tests for SMTP Users models."""

import pytest
from pydantic import ValidationError

from mailersend.models.smtp_users import (
    SmtpUsersListQueryParams,
    SmtpUsersListRequest,
    SmtpUserGetRequest,
    SmtpUserCreateRequest,
    SmtpUserUpdateRequest,
    SmtpUserDeleteRequest,
)


class TestSmtpUsersListQueryParams:
    """Test SmtpUsersListQueryParams model."""

    def test_smtp_users_list_query_params_defaults(self):
        """Test SmtpUsersListQueryParams with default values."""
        params = SmtpUsersListQueryParams()

        assert params.limit == 25

    def test_smtp_users_list_query_params_custom_values(self):
        """Test SmtpUsersListQueryParams with custom values."""
        params = SmtpUsersListQueryParams(limit=50)

        assert params.limit == 50

    def test_smtp_users_list_query_params_limit_validation(self):
        """Test SmtpUsersListQueryParams limit validation."""
        # Test minimum limit
        with pytest.raises(ValidationError):
            SmtpUsersListQueryParams(limit=9)

        # Test maximum limit
        with pytest.raises(ValidationError):
            SmtpUsersListQueryParams(limit=101)

        # Test valid boundary values
        params_min = SmtpUsersListQueryParams(limit=10)
        assert params_min.limit == 10

        params_max = SmtpUsersListQueryParams(limit=100)
        assert params_max.limit == 100

    def test_to_query_params_default_limit(self):
        """Test to_query_params with default limit."""
        params = SmtpUsersListQueryParams()
        result = params.to_query_params()

        # Default limit should not be included
        assert result == {}

    def test_to_query_params_custom_limit(self):
        """Test to_query_params with custom limit."""
        params = SmtpUsersListQueryParams(limit=50)
        result = params.to_query_params()

        assert result == {"limit": 50}


class TestSmtpUsersListRequest:
    """Test SmtpUsersListRequest model."""

    def test_smtp_users_list_request_basic(self):
        """Test basic SmtpUsersListRequest creation."""
        request = SmtpUsersListRequest(domain_id="test-domain")

        assert request.domain_id == "test-domain"
        assert isinstance(request.query_params, SmtpUsersListQueryParams)
        assert request.query_params.limit == 25  # default

    def test_smtp_users_list_request_with_query_params(self):
        """Test SmtpUsersListRequest with custom query params."""
        query_params = SmtpUsersListQueryParams(limit=50)
        request = SmtpUsersListRequest(
            domain_id="test-domain", query_params=query_params
        )

        assert request.domain_id == "test-domain"
        assert request.query_params.limit == 50

    def test_smtp_users_list_request_domain_id_validation(self):
        """Test SmtpUsersListRequest domain_id validation."""
        # Empty domain_id
        with pytest.raises(ValidationError):
            SmtpUsersListRequest(domain_id="")

        # Whitespace-only domain_id
        with pytest.raises(ValidationError, match="Domain ID cannot be empty"):
            SmtpUsersListRequest(domain_id="   ")

    def test_smtp_users_list_request_domain_id_trimming(self):
        """Test SmtpUsersListRequest domain_id trimming."""
        request = SmtpUsersListRequest(domain_id="  test-domain  ")
        assert request.domain_id == "test-domain"

    def test_to_query_params_delegation(self):
        """Test to_query_params delegates to query_params."""
        query_params = SmtpUsersListQueryParams(limit=75)
        request = SmtpUsersListRequest(
            domain_id="test-domain", query_params=query_params
        )

        result = request.to_query_params()
        assert result == {"limit": 75}


class TestSmtpUserGetRequest:
    """Test SmtpUserGetRequest model."""

    def test_smtp_user_get_request_basic(self):
        """Test basic SmtpUserGetRequest creation."""
        request = SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="user123")

        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"

    def test_smtp_user_get_request_validation(self):
        """Test SmtpUserGetRequest validation."""
        # Empty domain_id
        with pytest.raises(ValidationError):
            SmtpUserGetRequest(domain_id="", smtp_user_id="user123")
        # Empty smtp_user_id
        with pytest.raises(ValidationError):
            SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="")
        # Whitespace domain_id
        with pytest.raises(ValidationError):
            SmtpUserGetRequest(domain_id="   ", smtp_user_id="user123")
        # Whitespace smtp_user_id
        with pytest.raises(ValidationError):
            SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="   ")

    def test_smtp_user_get_request_trimming(self):
        """Test SmtpUserGetRequest trimming."""
        request = SmtpUserGetRequest(
            domain_id="  test-domain  ", smtp_user_id="  user123  "
        )
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"


class TestSmtpUserCreateRequest:
    """Test SmtpUserCreateRequest model."""

    def test_smtp_user_create_request_basic(self):
        """Test basic SmtpUserCreateRequest creation."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User")

        assert request.domain_id == "test-domain"
        assert request.name == "Test User"
        assert request.enabled is None

    def test_smtp_user_create_request_with_enabled(self):
        """Test SmtpUserCreateRequest creation with enabled flag."""
        request = SmtpUserCreateRequest(
            domain_id="test-domain", name="Test User", enabled=True
        )

        assert request.domain_id == "test-domain"
        assert request.name == "Test User"
        assert request.enabled is True

    def test_smtp_user_create_request_name_validation(self):
        """Test SmtpUserCreateRequest name validation."""
        # Empty name
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="test-domain", name="")
        # Whitespace name
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="test-domain", name="   ")
        # Name too long
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="test-domain", name="a" * 51)
        # Valid maximum length
        request = SmtpUserCreateRequest(domain_id="test-domain", name="a" * 50)
        assert request.name == "a" * 50

    def test_smtp_user_create_request_name_trimming(self):
        """Test SmtpUserCreateRequest name trimming."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="  Test User  ")
        assert request.name == "Test User"

    def test_smtp_user_create_request_domain_id_validation(self):
        """Test SmtpUserCreateRequest domain_id validation."""
        # Empty domain_id
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="", name="Test User")
        # Whitespace domain_id
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="   ", name="Test User")

    def test_smtp_user_create_request_domain_id_trimming(self):
        """Test SmtpUserCreateRequest domain_id trimming."""
        request = SmtpUserCreateRequest(domain_id="  test-domain  ", name="Test User")
        assert request.domain_id == "test-domain"

    def test_to_json_basic(self):
        """Test to_json with basic request."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User")
        result = request.to_json()

        assert result == {"name": "Test User"}

    def test_to_json_with_enabled(self):
        """Test to_json with enabled flag."""
        request = SmtpUserCreateRequest(
            domain_id="test-domain", name="Test User", enabled=False
        )
        result = request.to_json()

        assert result == {"name": "Test User", "enabled": False}


class TestSmtpUserUpdateRequest:
    """Test SmtpUserUpdateRequest model."""

    def test_smtp_user_update_request_basic(self):
        """Test basic SmtpUserUpdateRequest creation."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", smtp_user_id="user123", name="Updated User"
        )

        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
        assert request.name == "Updated User"
        assert request.enabled is None

    def test_smtp_user_update_request_with_enabled(self):
        """Test SmtpUserUpdateRequest creation with enabled flag."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain",
            smtp_user_id="user123",
            name="Updated User",
            enabled=True,
        )

        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
        assert request.name == "Updated User"
        assert request.enabled is True

    def test_smtp_user_update_request_validation(self):
        """Test SmtpUserUpdateRequest validation."""
        # Empty domain_id
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(domain_id="", smtp_user_id="user123", name="Test")
        # Empty smtp_user_id
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(domain_id="test-domain", smtp_user_id="", name="Test")

        # Empty name
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(
                domain_id="test-domain", smtp_user_id="user123", name=""
            )
        # Whitespace name
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(
                domain_id="test-domain", smtp_user_id="user123", name="   "
            )
        # Name too long
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(
                domain_id="test-domain", smtp_user_id="user123", name="a" * 51
            )

    def test_smtp_user_update_request_trimming(self):
        """Test SmtpUserUpdateRequest trimming."""
        request = SmtpUserUpdateRequest(
            domain_id="  test-domain  ",
            smtp_user_id="  user123  ",
            name="  Updated User  ",
        )

        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
        assert request.name == "Updated User"

    def test_to_json_basic(self):
        """Test to_json with basic request."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", smtp_user_id="user123", name="Updated User"
        )
        result = request.to_json()

        assert result == {"name": "Updated User"}

    def test_to_json_with_enabled(self):
        """Test to_json with enabled flag."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain",
            smtp_user_id="user123",
            name="Updated User",
            enabled=True,
        )
        result = request.to_json()

        assert result == {"name": "Updated User", "enabled": True}


class TestSmtpUserDeleteRequest:
    """Test SmtpUserDeleteRequest model."""

    def test_smtp_user_delete_request_basic(self):
        """Test basic SmtpUserDeleteRequest creation."""
        request = SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="user123")

        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"

    def test_smtp_user_delete_request_validation(self):
        """Test SmtpUserDeleteRequest validation."""
        # Empty domain_id
        with pytest.raises(ValidationError):
            SmtpUserDeleteRequest(domain_id="", smtp_user_id="user123")
        # Empty smtp_user_id
        with pytest.raises(ValidationError):
            SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="")

    def test_smtp_user_delete_request_trimming(self):
        """Test SmtpUserDeleteRequest trimming."""
        request = SmtpUserDeleteRequest(
            domain_id="  test-domain  ", smtp_user_id="  user123  "
        )

        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
