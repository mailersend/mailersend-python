import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.identities import IdentitiesResource
from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.identities import (
    IdentityListRequest,
    IdentityCreateRequest,
    IdentityGetRequest,
    IdentityGetByEmailRequest,
    IdentityUpdateRequest,
    IdentityUpdateByEmailRequest,
    IdentityDeleteRequest,
    IdentityDeleteByEmailRequest
)


class TestIdentitiesResource:
    """Test IdentitiesResource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = IdentitiesResource(self.mock_client)

    def test_initialization(self):
        """Test resource initialization."""
        assert self.resource.client is self.mock_client

    def test_list_identities_with_none_request(self):
        """Test list_identities with None request."""
        with pytest.raises(MailerSendValidationError, match="Request is required"):
            self.resource.list_identities(None)

    def test_list_identities_minimal_request(self):
        """Test list_identities with minimal request."""
        request = IdentityListRequest()
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities',
            params={'limit': 25}  # Model default value is included
        )

    def test_list_identities_with_all_parameters(self):
        """Test list_identities with all parameters."""
        request = IdentityListRequest(
            domain_id="domain123",
            page=2,
            limit=50
        )
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities',
            params={
                'domain_id': 'domain123',
                'page': 2,
                'limit': 50
            }
        )

    def test_list_identities_with_partial_parameters(self):
        """Test list_identities with partial parameters."""
        request = IdentityListRequest(domain_id="domain123", page=2)
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities',
            params={
                'domain_id': 'domain123',
                'page': 2,
                'limit': 25  # Default value
            }
        )

    def test_create_identity_with_none_request(self):
        """Test create_identity with None request."""
        with pytest.raises(MailerSendValidationError, match="Request is required"):
            self.resource.create_identity(None)

    def test_create_identity_minimal_request(self):
        """Test create_identity with minimal required fields."""
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com"
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_identity(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='POST',
            endpoint='/identities',
            json={
                'domain_id': 'domain123',
                'name': 'John Doe',
                'email': 'john@example.com'
            }
        )

    def test_create_identity_with_all_fields(self):
        """Test create_identity with all fields."""
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            reply_to_email="reply@example.com",
            reply_to_name="Reply Name",
            add_note=True,
            personal_note="Personal note content"
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_identity(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='POST',
            endpoint='/identities',
            json={
                'domain_id': 'domain123',
                'name': 'John Doe',
                'email': 'john@example.com',
                'reply_to_email': 'reply@example.com',
                'reply_to_name': 'Reply Name',
                'add_note': True,
                'personal_note': 'Personal note content'
            }
        )

    def test_create_identity_excludes_none_values(self):
        """Test create_identity excludes None values from request body."""
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            reply_to_email="reply@example.com",
            reply_to_name=None,  # Should be excluded
            add_note=None,       # Should be excluded
            personal_note=None   # Should be excluded
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_identity(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='POST',
            endpoint='/identities',
            json={
                'domain_id': 'domain123',
                'name': 'John Doe',
                'email': 'john@example.com',
                'reply_to_email': 'reply@example.com'
            }
        )

    def test_get_identity_with_none_request(self):
        """Test get_identity with None request."""
        with pytest.raises(MailerSendValidationError, match="Request is required"):
            self.resource.get_identity(None)

    def test_get_identity_success(self):
        """Test get_identity success."""
        request = IdentityGetRequest(identity_id="identity123")
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_identity(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities/identity123'
        )

    def test_get_identity_by_email_with_none_request(self):
        """Test get_identity_by_email with None request."""
        with pytest.raises(MailerSendValidationError, match="Request is required"):
            self.resource.get_identity_by_email(None)

    def test_get_identity_by_email_success(self):
        """Test get_identity_by_email success."""
        request = IdentityGetByEmailRequest(email="john@example.com")
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_identity_by_email(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities/email/john@example.com'
        )

    def test_update_identity_with_none_request(self):
        """Test update_identity with None request."""
        with pytest.raises(MailerSendValidationError, match="Request is required"):
            self.resource.update_identity(None)

    def test_update_identity_with_minimal_data(self):
        """Test update_identity with minimal data."""
        request = IdentityUpdateRequest(identity_id="identity123")
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='/identities/identity123',
            json=None
        )

    def test_update_identity_with_all_fields(self):
        """Test update_identity with all update fields."""
        request = IdentityUpdateRequest(
            identity_id="identity123",
            name="Updated Name",
            reply_to_email="updated@example.com",
            reply_to_name="Updated Reply Name",
            add_note=False,
            personal_note="Updated note"
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='/identities/identity123',
            json={
                'name': 'Updated Name',
                'reply_to_email': 'updated@example.com',
                'reply_to_name': 'Updated Reply Name',
                'add_note': False,
                'personal_note': 'Updated note'
            }
        )

    def test_update_identity_excludes_identity_id_from_body(self):
        """Test update_identity excludes identity_id from request body."""
        request = IdentityUpdateRequest(
            identity_id="identity123",
            name="Updated Name"
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity(request)

        assert result == mock_response
        # Verify identity_id is not in the JSON body
        call_args = self.mock_client.request.call_args
        assert 'identity_id' not in call_args[1]['json']
        assert call_args[1]['json'] == {'name': 'Updated Name'}

    def test_update_identity_excludes_none_values(self):
        """Test update_identity excludes None values from request body."""
        request = IdentityUpdateRequest(
            identity_id="identity123",
            name="Updated Name",
            reply_to_email=None,  # Should be excluded
            reply_to_name=None,   # Should be excluded
            add_note=None,        # Should be excluded
            personal_note=None    # Should be excluded
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='/identities/identity123',
            json={'name': 'Updated Name'}
        )

    def test_update_identity_by_email_with_none_request(self):
        """Test update_identity_by_email with None request."""
        with pytest.raises(MailerSendValidationError, match="Request is required"):
            self.resource.update_identity_by_email(None)

    def test_update_identity_by_email_with_minimal_data(self):
        """Test update_identity_by_email with minimal data."""
        request = IdentityUpdateByEmailRequest(email="john@example.com")
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity_by_email(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='/identities/email/john@example.com',
            json=None
        )

    def test_update_identity_by_email_with_all_fields(self):
        """Test update_identity_by_email with all update fields."""
        request = IdentityUpdateByEmailRequest(
            email="john@example.com",
            name="Updated Name",
            reply_to_email="updated@example.com",
            reply_to_name="Updated Reply Name",
            add_note=False,
            personal_note="Updated note"
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity_by_email(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='/identities/email/john@example.com',
            json={
                'name': 'Updated Name',
                'reply_to_email': 'updated@example.com',
                'reply_to_name': 'Updated Reply Name',
                'add_note': False,
                'personal_note': 'Updated note'
            }
        )

    def test_update_identity_by_email_excludes_email_from_body(self):
        """Test update_identity_by_email excludes email from request body."""
        request = IdentityUpdateByEmailRequest(
            email="john@example.com",
            name="Updated Name"
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity_by_email(request)

        assert result == mock_response
        # Verify email is not in the JSON body
        call_args = self.mock_client.request.call_args
        assert 'email' not in call_args[1]['json']
        assert call_args[1]['json'] == {'name': 'Updated Name'}

    def test_delete_identity_with_none_request(self):
        """Test delete_identity with None request."""
        with pytest.raises(MailerSendValidationError, match="Request is required"):
            self.resource.delete_identity(None)

    def test_delete_identity_success(self):
        """Test delete_identity success."""
        request = IdentityDeleteRequest(identity_id="identity123")
        mock_response = {}
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_identity(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='DELETE',
            endpoint='/identities/identity123'
        )

    def test_delete_identity_by_email_with_none_request(self):
        """Test delete_identity_by_email with None request."""
        with pytest.raises(MailerSendValidationError, match="Request is required"):
            self.resource.delete_identity_by_email(None)

    def test_delete_identity_by_email_success(self):
        """Test delete_identity_by_email success."""
        request = IdentityDeleteByEmailRequest(email="john@example.com")
        mock_response = {}
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_identity_by_email(request)

        assert result == mock_response
        self.mock_client.request.assert_called_once_with(
            method='DELETE',
            endpoint='/identities/email/john@example.com'
        )

    def test_all_methods_exist(self):
        """Test that all expected methods exist."""
        expected_methods = [
            'list_identities',
            'create_identity',
            'get_identity',
            'get_identity_by_email',
            'update_identity',
            'update_identity_by_email',
            'delete_identity',
            'delete_identity_by_email'
        ]
        
        for method_name in expected_methods:
            assert hasattr(self.resource, method_name)
            assert callable(getattr(self.resource, method_name))

    def test_method_signatures(self):
        """Test method signatures accept correct parameter types."""
        # Test that methods accept their respective request types
        # (This is more of a documentation test since Python is dynamically typed)
        
        # List identities
        request = IdentityListRequest()
        assert hasattr(request, 'domain_id')
        assert hasattr(request, 'page')
        assert hasattr(request, 'limit')
        
        # Create identity
        request = IdentityCreateRequest(
            domain_id="test",
            name="test",
            email="test@example.com"
        )
        assert hasattr(request, 'domain_id')
        assert hasattr(request, 'name')
        assert hasattr(request, 'email')
        
        # Get identity
        request = IdentityGetRequest(identity_id="test")
        assert hasattr(request, 'identity_id')
        
        # Get identity by email
        request = IdentityGetByEmailRequest(email="test@example.com")
        assert hasattr(request, 'email')
        
        # Update identity
        request = IdentityUpdateRequest(identity_id="test")
        assert hasattr(request, 'identity_id')
        
        # Update identity by email
        request = IdentityUpdateByEmailRequest(email="test@example.com")
        assert hasattr(request, 'email')
        
        # Delete identity
        request = IdentityDeleteRequest(identity_id="test")
        assert hasattr(request, 'identity_id')
        
        # Delete identity by email
        request = IdentityDeleteByEmailRequest(email="test@example.com")
        assert hasattr(request, 'email')

    def test_client_request_method_calls(self):
        """Test that all methods properly call client.request."""
        # This test ensures all methods follow the same pattern
        test_cases = [
            (
                'list_identities',
                IdentityListRequest(),
                'GET',
                '/identities'
            ),
            (
                'create_identity',
                IdentityCreateRequest(
                    domain_id="domain123",
                    name="John Doe",
                    email="john@example.com"
                ),
                'POST',
                '/identities'
            ),
            (
                'get_identity',
                IdentityGetRequest(identity_id="identity123"),
                'GET',
                '/identities/identity123'
            ),
            (
                'get_identity_by_email',
                IdentityGetByEmailRequest(email="john@example.com"),
                'GET',
                '/identities/email/john@example.com'
            ),
            (
                'update_identity',
                IdentityUpdateRequest(identity_id="identity123"),
                'PUT',
                '/identities/identity123'
            ),
            (
                'update_identity_by_email',
                IdentityUpdateByEmailRequest(email="john@example.com"),
                'PUT',
                '/identities/email/john@example.com'
            ),
            (
                'delete_identity',
                IdentityDeleteRequest(identity_id="identity123"),
                'DELETE',
                '/identities/identity123'
            ),
            (
                'delete_identity_by_email',
                IdentityDeleteByEmailRequest(email="john@example.com"),
                'DELETE',
                '/identities/email/john@example.com'
            )
        ]
        
        for method_name, request, expected_method, expected_endpoint in test_cases:
            # Reset mock for each test
            self.mock_client.reset_mock()
            mock_response = {"data": {"id": "test"}}
            self.mock_client.request.return_value = mock_response
            
            # Call the method
            method = getattr(self.resource, method_name)
            result = method(request)
            
            # Verify client.request was called
            assert self.mock_client.request.called
            call_args = self.mock_client.request.call_args
            
            # Verify method and endpoint
            assert call_args[1]['method'] == expected_method
            assert call_args[1]['endpoint'] == expected_endpoint
            
            # Verify response is returned
            assert result == mock_response 