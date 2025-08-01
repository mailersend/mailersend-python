"""Unit tests for SMS Messages models."""

import pytest
from pydantic import ValidationError

from mailersend.models.sms_messages import (
    SmsMessagesListQueryParams,
    SmsMessagesListRequest,
    SmsMessageGetRequest,
)


class TestSmsMessagesListQueryParams:
    """Test SmsMessagesListQueryParams model."""

    def test_default_values(self):
        """Test SmsMessagesListQueryParams with default values."""
        params = SmsMessagesListQueryParams()

        assert params.page == 1
        assert params.limit == 25

    def test_custom_values(self):
        """Test SmsMessagesListQueryParams with custom values."""
        params = SmsMessagesListQueryParams(page=2, limit=50)

        assert params.page == 2
        assert params.limit == 50

    def test_validation(self):
        """Test SmsMessagesListQueryParams validation."""
        # Page must be >= 1
        with pytest.raises(ValidationError):
            SmsMessagesListQueryParams(page=0)

        # Limit must be between 10 and 100
        with pytest.raises(ValidationError):
            SmsMessagesListQueryParams(limit=5)

        with pytest.raises(ValidationError):
            SmsMessagesListQueryParams(limit=150)

    def test_to_query_params_defaults(self):
        """Test to_query_params with default values excludes them."""
        params = SmsMessagesListQueryParams()
        result = params.to_query_params()

        # Default values should be excluded
        assert result == {}

    def test_to_query_params_custom(self):
        """Test to_query_params with custom values includes them."""
        params = SmsMessagesListQueryParams(page=3, limit=50)
        result = params.to_query_params()

        expected = {"page": 3, "limit": 50}
        assert result == expected

    def test_to_query_params_partial(self):
        """Test to_query_params with only some custom values."""
        params = SmsMessagesListQueryParams(page=2)
        result = params.to_query_params()

        expected = {"page": 2}
        assert result == expected

        params = SmsMessagesListQueryParams(limit=10)
        result = params.to_query_params()

        expected = {"limit": 10}
        assert result == expected


class TestSmsMessagesListRequest:
    """Test SmsMessagesListRequest model."""

    def test_default_request(self):
        """Test SmsMessagesListRequest with defaults."""
        request = SmsMessagesListRequest()

        assert isinstance(request.query_params, SmsMessagesListQueryParams)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_custom_request(self):
        """Test SmsMessagesListRequest with custom params."""
        query_params = SmsMessagesListQueryParams(page=2, limit=50)
        request = SmsMessagesListRequest(query_params=query_params)

        assert request.query_params.page == 2
        assert request.query_params.limit == 50

    def test_to_query_params(self):
        """Test SmsMessagesListRequest to_query_params method."""
        query_params = SmsMessagesListQueryParams(page=3, limit=30)
        request = SmsMessagesListRequest(query_params=query_params)
        result = request.to_query_params()

        expected = {"page": 3, "limit": 30}
        assert result == expected


class TestSmsMessageGetRequest:
    """Test SmsMessageGetRequest model."""

    def test_basic_creation(self):
        """Test basic SmsMessageGetRequest creation."""
        request = SmsMessageGetRequest(sms_message_id="msg123")

        assert request.sms_message_id == "msg123"

    def test_sms_message_id_validation_empty(self):
        """Test SMS message ID validation with empty string."""
        with pytest.raises(ValidationError):
            SmsMessageGetRequest(sms_message_id="")

    def test_sms_message_id_validation_whitespace(self):
        """Test SMS message ID validation with whitespace only."""
        with pytest.raises(ValueError, match="SMS message ID cannot be empty"):
            SmsMessageGetRequest(sms_message_id="   ")

    def test_sms_message_id_trimming(self):
        """Test SMS message ID gets trimmed."""
        request = SmsMessageGetRequest(sms_message_id="  msg123  ")
        assert request.sms_message_id == "msg123"
