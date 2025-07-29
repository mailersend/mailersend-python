import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.inbound import InboundResource
from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.base import APIResponse
from mailersend.models.inbound import (
    InboundListRequest,
    InboundListQueryParams,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
    InboundFilterGroup,
    InboundForward
)


class TestInboundResource:
    """Test InboundResource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = InboundResource(self.mock_client)
        self.resource.logger = Mock()
        
        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_returns_api_response(self):
        """Test list method returns APIResponse."""
        query_params = InboundListQueryParams()
        request = InboundListRequest(query_params=query_params)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_with_query_params(self):
        """Test list method uses query params correctly."""
        query_params = InboundListQueryParams(page=2, limit=50, domain_id="domain123")
        request = InboundListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='inbound',
            params={'page': 2, 'limit': 50, 'domain_id': 'domain123'}
        )

        # Verify _create_response was called
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_with_default_query_params(self):
        """Test list with default query params."""
        query_params = InboundListQueryParams()
        request = InboundListRequest(query_params=query_params)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        # Verify client was called with defaults
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='inbound',
            params={'page': 1, 'limit': 25}
        )

    def test_list_excludes_none_values(self):
        """Test list excludes None values from params."""
        query_params = InboundListQueryParams(page=1, limit=25)  # domain_id is None
        request = InboundListRequest(query_params=query_params)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list(request)

        # Verify None values are excluded
        call_args = self.mock_client.request.call_args
        params = call_args[1]['params']
        assert 'domain_id' not in params

    def test_get_returns_api_response(self):
        """Test get method returns APIResponse."""
        request = InboundGetRequest(inbound_id="test-id")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_with_valid_request(self):
        """Test get with valid request."""
        request = InboundGetRequest(inbound_id="test-id")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='inbound/test-id'
        )

    def test_create_returns_api_response(self):
        """Test create method returns APIResponse."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]

        request = InboundCreateRequest(
            domain_id="domain123",
            name="Test Route",
            domain_enabled=False,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_request_body_serialization(self):
        """Test create request body is serialized correctly."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(id="forward-id", type="email", value="test@example.com")]

        request = InboundCreateRequest(
            domain_id="domain123",
            name="Test Route",
            domain_enabled=False,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.create(request)

        # Verify the request was made with correct data structure
        call_args = self.mock_client.request.call_args
        assert call_args[1]['method'] == 'POST'
        assert call_args[1]['endpoint'] == 'inbound'

        # Verify data structure
        data = call_args[1]['body']
        assert 'domain_id' in data
        assert 'name' in data
        assert 'domain_enabled' in data
        assert 'catch_filter' in data
        assert 'match_filter' in data
        assert 'forwards' in data

        # Verify 'id' is excluded from forwards
        for forward in data['forwards']:
            assert 'id' not in forward

    def test_update_returns_api_response(self):
        """Test update method returns APIResponse."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]

        request = InboundUpdateRequest(
            inbound_id="test-id",
            name="Updated Route",
            domain_enabled=False,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_excludes_inbound_id_from_body(self):
        """Test update excludes inbound_id from request body."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]

        request = InboundUpdateRequest(
            inbound_id="test-id",
            name="Updated Route",
            domain_enabled=False,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.update(request)

        # Verify the request structure
        call_args = self.mock_client.request.call_args
        assert call_args[1]['method'] == 'PUT'
        assert call_args[1]['endpoint'] == 'inbound/test-id'

        # Verify inbound_id is not in the request body
        data = call_args[1]['body']
        assert 'inbound_id' not in data
        assert 'name' in data

    def test_delete_returns_api_response(self):
        """Test delete method returns APIResponse."""
        request = InboundDeleteRequest(inbound_id="test-id")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_with_valid_request(self):
        """Test delete with valid request."""
        request = InboundDeleteRequest(inbound_id="test-id")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method='DELETE',
            endpoint='inbound/test-id'
        )

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        query_params = InboundListQueryParams()
        request_list = InboundListRequest(query_params=query_params)
        request_get = InboundGetRequest(inbound_id="test-id")
        
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        request_create = InboundCreateRequest(
            domain_id="domain123",
            name="Test Route",
            domain_enabled=False,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        
        request_update = InboundUpdateRequest(
            inbound_id="test-id",
            name="Updated Route",
            domain_enabled=False,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        
        request_delete = InboundDeleteRequest(inbound_id="test-id")

        # Test that each method returns the expected APIResponse type
        assert isinstance(self.resource.list(request_list), type(self.mock_api_response))
        assert isinstance(self.resource.get(request_get), type(self.mock_api_response))
        assert isinstance(self.resource.create(request_create), type(self.mock_api_response))
        assert isinstance(self.resource.update(request_update), type(self.mock_api_response))
        assert isinstance(self.resource.delete(request_delete), type(self.mock_api_response)) 