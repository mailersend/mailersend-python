"""Tests for Users models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.users import (
    User,
    UserDomain,
    UserTemplate,
    UserInvite,
    UserInviteData,
    UsersListRequest,
    UsersListQueryParams,
    UserGetRequest,
    UserInviteRequest,
    UserUpdateRequest,
    UserDeleteRequest,
    InvitesListRequest,
    InvitesListQueryParams,
    InviteGetRequest,
    InviteResendRequest,
    InviteCancelRequest,
)


class TestUserDomain:
    """Test UserDomain model."""

    def test_user_domain_valid(self):
        """Test valid UserDomain creation."""
        domain_data = {
            "id": "domain123",
            "name": "example.com",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        domain = UserDomain(**domain_data)
        assert domain.id == "domain123"
        assert domain.name == "example.com"
        assert isinstance(domain.created_at, datetime)
        assert isinstance(domain.updated_at, datetime)


class TestUserTemplate:
    """Test UserTemplate model."""

    def test_user_template_valid(self):
        """Test valid UserTemplate creation."""
        template_data = {
            "id": "template123",
            "name": "My Template",
            "type": "html",
            "created_at": "2024-01-01T00:00:00Z"
        }
        template = UserTemplate(**template_data)
        assert template.id == "template123"
        assert template.name == "My Template"
        assert template.type == "html"
        assert isinstance(template.created_at, datetime)


class TestUser:
    """Test User model."""

    def test_user_minimal(self):
        """Test User with minimal required fields."""
        user_data = {
            "id": "user123",
            "email": "user@example.com",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "role": "Custom User"
        }
        user = User(**user_data)
        assert user.id == "user123"
        assert user.email == "user@example.com"
        assert user.last_name is None
        assert user.name is None
        assert user.avatar is None
        assert user.twofa is False
        assert user.role == "Custom User"
        assert user.permissions == []
        assert user.domains == []
        assert user.templates == []

    def test_user_complete(self):
        """Test User with all fields."""
        user_data = {
            "id": "user123",
            "email": "user@example.com",
            "last_name": "Doe",
            "name": "John",
            "avatar": "avatar.jpg",
            "2fa": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "role": "Custom User",
            "permissions": ["read-templates", "manage-domain"],
            "domains": [
                {
                    "id": "domain123",
                    "name": "example.com",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                }
            ],
            "templates": [
                {
                    "id": "template123",
                    "name": "My Template",
                    "type": "html",
                    "created_at": "2024-01-01T00:00:00Z"
                }
            ]
        }
        user = User(**user_data)
        assert user.name == "John"
        assert user.last_name == "Doe"
        assert user.avatar == "avatar.jpg"
        assert user.twofa is True
        assert len(user.permissions) == 2
        assert len(user.domains) == 1
        assert len(user.templates) == 1
        assert isinstance(user.domains[0], UserDomain)
        assert isinstance(user.templates[0], UserTemplate)


class TestUserInviteData:
    """Test UserInviteData model."""

    def test_user_invite_data_minimal(self):
        """Test UserInviteData with empty lists."""
        invite_data = UserInviteData()
        assert invite_data.domains == []
        assert invite_data.templates == []

    def test_user_invite_data_with_data(self):
        """Test UserInviteData with data."""
        invite_data = UserInviteData(
            domains=["domain1", "domain2"],
            templates=["template1", "template2"]
        )
        assert invite_data.domains == ["domain1", "domain2"]
        assert invite_data.templates == ["template1", "template2"]


class TestUserInvite:
    """Test UserInvite model."""

    def test_user_invite_minimal(self):
        """Test UserInvite with minimal fields."""
        invite_data = {
            "id": "invite123",
            "email": "invite@example.com",
            "role": "Custom User",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        invite = UserInvite(**invite_data)
        assert invite.id == "invite123"
        assert invite.email == "invite@example.com"
        assert invite.role == "Custom User"
        assert invite.data is None
        assert invite.permissions == []
        assert invite.requires_periodic_password_change is None

    def test_user_invite_complete(self):
        """Test UserInvite with all fields."""
        invite_data = {
            "id": "invite123",
            "email": "invite@example.com",
            "data": {
                "domains": ["domain1"],
                "templates": ["template1"]
            },
            "role": "Manager",
            "permissions": ["read-templates"],
            "requires_periodic_password_change": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        invite = UserInvite(**invite_data)
        assert invite.role == "Manager"
        assert isinstance(invite.data, UserInviteData)
        assert invite.data.domains == ["domain1"]
        assert invite.permissions == ["read-templates"]
        assert invite.requires_periodic_password_change is True


class TestUsersListQueryParams:
    """Test UsersListQueryParams model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        query_params = UsersListQueryParams()
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test setting custom values."""
        query_params = UsersListQueryParams(page=2, limit=50)
        assert query_params.page == 2
        assert query_params.limit == 50

    def test_validation(self):
        """Test validation constraints."""
        # Page must be >= 1
        with pytest.raises(ValidationError):
            UsersListQueryParams(page=0)

        # Limit must be 10-100
        with pytest.raises(ValidationError):
            UsersListQueryParams(limit=9)

        with pytest.raises(ValidationError):
            UsersListQueryParams(limit=101)

    def test_to_query_params_with_defaults(self):
        """Test to_query_params excludes default values."""
        query_params = UsersListQueryParams()
        result = query_params.to_query_params()
        assert result == {}

    def test_to_query_params_with_custom_values(self):
        """Test to_query_params with custom values."""
        query_params = UsersListQueryParams(page=3, limit=50)
        result = query_params.to_query_params()
        expected = {'page': 3, 'limit': 50}
        assert result == expected


class TestInvitesListQueryParams:
    """Test InvitesListQueryParams model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        query_params = InvitesListQueryParams()
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test setting custom values."""
        query_params = InvitesListQueryParams(page=2, limit=50)
        assert query_params.page == 2
        assert query_params.limit == 50

    def test_to_query_params_excludes_defaults(self):
        """Test to_query_params excludes default values."""
        query_params = InvitesListQueryParams()
        result = query_params.to_query_params()
        assert result == {}


class TestUsersListRequest:
    """Test UsersListRequest model."""

    def test_create_request_with_defaults(self):
        """Test creating request with default query params."""
        request = UsersListRequest()
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_create_request_with_query_params(self):
        """Test creating request with custom query params."""
        query_params = UsersListQueryParams(page=2, limit=50)
        request = UsersListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params object."""
        query_params = UsersListQueryParams(page=3, limit=75)
        request = UsersListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {'page': 3, 'limit': 75}
        assert result == expected


