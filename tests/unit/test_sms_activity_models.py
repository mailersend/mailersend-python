import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.sms_activity import (
    SmsActivity, SmsActivityListRequest, SmsMessageGetRequest,
    SmsActivityListResponse, SmsMessage, SmsMessageResponse
)


class TestSmsActivity:
    """Test SMS Activity model."""

    def test_valid_sms_activity(self):
        """Test creating valid SMS activity."""
        sms_activity = SmsActivity(
            from_="+18332647501",
            to="+16203221059",
            created_at=datetime.fromisoformat("2022-02-21T08:15:46.627000"),
            content="Lorem Ipsum is simply dummy text",
            status="delivered",
            sms_message_id="62134a2d7de3253bf10d6642"
        )
        
        assert sms_activity.from_ == "+18332647501"
        assert sms_activity.to == "+16203221059"
        assert sms_activity.created_at == datetime.fromisoformat("2022-02-21T08:15:46.627000")
        assert sms_activity.content == "Lorem Ipsum is simply dummy text"
        assert sms_activity.status == "delivered"
        assert sms_activity.sms_message_id == "62134a2d7de3253bf10d6642"

    def test_sms_activity_with_different_status(self):
        """Test SMS activity with different status values."""
        statuses = ["processed", "queued", "sent", "delivered", "failed"]
        
        for status in statuses:
            sms_activity = SmsActivity(
                from_="+18332647501",
                to="+16203221059",
                created_at=datetime.fromisoformat("2022-02-21T08:15:46.627000"),
                content="Test message",
                status=status,
                sms_message_id="62134a2d7de3253bf10d6642"
            )
            
            assert sms_activity.status == status


class TestSmsActivityListRequest:
    """Test SMS Activity list request model."""

    def test_valid_list_request(self):
        """Test creating valid list request."""
        request = SmsActivityListRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            date_from=1443651141,
            date_to=1443651200,
            status=["delivered", "sent"],
            page=1,
            limit=25
        )
        
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.date_from == 1443651141
        assert request.date_to == 1443651200
        assert request.status == ["delivered", "sent"]
        assert request.page == 1
        assert request.limit == 25

    def test_empty_list_request(self):
        """Test creating empty list request."""
        request = SmsActivityListRequest()
        
        assert request.sms_number_id is None
        assert request.date_from is None
        assert request.date_to is None
        assert request.status is None
        assert request.page is None
        assert request.limit is None

    def test_to_query_params_full(self):
        """Test converting full request to query parameters."""
        request = SmsActivityListRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            date_from=1443651141,
            date_to=1443651200,
            status=["delivered", "sent"],
            page=2,
            limit=50
        )
        
        params = request.to_query_params()
        expected = {
            "sms_number_id": "7z3m5jgrogdpyo6n",
            "date_from": 1443651141,
            "date_to": 1443651200,
            "status[]": ["delivered", "sent"],
            "page": 2,
            "limit": 50
        }
        
        assert params == expected

    def test_to_query_params_partial(self):
        """Test converting partial request to query parameters."""
        request = SmsActivityListRequest(
            sms_number_id="7z3m5jgrogdpyo6n",
            page=1
        )
        
        params = request.to_query_params()
        expected = {
            "sms_number_id": "7z3m5jgrogdpyo6n",
            "page": 1
        }
        
        assert params == expected

    def test_to_query_params_empty(self):
        """Test converting empty request to query parameters."""
        request = SmsActivityListRequest()
        
        params = request.to_query_params()
        expected = {}
        
        assert params == expected

    def test_to_query_params_single_status(self):
        """Test converting request with single status to query parameters."""
        request = SmsActivityListRequest(status=["delivered"])
        
        params = request.to_query_params()
        expected = {"status[]": ["delivered"]}
        
        assert params == expected


class TestSmsMessageGetRequest:
    """Test SMS Message get request model."""

    def test_valid_get_request(self):
        """Test creating valid get request."""
        request = SmsMessageGetRequest(sms_message_id="62134a2d7de3253bf10d6642")
        
        assert request.sms_message_id == "62134a2d7de3253bf10d6642"

    def test_empty_sms_message_id(self):
        """Test validation error for empty SMS message ID."""
        with pytest.raises(ValidationError) as exc_info:
            SmsMessageGetRequest(sms_message_id="")
        
        error = exc_info.value.errors()[0]
        assert "String should have at least 1 character" in error['msg']


class TestSmsActivityListResponse:
    """Test SMS Activity list response model."""

    def test_valid_list_response(self):
        """Test creating valid list response."""
        activities = [
            SmsActivity(
                from_="+18332647501",
                to="+16203221059",
                created_at=datetime.fromisoformat("2022-02-21T08:15:46.627000"),
                content="Lorem Ipsum is simply dummy text",
                status="delivered",
                sms_message_id="62134a2d7de3253bf10d6642"
            ),
            SmsActivity(
                from_="+18332647501",
                to="+16203221059",
                created_at=datetime.fromisoformat("2022-02-21T08:15:42.508000"),
                content="Lorem Ipsum is simply dummy text",
                status="processed",
                sms_message_id="62134a2d7de3253bf10d6642"
            )
        ]
        
        response = SmsActivityListResponse(data=activities)
        
        assert len(response.data) == 2
        assert response.data[0].status == "delivered"
        assert response.data[1].status == "processed"

    def test_empty_list_response(self):
        """Test creating empty list response."""
        response = SmsActivityListResponse(data=[])
        
        assert len(response.data) == 0


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
                sms_message_id="62134a2d7de3253bf10d6642"
            )
        ]
        
        sms_message = SmsMessage(
            id="62134a2d7de3253bf10d6642",
            from_="+18332647501",
            to=["+16203221059", "+18044064234"],
            text="Lorem Ipsum is simply dummy text",
            paused=False,
            created_at=datetime.fromisoformat("2022-02-21T08:15:41.339000"),
            sms=[{
                "id": "62134a2e4709ec689f72ea62",
                "from": "+18332647501",
                "to": "+16203221059",
                "text": "Lorem Ipsum is simply dummy text",
                "status": "delivered",
                "segment_count": 1,
                "error_type": None,
                "error_description": None
            }],
            sms_activity=activities
        )
        
        assert sms_message.id == "62134a2d7de3253bf10d6642"
        assert sms_message.from_ == "+18332647501"
        assert sms_message.to == ["+16203221059", "+18044064234"]
        assert sms_message.text == "Lorem Ipsum is simply dummy text"
        assert sms_message.paused is False
        assert len(sms_message.sms) == 1
        assert len(sms_message.sms_activity) == 1


class TestSmsMessageResponse:
    """Test SMS Message response model."""

    def test_valid_response(self):
        """Test creating valid response."""
        sms_message = SmsMessage(
            id="62134a2d7de3253bf10d6642",
            from_="+18332647501",
            to=["+16203221059"],
            text="Lorem Ipsum is simply dummy text",
            paused=False,
            created_at=datetime.fromisoformat("2022-02-21T08:15:41.339000"),
            sms=[],
            sms_activity=[]
        )
        
        response = SmsMessageResponse(data=sms_message)
        
        assert response.data.id == "62134a2d7de3253bf10d6642"
        assert response.data.from_ == "+18332647501"
        assert response.data.text == "Lorem Ipsum is simply dummy text"
        assert response.data.paused is False