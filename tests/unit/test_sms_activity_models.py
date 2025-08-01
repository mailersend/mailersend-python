"""Tests for SMS Activity models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_activity import (
    SmsActivity,
    SmsActivityListRequest,
    SmsMessageGetRequest,
    SmsMessage,
)


class TestSmsActivity:
    """Test SMS Activity model."""

    def test_valid_sms_activity(self):
        """Test creating valid SMS activity."""
        activity = SmsActivity(
            from_="+18332647501",
            to="+16203221059",
            created_at=datetime.fromisoformat("2022-02-21T08:15:46.627000"),
            content="Lorem Ipsum is simply dummy text",
            status="delivered",
            sms_message_id="62134a2d7de3253bf10d6642",
        )

        assert activity.from_ == "+18332647501"
        assert activity.to == "+16203221059"
        assert activity.content == "Lorem Ipsum is simply dummy text"
        assert activity.status == "delivered"
        assert activity.sms_message_id == "62134a2d7de3253bf10d6642"

    def test_sms_activity_from_field_alias(self):
        """Test that 'from' field alias works correctly."""
        data = {
            "from": "+18332647501",
            "to": "+16203221059",
            "created_at": "2022-02-21T08:15:46.627000",
            "content": "Lorem Ipsum is simply dummy text",
            "status": "delivered",
            "sms_message_id": "62134a2d7de3253bf10d6642",
        }

        activity = SmsActivity(**data)
        assert activity.from_ == "+18332647501"


class TestSmsActivityListRequest:
    """Test SMS Activity list request model."""

    def test_empty_request(self):
        """Test creating empty request."""
        request = SmsActivityListRequest()

        params = request.to_query_params()
        assert params == {}

    def test_full_request(self):
        """Test creating request with all parameters."""
        request = SmsActivityListRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            date_from=1443651141,
            date_to=1443651200,
            status=["delivered", "sent"],
            page=1,
            limit=25,
        )

        params = request.to_query_params()
        expected = {
            "sms_number_id": "7z3m5jgrogdpyo6n",
            "date_from": 1443651141,
            "date_to": 1443651200,
            "status[]": ["delivered", "sent"],
            "page": 1,
            "limit": 25,
        }

        assert params == expected

    def test_partial_request(self):
        """Test creating request with some parameters."""
        request = SmsActivityListRequest(
            sms_number_id="7z3m5jgrogdpyo6n", status=["delivered"]
        )

        params = request.to_query_params()
        expected = {"sms_number_id": "7z3m5jgrogdpyo6n", "status[]": ["delivered"]}

        assert params == expected

    def test_status_array_handling(self):
        """Test that status parameter is correctly converted to array format."""
        request = SmsActivityListRequest(status=["delivered", "sent", "failed"])

        params = request.to_query_params()
        assert "status[]" in params
        assert params["status[]"] == ["delivered", "sent", "failed"]

    def test_single_status_handling(self):
        """Test that single status is correctly handled."""
        request = SmsActivityListRequest(status=["delivered"])

        params = request.to_query_params()
        assert "status[]" in params
        assert params["status[]"] == ["delivered"]


class TestSmsMessageGetRequest:
    """Test SMS Message get request model."""

    def test_valid_request(self):
        """Test creating valid request."""
        request = SmsMessageGetRequest(sms_message_id="62134a2d7de3253bf10d6642")

        assert request.sms_message_id == "62134a2d7de3253bf10d6642"

    def test_empty_sms_message_id_validation(self):
        """Test that empty SMS message ID is rejected."""
        with pytest.raises(ValidationError):
            SmsMessageGetRequest(sms_message_id="")


class TestSmsMessage:
    """Test SMS Message model."""

    def test_valid_sms_message(self):
        """Test creating valid SMS message."""
        activities = [
            SmsActivity(
                from_="+18332647501",
                to="+16203221059",
                created_at=datetime.fromisoformat("2022-02-21T08:15:46.627000"),
                content="Lorem Ipsum is simply dummy text",
                status="delivered",
                sms_message_id="62134a2d7de3253bf10d6642",
            )
        ]

        message = SmsMessage(
            id="62134a2d7de3253bf10d6642",
            from_="+18332647501",
            to=["+16203221059"],
            text="Lorem Ipsum is simply dummy text",
            paused=False,
            created_at=datetime.fromisoformat("2022-02-21T08:15:45.627000"),
            sms=[],
            sms_activity=activities,
        )

        assert message.id == "62134a2d7de3253bf10d6642"
        assert message.from_ == "+18332647501"
        assert message.to == ["+16203221059"]
        assert message.text == "Lorem Ipsum is simply dummy text"
        assert message.paused is False
        assert len(message.sms_activity) == 1
        assert isinstance(message.sms_activity[0], SmsActivity)

    def test_sms_message_from_field_alias(self):
        """Test that 'from' field alias works correctly."""
        data = {
            "id": "62134a2d7de3253bf10d6642",
            "from": "+18332647501",
            "to": ["+16203221059"],
            "text": "Lorem Ipsum is simply dummy text",
            "paused": False,
            "created_at": "2022-02-21T08:15:45.627000",
            "sms": [],
            "sms_activity": [],
        }

        message = SmsMessage(**data)
        assert message.from_ == "+18332647501"
