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
    SmsInbound,
)


class TestFilterComparer:
    """Test FilterComparer enum."""

    def test_filter_comparer_values(self):
        """Test all FilterComparer enum values."""
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

    def test_valid_filter(self):
        """Test creating valid filter."""
        filter_obj = SmsInboundFilter(comparer=FilterComparer.STARTS_WITH, value="STOP")

        assert filter_obj.comparer == FilterComparer.STARTS_WITH
        assert filter_obj.value == "STOP"

    def test_filter_value_trimming(self):
        """Test that filter value is trimmed."""
        filter_obj = SmsInboundFilter(comparer=FilterComparer.EQUAL, value="  test  ")

        assert filter_obj.value == "test"

    def test_filter_value_validation(self):
        """Test filter value validation."""
        # Empty value should raise error
        with pytest.raises(ValidationError):
            SmsInboundFilter(comparer=FilterComparer.EQUAL, value="")

        # Value too long should raise error
        with pytest.raises(ValidationError):
            SmsInboundFilter(comparer=FilterComparer.EQUAL, value="x" * 256)


class TestSmsInboundsListQueryParams:
    """Test SmsInboundsListQueryParams model."""

    def test_default_values(self):
        """Test default values."""
        params = SmsInboundsListQueryParams()

        assert params.sms_number_id is None
        assert params.enabled is None
        assert params.page is None
        assert params.limit is None

    def test_custom_values(self):
        """Test custom values."""
        params = SmsInboundsListQueryParams(
            sms_number_id="sms123", enabled=True, page=2, limit=50
        )

        assert params.sms_number_id == "sms123"
        assert params.enabled is True
        assert params.page == 2
        assert params.limit == 50

    def test_sms_number_id_trimming(self):
        """Test SMS number ID trimming."""
        params = SmsInboundsListQueryParams(sms_number_id="  sms123  ")
        assert params.sms_number_id == "sms123"

    def test_validation(self):
        """Test field validation."""
        # Page must be >= 1
        with pytest.raises(ValidationError):
            SmsInboundsListQueryParams(page=0)

        # Limit must be between 10 and 100
        with pytest.raises(ValidationError):
            SmsInboundsListQueryParams(limit=9)

        with pytest.raises(ValidationError):
            SmsInboundsListQueryParams(limit=101)

    def test_to_query_params_empty(self):
        """Test to_query_params with default values."""
        params = SmsInboundsListQueryParams()
        result = params.to_query_params()

        assert result == {}

    def test_to_query_params_full(self):
        """Test to_query_params with all values."""
        params = SmsInboundsListQueryParams(
            sms_number_id="sms123", enabled=True, page=2, limit=50
        )
        result = params.to_query_params()

        expected = {"sms_number_id": "sms123", "enabled": True, "page": 2, "limit": 50}
        assert result == expected


class TestSmsInboundsListRequest:
    """Test SmsInboundsListRequest model."""

    def test_default_request(self):
        """Test creating request with default query params."""
        request = SmsInboundsListRequest()

        assert isinstance(request.query_params, SmsInboundsListQueryParams)
        assert request.to_query_params() == {}

    def test_custom_request(self):
        """Test creating request with custom query params."""
        query_params = SmsInboundsListQueryParams(sms_number_id="sms123", enabled=False)
        request = SmsInboundsListRequest(query_params=query_params)

        result = request.to_query_params()
        expected = {"sms_number_id": "sms123", "enabled": False}
        assert result == expected


class TestSmsInboundGetRequest:
    """Test SmsInboundGetRequest model."""

    def test_valid_request(self):
        """Test creating valid get request."""
        request = SmsInboundGetRequest(sms_inbound_id="inbound123")

        assert request.sms_inbound_id == "inbound123"

    def test_id_trimming(self):
        """Test SMS inbound ID trimming."""
        request = SmsInboundGetRequest(sms_inbound_id="  inbound123  ")
        assert request.sms_inbound_id == "inbound123"

    def test_empty_id_validation(self):
        """Test empty ID validation."""
        with pytest.raises(ValidationError):
            SmsInboundGetRequest(sms_inbound_id="")


class TestSmsInboundCreateRequest:
    """Test SmsInboundCreateRequest model."""

    def test_minimal_request(self):
        """Test creating request with minimal fields."""
        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Test Route",
            forward_url="https://example.com/webhook",
        )

        assert request.sms_number_id == "sms123"
        assert request.name == "Test Route"
        assert request.forward_url == "https://example.com/webhook"
        assert request.filter is None
        assert request.enabled is True  # default value

    def test_complete_request(self):
        """Test creating request with all fields."""
        filter_obj = SmsInboundFilter(comparer=FilterComparer.STARTS_WITH, value="STOP")

        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Test Route",
            forward_url="https://example.com/webhook",
            filter=filter_obj,
            enabled=False,
        )

        assert request.filter == filter_obj
        assert request.enabled is False

    def test_field_trimming(self):
        """Test field trimming."""
        request = SmsInboundCreateRequest(
            sms_number_id="  sms123  ",
            name="  Test Route  ",
            forward_url="  https://example.com/webhook  ",
        )

        assert request.sms_number_id == "sms123"
        assert request.name == "Test Route"
        assert request.forward_url == "https://example.com/webhook"

    def test_field_validation(self):
        """Test field validation."""
        # Empty fields should raise errors
        with pytest.raises(ValidationError):
            SmsInboundCreateRequest(
                sms_number_id="", name="Test", forward_url="https://example.com"
            )

        # Name too long should raise error
        with pytest.raises(ValidationError):
            SmsInboundCreateRequest(
                sms_number_id="sms123",
                name="x" * 192,
                forward_url="https://example.com",
            )

        # URL too long should raise error
        with pytest.raises(ValidationError):
            SmsInboundCreateRequest(
                sms_number_id="sms123",
                name="Test",
                forward_url="https://example.com/" + "x" * 250,
            )

    def test_to_request_body_minimal(self):
        """Test converting minimal request to body."""
        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Test Route",
            forward_url="https://example.com/webhook",
        )

        body = request.to_request_body()
        expected = {
            "sms_number_id": "sms123",
            "name": "Test Route",
            "forward_url": "https://example.com/webhook",
            "enabled": True,
        }
        assert body == expected

    def test_to_request_body_with_filter(self):
        """Test converting request with filter to body."""
        filter_obj = SmsInboundFilter(comparer=FilterComparer.CONTAINS, value="STOP")

        request = SmsInboundCreateRequest(
            sms_number_id="sms123",
            name="Test Route",
            forward_url="https://example.com/webhook",
            filter=filter_obj,
            enabled=False,
        )

        body = request.to_request_body()
        expected = {
            "sms_number_id": "sms123",
            "name": "Test Route",
            "forward_url": "https://example.com/webhook",
            "enabled": False,
            "filter": {"comparer": "contains", "value": "STOP"},
        }
        assert body == expected


