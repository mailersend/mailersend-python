"""Unit tests for SMTP Users resource."""
from unittest.mock import Mock, MagicMock

from mailersend.resources.smtp_users import SmtpUsers
from mailersend.models.base import APIResponse
from mailersend.models.smtp_users import (
    SmtpUsersListRequest,
    SmtpUsersListQueryParams,
    SmtpUserGetRequest,
    SmtpUserCreateRequest,
    SmtpUserUpdateRequest,
    SmtpUserDeleteRequest,
)


class TestSmtpUsers:
    """Test SmtpUsers resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = SmtpUsers(self.mock_client)
        self.resource.logger = Mock()
        
        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_smtp_users_returns_api_response(self):
        """Test list_smtp_users method returns APIResponse."""
        query_params = SmtpUsersListQueryParams()
        request = SmtpUsersListRequest(domain_id="test-domain", query_params=query_params)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_smtp_users(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_smtp_users_uses_query_params(self):
        """Test list_smtp_users method uses query params correctly."""
        query_params = SmtpUsersListQueryParams(limit=50)
        request = SmtpUsersListRequest(domain_id="test-domain", query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_smtp_users(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='domains/test-domain/smtp-users',
            params={'limit': 50}
        )

        # Verify _create_response was called
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_smtp_users_with_defaults(self):
        """Test list_smtp_users with default query params."""
        query_params = SmtpUsersListQueryParams()
        request = SmtpUsersListRequest(domain_id="test-domain", query_params=query_params)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_smtp_users(request)

        # Verify client was called with empty params (defaults excluded)
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='domains/test-domain/smtp-users',
            params={}
        )

    def test_get_smtp_user_returns_api_response(self):
        """Test get_smtp_user method returns APIResponse."""
        request = SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="user123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_smtp_user(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_smtp_user_endpoint_construction(self):
        """Test get_smtp_user constructs endpoint correctly."""
        request = SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="user123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_smtp_user(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='domains/test-domain/smtp-users/user123'
        )

    def test_create_smtp_user_returns_api_response(self):
        """Test create_smtp_user method returns APIResponse."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_smtp_user(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_smtp_user_with_request_body(self):
        """Test create_smtp_user sends correct request body."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User", enabled=True)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_smtp_user(request)

        # Verify client was called with correct body
        self.mock_client.request.assert_called_once_with(
            method='POST',
            endpoint='domains/test-domain/smtp-users',
            body={'name': 'Test User', 'enabled': True}
        )

    def test_update_smtp_user_returns_api_response(self):
        """Test update_smtp_user method returns APIResponse."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain",
            smtp_user_id="user123",
            name="Updated User"
        )
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_smtp_user(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_smtp_user_with_request_body(self):
        """Test update_smtp_user sends correct request body."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain",
            smtp_user_id="user123",
            name="Updated User",
            enabled=False
        )
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_smtp_user(request)

        # Verify client was called with correct body and endpoint
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='domains/test-domain/smtp-users/user123',
            body={'name': 'Updated User', 'enabled': False}
        )

    def test_delete_smtp_user_returns_api_response(self):
        """Test delete_smtp_user method returns APIResponse."""
        request = SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="user123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_smtp_user(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_smtp_user_endpoint_construction(self):
        """Test delete_smtp_user constructs endpoint correctly."""
        request = SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="user123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_smtp_user(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method='DELETE',
            endpoint='domains/test-domain/smtp-users/user123'
        )

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        query_params = SmtpUsersListQueryParams()
        request_list = SmtpUsersListRequest(domain_id="test-domain", query_params=query_params)
        request_get = SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="user123")
        request_create = SmtpUserCreateRequest(domain_id="test-domain", name="Test User")
        request_update = SmtpUserUpdateRequest(
            domain_id="test-domain", smtp_user_id="user123", name="Updated User"
        )
        request_delete = SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="user123")

        # Test that each method returns the expected APIResponse type
        assert isinstance(self.resource.list_smtp_users(request_list), type(self.mock_api_response))
        assert isinstance(self.resource.get_smtp_user(request_get), type(self.mock_api_response))
        assert isinstance(self.resource.create_smtp_user(request_create), type(self.mock_api_response))
        assert isinstance(self.resource.update_smtp_user(request_update), type(self.mock_api_response))
        assert isinstance(self.resource.delete_smtp_user(request_delete), type(self.mock_api_response))
