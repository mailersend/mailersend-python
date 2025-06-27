import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.inbound import InboundResource
from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.inbound import (
    InboundListRequest,
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
        client.get = Mock()
        client.post = Mock()
        client.put = Mock()
        client.delete = Mock()
        return client

    @pytest.fixture
    def resource(self, mock_client):
        """Create InboundResource with mock client."""
        return InboundResource(mock_client)

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

    def test_list_method_signature(self, resource):
        """Test list method accepts InboundListRequest."""
        request = InboundListRequest()
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        resource.client.get.return_value = mock_response
        
        result = resource.list(request)
        assert isinstance(result, InboundListResponse)

    def test_list_with_none_request(self, resource):
        """Test list method with None request raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.list(None)
        assert "Request cannot be None" in str(exc_info.value)

    def test_list_with_minimal_request(self, resource, sample_route_data):
        """Test list with minimal request parameters."""
        request = InboundListRequest()
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": [sample_route_data]}
        resource.client.get.return_value = mock_response
        
        result = resource.list(request)
        
        # Verify client was called correctly (includes default limit)
        resource.client.get.assert_called_once_with("inbound", params={'limit': 25})
        assert isinstance(result, InboundListResponse)
        assert len(result.data) == 1

    def test_list_with_all_parameters(self, resource, sample_route_data):
        """Test list with all parameters."""
        request = InboundListRequest(
            domain_id="domain123",
            page=2,
            limit=50
        )
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": [sample_route_data]}
        resource.client.get.return_value = mock_response
        
        result = resource.list(request)
        
        # Verify parameters were built correctly
        expected_params = {
            "domain_id": "domain123",
            "page": 2,
            "limit": 50
        }
        resource.client.get.assert_called_once_with("inbound", params=expected_params)

    def test_list_excludes_none_values(self, resource, sample_route_data):
        """Test list excludes None values from parameters."""
        request = InboundListRequest(
            domain_id="domain123",
            page=None,  # Should be excluded
            limit=50
        )
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": [sample_route_data]}
        resource.client.get.return_value = mock_response
        
        resource.list(request)
        
        # Verify None values are excluded
        expected_params = {
            "domain_id": "domain123",
            "limit": 50
        }
        resource.client.get.assert_called_once_with("inbound", params=expected_params)

    def test_get_method_signature(self, resource, sample_route_data):
        """Test get method accepts InboundGetRequest."""
        request = InboundGetRequest(inbound_id="test-id")
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.get.return_value = mock_response
        
        result = resource.get(request)
        assert isinstance(result, InboundResponse)

    def test_get_with_none_request(self, resource):
        """Test get method with None request raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.get(None)
        assert "Request cannot be None" in str(exc_info.value)

    def test_get_with_valid_request(self, resource, sample_route_data):
        """Test get with valid request."""
        request = InboundGetRequest(inbound_id="test-id")
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.get.return_value = mock_response
        
        result = resource.get(request)
        
        # Verify client was called correctly
        resource.client.get.assert_called_once_with("inbound/test-id")
        assert isinstance(result, InboundResponse)

    def test_create_method_signature(self, resource, sample_route_data):
        """Test create method accepts InboundCreateRequest."""
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
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.post.return_value = mock_response
        
        result = resource.create(request)
        assert isinstance(result, InboundResponse)

    def test_create_with_none_request(self, resource):
        """Test create method with None request raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.create(None)
        assert "Request cannot be None" in str(exc_info.value)

    def test_create_with_minimal_request(self, resource, sample_route_data):
        """Test create with minimal request."""
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
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.post.return_value = mock_response
        
        result = resource.create(request)
        
        # Verify data was built correctly
        expected_data = {
            "domain_id": "domain123",
            "name": "Test Route",
            "domain_enabled": False,
            "catch_filter": [{"type": "catch_all", "filters": None}],
            "match_filter": [{"type": "match_all", "filters": None}],
            "forwards": [{"type": "email", "value": "test@example.com", "secret": None}]
        }
        resource.client.post.assert_called_once_with("inbound", json=expected_data)

    def test_create_with_domain_enabled(self, resource, sample_route_data):
        """Test create with domain enabled."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        request = InboundCreateRequest(
            domain_id="domain123",
            name="Test Route",
            domain_enabled=True,
            inbound_domain="inbound.example.com",
            inbound_priority=50,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards,
            catch_type="all",
            match_type="one"
        )
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.post.return_value = mock_response
        
        resource.create(request)
        
        # Verify all fields are included
        call_args = resource.client.post.call_args
        data = call_args[1]["json"]
        assert data["domain_enabled"] is True
        assert data["inbound_domain"] == "inbound.example.com"
        assert data["inbound_priority"] == 50
        assert data["catch_type"] == "all"
        assert data["match_type"] == "one"

    def test_create_excludes_none_values(self, resource, sample_route_data):
        """Test create excludes None values from request data."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        request = InboundCreateRequest(
            domain_id="domain123",
            name="Test Route",
            domain_enabled=False,
            inbound_domain=None,  # Should be excluded
            inbound_priority=None,  # Should be excluded
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards,
            catch_type=None,  # Should be excluded
            match_type=None   # Should be excluded
        )
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.post.return_value = mock_response
        
        resource.create(request)
        
        # Verify None values are excluded
        call_args = resource.client.post.call_args
        data = call_args[1]["json"]
        assert "inbound_domain" not in data
        assert "inbound_priority" not in data
        assert "catch_type" not in data
        assert "match_type" not in data

    def test_create_excludes_forward_ids(self, resource, sample_route_data):
        """Test create excludes forward IDs from request data."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(id="should-be-excluded", type="email", value="test@example.com")]
        
        request = InboundCreateRequest(
            domain_id="domain123",
            name="Test Route",
            domain_enabled=False,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.post.return_value = mock_response
        
        resource.create(request)
        
        # Verify forward ID is excluded
        call_args = resource.client.post.call_args
        data = call_args[1]["json"]
        forward_data = data["forwards"][0]
        assert "id" not in forward_data
        assert forward_data["type"] == "email"
        assert forward_data["value"] == "test@example.com"

    def test_update_method_signature(self, resource, sample_route_data):
        """Test update method accepts InboundUpdateRequest."""
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
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.put.return_value = mock_response
        
        result = resource.update(request)
        assert isinstance(result, InboundResponse)

    def test_update_with_none_request(self, resource):
        """Test update method with None request raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.update(None)
        assert "Request cannot be None" in str(exc_info.value)

    def test_update_with_valid_request(self, resource, sample_route_data):
        """Test update with valid request."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="updated@example.com")]
        
        request = InboundUpdateRequest(
            inbound_id="test-id",
            name="Updated Route",
            domain_enabled=True,
            inbound_domain="updated.example.com",
            inbound_priority=75,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.put.return_value = mock_response
        
        result = resource.update(request)
        
        # Verify client was called correctly
        resource.client.put.assert_called_once()
        call_args = resource.client.put.call_args
        assert call_args[0][0] == "inbound/test-id"
        
        # Verify data structure
        data = call_args[1]["json"]
        assert data["name"] == "Updated Route"
        assert data["domain_enabled"] is True
        assert data["inbound_domain"] == "updated.example.com"
        assert data["inbound_priority"] == 75

    def test_update_excludes_inbound_id_from_data(self, resource, sample_route_data):
        """Test update excludes inbound_id from request data."""
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
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.put.return_value = mock_response
        
        resource.update(request)
        
        # Verify inbound_id is not in request data
        call_args = resource.client.put.call_args
        data = call_args[1]["json"]
        assert "inbound_id" not in data

    def test_delete_method_signature(self, resource):
        """Test delete method accepts InboundDeleteRequest."""
        request = InboundDeleteRequest(inbound_id="test-id")
        
        # Mock successful response
        resource.client.delete.return_value = Mock()
        
        result = resource.delete(request)
        assert result is None

    def test_delete_with_none_request(self, resource):
        """Test delete method with None request raises error."""
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.delete(None)
        assert "Request cannot be None" in str(exc_info.value)

    def test_delete_with_valid_request(self, resource):
        """Test delete with valid request."""
        request = InboundDeleteRequest(inbound_id="test-id")
        
        # Mock successful response
        resource.client.delete.return_value = Mock()
        
        resource.delete(request)
        
        # Verify client was called correctly
        resource.client.delete.assert_called_once_with("inbound/test-id")

    def test_list_response_parsing_error(self, resource):
        """Test list handles response parsing errors."""
        request = InboundListRequest()
        
        # Mock response with invalid data structure that would cause validation errors
        mock_response = Mock()
        mock_response.json.return_value = {"data": [{"invalid": "route_data"}]}
        resource.client.get.return_value = mock_response
        
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.list(request)
        assert "Invalid response format" in str(exc_info.value)

    def test_get_response_parsing_error(self, resource):
        """Test get handles response parsing errors."""
        request = InboundGetRequest(inbound_id="test-id")
        
        # Mock response with invalid JSON structure
        mock_response = Mock()
        mock_response.json.return_value = {"invalid": "structure"}
        resource.client.get.return_value = mock_response
        
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.get(request)
        assert "Invalid response format" in str(exc_info.value)

    def test_create_response_parsing_error(self, resource):
        """Test create handles response parsing errors."""
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
        
        # Mock response with invalid JSON structure
        mock_response = Mock()
        mock_response.json.return_value = {"invalid": "structure"}
        resource.client.post.return_value = mock_response
        
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.create(request)
        assert "Invalid response format" in str(exc_info.value)

    def test_update_response_parsing_error(self, resource):
        """Test update handles response parsing errors."""
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
        
        # Mock response with invalid JSON structure
        mock_response = Mock()
        mock_response.json.return_value = {"invalid": "structure"}
        resource.client.put.return_value = mock_response
        
        with pytest.raises(MailerSendValidationError) as exc_info:
            resource.update(request)
        assert "Invalid response format" in str(exc_info.value)

    def test_complex_filter_serialization(self, resource, sample_route_data):
        """Test complex filter configurations are serialized correctly."""
        # Create complex filter groups
        catch_filters = [{"comparer": "equal", "value": "support"}]
        match_filters = [{"comparer": "contains", "value": "urgent"}]
        
        catch_filter = [InboundFilterGroup(type="catch_recipient", filters=catch_filters)]
        match_filter = [InboundFilterGroup(type="match_sender", filters=match_filters)]
        forwards = [
            InboundForward(type="email", value="support@example.com"),
            InboundForward(type="webhook", value="https://api.example.com/webhook", secret="secret123")
        ]
        
        request = InboundCreateRequest(
            domain_id="domain123",
            name="Complex Route",
            domain_enabled=True,
            inbound_domain="inbound.example.com",
            inbound_priority=25,
            catch_filter=catch_filter,
            catch_type="one",
            match_filter=match_filter,
            match_type="all",
            forwards=forwards
        )
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"data": sample_route_data}
        resource.client.post.return_value = mock_response
        
        resource.create(request)
        
        # Verify complex serialization
        call_args = resource.client.post.call_args
        data = call_args[1]["json"]
        
        # Check catch filter
        assert data["catch_filter"][0]["type"] == "catch_recipient"
        assert data["catch_filter"][0]["filters"] == catch_filters
        assert data["catch_type"] == "one"
        
        # Check match filter
        assert data["match_filter"][0]["type"] == "match_sender"
        assert data["match_filter"][0]["filters"] == match_filters
        assert data["match_type"] == "all"
        
        # Check forwards
        assert len(data["forwards"]) == 2
        assert data["forwards"][0]["type"] == "email"
        assert data["forwards"][1]["type"] == "webhook"
        assert data["forwards"][1]["secret"] == "secret123" 