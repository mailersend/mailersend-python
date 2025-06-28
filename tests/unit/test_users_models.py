"""Tests for Users API models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.users import (
    User, UserDomain, UserTemplate, UserInvite, UserInviteData,
    UsersListRequest, UserGetRequest, UserInviteRequest, UserUpdateRequest,
    UserDeleteRequest, InvitesListRequest, InviteGetRequest,
    InviteResendRequest, InviteCancelRequest, UsersListResponse,
    UserResponse, UserInviteResponse, UserUpdateResponse,
    InvitesListResponse, InviteResponse, InviteResendResponse,
    UsersListQueryParams, InvitesListQueryParams
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
            "role": "Admin"
        }
        user = User(**user_data)
        assert user.id == "user123"
        assert user.email == "user@example.com"
        assert user.role == "Admin"
        assert user.twofa is False  # default value
        assert user.permissions == []
        assert user.domains == []
        assert user.templates == []

    def test_user_with_2fa_alias(self):
        """Test User with 2fa field alias."""
        user_data = {
            "id": "user123",
            "email": "user@example.com",
            "2fa": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "role": "Admin"
        }
        user = User(**user_data)
        assert user.twofa is True

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

    def test_user_invite_data_empty(self):
        """Test UserInviteData with empty lists."""
        data = UserInviteData()
        assert data.domains == []
        assert data.templates == []

    def test_user_invite_data_with_values(self):
        """Test UserInviteData with values."""
        data = UserInviteData(
            domains=["domain1", "domain2"],
            templates=["template1", "template2"]
        )
        assert len(data.domains) == 2
        assert len(data.templates) == 2


class TestUserInvite:
    """Test UserInvite model."""

    def test_user_invite_minimal(self):
        """Test UserInvite with minimal fields."""
        invite_data = {
            "id": "invite123",
            "email": "user@example.com",
            "role": "Admin",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        invite = UserInvite(**invite_data)
        assert invite.id == "invite123"
        assert invite.email == "user@example.com"
        assert invite.role == "Admin"
        assert invite.permissions == []
        assert invite.data is None
        assert invite.requires_periodic_password_change is None

    def test_user_invite_complete(self):
        """Test UserInvite with all fields."""
        invite_data = {
            "id": "invite123",
            "email": "user@example.com",
            "data": {
                "domains": ["domain1"],
                "templates": ["template1"]
            },
            "role": "Custom User",
            "permissions": ["read-templates"],
            "requires_periodic_password_change": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        invite = UserInvite(**invite_data)
        assert isinstance(invite.data, UserInviteData)
        assert len(invite.data.domains) == 1
        assert len(invite.data.templates) == 1
        assert invite.requires_periodic_password_change is True


class TestUserInviteRequest:
    """Test UserInviteRequest model."""

    def test_user_invite_request_minimal(self):
        """Test UserInviteRequest with minimal fields."""
        request = UserInviteRequest(
            email="user@example.com",
            role="Admin"
        )
        assert request.email == "user@example.com"
        assert request.role == "Admin"
        assert request.permissions == []
        assert request.templates == []
        assert request.domains == []
        assert request.requires_periodic_password_change is None

    def test_user_invite_request_complete(self):
        """Test UserInviteRequest with all fields."""
        request = UserInviteRequest(
            email="user@example.com",
            role="Custom User",
            permissions=["read-templates", "manage-domain"],
            templates=["template1", "template2"],
            domains=["domain1", "domain2"],
            requires_periodic_password_change=True
        )
        assert len(request.permissions) == 2
        assert len(request.templates) == 2
        assert len(request.domains) == 2
        assert request.requires_periodic_password_change is True

    def test_user_invite_request_email_validation(self):
        """Test email validation in UserInviteRequest."""
        # Valid email
        request = UserInviteRequest(email="user@example.com", role="Admin")
        assert request.email == "user@example.com"

        # Invalid email - no @ symbol
        with pytest.raises(ValidationError) as exc_info:
            UserInviteRequest(email="invalid-email", role="Admin")
        assert "Invalid email address" in str(exc_info.value)

        # Empty email
        with pytest.raises(ValidationError) as exc_info:
            UserInviteRequest(email="", role="Admin")
        assert "Invalid email address" in str(exc_info.value)

    def test_user_invite_request_email_max_length(self):
        """Test email max length validation."""
        long_email = "a" * 180 + "@example.com"  # 192 chars total
        with pytest.raises(ValidationError) as exc_info:
            UserInviteRequest(email=long_email, role="Admin")
        assert "at most 191 characters" in str(exc_info.value)

    def test_user_invite_request_role_validation(self):
        """Test role validation in UserInviteRequest."""
        # Valid role
        request = UserInviteRequest(email="user@example.com", role="Admin")
        assert request.role == "Admin"

        # Empty role
        with pytest.raises(ValidationError) as exc_info:
            UserInviteRequest(email="user@example.com", role="")
        assert "Role cannot be empty" in str(exc_info.value)

        # Whitespace only role
        with pytest.raises(ValidationError) as exc_info:
            UserInviteRequest(email="user@example.com", role="   ")
        assert "Role cannot be empty" in str(exc_info.value)


class TestUserUpdateRequest:
    """Test UserUpdateRequest model."""

    def test_user_update_request_minimal(self):
        """Test UserUpdateRequest with minimal fields."""
        request = UserUpdateRequest(
            user_id="user123",
            role="Manager"
        )
        assert request.user_id == "user123"
        assert request.role == "Manager"
        assert request.permissions == []
        assert request.templates == []
        assert request.domains == []
        assert request.requires_periodic_password_change is None

    def test_user_update_request_complete(self):
        """Test UserUpdateRequest with all fields."""
        request = UserUpdateRequest(
            user_id="user123",
            role="Custom User",
            permissions=["read-templates"],
            templates=["template1"],
            domains=["domain1"],
            requires_periodic_password_change=False
        )
        assert request.user_id == "user123"
        assert request.role == "Custom User"
        assert len(request.permissions) == 1
        assert len(request.templates) == 1
        assert len(request.domains) == 1
        assert request.requires_periodic_password_change is False

    def test_user_update_request_role_validation(self):
        """Test role validation in UserUpdateRequest."""
        with pytest.raises(ValidationError) as exc_info:
            UserUpdateRequest(user_id="user123", role="")
        assert "Role cannot be empty" in str(exc_info.value)


class TestUsersListQueryParams:
    """Test UsersListQueryParams model."""

    def test_users_list_query_params_defaults(self):
        """Test UsersListQueryParams with default values."""
        params = UsersListQueryParams()
        assert params.page == 1
        assert params.limit == 25

    def test_users_list_query_params_custom_values(self):
        """Test UsersListQueryParams with custom values."""
        params = UsersListQueryParams(page=2, limit=50)
        assert params.page == 2
        assert params.limit == 50

    def test_users_list_query_params_validation(self):
        """Test UsersListQueryParams validation."""
        # Valid values
        params = UsersListQueryParams(page=1, limit=10)
        assert params.page == 1
        assert params.limit == 10

        # Invalid page (< 1)
        with pytest.raises(ValidationError):
            UsersListQueryParams(page=0)

        # Invalid limit (< 10)
        with pytest.raises(ValidationError):
            UsersListQueryParams(limit=9)

        # Invalid limit (> 100)
        with pytest.raises(ValidationError):
            UsersListQueryParams(limit=101)

    def test_users_list_query_params_to_query_params_defaults(self):
        """Test to_query_params with default values."""
        params = UsersListQueryParams()
        query_params = params.to_query_params()
        # Should return empty dict when values are defaults
        assert query_params == {}

    def test_users_list_query_params_to_query_params_custom(self):
        """Test to_query_params with custom values."""
        params = UsersListQueryParams(page=2, limit=50)
        query_params = params.to_query_params()
        assert query_params == {"page": 2, "limit": 50}


class TestInvitesListQueryParams:
    """Test InvitesListQueryParams model."""

    def test_invites_list_query_params_defaults(self):
        """Test InvitesListQueryParams with default values."""
        params = InvitesListQueryParams()
        assert params.page == 1
        assert params.limit == 25

    def test_invites_list_query_params_custom_values(self):
        """Test InvitesListQueryParams with custom values."""
        params = InvitesListQueryParams(page=3, limit=15)
        assert params.page == 3
        assert params.limit == 15

    def test_invites_list_query_params_validation(self):
        """Test InvitesListQueryParams validation."""
        # Valid values
        params = InvitesListQueryParams(page=1, limit=10)
        assert params.page == 1
        assert params.limit == 10

        # Invalid page (< 1)
        with pytest.raises(ValidationError):
            InvitesListQueryParams(page=0)

        # Invalid limit (< 10)
        with pytest.raises(ValidationError):
            InvitesListQueryParams(limit=9)

        # Invalid limit (> 100)
        with pytest.raises(ValidationError):
            InvitesListQueryParams(limit=101)

    def test_invites_list_query_params_to_query_params_defaults(self):
        """Test to_query_params with default values."""
        params = InvitesListQueryParams()
        query_params = params.to_query_params()
        # Should return empty dict when values are defaults
        assert query_params == {}

    def test_invites_list_query_params_to_query_params_custom(self):
        """Test to_query_params with custom values."""
        params = InvitesListQueryParams(page=4, limit=75)
        query_params = params.to_query_params()
        assert query_params == {"page": 4, "limit": 75}


class TestRequestModels:
    """Test other request models."""

    def test_users_list_request(self):
        """Test UsersListRequest model."""
        request = UsersListRequest()
        assert request is not None
        assert hasattr(request, 'query_params')
        assert isinstance(request.query_params, UsersListQueryParams)

    def test_users_list_request_with_custom_params(self):
        """Test UsersListRequest with custom query params."""
        query_params = UsersListQueryParams(page=2, limit=50)
        request = UsersListRequest(query_params=query_params)
        assert request.query_params.page == 2
        assert request.query_params.limit == 50

    def test_users_list_request_to_query_params(self):
        """Test UsersListRequest to_query_params method."""
        query_params = UsersListQueryParams(page=3, limit=20)
        request = UsersListRequest(query_params=query_params)
        result = request.to_query_params()
        assert result == {"page": 3, "limit": 20}

    def test_user_get_request(self):
        """Test UserGetRequest model."""
        request = UserGetRequest(user_id="user123")
        assert request.user_id == "user123"

    def test_user_delete_request(self):
        """Test UserDeleteRequest model."""
        request = UserDeleteRequest(user_id="user123")
        assert request.user_id == "user123"

    def test_invites_list_request(self):
        """Test InvitesListRequest model."""
        request = InvitesListRequest()
        assert request is not None
        assert hasattr(request, 'query_params')
        assert isinstance(request.query_params, InvitesListQueryParams)

    def test_invites_list_request_with_custom_params(self):
        """Test InvitesListRequest with custom query params."""
        query_params = InvitesListQueryParams(page=5, limit=10)
        request = InvitesListRequest(query_params=query_params)
        assert request.query_params.page == 5
        assert request.query_params.limit == 10

    def test_invites_list_request_to_query_params(self):
        """Test InvitesListRequest to_query_params method."""
        query_params = InvitesListQueryParams(page=2, limit=30)
        request = InvitesListRequest(query_params=query_params)
        result = request.to_query_params()
        assert result == {"page": 2, "limit": 30}

    def test_invite_get_request(self):
        """Test InviteGetRequest model."""
        request = InviteGetRequest(invite_id="invite123")
        assert request.invite_id == "invite123"

    def test_invite_resend_request(self):
        """Test InviteResendRequest model."""
        request = InviteResendRequest(invite_id="invite123")
        assert request.invite_id == "invite123"

    def test_invite_cancel_request(self):
        """Test InviteCancelRequest model."""
        request = InviteCancelRequest(invite_id="invite123")
        assert request.invite_id == "invite123"


class TestResponseModels:
    """Test response models."""

    def test_users_list_response(self):
        """Test UsersListResponse model."""
        user_data = {
            "id": "user123",
            "email": "user@example.com",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "role": "Admin"
        }
        response = UsersListResponse(data=[user_data])
        assert len(response.data) == 1
        assert isinstance(response.data[0], User)

    def test_user_response(self):
        """Test UserResponse model."""
        user_data = {
            "id": "user123",
            "email": "user@example.com",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "role": "Admin"
        }
        response = UserResponse(data=user_data)
        assert isinstance(response.data, User)
        assert response.data.id == "user123"

    def test_user_invite_response(self):
        """Test UserInviteResponse model."""
        invite_data = {
            "id": "invite123",
            "email": "user@example.com",
            "role": "Admin",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        response = UserInviteResponse(data=invite_data)
        assert isinstance(response.data, UserInvite)
        assert response.data.id == "invite123"

    def test_user_update_response(self):
        """Test UserUpdateResponse model."""
        user_data = {
            "id": "user123",
            "email": "user@example.com",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "role": "Manager"
        }
        response = UserUpdateResponse(data=user_data)
        assert isinstance(response.data, User)
        assert response.data.role == "Manager"

    def test_invites_list_response(self):
        """Test InvitesListResponse model."""
        invite_data = {
            "id": "invite123",
            "email": "user@example.com",
            "role": "Admin",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        response = InvitesListResponse(data=[invite_data])
        assert len(response.data) == 1
        assert isinstance(response.data[0], UserInvite)

    def test_invite_response(self):
        """Test InviteResponse model."""
        invite_data = {
            "id": "invite123",
            "email": "user@example.com",
            "role": "Admin",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        response = InviteResponse(data=invite_data)
        assert isinstance(response.data, UserInvite)
        assert response.data.id == "invite123"

    def test_invite_resend_response(self):
        """Test InviteResendResponse model."""
        invite_data = {
            "id": "invite123",
            "email": "user@example.com",
            "role": "Admin",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        response = InviteResendResponse(data=invite_data)
        assert isinstance(response.data, UserInvite)
        assert response.data.id == "invite123" 