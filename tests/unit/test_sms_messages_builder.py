"""Tests for SMS Messages builder."""

import pytest

from mailersend.builders.sms_messages import SmsMessagesBuilder
from mailersend.models.sms_messages import (
    SmsMessagesListRequest, SmsMessageGetRequest
)
from mailersend.exceptions import ValidationError


class TestSmsMessagesBuilderBasicMethods:
    """Test basic SmsMessagesBuilder methods."""
    
    def test_initialization(self):
        """Test SmsMessagesBuilder initialization."""
        builder = SmsMessagesBuilder()
        
        assert builder._sms_message_id is None
        assert builder._page == 1
        assert builder._limit == 25
    
    def test_sms_message_id_method(self):
        """Test sms_message_id method."""
        builder = SmsMessagesBuilder()
        result = builder.sms_message_id("msg123")
        
        assert result is builder  # Method chaining
        assert builder._sms_message_id == "msg123"
    
    def test_page_method(self):
        """Test page method."""
        builder = SmsMessagesBuilder()
        result = builder.page(2)
        
        assert result is builder  # Method chaining
        assert builder._page == 2
    
    def test_page_method_validation(self):
        """Test page method validation."""
        builder = SmsMessagesBuilder()
        
        with pytest.raises(ValidationError, match="Page must be >= 1"):
            builder.page(0)
        
        with pytest.raises(ValidationError, match="Page must be >= 1"):
            builder.page(-1)
        
        # Valid page numbers should work
        builder.page(1)
        assert builder._page == 1
    
    def test_limit_method(self):
        """Test limit method."""
        builder = SmsMessagesBuilder()
        result = builder.limit(50)
        
        assert result is builder  # Method chaining
        assert builder._limit == 50
    
    def test_limit_method_validation(self):
        """Test limit method validation."""
        builder = SmsMessagesBuilder()
        
        with pytest.raises(ValidationError, match="Limit must be between 10 and 100"):
            builder.limit(5)
        
        with pytest.raises(ValidationError, match="Limit must be between 10 and 100"):
            builder.limit(150)
        
        # Valid limits should work
        builder.limit(10)
        assert builder._limit == 10
        
        builder.limit(100)
        assert builder._limit == 100


class TestSmsMessagesBuilderBuildMethods:
    """Test SmsMessagesBuilder build methods."""
    
    def test_build_sms_messages_list_basic(self):
        """Test build_sms_messages_list with basic setup."""
        builder = SmsMessagesBuilder()
        
        request = builder.build_sms_messages_list()
        
        assert isinstance(request, SmsMessagesListRequest)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
    
    def test_build_sms_messages_list_with_custom_params(self):
        """Test build_sms_messages_list with custom parameters."""
        builder = SmsMessagesBuilder()
        builder.page(3).limit(50)
        
        request = builder.build_sms_messages_list()
        
        assert isinstance(request, SmsMessagesListRequest)
        assert request.query_params.page == 3
        assert request.query_params.limit == 50
    
    def test_build_sms_message_get_success(self):
        """Test build_sms_message_get with valid data."""
        builder = SmsMessagesBuilder()
        builder.sms_message_id("msg123")
        
        request = builder.build_sms_message_get()
        
        assert isinstance(request, SmsMessageGetRequest)
        assert request.sms_message_id == "msg123"
    
    def test_build_sms_message_get_missing_id(self):
        """Test build_sms_message_get validation when SMS message ID is missing."""
        builder = SmsMessagesBuilder()
        
        with pytest.raises(ValidationError, match="SMS message ID is required"):
            builder.build_sms_message_get()
