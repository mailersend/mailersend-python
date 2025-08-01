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
)


class TestIdentitiesResource:
    """Test IdentitiesResource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = IdentitiesResource(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_identities_basic(self):
        """Test list_identities with basic request."""
        query_params = IdentityListQueryParams()
        request = IdentityListRequest(query_params=query_params)
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="GET", path="identities", params={"page": 1, "limit": 25}
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_identities_with_params(self):
        """Test list_identities with query parameters."""
        query_params = IdentityListQueryParams(page=2, limit=50, domain_id="domain123")
        request = IdentityListRequest(query_params=query_params)
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="identities",
            params={"page": 2, "limit": 50, "domain_id": "domain123"},
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_identities_with_minimal_params(self):
        """Test list_identities with minimal parameters."""
        query_params = IdentityListQueryParams(domain_id="domain123")
        request = IdentityListRequest(query_params=query_params)
        mock_response = {"data": []}
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_identities(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="identities",
            params={"page": 1, "limit": 25, "domain_id": "domain123"},
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_identity_minimal_request(self):
        """Test create_identity with minimal required fields."""
        request = IdentityCreateRequest(
            domain_id="domain123", name="John Doe", email="john@example.com"
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_identity(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="POST",
            path="identities",
            body={
                "domain_id": "domain123",
                "name": "John Doe",
                "email": "john@example.com",
            },
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_identity_with_all_fields(self):
        """Test create_identity with all fields."""
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            reply_to_email="reply@example.com",
            reply_to_name="Reply Name",
            add_note=True,
            personal_note="Personal note content",
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_identity(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="POST",
            path="identities",
            body={
                "domain_id": "domain123",
                "name": "John Doe",
                "email": "john@example.com",
                "reply_to_email": "reply@example.com",
                "reply_to_name": "Reply Name",
                "add_note": True,
                "personal_note": "Personal note content",
            },
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_identity_model_dump_serialization(self):
        """Test create_identity uses model_dump for request body serialization."""
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            reply_to_email="reply@example.com",
            reply_to_name=None,  # Should be excluded
            add_note=None,  # Should be excluded
            personal_note=None,  # Should be excluded
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.create_identity(request)

        # Verify that None values are excluded via model_dump
        self.mock_client.request.assert_called_once_with(
            method="POST",
            path="identities",
            body={
                "domain_id": "domain123",
                "name": "John Doe",
                "email": "john@example.com",
                "reply_to_email": "reply@example.com",
            },
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_identity_success(self):
        """Test get_identity with valid request."""
        request = IdentityGetRequest(identity_id="identity123")
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_identity(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="GET", path="identities/identity123"
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_identity_by_email_success(self):
        """Test get_identity_by_email with valid request."""
        request = IdentityGetByEmailRequest(email="john@example.com")
        mock_response = {"data": {"email": "john@example.com"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_identity_by_email(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="GET", path="identities/email/john@example.com"
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_identity_with_minimal_data(self):
        """Test update_identity with minimal data."""
        request = IdentityUpdateRequest(identity_id="identity123", name="Updated Name")
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="PUT",
            path="identities/identity123",
            body={"name": "Updated Name"},
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_identity_excludes_identity_id_from_body(self):
        """Test update_identity excludes identity_id from request body."""
        request = IdentityUpdateRequest(
            identity_id="identity123",
            name="Updated Name",
            reply_to_email="updated@example.com",
        )
        mock_response = {"data": {"id": "identity123"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity(request)

        # Verify identity_id is not in the JSON body
        expected_data = {
            "name": "Updated Name",
            "reply_to_email": "updated@example.com",
        }
        self.mock_client.request.assert_called_once_with(
            method="PUT", path="identities/identity123", body=expected_data
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_identity_by_email_excludes_email_from_body(self):
        """Test update_identity_by_email excludes email from request body."""
        request = IdentityUpdateByEmailRequest(
            email="john@example.com",
            name="Updated Name",
            reply_to_email="updated@example.com",
        )
        mock_response = {"data": {"email": "john@example.com"}}
        self.mock_client.request.return_value = mock_response

        result = self.resource.update_identity_by_email(request)

        # Verify email is not in the JSON body
        expected_data = {
            "name": "Updated Name",
            "reply_to_email": "updated@example.com",
        }
        self.mock_client.request.assert_called_once_with(
            method="PUT",
            path="identities/email/john@example.com",
            body=expected_data,
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_identity_success(self):
        """Test delete_identity with valid request."""
        request = IdentityDeleteRequest(identity_id="identity123")
        mock_response = {}
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_identity(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="identities/identity123"
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_identity_by_email_success(self):
        """Test delete_identity_by_email with valid request."""
        request = IdentityDeleteByEmailRequest(email="john@example.com")
        mock_response = {}
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_identity_by_email(request)

        assert result == self.mock_api_response
        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="identities/email/john@example.com"
        )
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        request_create = IdentityCreateRequest(
            domain_id="domain123", name="John Doe", email="john@example.com"
        )
        request_get = IdentityGetRequest(identity_id="identity123")
        request_get_email = IdentityGetByEmailRequest(email="john@example.com")
        request_update = IdentityUpdateRequest(
            identity_id="identity123", name="Updated"
        )
        request_update_email = IdentityUpdateByEmailRequest(
            email="john@example.com", name="Updated"
        )
        request_delete = IdentityDeleteRequest(identity_id="identity123")
        request_delete_email = IdentityDeleteByEmailRequest(email="john@example.com")

        # Test that each method returns the expected APIResponse type
        assert isinstance(
            self.resource.create_identity(request_create), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.get_identity(request_get), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.get_identity_by_email(request_get_email),
            type(self.mock_api_response),
        )
        assert isinstance(
            self.resource.update_identity(request_update), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.update_identity_by_email(request_update_email),
            type(self.mock_api_response),
        )
        assert isinstance(
            self.resource.delete_identity(request_delete), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.delete_identity_by_email(request_delete_email),
            type(self.mock_api_response),
        )
