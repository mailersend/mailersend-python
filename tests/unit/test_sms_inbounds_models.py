"""Tests for SMS Inbounds models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_inbounds import (
    FilterComparer,
    SmsInboundFilter,
    SmsInboundsListQueryParams,
    SmsInboundsListRequest,
    SmsInboundGetRequest,
    SmsInboundCreateRequest,
    SmsInboundUpdateRequest,
    SmsInboundDeleteRequest,
    SmsNumber,
    SmsInbound,
    SmsInboundsListResponse,
    SmsInboundGetResponse,
    SmsInboundCreateResponse,
    SmsInboundUpdateResponse,
    SmsInboundDeleteResponse,
)


class TestFilterComparer:
    """Test FilterComparer enum."""
    
    def test_filter_comparer_values(self):
        """Test FilterComparer enum values."""
        assert FilterComparer.EQUAL == "equal"
        assert FilterComparer.NOT_EQUAL == "not-equal"
        assert FilterComparer.CONTAINS == "contains"
        assert FilterComparer.NOT_CONTAINS == "not-contains"
        assert FilterComparer.STARTS_WITH == "starts-with"
        assert FilterComparer.ENDS_WITH == "ends-with"
        assert FilterComparer.NOT_STARTS_WITH == "not-starts-with"
        assert FilterComparer.NOT_ENDS_WITH == "not-ends-with"


class TestSmsInboundFilter:
    """Test SmsInboundFilter model."""
    
    def test_sms_inbound_filter_valid(self):
        """Test SmsInboundFilter with valid data."""
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.EQUAL,
            value="START"
        )
        
        assert filter_obj.comparer == FilterComparer.EQUAL
        assert filter_obj.value == "START"
    
    def test_sms_inbound_filter_whitespace_strip(self):
        """Test filter value whitespace stripping."""
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.CONTAINS,
            value="  test value  "
        )
        assert filter_obj.value == "test value"
    
    def test_sms_inbound_filter_validation_empty_value(self):
        """Test SmsInboundFilter validation with empty value."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsInboundFilter(
                comparer=FilterComparer.EQUAL,
                value=""
            )
    
    def test_sms_inbound_filter_validation_missing_fields(self):
        """Test SmsInboundFilter validation with missing fields."""
        with pytest.raises(ValidationError):
            SmsInboundFilter()


class TestSmsInboundsListQueryParams:
    """Test SmsInboundsListQueryParams model."""
    
    def test_sms_inbounds_list_query_params_all_fields(self):
        """Test SmsInboundsListQueryParams with all fields."""
        params = SmsInboundsListQueryParams(
            sms_number_id="sms123",
            enabled=True,
            page=2,
            limit=50
        )
        
        assert params.sms_number_id == "sms123"
        assert params.enabled is True
        assert params.page == 2
        assert params.limit == 50
    
    def test_sms_inbounds_list_query_params_defaults(self):
        """Test SmsInboundsListQueryParams with default values."""
        params = SmsInboundsListQueryParams()
        
        assert params.sms_number_id is None
        assert params.enabled is None
        assert params.page is None
        assert params.limit is None
    
    def test_sms_inbounds_list_query_params_whitespace_strip(self):
        """Test sms_number_id whitespace stripping."""
        params = SmsInboundsListQueryParams(sms_number_id="  sms456  ")
        assert params.sms_number_id == "sms456"
    
    def test_sms_inbounds_list_query_params_validation_limits(self):
        """Test SmsInboundsListQueryParams validation for page and limit."""
        # Test page validation
        with pytest.raises(ValidationError):
            SmsInboundsListQueryParams(page=0)
        
        # Test limit validation
        with pytest.raises(ValidationError):
            SmsInboundsListQueryParams(limit=5)  # Too low
        
        with pytest.raises(ValidationError):
            SmsInboundsListQueryParams(limit=150)  # Too high
    
    def test_sms_inbounds_list_query_params_to_query_params_all(self):
        """Test to_query_params with all fields set."""
        params = SmsInboundsListQueryParams(
            sms_number_id="sms789",
            enabled=False,
            page=3,
            limit=25
        )
        result = params.to_query_params()
        
        expected = {
            "sms_number_id": "sms789",
            "enabled": False,
            "page": 3,
            "limit": 25
        }
        assert result == expected
    
    def test_sms_inbounds_list_query_params_to_query_params_partial(self):
        """Test to_query_params with only some fields set."""
        params = SmsInboundsListQueryParams(
            sms_number_id="sms999",
            page=1
        )
        result = params.to_query_params()
        
        expected = {
            "sms_number_id": "sms999",
            "page": 1
        }
        assert result == expected
    
    def test_sms_inbounds_list_query_params_to_query_params_empty(self):
        """Test to_query_params with no fields set."""
        params = SmsInboundsListQueryParams()
        result = params.to_query_params()
        
        assert result == {}