class TestUserGetRequest:
    """Test UserGetRequest model."""

    def test_valid_user_id(self):
        """Test with valid user ID."""
        request = UserGetRequest(user_id="user123")
        assert request.user_id == "user123"


class TestUserInviteRequest:
    """Test UserInviteRequest model."""

    def test_valid_request(self):
        """Test with valid parameters."""
        request = UserInviteRequest(
            email="test@example.com",
            role="Manager",
            permissions=["read-templates"],
            templates=["template1"],
            domains=["domain1"]
        )
        assert request.email == "test@example.com"
        assert request.role == "Manager"
        assert request.permissions == ["read-templates"]
        assert request.templates == ["template1"]
        assert request.domains == ["domain1"]
        assert request.requires_periodic_password_change is None

    def test_email_validation(self):
        """Test email validation."""
        # Empty email
        with pytest.raises(ValidationError, match="Invalid email address"):
            UserInviteRequest(email="", role="Manager")

        # Invalid email format
        with pytest.raises(ValidationError, match="Invalid email address"):
            UserInviteRequest(email="invalid-email", role="Manager")

    def test_email_trimming(self):
        """Test email is trimmed."""
        request = UserInviteRequest(email="  test@example.com  ", role="Manager")
        assert request.email == "test@example.com"

    def test_role_validation(self):
        """Test role validation."""
        # Empty role
        with pytest.raises(ValidationError, match="Role cannot be empty"):
            UserInviteRequest(email="test@example.com", role="")

    def test_role_trimming(self):
        """Test role is trimmed."""
        request = UserInviteRequest(email="test@example.com", role="  Manager  ")
        assert request.role == "Manager"

    def test_to_json(self):
        """Test to_json method."""
        request = UserInviteRequest(
            email="test@example.com",
            role="Manager",
            permissions=["read-templates"],
            templates=["template1"],
            domains=["domain1"],
            requires_periodic_password_change=True
        )
        result = request.to_json()
        expected = {
            "email": "test@example.com",
            "role": "Manager",
            "permissions": ["read-templates"],
            "templates": ["template1"],
            "domains": ["domain1"],
            "requires_periodic_password_change": True
        }
        assert result == expected

    def test_to_json_without_optional_field(self):
        """Test to_json without requires_periodic_password_change."""
        request = UserInviteRequest(email="test@example.com", role="Manager")
        result = request.to_json()
        expected = {
            "email": "test@example.com",
            "role": "Manager",
            "permissions": [],
            "templates": [],
            "domains": [],
        }
        assert result == expected


