"""Unit tests for Users resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.users import Users
from mailersend.models.base import APIResponse
from mailersend.models.users import (
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
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestUsers:
    """Test Users resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = Users(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_users_returns_api_response(self):
        """Test list_users method returns APIResponse."""
        query_params = UsersListQueryParams()
        request = UsersListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_users(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_users_with_custom_pagination(self):
        """Test list_users with custom pagination parameters."""
        query_params = UsersListQueryParams(page=2, limit=50)
        request = UsersListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_users(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", endpoint="users", params={"page": 2, "limit": 50}
        )
        assert result == self.mock_api_response

    def test_get_user_returns_api_response(self):
        """Test get_user method returns APIResponse."""
        request = UserGetRequest(user_id="user123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_user(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", endpoint="users/user123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_invite_user_returns_api_response(self):
        """Test invite_user method returns APIResponse."""
        request = UserInviteRequest(
            email="test@example.com",
            role="Manager",
            permissions=["read-templates"],
            templates=["template1"],
            domains=["domain1"],
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.invite_user(request)

        expected_body = {
            "email": "test@example.com",
            "role": "Manager",
            "permissions": ["read-templates"],
            "templates": ["template1"],
            "domains": ["domain1"],
        }

        self.mock_client.request.assert_called_once_with(
            method="POST", endpoint="users", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_user_returns_api_response(self):
        """Test update_user method returns APIResponse."""
        request = UserUpdateRequest(
            user_id="user123",
            role="Manager",
            permissions=["read-templates"],
            templates=["template1"],
            domains=["domain1"],
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_user(request)

        expected_body = {
            "role": "Manager",
            "permissions": ["read-templates"],
            "templates": ["template1"],
            "domains": ["domain1"],
        }

        self.mock_client.request.assert_called_once_with(
            method="PUT", endpoint="users/user123", body=expected_body
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_user_returns_api_response(self):
        """Test delete_user method returns APIResponse."""
        request = UserDeleteRequest(user_id="user123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_user(request)

        self.mock_client.request.assert_called_once_with(
            method="DELETE", endpoint="users/user123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response, None)

    def test_list_invites_returns_api_response(self):
        """Test list_invites method returns APIResponse."""
        query_params = InvitesListQueryParams()
        request = InvitesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_invites(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_invite_returns_api_response(self):
        """Test get_invite method returns APIResponse."""
        request = InviteGetRequest(invite_id="invite123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_invite(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", endpoint="invites/invite123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_resend_invite_returns_api_response(self):
        """Test resend_invite method returns APIResponse."""
        request = InviteResendRequest(invite_id="invite123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.resend_invite(request)

        self.mock_client.request.assert_called_once_with(
            method="POST", endpoint="invites/invite123/resend"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_cancel_invite_returns_api_response(self):
        """Test cancel_invite method returns APIResponse."""
        request = InviteCancelRequest(invite_id="invite123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.cancel_invite(request)

        self.mock_client.request.assert_called_once_with(
            method="DELETE", endpoint="invites/invite123"
        )
        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response, None)
