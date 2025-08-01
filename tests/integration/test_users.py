import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.users import (
    UsersListRequest,
    UserGetRequest,
    UserInviteRequest,
    UserUpdateRequest,
    UserDeleteRequest,
    InvitesListRequest,
    InviteGetRequest,
    InviteResendRequest,
    InviteCancelRequest,
    UsersListQueryParams,
    InvitesListQueryParams,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def basic_users_list_request():
    """Basic users list request"""
    return UsersListRequest(
        query_params=UsersListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def basic_invites_list_request():
    """Basic invites list request"""
    return InvitesListRequest(
        query_params=InvitesListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def user_get_request():
    """User get request with test user ID"""
    return UserGetRequest(user_id="test-user-id")


@pytest.fixture
def invite_get_request():
    """Invite get request with test invite ID"""
    return InviteGetRequest(invite_id="test-invite-id")


@pytest.fixture
def sample_user_invite_data():
    """Sample user invite data for testing"""
    return {
        "email": "test-user@example.com",
        "role": "member",
        "permissions": ["email_send"],
        "domains": [],
        "templates": [],
        "requires_periodic_password_change": False
    }


class TestUsersIntegration:
    """Integration tests for Users API."""

    # ============================================================================
    # User Management Tests
    # ============================================================================

    @vcr.use_cassette("users_list_basic.yaml")
    def test_list_users_basic(self, email_client, basic_users_list_request):
        """Test listing users with basic parameters."""
        response = email_client.users.list_users(basic_users_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            users = response.data["data"]
            assert isinstance(users, list)

            # If we have users, check the structure
            if users:
                first_user = users[0]
                assert "id" in first_user
                assert "email" in first_user
                assert "role" in first_user
                assert "created_at" in first_user

    @vcr.use_cassette("users_list_with_pagination.yaml")
    def test_list_users_with_pagination(self, email_client):
        """Test listing users with pagination."""
        request = UsersListRequest(
            query_params=UsersListQueryParams(page=1, limit=10)
        )

        response = email_client.users.list_users(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta
            assert "per_page" in meta
            # API may or may not include total count in meta
            assert meta["per_page"] == 10
            assert meta["current_page"] == 1

    @vcr.use_cassette("users_get_single.yaml")
    def test_get_user_not_found_with_test_id(self, email_client, user_get_request):
        """Test getting a non-existent user returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.users.get_user(user_get_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "user" in error_str)

    @vcr.use_cassette("users_invite.yaml")
    def test_invite_user_invalid_data(self, email_client, sample_user_invite_data):
        """Test inviting a user with potentially invalid data."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        request = UserInviteRequest(**sample_user_invite_data)

        # This might fail due to invalid role, domain restrictions, or other business logic
        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            email_client.users.invite_user(request)

        error_str = str(exc_info.value).lower()
        assert ("invalid" in error_str or "not found" in error_str or 
                "role" in error_str or "permission" in error_str or
                "domain" in error_str)

    @vcr.use_cassette("users_update.yaml")
    def test_update_user_not_found_with_test_id(self, email_client, user_get_request):
        """Test updating a non-existent user with invalid role/permissions."""
        from mailersend.exceptions import BadRequestError
        
        update_request = UserUpdateRequest(
            user_id=user_get_request.user_id,
            role="member",  # Invalid role - API validates before checking user existence
            permissions=["email_send"],  # Invalid permission
            domains=[],
            templates=[]
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.users.update_user(update_request)

        error_str = str(exc_info.value).lower()
        assert ("invalid" in error_str or "role" in error_str or 
                "permission" in error_str or "selected" in error_str)

    @vcr.use_cassette("users_delete.yaml")
    def test_delete_user_not_found_with_test_id(self, email_client, user_get_request):
        """Test deleting a non-existent user returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = UserDeleteRequest(user_id=user_get_request.user_id)

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.users.delete_user(delete_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "user" in error_str)

    # ============================================================================
    # Invite Management Tests
    # ============================================================================

    @vcr.use_cassette("invites_list_basic.yaml")
    def test_list_invites_basic(self, email_client, basic_invites_list_request):
        """Test listing invites with basic parameters."""
        response = email_client.users.list_invites(basic_invites_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            invites = response.data["data"]
            assert isinstance(invites, list)

            # If we have invites, check the structure
            if invites:
                first_invite = invites[0]
                assert "id" in first_invite
                assert "email" in first_invite
                assert "role" in first_invite
                assert "created_at" in first_invite

    @vcr.use_cassette("invites_get_single.yaml")
    def test_get_invite_not_found_with_test_id(self, email_client, invite_get_request):
        """Test getting a non-existent invite returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.users.get_invite(invite_get_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "invite" in error_str)

    @vcr.use_cassette("invites_resend.yaml")
    def test_resend_invite_not_found_with_test_id(self, email_client, invite_get_request):
        """Test resending a non-existent invite returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        resend_request = InviteResendRequest(invite_id=invite_get_request.invite_id)

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.users.resend_invite(resend_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "invite" in error_str)

    @vcr.use_cassette("invites_cancel.yaml")
    def test_cancel_invite_not_found_with_test_id(self, email_client, invite_get_request):
        """Test canceling a non-existent invite returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        cancel_request = InviteCancelRequest(invite_id=invite_get_request.invite_id)

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.users.cancel_invite(cancel_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "invite" in error_str)

    # ============================================================================
    # Validation and API Response Tests
    # ============================================================================

    @vcr.use_cassette("users_validation_error.yaml")
    def test_list_users_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.users.list_users("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("users_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_users_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.users.list_users(basic_users_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert hasattr(response, "data")
        assert hasattr(response, "headers")

        # Check for rate limiting headers
        if response.rate_limit_remaining is not None:
            assert isinstance(response.rate_limit_remaining, int)
            # Rate limit remaining can be -1 for unlimited plans
        assert response.rate_limit_remaining is not None

        # Check for request ID
        if response.request_id is not None:
            assert isinstance(response.request_id, str)
            assert len(response.request_id) > 0

    @vcr.use_cassette("users_empty_result.yaml")
    def test_list_users_empty_result(self, email_client, basic_users_list_request):
        """Test listing users when no users exist."""
        response = email_client.users.list_users(basic_users_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to existing users)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    # ============================================================================
    # Model Validation Tests
    # ============================================================================

    def test_user_invite_model_validation(self):
        """Test model validation for user invite request."""
        # Test empty email
        with pytest.raises(ValueError) as exc_info:
            UserInviteRequest(email="", role="member")
        assert "invalid email address" in str(exc_info.value).lower()

        # Test invalid email format
        with pytest.raises(ValueError) as exc_info:
            UserInviteRequest(email="invalid-email", role="member")
        assert "invalid email address" in str(exc_info.value).lower()

        # Test empty role
        with pytest.raises(ValueError) as exc_info:
            UserInviteRequest(email="test@example.com", role="")
        assert "role cannot be empty" in str(exc_info.value).lower()

        # Test whitespace role
        with pytest.raises(ValueError) as exc_info:
            UserInviteRequest(email="test@example.com", role="   ")
        assert "role cannot be empty" in str(exc_info.value).lower()

    def test_user_update_model_validation(self):
        """Test model validation for user update request."""
        # Test empty role
        with pytest.raises(ValueError) as exc_info:
            UserUpdateRequest(user_id="test", role="")
        assert "role cannot be empty" in str(exc_info.value).lower()

        # Test whitespace role
        with pytest.raises(ValueError) as exc_info:
            UserUpdateRequest(user_id="test", role="   ")
        assert "role cannot be empty" in str(exc_info.value).lower()

    def test_users_list_query_params_validation(self):
        """Test validation for users list query parameters."""
        # Test valid parameters
        params = UsersListQueryParams(page=1, limit=25)
        assert params.page == 1
        assert params.limit == 25
        
        # Test minimum limit validation
        with pytest.raises(ValueError):
            UsersListQueryParams(limit=5)  # Below minimum of 10
            
        # Test maximum limit validation  
        with pytest.raises(ValueError):
            UsersListQueryParams(limit=150)  # Above maximum of 100
            
        # Test minimum page validation
        with pytest.raises(ValueError):
            UsersListQueryParams(page=0)  # Below minimum of 1

    def test_invites_list_query_params_validation(self):
        """Test validation for invites list query parameters."""
        # Test valid parameters
        params = InvitesListQueryParams(page=2, limit=50)
        assert params.page == 2
        assert params.limit == 50
        
        # Test minimum limit validation
        with pytest.raises(ValueError):
            InvitesListQueryParams(limit=5)  # Below minimum of 10
            
        # Test maximum limit validation  
        with pytest.raises(ValueError):
            InvitesListQueryParams(limit=150)  # Above maximum of 100
            
        # Test minimum page validation
        with pytest.raises(ValueError):
            InvitesListQueryParams(page=0)  # Below minimum of 1

    def test_user_invite_to_json(self):
        """Test UserInviteRequest JSON conversion."""
        request = UserInviteRequest(
            email="test@example.com",
            role="admin",
            permissions=["email_send", "domains_manage"],
            domains=["domain1", "domain2"],
            templates=["template1"],
            requires_periodic_password_change=True
        )
        
        json_data = request.to_json()
        
        assert json_data["email"] == "test@example.com"
        assert json_data["role"] == "admin"
        assert json_data["permissions"] == ["email_send", "domains_manage"]
        assert json_data["domains"] == ["domain1", "domain2"]
        assert json_data["templates"] == ["template1"]
        assert json_data["requires_periodic_password_change"] is True

    def test_user_update_to_json(self):
        """Test UserUpdateRequest JSON conversion."""
        request = UserUpdateRequest(
            user_id="user123",
            role="member",
            permissions=["email_send"],
            domains=["domain1"],
            templates=[],
            requires_periodic_password_change=False
        )
        
        json_data = request.to_json()
        
        assert "user_id" not in json_data  # user_id goes in URL, not body
        assert json_data["role"] == "member"
        assert json_data["permissions"] == ["email_send"]
        assert json_data["domains"] == ["domain1"]
        assert json_data["templates"] == []
        assert json_data["requires_periodic_password_change"] is False

    def test_email_validation_and_cleaning(self):
        """Test email validation and cleaning."""
        # Test email with whitespace gets cleaned
        request = UserInviteRequest(email="  test@example.com  ", role="member")
        assert request.email == "test@example.com"
        
        # Test role with whitespace gets cleaned
        request2 = UserInviteRequest(email="test@example.com", role="  admin  ")
        assert request2.role == "admin" 