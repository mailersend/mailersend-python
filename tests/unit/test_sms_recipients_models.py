"""Unit tests for SMS Recipients models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_recipients import (
    SmsRecipientStatus,
    SmsRecipientsListQueryParams,
    SmsRecipientsListRequest,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsRecipient,
    SmsRecipientDetails,
)


class TestSmsRecipientStatus:
    """Test SmsRecipientStatus enum."""

    def test_status_values(self):
        """Test SmsRecipientStatus enum values."""
        assert SmsRecipientStatus.ACTIVE == "active"
        assert SmsRecipientStatus.OPT_OUT == "opt_out"


class TestSmsRecipientsListQueryParams:
    """Test SmsRecipientsListQueryParams model."""

    def test_default_values(self):
        """Test default values."""
        params = SmsRecipientsListQueryParams()

        assert params.status is None
        assert params.sms_number_id is None
        assert params.page == 1
        assert params.limit == 25

    def test_custom_values(self):
        """Test custom values."""
        params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.ACTIVE, sms_number_id="sms123", page=2, limit=50
        )

        assert params.status == SmsRecipientStatus.ACTIVE
        assert params.sms_number_id == "sms123"
        assert params.page == 2
        assert params.limit == 50

    def test_sms_number_id_validation(self):
        """Test sms_number_id validation and trimming."""
        params = SmsRecipientsListQueryParams(sms_number_id="  sms123  ")
        assert params.sms_number_id == "sms123"

    def test_field_validation(self):
        """Test field validation."""
        # Page must be >= 1
        with pytest.raises(ValidationError):
            SmsRecipientsListQueryParams(page=0)

        # Limit must be between 10 and 100
        with pytest.raises(ValidationError):
            SmsRecipientsListQueryParams(limit=9)

        with pytest.raises(ValidationError):
            SmsRecipientsListQueryParams(limit=101)

    def test_to_query_params_defaults(self):
        """Test to_query_params with default values excludes them."""
        params = SmsRecipientsListQueryParams()
        result = params.to_query_params()

        # Default values should be excluded
        assert result == {}

    def test_to_query_params_custom(self):
        """Test to_query_params with custom values includes them."""
        params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.OPT_OUT, sms_number_id="sms456", page=3, limit=15
        )
        result = params.to_query_params()

        expected = {
            "status": "opt_out",
            "sms_number_id": "sms456",
            "page": 3,
            "limit": 15,
        }
        assert result == expected

    def test_to_query_params_partial(self):
        """Test to_query_params with only some custom values."""
        params = SmsRecipientsListQueryParams(status=SmsRecipientStatus.ACTIVE)
        result = params.to_query_params()

        expected = {"status": "active"}
        assert result == expected


class TestSmsRecipientsListRequest:
    """Test SmsRecipientsListRequest model."""

    def test_default_request(self):
        """Test creating request with default query params."""
        request = SmsRecipientsListRequest()

        assert isinstance(request.query_params, SmsRecipientsListQueryParams)
        assert request.to_query_params() == {}

    def test_custom_request(self):
        """Test creating request with custom query params."""
        query_params = SmsRecipientsListQueryParams(
            status=SmsRecipientStatus.ACTIVE, page=2
        )
        request = SmsRecipientsListRequest(query_params=query_params)

        result = request.to_query_params()
        expected = {"status": "active", "page": 2}
        assert result == expected


class TestSmsRecipientGetRequest:
    """Test SmsRecipientGetRequest model."""

    def test_valid_request(self):
        """Test creating valid get request."""
        request = SmsRecipientGetRequest(sms_recipient_id="recipient123")

        assert request.sms_recipient_id == "recipient123"

    def test_id_trimming(self):
        """Test SMS recipient ID trimming."""
        request = SmsRecipientGetRequest(sms_recipient_id="  recipient123  ")
        assert request.sms_recipient_id == "recipient123"

    def test_empty_id_validation(self):
        """Test empty ID validation."""
        with pytest.raises(ValidationError):
            SmsRecipientGetRequest(sms_recipient_id="")

    def test_whitespace_id_validation(self):
        """Test whitespace-only ID validation."""
        with pytest.raises(ValueError, match="SMS recipient ID cannot be empty"):
            SmsRecipientGetRequest(sms_recipient_id="   ")


class TestSmsRecipientUpdateRequest:
    """Test SmsRecipientUpdateRequest model."""

    def test_valid_request(self):
        """Test creating valid update request."""
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient123", status=SmsRecipientStatus.OPT_OUT
        )

        assert request.sms_recipient_id == "recipient123"
        assert request.status == SmsRecipientStatus.OPT_OUT

    def test_id_trimming(self):
        """Test SMS recipient ID trimming."""
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="  recipient123  ", status=SmsRecipientStatus.ACTIVE
        )
        assert request.sms_recipient_id == "recipient123"

    def test_to_request_body(self):
        """Test converting to request body."""
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="recipient123", status=SmsRecipientStatus.OPT_OUT
        )

        body = request.to_request_body()
        expected = {"status": "opt_out"}
        assert body == expected

    def test_empty_id_validation(self):
        """Test empty ID validation."""
        with pytest.raises(ValidationError):
            SmsRecipientUpdateRequest(
                sms_recipient_id="", status=SmsRecipientStatus.ACTIVE
            )


class TestSmsRecipient:
    """Test SmsRecipient model."""

    def test_valid_recipient(self):
        """Test creating valid SMS recipient."""
        data = {
            "id": "recipient123",
            "number": "+1234567890",
            "status": "active",
            "created_at": "2023-01-01T12:00:00.000000Z",
        }

        recipient = SmsRecipient.model_validate(data)

        assert recipient.id == "recipient123"
        assert recipient.number == "+1234567890"
        assert recipient.status == "active"
        assert isinstance(recipient.created_at, datetime)


class TestSmsRecipientDetails:
    """Test SmsRecipientDetails model."""

    def test_recipient_details_with_sms_history(self):
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
                    "created_at": "2023-01-01T12:00:00.000000Z",
                }
            ],
        }

        recipient = SmsRecipientDetails.model_validate(data)

        assert recipient.id == "recipient123"
        assert len(recipient.sms) == 1
        assert isinstance(recipient.sms[0], dict)
        assert recipient.sms[0]["id"] == "msg123"

    def test_recipient_details_empty_sms_list(self):
        """Test SmsRecipientDetails with empty SMS list."""
        data = {
            "id": "recipient456",
            "number": "+1234567890",
            "status": "opt_out",
            "created_at": "2023-01-01T12:00:00.000000Z",
            "sms": [],
        }

        recipient = SmsRecipientDetails.model_validate(data)

        assert len(recipient.sms) == 0

    def test_recipient_details_default_sms_list(self):
        """Test SmsRecipientDetails with default SMS list."""
        data = {
            "id": "recipient789",
            "number": "+1234567890",
            "status": "active",
            "created_at": "2023-01-01T12:00:00.000000Z",
        }

        recipient = SmsRecipientDetails.model_validate(data)

        assert len(recipient.sms) == 0