class TestSmsInboundUpdateRequest:
    """Test SmsInboundUpdateRequest model."""

    def test_minimal_request(self):
        """Test creating request with only ID."""
        request = SmsInboundUpdateRequest(sms_inbound_id="inbound123")

        assert request.sms_inbound_id == "inbound123"
        assert request.sms_number_id is None
        assert request.name is None
        assert request.forward_url is None
        assert request.filter is None
        assert request.enabled is None

    def test_complete_request(self):
        """Test creating request with all fields."""
        filter_obj = SmsInboundFilter(comparer=FilterComparer.EQUAL, value="HELP")

        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound123",
            sms_number_id="sms456",
            name="Updated Route",
            forward_url="https://updated.com/webhook",
            filter=filter_obj,
            enabled=True,
        )

        assert request.sms_inbound_id == "inbound123"
        assert request.sms_number_id == "sms456"
        assert request.name == "Updated Route"
        assert request.forward_url == "https://updated.com/webhook"
        assert request.filter == filter_obj
        assert request.enabled is True

    def test_field_trimming(self):
        """Test field trimming."""
        request = SmsInboundUpdateRequest(
            sms_inbound_id="  inbound123  ",
            sms_number_id="  sms456  ",
            name="  Updated Route  ",
            forward_url="  https://updated.com/webhook  ",
        )

        assert request.sms_inbound_id == "inbound123"
        assert request.sms_number_id == "sms456"
        assert request.name == "Updated Route"
        assert request.forward_url == "https://updated.com/webhook"

    def test_to_request_body_minimal(self):
        """Test converting minimal request to body."""
        request = SmsInboundUpdateRequest(sms_inbound_id="inbound123")

        body = request.to_request_body()
        assert body == {}

    def test_to_request_body_partial(self):
        """Test converting partial request to body."""
        request = SmsInboundUpdateRequest(
            sms_inbound_id="inbound123", name="Updated Route", enabled=False
        )

        body = request.to_request_body()
        expected = {"name": "Updated Route", "enabled": False}
        assert body == expected


class TestSmsInboundDeleteRequest:
    """Test SmsInboundDeleteRequest model."""

    def test_valid_request(self):
        """Test creating valid delete request."""
        request = SmsInboundDeleteRequest(sms_inbound_id="inbound123")

        assert request.sms_inbound_id == "inbound123"

    def test_id_trimming(self):
        """Test SMS inbound ID trimming."""
        request = SmsInboundDeleteRequest(sms_inbound_id="  inbound123  ")
        assert request.sms_inbound_id == "inbound123"

    def test_empty_id_validation(self):
        """Test empty ID validation."""
        with pytest.raises(ValidationError):
            SmsInboundDeleteRequest(sms_inbound_id="")


class TestSmsInbound:
    """Test SmsInbound model."""

    def test_minimal_inbound(self):
        """Test creating minimal SMS inbound."""
        data = {
            "id": "inbound123",
            "name": "Basic Route",
            "forward_url": "https://example.com/webhook",
            "enabled": True,
            "created_at": "2023-01-01T12:00:00.000000Z",
        }

        inbound = SmsInbound.model_validate(data)

        assert inbound.id == "inbound123"
        assert inbound.name == "Basic Route"
        assert inbound.filter is None
        assert inbound.forward_url == "https://example.com/webhook"
        assert inbound.enabled is True
        assert inbound.secret is None
        assert isinstance(inbound.created_at, datetime)
        assert inbound.sms_number is None

    def test_complete_inbound(self):
        """Test creating complete SMS inbound."""
        data = {
            "id": "inbound456",
            "name": "Filtered Inbound",
            "filter": {"comparer": "starts-with", "value": "START"},
            "forward_url": "https://example.com/filtered",
            "enabled": False,
            "secret": "secret123",
            "created_at": "2023-01-01T12:00:00.000000Z",
            "sms_number": {
                "id": "sms789",
                "telephone_number": "+9876543210",
                "paused": True,
                "created_at": "2023-01-01T11:00:00.000000Z",
            },
        }

        inbound = SmsInbound.model_validate(data)

        assert inbound.id == "inbound456"
        assert inbound.name == "Filtered Inbound"
        assert inbound.filter == {"comparer": "starts-with", "value": "START"}
        assert inbound.forward_url == "https://example.com/filtered"
        assert inbound.enabled is False
        assert inbound.secret == "secret123"
        assert isinstance(inbound.created_at, datetime)
        assert isinstance(inbound.sms_number, dict)
        assert inbound.sms_number["id"] == "sms789"