class TestSmsInboundsListRequest:
    """Test SmsInboundsListRequest model."""
    
    def test_sms_inbounds_list_request_with_query_params(self):
        """Test SmsInboundsListRequest with query parameters."""
        query_params = SmsInboundsListQueryParams(
            sms_number_id="sms123",
            enabled=True
        )
        request = SmsInboundsListRequest(query_params=query_params)
        
        assert request.query_params == query_params
    
    def test_sms_inbounds_list_request_default_factory(self):
        """Test SmsInboundsListRequest with default factory."""
        request = SmsInboundsListRequest()
        
        assert isinstance(request.query_params, SmsInboundsListQueryParams)
        assert request.query_params.sms_number_id is None
    
    def test_sms_inbounds_list_request_to_query_params(self):
        """Test to_query_params method."""
        query_params = SmsInboundsListQueryParams(
            sms_number_id="sms456",
            page=2
        )
        request = SmsInboundsListRequest(query_params=query_params)
        result = request.to_query_params()
        
        expected = {
            "sms_number_id": "sms456",
            "page": 2
        }
        assert result == expected


class TestSmsInboundGetRequest:
    """Test SmsInboundGetRequest model."""
    
    def test_sms_inbound_get_request_valid(self):
        """Test SmsInboundGetRequest with valid data."""
        request = SmsInboundGetRequest(sms_inbound_id="inbound123")
        assert request.sms_inbound_id == "inbound123"
    
    def test_sms_inbound_get_request_whitespace_strip(self):
        """Test sms_inbound_id whitespace stripping."""
        request = SmsInboundGetRequest(sms_inbound_id="  inbound456  ")
        assert request.sms_inbound_id == "inbound456"
    
    def test_sms_inbound_get_request_validation_empty(self):
        """Test SmsInboundGetRequest validation with empty ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsInboundGetRequest(sms_inbound_id="")
    
    def test_sms_inbound_get_request_validation_missing(self):
        """Test SmsInboundGetRequest validation with missing ID."""
        with pytest.raises(ValidationError):
            SmsInboundGetRequest()


class TestSmsInboundCreateRequest:
    """Test SmsInboundCreateRequest model."""
    
    def test_sms_inbound_create_request_valid_minimal(self):
        """Test SmsInboundCreateRequest with minimal required fields."""
        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Test Inbound",
            forward_url="https://example.com/webhook"
        )
        
        assert request.sms_number_id == "sms123"
        assert request.name == "Test Inbound"
        assert request.forward_url == "https://example.com/webhook"
        assert request.filter is None
        assert request.enabled is True  # Default value
    
    def test_sms_inbound_create_request_valid_with_filter(self):
        """Test SmsInboundCreateRequest with filter."""
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.STARTS_WITH,
            value="START"
        )
        request = SmsInboundCreateRequest(
            sms_number_id="sms456",
            name="Filtered Inbound",
            forward_url="https://example.com/filtered",
            filter=filter_obj,
            enabled=False
        )
        
        assert request.sms_number_id == "sms456"
        assert request.name == "Filtered Inbound"
        assert request.forward_url == "https://example.com/filtered"
        assert request.filter == filter_obj
        assert request.enabled is False
    
    def test_sms_inbound_create_request_whitespace_strip(self):
        """Test string field whitespace stripping."""
        request = SmsInboundCreateRequest(
            sms_number_id="  sms789  ",
            name="  Test Name  ",
            forward_url="  https://example.com/test  "
        )
        
        assert request.sms_number_id == "sms789"
        assert request.name == "Test Name"
        assert request.forward_url == "https://example.com/test"
    
    def test_sms_inbound_create_request_validation_empty_fields(self):
        """Test SmsInboundCreateRequest validation with empty required fields."""
        # Empty SMS number ID
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsInboundCreateRequest(
                sms_number_id="",
                name="Test",
                forward_url="https://example.com"
            )
        
        # Empty name
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsInboundCreateRequest(
                sms_number_id="sms123",
                name="",
                forward_url="https://example.com"
            )
        
        # Empty forward URL
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsInboundCreateRequest(
                sms_number_id="sms123",
                name="Test",
                forward_url=""
            )
    
    def test_sms_inbound_create_request_validation_missing_fields(self):
        """Test SmsInboundCreateRequest validation with missing required fields."""
        with pytest.raises(ValidationError):
            SmsInboundCreateRequest()
    
    def test_sms_inbound_create_request_to_request_body_minimal(self):
        """Test to_request_body with minimal fields."""
        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Test Inbound",
            forward_url="https://example.com/webhook"
        )
        result = request.to_request_body()
        
        expected = {
            "sms_number_id": "sms123",
            "name": "Test Inbound",
            "forward_url": "https://example.com/webhook",
            "enabled": True
        }
        assert result == expected
    
    def test_sms_inbound_create_request_to_request_body_with_filter(self):
        """Test to_request_body with filter."""
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.CONTAINS,
            value="STOP"
        )
        request = SmsInboundCreateRequest(
            sms_number_id="sms456",
            name="Filtered Route",
            forward_url="https://example.com/filtered",
            filter=filter_obj,
            enabled=False
        )
        result = request.to_request_body()
        
        expected = {
            "sms_number_id": "sms456",
            "name": "Filtered Route",
            "forward_url": "https://example.com/filtered",
            "filter": {
                "comparer": "contains",
                "value": "STOP"
            },
            "enabled": False
        }
        assert result == expected


class TestSmsInboundUpdateRequest:
    """Test SmsInboundUpdateRequest model."""
    
    def test_sms_inbound_update_request_valid_partial(self):
        """Test SmsInboundUpdateRequest with partial update."""
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound123",
            name="Updated Name"
        )
        
        assert request.sms_inbound_id == "inbound123"
        assert request.name == "Updated Name"
        assert request.sms_number_id is None
        assert request.forward_url is None
        assert request.filter is None
        assert request.enabled is None
    
    def test_sms_inbound_update_request_valid_full(self):
        """Test SmsInboundUpdateRequest with all fields."""
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.ENDS_WITH,
            value="END"
        )
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound456",
            sms_number_id="sms789",
            name="Fully Updated",
            forward_url="https://example.com/updated",
            filter=filter_obj,
            enabled=True
        )
        
        assert request.sms_inbound_id == "inbound456"
        assert request.sms_number_id == "sms789"
        assert request.name == "Fully Updated"
        assert request.forward_url == "https://example.com/updated"
        assert request.filter == filter_obj
        assert request.enabled is True
    
    def test_sms_inbound_update_request_whitespace_strip(self):
        """Test string field whitespace stripping."""
        request = SmsInboundUpdateRequest(
            sms_inbound_id="  inbound999  ",
            sms_number_id="  sms111  ",
            name="  Updated  ",
            forward_url="  https://example.com/new  "
        )
        
        assert request.sms_inbound_id == "inbound999"
        assert request.sms_number_id == "sms111"
        assert request.name == "Updated"
        assert request.forward_url == "https://example.com/new"
    
    def test_sms_inbound_update_request_validation_empty_id(self):
        """Test SmsInboundUpdateRequest validation with empty ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsInboundUpdateRequest(
                sms_inbound_id="",
                name="Test"
            )
    
    def test_sms_inbound_update_request_validation_missing_id(self):
        """Test SmsInboundUpdateRequest validation with missing ID."""
        with pytest.raises(ValidationError):
            SmsInboundUpdateRequest(name="Test")
    
    def test_sms_inbound_update_request_to_request_body_partial(self):
        """Test to_request_body with partial fields."""
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound123",
            name="New Name",
            enabled=False
        )
        result = request.to_request_body()
        
        expected = {
            "name": "New Name",
            "enabled": False
        }
        assert result == expected
    
    def test_sms_inbound_update_request_to_request_body_full(self):
        """Test to_request_body with all fields."""
        filter_obj = SmsInboundFilter(
            comparer=FilterComparer.NOT_EQUAL,
            value="IGNORE"
        )
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound456",
            sms_number_id="sms222",
            name="Complete Update",
            forward_url="https://example.com/complete",
            filter=filter_obj,
            enabled=True
        )
        result = request.to_request_body()
        
        expected = {
            "sms_number_id": "sms222",
            "name": "Complete Update",
            "forward_url": "https://example.com/complete",
            "filter": {
                "comparer": "not-equal",
                "value": "IGNORE"
            },
            "enabled": True
        }
        assert result == expected


