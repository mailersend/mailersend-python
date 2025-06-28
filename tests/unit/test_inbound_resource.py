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
    InboundListResponse,
    InboundResponse,
    InboundRoute,
    InboundFilterGroup,
    InboundForward
)


class TestInboundResource:
    """Test InboundResource functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        client = Mock()
        client.request = Mock()
        return client

    @pytest.fixture
    def resource(self, mock_client):
        """Create InboundResource with mock client."""
        resource = InboundResource(mock_client)
        resource._create_response = Mock(return_value=APIResponse(data={}, headers={}, status_code=200))
        return resource

    @pytest.fixture
    def sample_route_data(self):
        """Sample route data for responses."""
        return {
            "id": "test-id",
            "name": "Test Route",
            "address": "test@inbound.mailersend.net",
            "domain": "example.com",
            "dns_checked_at": None,
            "enabled": True,
            "filters": [],
            "forwards": [],
            "priority": 100,
            "mxValues": {
                "priority": 10,
                "target": "inbound.mailersend.net"
            }
        }

    def test_list_returns_api_response(self, resource):
        """Test list method returns APIResponse."""
        query_params = InboundListQueryParams()
        request = InboundListRequest(query_params=query_params)
        
        result = resource.list(request)
        assert isinstance(result, APIResponse)

    def test_list_validation_wrong_type(self, resource):
        """Test list method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.list("invalid_request")
        assert "Request must be an instance of InboundListRequest" in str(exc_info.value)

    def test_list_with_query_params(self, resource):
        """Test list method uses query params correctly."""
        query_params = InboundListQueryParams(page=2, limit=50, domain_id="domain123")
        request = InboundListRequest(query_params=query_params)
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.list(request)
        
        # Verify client was called correctly
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='inbound',
            params={'page': 2, 'limit': 50, 'domain_id': 'domain123'}
        )
        
        # Verify _create_response was called with correct params
        resource._create_response.assert_called_once_with(mock_response, InboundListResponse)

    def test_list_with_default_query_params(self, resource):
        """Test list with default query params."""
        query_params = InboundListQueryParams()  # Uses defaults
        request = InboundListRequest(query_params=query_params)
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.list(request)
        
        # Verify client was called with defaults
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='inbound',
            params={'page': 1, 'limit': 25}
        )

    def test_list_excludes_none_values(self, resource):
        """Test list excludes None values from query params."""
        query_params = InboundListQueryParams(page=2, limit=30)  # domain_id is None
        request = InboundListRequest(query_params=query_params)
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.list(request)
        
        # Verify None values are excluded
        expected_params = {'page': 2, 'limit': 30}
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='inbound',
            params=expected_params
        )

    def test_get_returns_api_response(self, resource):
        """Test get method returns APIResponse."""
        request = InboundGetRequest(inbound_id="test-id")
        
        result = resource.get(request)
        assert isinstance(result, APIResponse)

    def test_get_validation_wrong_type(self, resource):
        """Test get method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.get("invalid_request")
        assert "Request must be an instance of InboundGetRequest" in str(exc_info.value)

    def test_get_with_valid_request(self, resource):
        """Test get with valid request."""
        request = InboundGetRequest(inbound_id="test-id")
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.get(request)
        
        # Verify client was called correctly
        resource.client.request.assert_called_once_with(
            method='GET',
            endpoint='inbound/test-id'
        )
        
        # Verify _create_response was called
        resource._create_response.assert_called_once_with(mock_response, InboundResponse)

    def test_create_returns_api_response(self, resource):
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
        
        result = resource.create(request)
        assert isinstance(result, APIResponse)

    def test_create_validation_wrong_type(self, resource):
        """Test create method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.create("invalid_request")
        assert "Request must be an instance of InboundCreateRequest" in str(exc_info.value)

    def test_create_request_body_serialization(self, resource):
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
        resource.client.request.return_value = mock_response
        
        resource.create(request)
        
        # Verify the request was made with correct data structure
        call_args = resource.client.request.call_args
        assert call_args[1]['method'] == 'POST'
        assert call_args[1]['endpoint'] == 'inbound'
        
        # Verify data structure
        data = call_args[1]['json']
        assert 'domain_id' in data
        assert 'name' in data
        assert 'domain_enabled' in data
        assert 'catch_filter' in data
        assert 'match_filter' in data
        assert 'forwards' in data
        
        # Verify forwards exclude 'id' field
        assert all('id' not in forward for forward in data['forwards'])

    def test_update_returns_api_response(self, resource):
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
        
        result = resource.update(request)
        assert isinstance(result, APIResponse)

    def test_update_validation_wrong_type(self, resource):
        """Test update method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.update("invalid_request")
        assert "Request must be an instance of InboundUpdateRequest" in str(exc_info.value)

    def test_update_excludes_inbound_id_from_body(self, resource):
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
        resource.client.request.return_value = mock_response
        
        resource.update(request)
        
        # Verify the request structure
        call_args = resource.client.request.call_args
        assert call_args[1]['method'] == 'PUT'
        assert call_args[1]['endpoint'] == 'inbound/test-id'
        
        # Verify inbound_id is not in the request body
        data = call_args[1]['json']
        assert 'inbound_id' not in data

    def test_delete_returns_api_response(self, resource):
        """Test delete method returns APIResponse."""
        request = InboundDeleteRequest(inbound_id="test-id")
        
        result = resource.delete(request)
        assert isinstance(result, APIResponse)

    def test_delete_validation_wrong_type(self, resource):
        """Test delete method with wrong request type raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.delete("invalid_request")
        assert "Request must be an instance of InboundDeleteRequest" in str(exc_info.value)

    def test_delete_with_valid_request(self, resource):
        """Test delete with valid request."""
        request = InboundDeleteRequest(inbound_id="test-id")
        
        mock_response = Mock()
        resource.client.request.return_value = mock_response
        
        resource.delete(request)
        
        # Verify client was called correctly
        resource.client.request.assert_called_once_with(
            method='DELETE',
            endpoint='inbound/test-id'
        )
        
        # Verify _create_response was called (without response model for delete)
        resource._create_response.assert_called_once_with(mock_response) 