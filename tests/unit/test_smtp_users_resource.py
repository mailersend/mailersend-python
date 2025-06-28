"""Tests for SMTP Users resource."""

import pytest
from unittest.mock import Mock, patch

from mailersend.resources.smtp_users import SmtpUsers
from mailersend.models.smtp_users import (
    SmtpUsersListRequest, SmtpUsersListQueryParams, SmtpUserGetRequest,
    SmtpUserCreateRequest, SmtpUserUpdateRequest, SmtpUserDeleteRequest
)
from mailersend.models.base import APIResponse


class TestSmtpUsersResource:
    """Test cases for SmtpUsers resource."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()
    
    @pytest.fixture
    def smtp_users_resource(self, mock_client):
        """Create an SmtpUsers resource with mock client."""
        return SmtpUsers(mock_client)

    def test_list_smtp_users_basic(self, smtp_users_resource, mock_client):
        """Test list_smtp_users basic functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUsersListRequest(domain_id="test-domain")
        result = smtp_users_resource.list_smtp_users(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/domains/test-domain/smtp-users",
            params={}  # Default values don't get included
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(smtp_users_resource._create_response.return_value))

    def test_list_smtp_users_with_limit(self, smtp_users_resource, mock_client):
        """Test list_smtp_users with custom limit."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmtpUsersListQueryParams(limit=50)
        request = SmtpUsersListRequest(domain_id="test-domain", query_params=query_params)
        result = smtp_users_resource.list_smtp_users(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/domains/test-domain/smtp-users",
            params={"limit": 50}
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(smtp_users_resource._create_response.return_value))

    @patch('mailersend.resources.smtp_users.logger')
    def test_list_smtp_users_logging(self, mock_logger, smtp_users_resource, mock_client):
        """Test list_smtp_users logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = SmtpUsersListQueryParams(limit=30)
        request = SmtpUsersListRequest(domain_id="test-domain", query_params=query_params)
        smtp_users_resource.list_smtp_users(request)

        mock_logger.info.assert_called_once_with(
            "Listing SMTP users for domain: test-domain with limit: 30"
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)

    def test_get_smtp_user(self, smtp_users_resource, mock_client):
        """Test get_smtp_user functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="user123")
        result = smtp_users_resource.get_smtp_user(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="/v1/domains/test-domain/smtp-users/user123"
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(smtp_users_resource._create_response.return_value))

    @patch('mailersend.resources.smtp_users.logger')
    def test_get_smtp_user_logging(self, mock_logger, smtp_users_resource, mock_client):
        """Test get_smtp_user logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="user123")
        smtp_users_resource.get_smtp_user(request)

        mock_logger.info.assert_called_once_with(
            "Getting SMTP user: user123 from domain: test-domain"
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)

    def test_create_smtp_user(self, smtp_users_resource, mock_client):
        """Test create_smtp_user functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User")
        result = smtp_users_resource.create_smtp_user(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="POST",
            endpoint="/v1/domains/test-domain/smtp-users",
            json={"name": "Test User"}
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(smtp_users_resource._create_response.return_value))

    def test_create_smtp_user_with_enabled(self, smtp_users_resource, mock_client):
        """Test create_smtp_user with enabled flag."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User", enabled=True)
        result = smtp_users_resource.create_smtp_user(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="POST",
            endpoint="/v1/domains/test-domain/smtp-users",
            json={"name": "Test User", "enabled": True}
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(smtp_users_resource._create_response.return_value))

    @patch('mailersend.resources.smtp_users.logger')
    def test_create_smtp_user_logging(self, mock_logger, smtp_users_resource, mock_client):
        """Test create_smtp_user logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User")
        smtp_users_resource.create_smtp_user(request)

        mock_logger.info.assert_called_once_with(
            "Creating SMTP user: Test User for domain: test-domain"
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)

    def test_update_smtp_user(self, smtp_users_resource, mock_client):
        """Test update_smtp_user functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", 
            smtp_user_id="user123", 
            name="Updated User"
        )
        result = smtp_users_resource.update_smtp_user(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            endpoint="/v1/domains/test-domain/smtp-users/user123",
            json={"name": "Updated User"}
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(smtp_users_resource._create_response.return_value))

    def test_update_smtp_user_with_enabled(self, smtp_users_resource, mock_client):
        """Test update_smtp_user with enabled flag."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", 
            smtp_user_id="user123", 
            name="Updated User", 
            enabled=False
        )
        result = smtp_users_resource.update_smtp_user(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="PUT",
            endpoint="/v1/domains/test-domain/smtp-users/user123",
            json={"name": "Updated User", "enabled": False}
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(smtp_users_resource._create_response.return_value))

    @patch('mailersend.resources.smtp_users.logger')
    def test_update_smtp_user_logging(self, mock_logger, smtp_users_resource, mock_client):
        """Test update_smtp_user logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {}}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", 
            smtp_user_id="user123", 
            name="Updated User"
        )
        smtp_users_resource.update_smtp_user(request)

        mock_logger.info.assert_called_once_with(
            "Updating SMTP user: user123 in domain: test-domain"
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)

    def test_delete_smtp_user(self, smtp_users_resource, mock_client):
        """Test delete_smtp_user functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="user123")
        result = smtp_users_resource.delete_smtp_user(request)

        # Check the request was made correctly
        mock_client.request.assert_called_once_with(
            method="DELETE",
            endpoint="/v1/domains/test-domain/smtp-users/user123"
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(smtp_users_resource._create_response.return_value))

    @patch('mailersend.resources.smtp_users.logger')
    def test_delete_smtp_user_logging(self, mock_logger, smtp_users_resource, mock_client):
        """Test delete_smtp_user logs correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_client.request.return_value = mock_response
        smtp_users_resource._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="user123")
        smtp_users_resource.delete_smtp_user(request)

        mock_logger.info.assert_called_once_with(
            "Deleting SMTP user: user123 from domain: test-domain"
        )
        smtp_users_resource._create_response.assert_called_once_with(mock_response)
