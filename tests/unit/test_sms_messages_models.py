"""Tests for SMS Messages models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_messages import (
    SmsMessagesListQueryParams, SmsMessagesListRequest, SmsMessageGetRequest,
    SmsActivity, Sms, SmsMessage, SmsMessagesListResponse, SmsMessageResponse
)


class TestSmsMessagesListQueryParams:
    """Test SmsMessagesListQueryParams model."""
    
    def test_sms_messages_list_query_params_defaults(self):
        """Test SmsMessagesListQueryParams with default values."""
        params = SmsMessagesListQueryParams()
        
        assert params.page == 1
        assert params.limit == 25
    
    def test_sms_messages_list_query_params_custom_values(self):
        """Test SmsMessagesListQueryParams with custom values."""
        params = SmsMessagesListQueryParams(page=2, limit=50)
        
        assert params.page == 2
        assert params.limit == 50
    
    def test_sms_messages_list_query_params_validation(self):
        """Test SmsMessagesListQueryParams validation."""
        # Test invalid page
        with pytest.raises(ValidationError):
            SmsMessagesListQueryParams(page=0)
        
        # Test invalid limit (too low)
        with pytest.raises(ValidationError):
            SmsMessagesListQueryParams(limit=5)
        
        # Test invalid limit (too high)
        with pytest.raises(ValidationError):
            SmsMessagesListQueryParams(limit=150)
    
    def test_sms_messages_list_query_params_to_query_params_defaults(self):
        """Test to_query_params with default values."""
        params = SmsMessagesListQueryParams()
        result = params.to_query_params()
        
        # Default values should be excluded
        assert result == {}
    
    def test_sms_messages_list_query_params_to_query_params_custom(self):
        """Test to_query_params with custom values."""
        params = SmsMessagesListQueryParams(page=3, limit=50)
        result = params.to_query_params()
        
        assert result == {'page': 3, 'limit': 50}
    
    def test_sms_messages_list_query_params_to_query_params_partial(self):
        """Test to_query_params with partial custom values."""
        params = SmsMessagesListQueryParams(page=2)
        result = params.to_query_params()
        
        assert result == {'page': 2}
        
        params = SmsMessagesListQueryParams(limit=10)
        result = params.to_query_params()
        
        assert result == {'limit': 10}


class TestSmsMessagesListRequest:
    """Test SmsMessagesListRequest model."""
    
    def test_sms_messages_list_request_defaults(self):
        """Test SmsMessagesListRequest with defaults."""
        request = SmsMessagesListRequest()
        
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
    
    def test_sms_messages_list_request_with_custom_params(self):
        """Test SmsMessagesListRequest with custom params."""
        query_params = SmsMessagesListQueryParams(page=2, limit=50)
        request = SmsMessagesListRequest(query_params=query_params)
        
        assert request.query_params.page == 2
        assert request.query_params.limit == 50
    
    def test_sms_messages_list_request_to_query_params(self):
        """Test SmsMessagesListRequest to_query_params method."""
        query_params = SmsMessagesListQueryParams(page=3, limit=30)
        request = SmsMessagesListRequest(query_params=query_params)
        result = request.to_query_params()
        
        assert result == {'page': 3, 'limit': 30}


class TestSmsMessageGetRequest:
    """Test SmsMessageGetRequest model."""
    
    def test_basic_creation(self):
        """Test basic SmsMessageGetRequest creation."""
        request = SmsMessageGetRequest(sms_message_id='msg123')
        
        assert request.sms_message_id == 'msg123'
    
    def test_id_validation(self):
        """Test SMS message ID validation."""
        # Test empty string
        with pytest.raises(ValueError, match="SMS message ID cannot be empty"):
            SmsMessageGetRequest(sms_message_id="")
        
        # Test whitespace only
        with pytest.raises(ValueError, match="SMS message ID cannot be empty"):
            SmsMessageGetRequest(sms_message_id="   ")
    
    def test_id_trimming(self):
        """Test SMS message ID trimming."""
        request = SmsMessageGetRequest(sms_message_id="  msg123  ")
        assert request.sms_message_id == "msg123"


class TestSmsActivity:
    """Test SmsActivity model."""
    
    def test_basic_creation(self):
        """Test basic SmsActivity creation."""
        activity = SmsActivity(
            **{
                "from": "+1234567890",
                "to": "+0987654321",
                "created_at": "2023-01-01T12:00:00Z",
                "status": "sent",
                "sms_message_id": "msg123"
            }
        )
        
        assert activity.from_ == "+1234567890"
        assert activity.to == "+0987654321"
        assert activity.status == "sent"
        assert activity.sms_message_id == "msg123"
        assert isinstance(activity.created_at, datetime)


class TestSms:
    """Test Sms model."""
    
    def test_basic_creation(self):
        """Test basic Sms creation."""
        sms = Sms(
            **{
                "id": "sms123",
                "from": "+1234567890",
                "to": "+0987654321",
                "text": "Hello World",
                "compiled_text": "Hello World",
                "status": "sent",
                "segment_count": 1,
                "error_type": None,
                "error_description": None,
                "created_at": "2023-01-01T12:00:00Z"
            }
        )
        
        assert sms.id == "sms123"
        assert sms.from_ == "+1234567890"
        assert sms.to == "+0987654321"
        assert sms.text == "Hello World"
        assert sms.compiled_text == "Hello World"
        assert sms.status == "sent"
        assert sms.segment_count == 1
        assert sms.error_type is None
        assert sms.error_description is None
        assert isinstance(sms.created_at, datetime)
    
    def test_creation_with_errors(self):
        """Test Sms creation with error fields."""
        sms = Sms(
            **{
                "id": "sms123",
                "from": "+1234567890",
                "to": "+0987654321",
                "text": "Hello World",
                "compiled_text": "Hello World",
                "status": "failed",
                "segment_count": 1,
                "error_type": "INVALID_DESTINATION",
                "error_description": "Invalid phone number",
                "created_at": "2023-01-01T12:00:00Z"
            }
        )
        
        assert sms.error_type == "INVALID_DESTINATION"
        assert sms.error_description == "Invalid phone number"


class TestSmsMessage:
    """Test SmsMessage model."""
    
    def test_basic_creation(self):
        """Test basic SmsMessage creation."""
        message = SmsMessage(
            **{
                "id": "msg123",
                "from": "+1234567890",
                "to": ["+0987654321", "+1122334455"],
                "text": "Hello World",
                "paused": False,
                "created_at": "2023-01-01T12:00:00Z"
            }
        )
        
        assert message.id == "msg123"
        assert message.from_ == "+1234567890"
        assert message.to == ["+0987654321", "+1122334455"]
        assert message.text == "Hello World"
        assert message.paused is False
        assert isinstance(message.created_at, datetime)
        assert message.sms is None
        assert message.sms_activity is None
    
    def test_creation_with_nested_objects(self):
        """Test SmsMessage creation with nested SMS and activity objects."""
        message = SmsMessage(
            **{
                "id": "msg123",
                "from": "+1234567890",
                "to": ["+0987654321"],
                "text": "Hello World",
                "paused": False,
                "created_at": "2023-01-01T12:00:00Z",
                "sms": [
                    {
                        "id": "sms123",
                        "from": "+1234567890",
                        "to": "+0987654321",
                        "text": "Hello World",
                        "compiled_text": "Hello World",
                        "status": "sent",
                        "segment_count": 1,
                        "error_type": None,
                        "error_description": None,
                        "created_at": "2023-01-01T12:00:00Z"
                    }
                ],
                "sms_activity": [
                    {
                        "from": "+1234567890",
                        "to": "+0987654321",
                        "created_at": "2023-01-01T12:00:00Z",
                        "status": "sent",
                        "sms_message_id": "msg123"
                    }
                ]
            }
        )
        
        assert len(message.sms) == 1
        assert isinstance(message.sms[0], Sms)
        assert message.sms[0].id == "sms123"
        
        assert len(message.sms_activity) == 1
        assert isinstance(message.sms_activity[0], SmsActivity)
        assert message.sms_activity[0].status == "sent"


class TestResponseModels:
    """Test response models."""
    
    def test_sms_messages_list_response(self):
        """Test SmsMessagesListResponse model."""
        response = SmsMessagesListResponse(
            data=[
                {
                    "id": "msg123",
                    "from": "+1234567890",
                    "to": ["+0987654321"],
                    "text": "Hello World",
                    "paused": False,
                    "created_at": "2023-01-01T12:00:00Z"
                }
            ]
        )
        
        assert len(response.data) == 1
        assert isinstance(response.data[0], SmsMessage)
        assert response.data[0].id == "msg123"
    
    def test_sms_message_response(self):
        """Test SmsMessageResponse model."""
        response = SmsMessageResponse(
            data={
                "id": "msg123",
                "from": "+1234567890",
                "to": ["+0987654321"],
                "text": "Hello World",
                "paused": False,
                "created_at": "2023-01-01T12:00:00Z"
            }
        )
        
        assert isinstance(response.data, SmsMessage)
        assert response.data.id == "msg123"