class TestUserUpdateRequest:
    """Test UserUpdateRequest model."""

    def test_valid_request(self):
        """Test with valid parameters."""
        request = UserUpdateRequest(
            user_id="user123",
            role="Manager",
            permissions=["read-templates"],
            templates=["template1"],
            domains=["domain1"]
        )
        assert request.user_id == "user123"
        assert request.role == "Manager"
        assert request.permissions == ["read-templates"]

    def test_role_validation(self):
        """Test role validation."""
        # Empty role
        with pytest.raises(ValidationError, match="Role cannot be empty"):
            UserUpdateRequest(user_id="user123", role="")

    def test_role_trimming(self):
        """Test role is trimmed."""
        request = UserUpdateRequest(user_id="user123", role="  Manager  ")
        assert request.role == "Manager"

    def test_to_json(self):
        """Test to_json method."""
        request = UserUpdateRequest(
            user_id="user123",
            role="Manager",
            permissions=["read-templates"],
            templates=["template1"],
            domains=["domain1"],
            requires_periodic_password_change=False
        )
        result = request.to_json()
        expected = {
            "role": "Manager",
            "permissions": ["read-templates"],
            "templates": ["template1"],
            "domains": ["domain1"],
            "requires_periodic_password_change": False
        }
        assert result == expected


class TestUserDeleteRequest:
    """Test UserDeleteRequest model."""

    def test_valid_user_id(self):
        """Test with valid user ID."""
        request = UserDeleteRequest(user_id="user123")
        assert request.user_id == "user123"


class TestInvitesListRequest:
    """Test InvitesListRequest model."""

    def test_create_request_with_defaults(self):
        """Test creating request with default query params."""
        request = InvitesListRequest()
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params object."""
        query_params = InvitesListQueryParams(page=2, limit=50)
        request = InvitesListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {'page': 2, 'limit': 50}
        assert result == expected


class TestInviteGetRequest:
    """Test InviteGetRequest model."""

    def test_valid_invite_id(self):
        """Test with valid invite ID."""
        request = InviteGetRequest(invite_id="invite123")
        assert request.invite_id == "invite123"


class TestInviteResendRequest:
    """Test InviteResendRequest model."""

    def test_valid_invite_id(self):
        """Test with valid invite ID."""
        request = InviteResendRequest(invite_id="invite123")
        assert request.invite_id == "invite123"


class TestInviteCancelRequest:
    """Test InviteCancelRequest model."""

    def test_valid_invite_id(self):
        """Test with valid invite ID."""
        request = InviteCancelRequest(invite_id="invite123")
        assert request.invite_id == "invite123" 