import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_numbers import (
    SmsNumber, SmsNumbersListRequest, SmsNumberGetRequest, 
    SmsNumberUpdateRequest, SmsNumberDeleteRequest,
    SmsNumbersListResponse, SmsNumberResponse
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

    def test_valid_list_request(self):
        """Test creating valid list request."""
        request = SmsNumbersListRequest(
            paused=False,
            page=1,
            limit=25
        )
        
        assert request.paused is False
        assert request.page == 1
        assert request.limit == 25

    def test_empty_list_request(self):
        """Test creating empty list request."""
        request = SmsNumbersListRequest()
        
        assert request.paused is None
        assert request.page is None
        assert request.limit is None

    def test_to_query_params_full(self):
        """Test converting full request to query parameters."""
        request = SmsNumbersListRequest(
            paused=True,
            page=2,
            limit=50
        )
        
        params = request.to_query_params()
        expected = {
            "paused": "true",
            "page": 2,
            "limit": 50
        }
        
        assert params == expected

    def test_to_query_params_partial(self):
        """Test converting partial request to query parameters."""
        request = SmsNumbersListRequest(page=1)
        
        params = request.to_query_params()
        expected = {"page": 1}
        
        assert params == expected

    def test_to_query_params_empty(self):
        """Test converting empty request to query parameters."""
        request = SmsNumbersListRequest()
        
        params = request.to_query_params()
        expected = {}
        
        assert params == expected

    def test_paused_false_to_query_params(self):
        """Test paused=False converts to 'false' string."""
        request = SmsNumbersListRequest(paused=False)
        
        params = request.to_query_params()
        assert params["paused"] == "false"


class TestSmsNumberGetRequest:
    """Test SMS Number get request model."""

    def test_valid_get_request(self):
        """Test creating valid get request."""
        request = SmsNumberGetRequest(sms_number_id="7z3m5jgrogdpyo6n")
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"

    def test_empty_sms_number_id(self):
        """Test validation error for empty SMS number ID."""
        with pytest.raises(ValidationError) as exc_info:
            SmsNumberGetRequest(sms_number_id="")
        
        error = exc_info.value.errors()[0]
        assert "String should have at least 1 character" in error['msg']


class TestSmsNumberUpdateRequest:
    """Test SMS Number update request model."""

    def test_valid_update_request(self):
        """Test creating valid update request."""
        request = SmsNumberUpdateRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            paused=True
        )
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.paused is True

    def test_update_request_without_paused(self):
        """Test update request without paused parameter."""
        request = SmsNumberUpdateRequest(sms_number_id="7z3m5jgrogdpyo6n")
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.paused is None

    def test_to_json_with_paused(self):
        """Test converting request with paused to JSON."""
        request = SmsNumberUpdateRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            paused=True
        )
        
        json_data = request.to_json()
        expected = {"paused": True}
        
        assert json_data == expected

    def test_to_json_without_paused(self):
        """Test converting request without paused to JSON."""
        request = SmsNumberUpdateRequest(sms_number_id="7z3m5jgrogdpyo6n")
        
        json_data = request.to_json()
        expected = {}
        
        assert json_data == expected


class TestSmsNumberDeleteRequest:
    """Test SMS Number delete request model."""

    def test_valid_delete_request(self):
        """Test creating valid delete request."""
        request = SmsNumberDeleteRequest(sms_number_id="7z3m5jgrogdpyo6n")
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"

    def test_empty_sms_number_id(self):
        """Test validation error for empty SMS number ID."""
        with pytest.raises(ValidationError) as exc_info:
            SmsNumberDeleteRequest(sms_number_id="")
        
        error = exc_info.value.errors()[0]
        assert "String should have at least 1 character" in error['msg']


class TestSmsNumbersListResponse:
    """Test SMS Numbers list response model."""

    def test_valid_list_response(self):
        """Test creating valid list response."""
        sms_numbers = [
            SmsNumber(
                id="7z3m5jgrogdpyo6n",
                telephone_number="+1234567890",
                paused=False,
                created_at=datetime.fromisoformat("2022-01-01T12:00:00.000000")
            ),
            SmsNumber(
                id="8a4n6khrphdqzp7o",
                telephone_number="+1987654321",
                paused=True,
                created_at=datetime.fromisoformat("2022-01-02T12:00:00.000000")
            )
        ]
        
        response = SmsNumbersListResponse(data=sms_numbers)
        
        assert len(response.data) == 2
        assert response.data[0].id == "7z3m5jgrogdpyo6n"
        assert response.data[1].id == "8a4n6khrphdqzp7o"

    def test_empty_list_response(self):
        """Test creating empty list response."""
        response = SmsNumbersListResponse(data=[])
        
        assert len(response.data) == 0


class TestSmsNumberResponse:
    """Test SMS Number response model."""

    def test_valid_response(self):
        """Test creating valid response."""
        sms_number = SmsNumber(
            id="7z3m5jgrogdpyo6n",
            telephone_number="+1234567890",
            paused=False,
            created_at=datetime.fromisoformat("2022-01-01T12:00:00.000000")
        )
        
        response = SmsNumberResponse(data=sms_number)
        
        assert response.data.id == "7z3m5jgrogdpyo6n"
        assert response.data.telephone_number == "+1234567890"
        assert response.data.paused is False