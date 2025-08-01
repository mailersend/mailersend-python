import pytest

from mailersend.builders.sms_activity import SmsActivityBuilder
from mailersend.models.sms_activity import SmsActivityListRequest, SmsMessageGetRequest


class TestSmsActivityBuilder:
    """Test SMS Activity builder."""

    @pytest.fixture
    def builder(self):
        """Create a fresh builder instance."""
        return SmsActivityBuilder()

    def test_builder_initialization(self, builder):
        """Test builder initializes with empty state."""
        assert builder._sms_number_id is None
        assert builder._date_from is None
        assert builder._date_to is None
        assert builder._status is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._sms_message_id is None

    def test_sms_number_id_method(self, builder):
        """Test sms_number_id method sets SMS number ID."""
        result = builder.sms_number_id("7z3m5jgrogdpyo6n")

        assert result is builder  # Returns self for chaining
        assert builder._sms_number_id == "7z3m5jgrogdpyo6n"

    def test_date_from_method(self, builder):
        """Test date_from method sets date from."""
        result = builder.date_from(1443651141)

        assert result is builder  # Returns self for chaining
        assert builder._date_from == 1443651141

    def test_date_to_method(self, builder):
        """Test date_to method sets date to."""
        result = builder.date_to(1443651200)

        assert result is builder  # Returns self for chaining
        assert builder._date_to == 1443651200

    def test_status_method(self, builder):
        """Test status method sets status list."""
        statuses = ["delivered", "sent"]
        result = builder.status(statuses)

        assert result is builder  # Returns self for chaining
        assert builder._status == statuses

    def test_page_method(self, builder):
        """Test page method sets page number."""
        result = builder.page(2)

        assert result is builder  # Returns self for chaining
        assert builder._page == 2

    def test_limit_method(self, builder):
        """Test limit method sets limit."""
        result = builder.limit(50)

        assert result is builder  # Returns self for chaining
        assert builder._limit == 50

    def test_sms_message_id_method(self, builder):
        """Test sms_message_id method sets SMS message ID."""
        result = builder.sms_message_id("62134a2d7de3253bf10d6642")

        assert result is builder  # Returns self for chaining
        assert builder._sms_message_id == "62134a2d7de3253bf10d6642"

    def test_method_chaining(self, builder):
        """Test method chaining works correctly."""
        result = (
            builder.sms_number_id("7z3m5jgrogdpyo6n")
            .date_from(1443651141)
            .date_to(1443651200)
            .status(["delivered", "sent"])
            .page(1)
            .limit(25)
            .sms_message_id("62134a2d7de3253bf10d6642")
        )

        assert result is builder
        assert builder._sms_number_id == "7z3m5jgrogdpyo6n"
        assert builder._date_from == 1443651141
        assert builder._date_to == 1443651200
        assert builder._status == ["delivered", "sent"]
        assert builder._page == 1
        assert builder._limit == 25
        assert builder._sms_message_id == "62134a2d7de3253bf10d6642"

    def test_build_list_request_full(self, builder):
        """Test building full list request."""
        request = (
            builder.sms_number_id("7z3m5jgrogdpyo6n")
            .date_from(1443651141)
            .date_to(1443651200)
            .status(["delivered", "sent"])
            .page(2)
            .limit(50)
            .build_list_request()
        )

        assert isinstance(request, SmsActivityListRequest)
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.date_from == 1443651141
        assert request.date_to == 1443651200
        assert request.status == ["delivered", "sent"]
        assert request.page == 2
        assert request.limit == 50

    def test_build_list_request_empty(self, builder):
        """Test building empty list request."""
        request = builder.build_list_request()

        assert isinstance(request, SmsActivityListRequest)
        assert request.sms_number_id is None
        assert request.date_from is None
        assert request.date_to is None
        assert request.status is None
        assert request.page is None
        assert request.limit is None

    def test_build_list_request_partial(self, builder):
        """Test building partial list request."""
        request = builder.sms_number_id("7z3m5jgrogdpyo6n").page(1).build_list_request()

        assert isinstance(request, SmsActivityListRequest)
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.date_from is None
        assert request.date_to is None
        assert request.status is None
        assert request.page == 1
        assert request.limit is None

    def test_build_get_request_success(self, builder):
        """Test building get request successfully."""
        request = builder.sms_message_id("62134a2d7de3253bf10d6642").build_get_request()

        assert isinstance(request, SmsMessageGetRequest)
        assert request.sms_message_id == "62134a2d7de3253bf10d6642"

    def test_build_get_request_missing_id(self, builder):
        """Test building get request without SMS message ID raises error."""
        with pytest.raises(ValueError) as exc_info:
            builder.build_get_request()

        assert "SMS message ID must be set" in str(exc_info.value)

    def test_reset_method(self, builder):
        """Test reset method clears all state."""
        # Set some state
        builder.sms_number_id("7z3m5jgrogdpyo6n").date_from(1443651141).status(
            ["delivered"]
        ).page(2).limit(50).sms_message_id("62134a2d7de3253bf10d6642")

        # Reset
        result = builder.reset()

        assert result is builder  # Returns self for chaining
        assert builder._sms_number_id is None
        assert builder._date_from is None
        assert builder._date_to is None
        assert builder._status is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._sms_message_id is None

    def test_builder_reuse_after_reset(self, builder):
        """Test builder can be reused after reset."""
        # First use
        request1 = builder.sms_message_id("id1").build_get_request()
        assert request1.sms_message_id == "id1"

        # Reset and reuse
        request2 = builder.reset().sms_message_id("id2").build_get_request()
        assert request2.sms_message_id == "id2"

    def test_multiple_requests_from_same_builder(self, builder):
        """Test building multiple requests from same builder state."""
        builder.sms_number_id("7z3m5jgrogdpyo6n").date_from(1443651141).sms_message_id(
            "62134a2d7de3253bf10d6642"
        )

        # Build different request types with same state
        list_request = builder.build_list_request()
        get_request = builder.build_get_request()

        assert list_request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert list_request.date_from == 1443651141
        assert get_request.sms_message_id == "62134a2d7de3253bf10d6642"

    def test_status_with_single_value(self, builder):
        """Test status method with single value in list."""
        request = builder.status(["delivered"]).build_list_request()

        assert isinstance(request, SmsActivityListRequest)
        assert request.status == ["delivered"]

    def test_status_with_multiple_values(self, builder):
        """Test status method with multiple values."""
        statuses = ["processed", "queued", "sent", "delivered", "failed"]
        request = builder.status(statuses).build_list_request()

        assert isinstance(request, SmsActivityListRequest)
        assert request.status == statuses
