"""Tests for Users API resource."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from mailersend.resources.users import Users
from mailersend.models.base import APIResponse
from mailersend.models.users import (
    UsersListRequest, UserGetRequest, UserInviteRequest, UserUpdateRequest, UserDeleteRequest,
    InvitesListRequest, InviteGetRequest, InviteResendRequest, InviteCancelRequest,
    UsersListQueryParams, InvitesListQueryParams
)


class TestUsersResource:
    """Test Users resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        
        # Create properly configured response mock with complete user data
        self.mock_response = Mock()
        self.mock_response.headers = {"x-request-id": "abc123", "x-apiquota-remaining": "100"}
        self.mock_response.status_code = 200
        self.mock_response.content = b'{"data": []}'
        
        # Set different response data based on the endpoint
        self.user_data = {
            "id": "123",
            "email": "test@test.com",
            "last_name": "User",
            "name": "Test",
            "avatar": None,
            "2fa": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "role": "Admin",
            "permissions": [],
            "domains": [],
            "templates": []
        }
        
        self.invite_data = {
            "id": "456",
            "email": "invite@test.com",
            "data": None,
            "role": "Admin", 
            "permissions": [],
            "requires_periodic_password_change": None,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
        
        # Default to list response
        self.mock_response.json.return_value = {"data": [self.user_data]}
        
        self.client.request = Mock(return_value=self.mock_response)
        self.users = Users(self.client)

    def _set_single_user_response(self):
        """Set response for single user."""
        self.mock_response.json.return_value = {"data": self.user_data}

    def _set_single_invite_response(self):
        """Set response for single invite."""
        self.mock_response.json.return_value = {"data": self.invite_data}

    def _set_invites_list_response(self):
        """Set response for invites list."""
        self.mock_response.json.return_value = {"data": [self.invite_data]}

    def test_list_users(self):
        """Test list_users method."""
        request = UsersListRequest()
        response = self.users.list_users(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/users",
            params={}
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_list_users_with_pagination(self):
        """Test list_users method with pagination."""
        query_params = UsersListQueryParams(page=2, limit=50)
        request = UsersListRequest(query_params=query_params)
        response = self.users.list_users(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/users",
            params={"page": 2, "limit": 50}
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_get_user(self):
        """Test get_user method."""
        self._set_single_user_response()
        request = UserGetRequest(user_id="user123")
        response = self.users.get_user(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/users/user123"
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_invite_user_minimal(self):
        """Test invite_user method with minimal parameters."""
        self._set_single_invite_response()
        request = UserInviteRequest(email="user@example.com", role="Admin")
        
        response = self.users.invite_user(request)
        
        # Verify client.request was called correctly
        expected_json = {
            "email": "user@example.com",
            "role": "Admin",
            "permissions": [],
            "templates": [],
            "domains": []
        }
        
        self.client.request.assert_called_once_with(
            method="POST",
            endpoint="/v1/users",
            json=expected_json
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_invite_user_complete(self):
        """Test invite_user method with all parameters."""
        self._set_single_invite_response()
        request = UserInviteRequest(
            email="user@example.com",
            role="Custom User",
            permissions=["read-templates", "manage-domain"],
            templates=["template1", "template2"],
            domains=["domain1", "domain2"],
            requires_periodic_password_change=True
        )
        
        response = self.users.invite_user(request)
        
        # Verify client.request was called correctly
        expected_json = {
            "email": "user@example.com",
            "role": "Custom User",
            "permissions": ["read-templates", "manage-domain"],
            "templates": ["template1", "template2"],
            "domains": ["domain1", "domain2"],
            "requires_periodic_password_change": True
        }
        
        self.client.request.assert_called_once_with(
            method="POST",
            endpoint="/v1/users",
            json=expected_json
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_invite_user_without_periodic_password_change(self):
        """Test invite_user method without requires_periodic_password_change."""
        self._set_single_invite_response()
        request = UserInviteRequest(email="user@example.com", role="Admin")
        
        response = self.users.invite_user(request)
        
        # Verify requires_periodic_password_change is not included when None
        call_args = self.client.request.call_args
        json_data = call_args[1]['json']
        assert 'requires_periodic_password_change' not in json_data

    def test_update_user_minimal(self):
        """Test update_user method with minimal parameters."""
        self._set_single_user_response()
        request = UserUpdateRequest(user_id="user123", role="Manager")
        
        response = self.users.update_user(request)
        
        # Verify client.request was called correctly
        expected_json = {
            "role": "Manager",
            "permissions": [],
            "templates": [],
            "domains": []
        }
        
        self.client.request.assert_called_once_with(
            method="PUT",
            endpoint="/v1/users/user123",
            json=expected_json
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_update_user_complete(self):
        """Test update_user method with all parameters."""
        self._set_single_user_response()
        request = UserUpdateRequest(
            user_id="user123",
            role="Custom User",
            permissions=["read-templates"],
            templates=["template1"],
            domains=["domain1"],
            requires_periodic_password_change=False
        )
        
        response = self.users.update_user(request)
        
        # Verify client.request was called correctly
        expected_json = {
            "role": "Custom User",
            "permissions": ["read-templates"],
            "templates": ["template1"],
            "domains": ["domain1"],
            "requires_periodic_password_change": False
        }
        
        self.client.request.assert_called_once_with(
            method="PUT",
            endpoint="/v1/users/user123",
            json=expected_json
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_delete_user(self):
        """Test delete_user method."""
        request = UserDeleteRequest(user_id="user123")
        response = self.users.delete_user(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="DELETE",
            endpoint="/v1/users/user123"
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_list_invites(self):
        """Test list_invites method."""
        self._set_invites_list_response()
        request = InvitesListRequest()
        response = self.users.list_invites(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/invites",
            params={}
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_list_invites_with_pagination(self):
        """Test list_invites method with pagination."""
        self._set_invites_list_response()
        query_params = InvitesListQueryParams(page=3, limit=15)
        request = InvitesListRequest(query_params=query_params)
        response = self.users.list_invites(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/invites",
            params={"page": 3, "limit": 15}
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_get_invite(self):
        """Test get_invite method."""
        self._set_single_invite_response()
        request = InviteGetRequest(invite_id="invite123")
        response = self.users.get_invite(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/invites/invite123"
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_resend_invite(self):
        """Test resend_invite method."""
        self._set_single_invite_response()
        request = InviteResendRequest(invite_id="invite123")
        response = self.users.resend_invite(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="POST",
            endpoint="/v1/invites/invite123/resend"
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)

    def test_cancel_invite(self):
        """Test cancel_invite method."""
        request = InviteCancelRequest(invite_id="invite123")
        response = self.users.cancel_invite(request)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="DELETE",
            endpoint="/v1/invites/invite123"
        )
        
        # Verify response is APIResponse type
        assert isinstance(response, APIResponse)


class TestUsersResourceLogging:
    """Test Users resource logging functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        
        # Create properly configured response mock with complete data
        self.mock_response = Mock()
        self.mock_response.headers = {"x-request-id": "abc123"}
        self.mock_response.status_code = 200
        self.mock_response.content = b'{"data": []}'
        
        # Set different response data based on the endpoint
        self.user_data = {
            "id": "123",
            "email": "test@test.com",
            "last_name": "User",
            "name": "Test",
            "avatar": None,
            "2fa": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "role": "Admin",
            "permissions": [],
            "domains": [],
            "templates": []
        }
        
        self.invite_data = {
            "id": "456",
            "email": "invite@test.com",
            "data": None,
            "role": "Admin", 
            "permissions": [],
            "requires_periodic_password_change": None,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
        
        # Default to list response
        self.mock_response.json.return_value = {"data": [self.user_data]}
        
        self.client.request = Mock(return_value=self.mock_response)
        self.users = Users(self.client)

    def _set_single_user_response(self):
        """Set response for single user."""
        self.mock_response.json.return_value = {"data": self.user_data}

    def _set_single_invite_response(self):
        """Set response for single invite."""
        self.mock_response.json.return_value = {"data": self.invite_data}

    def _set_invites_list_response(self):
        """Set response for invites list."""
        self.mock_response.json.return_value = {"data": [self.invite_data]}

    @patch('mailersend.resources.users.logger')
    def test_list_users_logging(self, mock_logger):
        """Test list_users method logging."""
        request = UsersListRequest()
        self.users.list_users(request)
        mock_logger.info.assert_called_once_with("Listing users with pagination: page=1, limit=25")

    @patch('mailersend.resources.users.logger')
    def test_get_user_logging(self, mock_logger):
        """Test get_user method logging."""
        self._set_single_user_response()
        request = UserGetRequest(user_id="user123")
        self.users.get_user(request)
        mock_logger.info.assert_called_once_with("Getting user: user123")

    @patch('mailersend.resources.users.logger')
    def test_invite_user_logging(self, mock_logger):
        """Test invite_user method logging."""
        self._set_single_invite_response()
        request = UserInviteRequest(email="user@example.com", role="Admin")
        self.users.invite_user(request)
        mock_logger.info.assert_called_once_with("Inviting user: user@example.com with role: Admin")

    @patch('mailersend.resources.users.logger')
    def test_update_user_logging(self, mock_logger):
        """Test update_user method logging."""
        self._set_single_user_response()
        request = UserUpdateRequest(user_id="user123", role="Manager")
        self.users.update_user(request)
        mock_logger.info.assert_called_once_with("Updating user: user123 with role: Manager")

    @patch('mailersend.resources.users.logger')
    def test_delete_user_logging(self, mock_logger):
        """Test delete_user method logging."""
        request = UserDeleteRequest(user_id="user123")
        self.users.delete_user(request)
        mock_logger.info.assert_called_once_with("Deleting user: user123")

    @patch('mailersend.resources.users.logger')
    def test_list_invites_logging(self, mock_logger):
        """Test list_invites method logging."""
        self._set_invites_list_response()
        request = InvitesListRequest()
        self.users.list_invites(request)
        mock_logger.info.assert_called_once_with("Listing invites with pagination: page=1, limit=25")

    @patch('mailersend.resources.users.logger')
    def test_get_invite_logging(self, mock_logger):
        """Test get_invite method logging."""
        self._set_single_invite_response()
        request = InviteGetRequest(invite_id="invite123")
        self.users.get_invite(request)
        mock_logger.info.assert_called_once_with("Getting invite: invite123")

    @patch('mailersend.resources.users.logger')
    def test_resend_invite_logging(self, mock_logger):
        """Test resend_invite method logging."""
        self._set_single_invite_response()
        request = InviteResendRequest(invite_id="invite123")
        self.users.resend_invite(request)
        mock_logger.info.assert_called_once_with("Resending invite: invite123")

    @patch('mailersend.resources.users.logger')
    def test_cancel_invite_logging(self, mock_logger):
        """Test cancel_invite method logging."""
        request = InviteCancelRequest(invite_id="invite123")
        self.users.cancel_invite(request)
        mock_logger.info.assert_called_once_with("Canceling invite: invite123") 