class TestSmsInboundDeleteRequest:
    """Test SmsInboundDeleteRequest model."""
    
    def test_sms_inbound_delete_request_valid(self):
        """Test SmsInboundDeleteRequest with valid data."""
        request = SmsInboundDeleteRequest(sms_inbound_id="inbound123")
        assert request.sms_inbound_id == "inbound123"
    
    def test_sms_inbound_delete_request_whitespace_strip(self):
        """Test sms_inbound_id whitespace stripping."""
        request = SmsInboundDeleteRequest(sms_inbound_id="  inbound456  ")
        assert request.sms_inbound_id == "inbound456"
    
    def test_sms_inbound_delete_request_validation_empty(self):
        """Test SmsInboundDeleteRequest validation with empty ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsInboundDeleteRequest(sms_inbound_id="")
    
    def test_sms_inbound_delete_request_validation_missing(self):
        """Test SmsInboundDeleteRequest validation with missing ID."""
        with pytest.raises(ValidationError):
            SmsInboundDeleteRequest()


class TestSmsNumber:
    """Test SmsNumber model."""
    
    def test_sms_number_creation(self):
        """Test SmsNumber creation."""
        data = {
            "id": "sms123",
            "telephone_number": "+1234567890",
            "paused": False,
            "created_at": "2023-01-01T12:00:00.000000Z"
        }
        
        sms_number = SmsNumber.model_validate(data)
        
        assert sms_number.id == "sms123"
        assert sms_number.telephone_number == "+1234567890"
        assert sms_number.paused is False
        assert isinstance(sms_number.created_at, datetime)


class TestSmsInbound:
    """Test SmsInbound model."""
    
    def test_sms_inbound_creation_minimal(self):
        """Test SmsInbound creation with minimal fields."""
        data = {
            "id": "inbound123",
            "name": "Test Inbound",
            "forward_url": "https://example.com/webhook",
            "enabled": True,
            "created_at": "2023-01-01T12:00:00.000000Z"
        }
        
        inbound = SmsInbound.model_validate(data)
        
        assert inbound.id == "inbound123"
        assert inbound.name == "Test Inbound"
        assert inbound.filter is None
        assert inbound.forward_url == "https://example.com/webhook"
        assert inbound.enabled is True
        assert inbound.secret is None
        assert isinstance(inbound.created_at, datetime)
        assert inbound.sms_number is None
    
    def test_sms_inbound_creation_with_filter_and_sms_number(self):
        """Test SmsInbound creation with filter and SMS number."""
        data = {
            "id": "inbound456",
            "name": "Filtered Inbound",
            "filter": {
                "comparer": "starts-with",
                "value": "START"
            },
            "forward_url": "https://example.com/filtered",
            "enabled": False,
            "secret": "secret123",
            "created_at": "2023-01-01T12:00:00.000000Z",
            "sms_number": {
                "id": "sms789",
                "telephone_number": "+9876543210",
                "paused": True,
                "created_at": "2023-01-01T11:00:00.000000Z"
            }
        }
        
        inbound = SmsInbound.model_validate(data)
        
        assert inbound.id == "inbound456"
        assert inbound.name == "Filtered Inbound"
        assert inbound.filter == {"comparer": "starts-with", "value": "START"}
        assert inbound.forward_url == "https://example.com/filtered"
        assert inbound.enabled is False
        assert inbound.secret == "secret123"
        assert isinstance(inbound.created_at, datetime)
        assert isinstance(inbound.sms_number, SmsNumber)
        assert inbound.sms_number.id == "sms789"


class TestSmsInboundsListResponse:
    """Test SmsInboundsListResponse model."""
    
    def test_sms_inbounds_list_response_creation(self):
        """Test SmsInboundsListResponse creation."""
        data = {
            "data": [
                {
                    "id": "inbound1",
                    "name": "First Inbound",
                    "forward_url": "https://example.com/first",
                    "enabled": True,
                    "created_at": "2023-01-01T12:00:00.000000Z"
                },
                {
                    "id": "inbound2",
                    "name": "Second Inbound",
                    "forward_url": "https://example.com/second",
                    "enabled": False,
                    "created_at": "2023-01-01T13:00:00.000000Z"
                }
            ]
        }
        
        response = SmsInboundsListResponse.model_validate(data)
        
        assert len(response.data) == 2
        assert all(isinstance(inbound, SmsInbound) for inbound in response.data)
        assert response.data[0].id == "inbound1"
        assert response.data[1].id == "inbound2"


class TestSmsInboundGetResponse:
    """Test SmsInboundGetResponse model."""
    
    def test_sms_inbound_get_response_creation(self):
        """Test SmsInboundGetResponse creation."""
        data = {
            "data": {
                "id": "inbound123",
                "name": "Get Response Inbound",
                "forward_url": "https://example.com/get",
                "enabled": True,
                "created_at": "2023-01-01T12:00:00.000000Z"
            }
        }
        
        response = SmsInboundGetResponse.model_validate(data)
        
        assert isinstance(response.data, SmsInbound)
        assert response.data.id == "inbound123"


class TestSmsInboundCreateResponse:
    """Test SmsInboundCreateResponse model."""
    
    def test_sms_inbound_create_response_creation(self):
        """Test SmsInboundCreateResponse creation."""
        data = {
            "data": {
                "id": "inbound456",
                "name": "Created Inbound",
                "forward_url": "https://example.com/created",
                "enabled": True,
                "secret": "new_secret",
                "created_at": "2023-01-01T12:00:00.000000Z"
            }
        }
        
        response = SmsInboundCreateResponse.model_validate(data)
        
        assert isinstance(response.data, SmsInbound)
        assert response.data.id == "inbound456"
        assert response.data.secret == "new_secret"


class TestSmsInboundUpdateResponse:
    """Test SmsInboundUpdateResponse model."""
    
    def test_sms_inbound_update_response_creation(self):
        """Test SmsInboundUpdateResponse creation."""
        data = {
            "data": {
                "id": "inbound789",
                "name": "Updated Inbound",
                "forward_url": "https://example.com/updated",
                "enabled": False,
                "created_at": "2023-01-01T12:00:00.000000Z"
            }
        }
        
        response = SmsInboundUpdateResponse.model_validate(data)
        
        assert isinstance(response.data, SmsInbound)
        assert response.data.id == "inbound789"
        assert response.data.enabled is False


class TestSmsInboundDeleteResponse:
    """Test SmsInboundDeleteResponse model."""
    
    def test_sms_inbound_delete_response_creation(self):
        """Test SmsInboundDeleteResponse creation."""
        data = {
            "message": "SMS inbound route deleted successfully"
        }
        
        response = SmsInboundDeleteResponse.model_validate(data)
        
        assert response.message == "SMS inbound route deleted successfully" 