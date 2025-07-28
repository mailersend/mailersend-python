"""Tests for SMS Recipients models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_recipients import (
    SmsRecipientStatus,
    SmsRecipientsListQueryParams,
    SmsRecipientsListRequest,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsMessage,
    SmsRecipient,
    SmsRecipientDetails,
    SmsRecipientsListResponse,
    SmsRecipientGetResponse,
    SmsRecipientUpdateResponse,
)


class TestSmsRecipientStatus:
    """Test SmsRecipientStatus enum."""
    
    def test_sms_recipient_status_values(self):
        """Test SmsRecipientStatus enum values."""
        assert SmsRecipientStatus.ACTIVE == "active"
        assert SmsRecipientStatus.OPT_OUT == "opt_out"


class TestSmsRecipientsListQueryParams:
    """Test SmsRecipientsListQueryParams model."""
    
    def test_sms_recipients_list_query_params_defaults(self):
        """Test SmsRecipientsListQueryParams with default values."""
        params = SmsRecipientsListQueryParams()
        
        assert params.status is None
        assert params.sms_number_id is None
        assert params.page == 1
        assert params.limit == 25
    
    def test_sms_recipients_list_query_params_custom_values(self):
        """Test SmsRecipientsListQueryParams with custom values."""
        params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.ACTIVE,
            sms_number_id="sms123",
            page=2,
            limit=50
        )
        
        assert params.status == SmsRecipientStatus.ACTIVE
        assert params.sms_number_id == "sms123"
        assert params.page == 2
        assert params.limit == 50
    
    def test_sms_recipients_list_query_params_validation(self):
        """Test SmsRecipientsListQueryParams validation."""
        # Test invalid page
        with pytest.raises(ValidationError):
            SmsRecipientsListQueryParams(page=0)
        
        # Test invalid limit (too low)
        with pytest.raises(ValidationError):
            SmsRecipientsListQueryParams(limit=5)
        
        # Test invalid limit (too high)
        with pytest.raises(ValidationError):
            SmsRecipientsListQueryParams(limit=150)
    
    def test_sms_recipients_list_query_params_sms_number_id_validation(self):
        """Test sms_number_id validation."""
        # Test whitespace stripping
        params = SmsRecipientsListQueryParams(sms_number_id="  sms123  ")
        assert params.sms_number_id == "sms123"
        
        # Test None value
        params = SmsRecipientsListQueryParams(sms_number_id=None)
        assert params.sms_number_id is None
    
    def test_sms_recipients_list_query_params_to_query_params_defaults(self):
        """Test to_query_params with default values."""
        params = SmsRecipientsListQueryParams()
        result = params.to_query_params()
        
        # Default values should be excluded
        assert result == {}
    
    def test_sms_recipients_list_query_params_to_query_params_custom(self):
        """Test to_query_params with custom values."""
        params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.OPT_OUT,
            sms_number_id="sms456",
            page=3,
            limit=15
        )
        result = params.to_query_params()
        
        expected = {
            "status": "opt_out",
            "sms_number_id": "sms456",
            "page": 3,
            "limit": 15
        }
        assert result == expected
    
    def test_sms_recipients_list_query_params_to_query_params_partial(self):
        """Test to_query_params with some custom values."""
        params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.ACTIVE,
            page=2  # limit stays default
        )
        result = params.to_query_params()
        
        expected = {
            "status": "active",
            "page": 2
        }
        assert result == expected


class TestSmsRecipientsListRequest:
    """Test SmsRecipientsListRequest model."""
    
    def test_sms_recipients_list_request_defaults(self):
        """Test SmsRecipientsListRequest with default values."""
        request = SmsRecipientsListRequest()
        
        assert isinstance(request.query_params, SmsRecipientsListQueryParams)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
    
    def test_sms_recipients_list_request_custom_query_params(self):
        """Test SmsRecipientsListRequest with custom query params."""
        query_params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.ACTIVE,
            page=2
        )
        request = SmsRecipientsListRequest(query_params=query_params)
        
        assert request.query_params == query_params
    
    def test_sms_recipients_list_request_to_query_params(self):
        """Test to_query_params method."""
        query_params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.OPT_OUT,
            sms_number_id="sms789",
            page=4
        )
        request = SmsRecipientsListRequest(query_params=query_params)
        result = request.to_query_params()
        
        expected = {
            "status": "opt_out",
            "sms_number_id": "sms789",
            "page": 4
        }
        assert result == expected


class TestSmsRecipientGetRequest:
    """Test SmsRecipientGetRequest model."""
    
    def test_sms_recipient_get_request_valid(self):
        """Test SmsRecipientGetRequest with valid data."""
        request = SmsRecipientGetRequest(sms_recipient_id="recipient123")
        assert request.sms_recipient_id == "recipient123"
    
    def test_sms_recipient_get_request_whitespace_strip(self):
        """Test sms_recipient_id whitespace stripping."""
        request = SmsRecipientGetRequest(sms_recipient_id="  recipient456  ")
        assert request.sms_recipient_id == "recipient456"
    
    def test_sms_recipient_get_request_validation_empty(self):
        """Test SmsRecipientGetRequest validation with empty ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsRecipientGetRequest(sms_recipient_id="")
    
    def test_sms_recipient_get_request_validation_whitespace_only(self):
        """Test SmsRecipientGetRequest validation with whitespace-only ID."""
        with pytest.raises(ValidationError, match="SMS recipient ID cannot be empty"):
            SmsRecipientGetRequest(sms_recipient_id="   ")
    
    def test_sms_recipient_get_request_validation_missing(self):
        """Test SmsRecipientGetRequest validation with missing ID."""
        with pytest.raises(ValidationError):
            SmsRecipientGetRequest()


