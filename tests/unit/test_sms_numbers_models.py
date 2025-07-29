"""Unit tests for SMS Numbers models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_numbers import (
    SmsNumber,
    SmsNumbersListRequest,
    SmsNumberGetRequest,
    SmsNumberUpdateRequest,
    SmsNumberDeleteRequest,
)


class TestSmsNumber:
    """Test SMS Number model."""

    def test_valid_sms_number(self):
        """Test creating valid SMS number."""
        sms_number = SmsNumber(
            id="7z3m5jgrogdpyo6n",
            telephone_number="+1234567890",
            paused=False,
            created_at=datetime.fromisoformat("2022-01-01T12:00:00.000000")
        )
        
        assert sms_number.id == "7z3m5jgrogdpyo6n"
        assert sms_number.telephone_number == "+1234567890"
        assert sms_number.paused is False
        assert sms_number.created_at == datetime.fromisoformat("2022-01-01T12:00:00.000000")

    def test_sms_number_paused_true(self):
        """Test SMS number with paused=True."""
        sms_number = SmsNumber(
            id="7z3m5jgrogdpyo6n",
            telephone_number="+1234567890",
            paused=True,
            created_at=datetime.fromisoformat("2022-01-01T12:00:00.000000")
        )
        
        assert sms_number.paused is True


class TestSmsNumbersListRequest:
    """Test SMS Numbers list request model."""

    def test_default_values(self):
        """Test SmsNumbersListRequest with default values."""
        request = SmsNumbersListRequest()
        
        assert request.paused is None
        assert request.page is None
        assert request.limit is None

    def test_custom_values(self):
        """Test SmsNumbersListRequest with custom values."""
        request = SmsNumbersListRequest(paused=True, page=2, limit=50)
        
        assert request.paused is True
        assert request.page == 2
        assert request.limit == 50

    def test_to_query_params_empty(self):
        """Test to_query_params with no values set."""
        request = SmsNumbersListRequest()
        params = request.to_query_params()
        
        assert params == {}

    def test_to_query_params_full(self):
        """Test to_query_params with all values set."""
        request = SmsNumbersListRequest(paused=True, page=2, limit=25)
        params = request.to_query_params()
        
        expected = {"paused": "true", "page": 2, "limit": 25}
        assert params == expected

    def test_to_query_params_paused_false(self):
        """Test to_query_params with paused=False."""
        request = SmsNumbersListRequest(paused=False)
        params = request.to_query_params()
        
        expected = {"paused": "false"}
        assert params == expected

    def test_to_query_params_partial(self):
        """Test to_query_params with only some values set."""
        request = SmsNumbersListRequest(page=3)
        params = request.to_query_params()
        
        expected = {"page": 3}
        assert params == expected


class TestSmsNumberGetRequest:
    """Test SMS Number get request model."""

    def test_valid_request(self):
        """Test creating valid get request."""
        request = SmsNumberGetRequest(sms_number_id="7z3m5jgrogdpyo6n")
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"

    def test_empty_id_validation(self):
        """Test validation with empty SMS number ID."""
        with pytest.raises(ValidationError):
            SmsNumberGetRequest(sms_number_id="")


class TestSmsNumberUpdateRequest:
    """Test SMS Number update request model."""

    def test_valid_request_with_paused(self):
        """Test creating valid update request with paused status."""
        request = SmsNumberUpdateRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            paused=True
        )
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.paused is True

    def test_valid_request_without_paused(self):
        """Test creating valid update request without paused status."""
        request = SmsNumberUpdateRequest(sms_number_id="7z3m5jgrogdpyo6n")
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.paused is None

    def test_to_json_with_paused(self):
        """Test to_json method with paused status."""
        request = SmsNumberUpdateRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            paused=False
        )
        json_data = request.to_json()
        
        expected = {"paused": False}
        assert json_data == expected

    def test_to_json_without_paused(self):
        """Test to_json method without paused status."""
        request = SmsNumberUpdateRequest(sms_number_id="7z3m5jgrogdpyo6n")
        json_data = request.to_json()
        
        assert json_data == {}

    def test_empty_id_validation(self):
        """Test validation with empty SMS number ID."""
        with pytest.raises(ValidationError):
            SmsNumberUpdateRequest(sms_number_id="")


class TestSmsNumberDeleteRequest:
    """Test SMS Number delete request model."""

    def test_valid_request(self):
        """Test creating valid delete request."""
        request = SmsNumberDeleteRequest(sms_number_id="7z3m5jgrogdpyo6n")
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"

    def test_empty_id_validation(self):
        """Test validation with empty SMS number ID."""
        with pytest.raises(ValidationError):
            SmsNumberDeleteRequest(sms_number_id="")