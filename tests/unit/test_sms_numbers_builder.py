import pytest

from mailersend.builders.sms_numbers import SmsNumbersBuilder
from mailersend.models.sms_numbers import (
    SmsNumbersListRequest, SmsNumberGetRequest, SmsNumberUpdateRequest, SmsNumberDeleteRequest
)


class TestSmsNumbersBuilder:
    """Test SMS Numbers builder."""

    @pytest.fixture
    def builder(self):
        """Create a fresh builder instance."""
        return SmsNumbersBuilder()

    def test_builder_initialization(self, builder):
        """Test builder initializes with empty state."""
        assert builder._paused is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._sms_number_id is None

    def test_paused_method(self, builder):
        """Test paused method sets paused filter."""
        result = builder.paused(True)
        
        assert result is builder  # Returns self for chaining
        assert builder._paused is True

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

    def test_sms_number_id_method(self, builder):
        """Test sms_number_id method sets SMS number ID."""
        result = builder.sms_number_id("7z3m5jgrogdpyo6n")
        
        assert result is builder  # Returns self for chaining
        assert builder._sms_number_id == "7z3m5jgrogdpyo6n"

    def test_method_chaining(self, builder):
        """Test method chaining works correctly."""
        result = (builder
                 .paused(True)
                 .page(1)
                 .limit(25)
                 .sms_number_id("7z3m5jgrogdpyo6n"))
        
        assert result is builder
        assert builder._paused is True
        assert builder._page == 1
        assert builder._limit == 25
        assert builder._sms_number_id == "7z3m5jgrogdpyo6n"

    def test_build_list_request_full(self, builder):
        """Test building full list request."""
        request = (builder
                  .paused(False)
                  .page(2)
                  .limit(50)
                  .build_list_request())
        
        assert isinstance(request, SmsNumbersListRequest)
        assert request.paused is False
        assert request.page == 2
        assert request.limit == 50

    def test_build_list_request_empty(self, builder):
        """Test building empty list request."""
        request = builder.build_list_request()
        
        assert isinstance(request, SmsNumbersListRequest)
        assert request.paused is None
        assert request.page is None
        assert request.limit is None

    def test_build_list_request_partial(self, builder):
        """Test building partial list request."""
        request = builder.page(1).build_list_request()
        
        assert isinstance(request, SmsNumbersListRequest)
        assert request.paused is None
        assert request.page == 1
        assert request.limit is None

    def test_build_get_request_success(self, builder):
        """Test building get request successfully."""
        request = builder.sms_number_id("7z3m5jgrogdpyo6n").build_get_request()
        
        assert isinstance(request, SmsNumberGetRequest)
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"

    def test_build_get_request_missing_id(self, builder):
        """Test building get request without SMS number ID raises error."""
        with pytest.raises(ValueError) as exc_info:
            builder.build_get_request()
        
        assert "SMS number ID must be set" in str(exc_info.value)

    def test_build_update_request_success(self, builder):
        """Test building update request successfully."""
        request = (builder
                  .sms_number_id("7z3m5jgrogdpyo6n")
                  .paused(True)
                  .build_update_request())
        
        assert isinstance(request, SmsNumberUpdateRequest)
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.paused is True

    def test_build_update_request_without_paused(self, builder):
        """Test building update request without paused parameter."""
        request = builder.sms_number_id("7z3m5jgrogdpyo6n").build_update_request()
        
        assert isinstance(request, SmsNumberUpdateRequest)
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert request.paused is None

    def test_build_update_request_missing_id(self, builder):
        """Test building update request without SMS number ID raises error."""
        with pytest.raises(ValueError) as exc_info:
            builder.paused(True).build_update_request()
        
        assert "SMS number ID must be set" in str(exc_info.value)

    def test_build_delete_request_success(self, builder):
        """Test building delete request successfully."""
        request = builder.sms_number_id("7z3m5jgrogdpyo6n").build_delete_request()
        
        assert isinstance(request, SmsNumberDeleteRequest)
        assert request.sms_number_id == "7z3m5jgrogdpyo6n"

    def test_build_delete_request_missing_id(self, builder):
        """Test building delete request without SMS number ID raises error."""
        with pytest.raises(ValueError) as exc_info:
            builder.build_delete_request()
        
        assert "SMS number ID must be set" in str(exc_info.value)

    def test_reset_method(self, builder):
        """Test reset method clears all state."""
        # Set some state
        builder.paused(True).page(2).limit(50).sms_number_id("7z3m5jgrogdpyo6n")
        
        # Reset
        result = builder.reset()
        
        assert result is builder  # Returns self for chaining
        assert builder._paused is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._sms_number_id is None

    def test_builder_reuse_after_reset(self, builder):
        """Test builder can be reused after reset."""
        # First use
        request1 = builder.sms_number_id("id1").build_get_request()
        assert request1.sms_number_id == "id1"
        
        # Reset and reuse
        request2 = builder.reset().sms_number_id("id2").build_get_request()
        assert request2.sms_number_id == "id2"

    def test_multiple_requests_from_same_builder(self, builder):
        """Test building multiple requests from same builder state."""
        builder.sms_number_id("7z3m5jgrogdpyo6n").paused(True)
        
        # Build different request types with same state
        get_request = builder.build_get_request()
        update_request = builder.build_update_request()
        delete_request = builder.build_delete_request()
        
        assert get_request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert update_request.sms_number_id == "7z3m5jgrogdpyo6n"
        assert update_request.paused is True
        assert delete_request.sms_number_id == "7z3m5jgrogdpyo6n"