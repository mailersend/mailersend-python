"""Tests for Users API resource."""

import pytest
from unittest.mock import Mock, patch

from mailersend.resources.users import Users
from mailersend.models.base import APIResponse


class TestUsersResource:
    """Test Users resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.client.request = Mock(return_value=Mock(spec=APIResponse))
        self.users = Users(self.client)

    def test_list_users(self):
        """Test list_users method."""
        response = self.users.list_users()
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/users"
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_get_user(self):
        """Test get_user method."""
        user_id = "user123"
        response = self.users.get_user(user_id)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint=f"/v1/users/{user_id}"
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_invite_user_minimal(self):
        """Test invite_user method with minimal parameters."""
        email = "user@example.com"
        role = "Admin"
        
        response = self.users.invite_user(email, role)
        
        # Verify client.request was called correctly
        expected_json = {
            "email": email,
            "role": role,
            "permissions": [],
            "templates": [],
            "domains": []
        }
        
        self.client.request.assert_called_once_with(
            method="POST",
            endpoint="/v1/users",
            json=expected_json
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_invite_user_complete(self):
        """Test invite_user method with all parameters."""
        email = "user@example.com"
        role = "Custom User"
        permissions = ["read-templates", "manage-domain"]
        templates = ["template1", "template2"]
        domains = ["domain1", "domain2"]
        requires_periodic_password_change = True
        
        response = self.users.invite_user(
            email=email,
            role=role,
            permissions=permissions,
            templates=templates,
            domains=domains,
            requires_periodic_password_change=requires_periodic_password_change
        )
        
        # Verify client.request was called correctly
        expected_json = {
            "email": email,
            "role": role,
            "permissions": permissions,
            "templates": templates,
            "domains": domains,
            "requires_periodic_password_change": requires_periodic_password_change
        }
        
        self.client.request.assert_called_once_with(
            method="POST",
            endpoint="/v1/users",
            json=expected_json
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_invite_user_without_periodic_password_change(self):
        """Test invite_user method without requires_periodic_password_change."""
        email = "user@example.com"
        role = "Admin"
        
        response = self.users.invite_user(email, role)
        
        # Verify requires_periodic_password_change is not included when None
        call_args = self.client.request.call_args
        json_data = call_args[1]['json']
        assert 'requires_periodic_password_change' not in json_data

    def test_update_user_minimal(self):
        """Test update_user method with minimal parameters."""
        user_id = "user123"
        role = "Manager"
        
        response = self.users.update_user(user_id, role)
        
        # Verify client.request was called correctly
        expected_json = {
            "role": role,
            "permissions": [],
            "templates": [],
            "domains": []
        }
        
        self.client.request.assert_called_once_with(
            method="PUT",
            endpoint=f"/v1/users/{user_id}",
            json=expected_json
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_update_user_complete(self):
        """Test update_user method with all parameters."""
        user_id = "user123"
        role = "Custom User"
        permissions = ["read-templates"]
        templates = ["template1"]
        domains = ["domain1"]
        requires_periodic_password_change = False
        
        response = self.users.update_user(
            user_id=user_id,
            role=role,
            permissions=permissions,
            templates=templates,
            domains=domains,
            requires_periodic_password_change=requires_periodic_password_change
        )
        
        # Verify client.request was called correctly
        expected_json = {
            "role": role,
            "permissions": permissions,
            "templates": templates,
            "domains": domains,
            "requires_periodic_password_change": requires_periodic_password_change
        }
        
        self.client.request.assert_called_once_with(
            method="PUT",
            endpoint=f"/v1/users/{user_id}",
            json=expected_json
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_delete_user(self):
        """Test delete_user method."""
        user_id = "user123"
        response = self.users.delete_user(user_id)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="DELETE",
            endpoint=f"/v1/users/{user_id}"
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_list_invites(self):
        """Test list_invites method."""
        response = self.users.list_invites()
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/invites"
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_get_invite(self):
        """Test get_invite method."""
        invite_id = "invite123"
        response = self.users.get_invite(invite_id)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="GET",
            endpoint=f"/v1/invites/{invite_id}"
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_resend_invite(self):
        """Test resend_invite method."""
        invite_id = "invite123"
        response = self.users.resend_invite(invite_id)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="POST",
            endpoint=f"/v1/invites/{invite_id}/resend"
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value

    def test_cancel_invite(self):
        """Test cancel_invite method."""
        invite_id = "invite123"
        response = self.users.cancel_invite(invite_id)
        
        # Verify client.request was called correctly
        self.client.request.assert_called_once_with(
            method="DELETE",
            endpoint=f"/v1/invites/{invite_id}"
        )
        
        # Verify response is returned
        assert response == self.client.request.return_value


class TestUsersResourceLogging:
    """Test Users resource logging functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.client.request = Mock(return_value=Mock(spec=APIResponse))
        self.users = Users(self.client)

    @patch('mailersend.resources.users.logger')
    def test_list_users_logging(self, mock_logger):
        """Test list_users method logging."""
        self.users.list_users()
        mock_logger.info.assert_called_once_with("Listing account users")

    @patch('mailersend.resources.users.logger')
    def test_get_user_logging(self, mock_logger):
        """Test get_user method logging."""
        user_id = "user123"
        self.users.get_user(user_id)
        mock_logger.info.assert_called_once_with(f"Getting user: {user_id}")

    @patch('mailersend.resources.users.logger')
    def test_invite_user_logging(self, mock_logger):
        """Test invite_user method logging."""
        email = "user@example.com"
        role = "Admin"
        self.users.invite_user(email, role)
        mock_logger.info.assert_called_once_with(f"Inviting user: {email} with role: {role}")

    @patch('mailersend.resources.users.logger')
    def test_update_user_logging(self, mock_logger):
        """Test update_user method logging."""
        user_id = "user123"
        role = "Manager"
        self.users.update_user(user_id, role)
        mock_logger.info.assert_called_once_with(f"Updating user: {user_id} with role: {role}")

    @patch('mailersend.resources.users.logger')
    def test_delete_user_logging(self, mock_logger):
        """Test delete_user method logging."""
        user_id = "user123"
        self.users.delete_user(user_id)
        mock_logger.info.assert_called_once_with(f"Deleting user: {user_id}")

    @patch('mailersend.resources.users.logger')
    def test_list_invites_logging(self, mock_logger):
        """Test list_invites method logging."""
        self.users.list_invites()
        mock_logger.info.assert_called_once_with("Listing account invites")

    @patch('mailersend.resources.users.logger')
    def test_get_invite_logging(self, mock_logger):
        """Test get_invite method logging."""
        invite_id = "invite123"
        self.users.get_invite(invite_id)
        mock_logger.info.assert_called_once_with(f"Getting invite: {invite_id}")

    @patch('mailersend.resources.users.logger')
    def test_resend_invite_logging(self, mock_logger):
        """Test resend_invite method logging."""
        invite_id = "invite123"
        self.users.resend_invite(invite_id)
        mock_logger.info.assert_called_once_with(f"Resending invite: {invite_id}")

    @patch('mailersend.resources.users.logger')
    def test_cancel_invite_logging(self, mock_logger):
        """Test cancel_invite method logging."""
        invite_id = "invite123"
        self.users.cancel_invite(invite_id)
        mock_logger.info.assert_called_once_with(f"Canceling invite: {invite_id}") 