import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.identities import IdentitiesResource
from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.base import APIResponse
from mailersend.models.identities import (
    IdentityListRequest,
    IdentityListQueryParams,
    IdentityCreateRequest,
    IdentityGetRequest,
    IdentityGetByEmailRequest,
    IdentityUpdateRequest,
    IdentityUpdateByEmailRequest,
    IdentityDeleteRequest,
    IdentityDeleteByEmailRequest,
    IdentityListResponse,
    IdentityResponse
)


class TestIdentitiesResource:
    """Test IdentitiesResource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = IdentitiesResource(self.mock_client)
        self.resource.logger = Mock()
        
        # Mock the _create_response method to return APIResponse
        self.mock_api_response = Mock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_initialization(self):
        """Test resource initialization."""
        assert self.resource.client is self.mock_client

    def test_list_identities_with_invalid_type(self):
        """Test list_identities with invalid request type."""
        with pytest.raises(MailerSendValidationError, match="Request must be an instance of IdentityListRequest"):
            self.resource.list_identities("invalid")

    def test_list_identities_minimal_request(self):
        """Test list_identities with minimal request."""
        query_params = IdentityListQueryParams()
        request = IdentityListRequest(query_params=query_params)
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities',
            params={'page': 1, 'limit': 25}  # Default values
        )
        self.resource._create_response.assert_called_once_with(mock_response, IdentityListResponse)

    def test_list_identities_with_all_parameters(self):
        """Test list_identities with all parameters."""
        query_params = IdentityListQueryParams(
            page=2,
            limit=50,
            domain_id="domain123"
        )
        request = IdentityListRequest(query_params=query_params)
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities',
            params={
                'page': 2,
                'limit': 50,
                'domain_id': 'domain123'
            }
        )
        self.resource._create_response.assert_called_once_with(mock_response, IdentityListResponse)

    def test_list_identities_with_partial_parameters(self):
        """Test list_identities with partial parameters."""
        query_params = IdentityListQueryParams(domain_id="domain123", page=3)
        request = IdentityListRequest(query_params=query_params)
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities',
            params={
                'page': 3,
                'limit': 25,  # Default value
                'domain_id': 'domain123'
            }
        )
        self.resource._create_response.assert_called_once_with(mock_response, IdentityListResponse)

    def test_list_identities_query_params_handling(self):
        """Test that query parameters are properly delegated."""
        query_params = IdentityListQueryParams(page=2, limit=30)
        request = IdentityListRequest(query_params=query_params)
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        # Verify to_query_params was called correctly
        expected_params = {'page': 2, 'limit': 30}
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities',
            params=expected_params
        )

    def test_create_identity_with_invalid_type(self):
        """Test create_identity with invalid request type."""
        with pytest.raises(MailerSendValidationError, match="Request must be an instance of IdentityCreateRequest"):
            self.resource.create_identity("invalid")

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

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='POST',
            endpoint='/identities',
            json={
                'domain_id': 'domain123',
                'name': 'John Doe',
                'email': 'john@example.com'
            }
        )
        self.resource._create_response.assert_called_once_with(mock_response, IdentityResponse)

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

        assert result == self.mock_api_response
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
        self.resource._create_response.assert_called_once_with(mock_response, IdentityResponse)

    def test_create_identity_model_dump_serialization(self):
        """Test create_identity uses model_dump for request body serialization."""
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

        # Verify that None values are excluded via model_dump
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

    def test_get_identity_with_invalid_type(self):
        """Test get_identity with invalid request type."""
        with pytest.raises(MailerSendValidationError, match="Request must be an instance of IdentityGetRequest"):
            self.resource.get_identity("invalid")

    def test_get_identity_success(self):
        """Test get_identity success."""
        request = IdentityGetRequest(identity_id="identity123")
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_identity(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities/identity123'
        )
        self.resource._create_response.assert_called_once_with(mock_response, IdentityResponse)

    def test_get_identity_by_email_with_invalid_type(self):
        """Test get_identity_by_email with invalid request type."""
        with pytest.raises(MailerSendValidationError, match="Request must be an instance of IdentityGetByEmailRequest"):
            self.resource.get_identity_by_email("invalid")

    def test_get_identity_by_email_success(self):
        """Test get_identity_by_email success."""
        request = IdentityGetByEmailRequest(email="john@example.com")
        mock_response = {"data": {"email": "john@example.com"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_identity_by_email(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='/identities/email/john@example.com'
        )
        self.resource._create_response.assert_called_once_with(mock_response, IdentityResponse)

    def test_update_identity_with_invalid_type(self):
        """Test update_identity with invalid request type."""
        with pytest.raises(MailerSendValidationError, match="Request must be an instance of IdentityUpdateRequest"):
            self.resource.update_identity("invalid")

    def test_update_identity_with_minimal_data(self):
        """Test update_identity with minimal data."""
        request = IdentityUpdateRequest(identity_id="identity123", name="Updated Name")
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='/identities/identity123',
            json={'name': 'Updated Name'}
        )
        self.resource._create_response.assert_called_once_with(mock_response, IdentityResponse)

    def test_update_identity_excludes_identity_id_from_body(self):
        """Test update_identity excludes identity_id from request body."""
        request = IdentityUpdateRequest(
            identity_id="identity123",
            name="Updated Name",
            reply_to_email="updated@example.com"
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity(request)

        # Verify identity_id is not in the JSON body
        expected_data = {
            'name': 'Updated Name',
            'reply_to_email': 'updated@example.com'
        }
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='/identities/identity123',
            json=expected_data
        )

    def test_update_identity_by_email_with_invalid_type(self):
        """Test update_identity_by_email with invalid request type."""
        with pytest.raises(MailerSendValidationError, match="Request must be an instance of IdentityUpdateByEmailRequest"):
            self.resource.update_identity_by_email("invalid")

    def test_update_identity_by_email_excludes_email_from_body(self):
        """Test update_identity_by_email excludes email from request body."""
        request = IdentityUpdateByEmailRequest(
            email="john@example.com",
            name="Updated Name",
            reply_to_email="updated@example.com"
        )
        mock_response = {"data": {"email": "john@example.com"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity_by_email(request)

        # Verify email is not in the JSON body
        expected_data = {
            'name': 'Updated Name',
            'reply_to_email': 'updated@example.com'
        }
        self.mock_client.request.assert_called_once_with(
            method='PUT',
            endpoint='/identities/email/john@example.com',
            json=expected_data
        )
        self.resource._create_response.assert_called_once_with(mock_response, IdentityResponse)

    def test_delete_identity_with_invalid_type(self):
        """Test delete_identity with invalid request type."""
        with pytest.raises(MailerSendValidationError, match="Request must be an instance of IdentityDeleteRequest"):
            self.resource.delete_identity("invalid")

    def test_delete_identity_success(self):
        """Test delete_identity success."""
        request = IdentityDeleteRequest(identity_id="identity123")
        mock_response = {"message": "Identity deleted"}
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_identity(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='DELETE',
            endpoint='/identities/identity123'
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_identity_by_email_with_invalid_type(self):
        """Test delete_identity_by_email with invalid request type."""
        with pytest.raises(MailerSendValidationError, match="Request must be an instance of IdentityDeleteByEmailRequest"):
            self.resource.delete_identity_by_email("invalid")

    def test_delete_identity_by_email_success(self):
        """Test delete_identity_by_email success."""
        request = IdentityDeleteByEmailRequest(email="john@example.com")
        mock_response = {"message": "Identity deleted"}
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_identity_by_email(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method='DELETE',
            endpoint='/identities/email/john@example.com'
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_all_methods_return_api_response(self):
        """Test that all methods return APIResponse objects."""
        mock_response = {"data": {}}
        self.mock_client.request.return_value = mock_response

        # Test each method returns APIResponse
        query_params = IdentityListQueryParams()
        request_list = IdentityListRequest(query_params=query_params)
        assert isinstance(self.resource.list_identities(request_list), type(self.mock_api_response))

        request_create = IdentityCreateRequest(domain_id="d1", name="n", email="e@e.com")
        assert isinstance(self.resource.create_identity(request_create), type(self.mock_api_response))

        request_get = IdentityGetRequest(identity_id="id1")
        assert isinstance(self.resource.get_identity(request_get), type(self.mock_api_response))

        request_get_email = IdentityGetByEmailRequest(email="e@e.com")
        assert isinstance(self.resource.get_identity_by_email(request_get_email), type(self.mock_api_response))

        request_update = IdentityUpdateRequest(identity_id="id1")
        assert isinstance(self.resource.update_identity(request_update), type(self.mock_api_response))

        request_update_email = IdentityUpdateByEmailRequest(email="e@e.com")
        assert isinstance(self.resource.update_identity_by_email(request_update_email), type(self.mock_api_response))

        request_delete = IdentityDeleteRequest(identity_id="id1")
        assert isinstance(self.resource.delete_identity(request_delete), type(self.mock_api_response))

        request_delete_email = IdentityDeleteByEmailRequest(email="e@e.com")
        assert isinstance(self.resource.delete_identity_by_email(request_delete_email), type(self.mock_api_response))

    def test_logging_is_called(self):
        """Test that logging is called for each method."""
        mock_response = {"data": {}}
        self.mock_client.request.return_value = mock_response

        # Test logging for list method
        query_params = IdentityListQueryParams()
        request = IdentityListRequest(query_params=query_params)
        self.resource.list_identities(request)
        
        # Verify logging was called
        assert self.resource.logger.debug.called 