class TestSmsRecipientUpdateRequest:
    """Test SmsRecipientUpdateRequest model."""
    
    def test_sms_recipient_update_request_valid(self):
        """Test SmsRecipientUpdateRequest with valid data."""
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient123",
            status=SmsRecipientStatus.OPT_OUT
        )
        assert request.sms_recipient_id == "recipient123"
        assert request.status == SmsRecipientStatus.OPT_OUT
    
    def test_sms_recipient_update_request_whitespace_strip(self):
        """Test sms_recipient_id whitespace stripping."""
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="  recipient456  ",
            status=SmsRecipientStatus.ACTIVE
        )
        assert request.sms_recipient_id == "recipient456"
    
    def test_sms_recipient_update_request_validation_empty_id(self):
        """Test SmsRecipientUpdateRequest validation with empty ID."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            SmsRecipientUpdateRequest(
                sms_recipient_id="",
                status=SmsRecipientStatus.ACTIVE
            )
    
    def test_sms_recipient_update_request_validation_missing_fields(self):
        """Test SmsRecipientUpdateRequest validation with missing fields."""
        with pytest.raises(ValidationError):
            SmsRecipientUpdateRequest()
        
        with pytest.raises(ValidationError):
            SmsRecipientUpdateRequest(sms_recipient_id="recipient123")
    
    def test_sms_recipient_update_request_to_request_body(self):
        """Test to_request_body method."""
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient123",
            status=SmsRecipientStatus.OPT_OUT
        )
        result = request.to_request_body()
        
        expected = {"status": "opt_out"}
        assert result == expected


class TestSmsMessage:
    """Test SmsMessage model."""
    
    def test_sms_message_creation(self):
        """Test SmsMessage creation with all fields."""
        data = {
            "id": "msg123",
            "from": "+1234567890",
            "to": "+0987654321",
            "text": "Test message",
            "status": "delivered",
            "segment_count": 1,
            "error_type": None,
            "error_description": None,
            "created_at": "2023-01-01T12:00:00.000000Z"
        }
        
        message = SmsMessage.model_validate(data)
        
        assert message.id == "msg123"
        assert message.from_ == "+1234567890"
        assert message.to == "+0987654321"
        assert message.text == "Test message"
        assert message.status == "delivered"
        assert message.segment_count == 1
        assert message.error_type is None
        assert message.error_description is None
        assert isinstance(message.created_at, datetime)
    
    def test_sms_message_with_error(self):
        """Test SmsMessage with error fields."""
        data = {
            "id": "msg456",
            "from": "+1234567890",
            "to": "+0987654321",
            "text": "Test message",
            "status": "failed",
            "segment_count": 1,
            "error_type": "invalid_number",
            "error_description": "Invalid phone number format",
            "created_at": "2023-01-01T12:00:00.000000Z"
        }
        
        message = SmsMessage.model_validate(data)
        
        assert message.error_type == "invalid_number"
        assert message.error_description == "Invalid phone number format"


class TestSmsRecipient:
    """Test SmsRecipient model."""
    
    def test_sms_recipient_creation(self):
        """Test SmsRecipient creation."""
        data = {
            "id": "recipient123",
            "number": "+1234567890",
            "status": "active",
            "created_at": "2023-01-01T12:00:00.000000Z"
        }
        
        recipient = SmsRecipient.model_validate(data)
        
        assert recipient.id == "recipient123"
        assert recipient.number == "+1234567890"
        assert recipient.status == "active"
        assert isinstance(recipient.created_at, datetime)


class TestSmsRecipientDetails:
    """Test SmsRecipientDetails model."""
    
    def test_sms_recipient_details_creation(self):
        """Test SmsRecipientDetails creation with SMS history."""
        data = {
            "id": "recipient123",
            "number": "+1234567890",
            "status": "active",
            "created_at": "2023-01-01T12:00:00.000000Z",
            "sms": [
                {
                    "id": "msg123",
                    "from": "+1234567890",
                    "to": "+0987654321",
                    "text": "Test message",
                    "status": "delivered",
                    "segment_count": 1,
                    "error_type": None,
                    "error_description": None,
                    "created_at": "2023-01-01T12:00:00.000000Z"
                }
            ]
        }
        
        recipient = SmsRecipientDetails.model_validate(data)
        
        assert recipient.id == "recipient123"
        assert len(recipient.sms) == 1
        assert isinstance(recipient.sms[0], SmsMessage)
        assert recipient.sms[0].id == "msg123"
    
    def test_sms_recipient_details_empty_sms_list(self):
        """Test SmsRecipientDetails with empty SMS list."""
        data = {
            "id": "recipient456",
            "number": "+1234567890",
            "status": "opt_out",
            "created_at": "2023-01-01T12:00:00.000000Z",
            "sms": []
        }
        
        recipient = SmsRecipientDetails.model_validate(data)
        
        assert len(recipient.sms) == 0


class TestSmsRecipientsListResponse:
    """Test SmsRecipientsListResponse model."""
    
    def test_sms_recipients_list_response_creation(self):
        """Test SmsRecipientsListResponse creation."""
        data = {
            "data": [
                {
                    "id": "recipient1",
                    "number": "+1111111111",
                    "status": "active",
                    "created_at": "2023-01-01T12:00:00.000000Z"
                },
                {
                    "id": "recipient2",
                    "number": "+2222222222",
                    "status": "opt_out",
                    "created_at": "2023-01-01T13:00:00.000000Z"
                }
            ]
        }
        
        response = SmsRecipientsListResponse.model_validate(data)
        
        assert len(response.data) == 2
        assert all(isinstance(recipient, SmsRecipient) for recipient in response.data)
        assert response.data[0].id == "recipient1"
        assert response.data[1].id == "recipient2"


class TestSmsRecipientGetResponse:
    """Test SmsRecipientGetResponse model."""
    
    def test_sms_recipient_get_response_creation(self):
        """Test SmsRecipientGetResponse creation."""
        data = {
            "data": {
                "id": "recipient123",
                "number": "+1234567890",
                "status": "active",
                "created_at": "2023-01-01T12:00:00.000000Z",
                "sms": []
            }
        }
        
        response = SmsRecipientGetResponse.model_validate(data)
        
        assert isinstance(response.data, SmsRecipientDetails)
        assert response.data.id == "recipient123"


class TestSmsRecipientUpdateResponse:
    """Test SmsRecipientUpdateResponse model."""
    
    def test_sms_recipient_update_response_creation(self):
        """Test SmsRecipientUpdateResponse creation."""
        data = {
            "data": {
                "id": "recipient123",
                "number": "+1234567890",
                "status": "opt_out",
                "created_at": "2023-01-01T12:00:00.000000Z"
            }
        }
        
        response = SmsRecipientUpdateResponse.model_validate(data)
        
        assert isinstance(response.data, SmsRecipient)
        assert response.data.id == "recipient123"
        assert response.data.status == "opt_out" 