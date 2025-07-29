"""Tests for SMS Recipients builder."""

import pytest

from mailersend.builders.sms_recipients import SmsRecipientsBuilder
from mailersend.models.sms_recipients import (
    SmsRecipientsListRequest,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsRecipientStatus,
)


class TestSmsRecipientsBuilderBasicMethods:
    """Test basic SmsRecipientsBuilder methods."""

    def test_initialization(self):
        """Test SmsRecipientsBuilder initialization."""
        builder = SmsRecipientsBuilder()

        assert builder._status is None
        assert builder._sms_number_id is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._sms_recipient_id is None

    def test_status_method(self):
        """Test status method."""
        builder = SmsRecipientsBuilder()
        result = builder.status(SmsRecipientStatus.ACTIVE)

        assert result is builder  # Method chaining
        assert builder._status == SmsRecipientStatus.ACTIVE

    def test_status_method_opt_out(self):
        """Test status method with opt_out."""
        builder = SmsRecipientsBuilder()
        result = builder.status(SmsRecipientStatus.OPT_OUT)

        assert result is builder  # Method chaining
        assert builder._status == SmsRecipientStatus.OPT_OUT

    def test_sms_number_id_method(self):
        """Test sms_number_id method."""
        builder = SmsRecipientsBuilder()
        result = builder.sms_number_id("sms123")

        assert result is builder  # Method chaining
        assert builder._sms_number_id == "sms123"

    def test_page_method(self):
        """Test page method."""
        builder = SmsRecipientsBuilder()
        result = builder.page(2)

        assert result is builder  # Method chaining
        assert builder._page == 2

    def test_limit_method(self):
        """Test limit method."""
        builder = SmsRecipientsBuilder()
        result = builder.limit(50)

        assert result is builder  # Method chaining
        assert builder._limit == 50

    def test_sms_recipient_id_method(self):
        """Test sms_recipient_id method."""
        builder = SmsRecipientsBuilder()
        result = builder.sms_recipient_id("recipient123")

        assert result is builder  # Method chaining
        assert builder._sms_recipient_id == "recipient123"


class TestSmsRecipientsBuilderChaining:
    """Test method chaining functionality."""

    def test_method_chaining_all_parameters(self):
        """Test chaining all methods together."""
        builder = (
            SmsRecipientsBuilder()
            .status(SmsRecipientStatus.ACTIVE)
            .sms_number_id("sms456")
            .page(3)
            .limit(75)
            .sms_recipient_id("recipient789")
        )

        assert builder._status == SmsRecipientStatus.ACTIVE
        assert builder._sms_number_id == "sms456"
        assert builder._page == 3
        assert builder._limit == 75
        assert builder._sms_recipient_id == "recipient789"

    def test_method_chaining_partial_parameters(self):
        """Test chaining some methods."""
        builder = SmsRecipientsBuilder().status(SmsRecipientStatus.OPT_OUT).page(2)

        assert builder._status == SmsRecipientStatus.OPT_OUT
        assert builder._sms_number_id is None
        assert builder._page == 2
        assert builder._limit is None
        assert builder._sms_recipient_id is None


class TestSmsRecipientsBuilderListRequest:
    """Test build_list_request method."""

    def test_build_list_request_defaults(self):
        """Test build_list_request with default values."""
        builder = SmsRecipientsBuilder()
        request = builder.build_list_request()

        assert isinstance(request, SmsRecipientsListRequest)
        assert request.query_params.status is None
        assert request.query_params.sms_number_id is None
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_build_list_request_with_status(self):
        """Test build_list_request with status filter."""
        builder = SmsRecipientsBuilder().status(SmsRecipientStatus.ACTIVE)
        request = builder.build_list_request()

        assert request.query_params.status == SmsRecipientStatus.ACTIVE
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_build_list_request_with_sms_number_id(self):
        """Test build_list_request with sms_number_id filter."""
        builder = SmsRecipientsBuilder().sms_number_id("sms789")
        request = builder.build_list_request()

        assert request.query_params.sms_number_id == "sms789"
        assert request.query_params.status is None
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_build_list_request_with_pagination(self):
        """Test build_list_request with pagination parameters."""
        builder = SmsRecipientsBuilder().page(5).limit(100)
        request = builder.build_list_request()

        assert request.query_params.page == 5
        assert request.query_params.limit == 100
        assert request.query_params.status is None
        assert request.query_params.sms_number_id is None

    def test_build_list_request_with_all_parameters(self):
        """Test build_list_request with all parameters."""
        builder = (
            SmsRecipientsBuilder()
            .status(SmsRecipientStatus.OPT_OUT)
            .sms_number_id("sms999")
            .page(10)
            .limit(50)
        )
        request = builder.build_list_request()

        assert request.query_params.status == SmsRecipientStatus.OPT_OUT
        assert request.query_params.sms_number_id == "sms999"
        assert request.query_params.page == 10
        assert request.query_params.limit == 50

    def test_build_list_request_multiple_calls(self):
        """Test build_list_request can be called multiple times."""
        builder = SmsRecipientsBuilder().status(SmsRecipientStatus.ACTIVE)

        request1 = builder.build_list_request()
        request2 = builder.build_list_request()

        # Both requests should have the same parameters
        assert request1.query_params.status == request2.query_params.status
        # But should be different instances
        assert request1 is not request2


class TestSmsRecipientsBuilderGetRequest:
    """Test build_get_request method."""

    def test_build_get_request_valid(self):
        """Test build_get_request with valid sms_recipient_id."""
        builder = SmsRecipientsBuilder().sms_recipient_id("recipient123")
        request = builder.build_get_request()

        assert isinstance(request, SmsRecipientGetRequest)
        assert request.sms_recipient_id == "recipient123"

    def test_build_get_request_without_id_raises_error(self):
        """Test build_get_request raises error when sms_recipient_id is not set."""
        builder = SmsRecipientsBuilder()

        with pytest.raises(
            ValueError, match="SMS recipient ID is required for get request"
        ):
            builder.build_get_request()

    def test_build_get_request_with_other_params_set(self):
        """Test build_get_request ignores other parameters."""
        builder = (
            SmsRecipientsBuilder()
            .sms_recipient_id("recipient456")
            .status(SmsRecipientStatus.ACTIVE)
            .page(5)
            .limit(100)
        )
        request = builder.build_get_request()

        assert request.sms_recipient_id == "recipient456"
        # Other parameters should not affect the get request
        assert isinstance(request, SmsRecipientGetRequest)

    def test_build_get_request_multiple_calls(self):
        """Test build_get_request can be called multiple times."""
        builder = SmsRecipientsBuilder().sms_recipient_id("recipient789")

        request1 = builder.build_get_request()
        request2 = builder.build_get_request()

        # Both requests should have the same ID
        assert request1.sms_recipient_id == request2.sms_recipient_id
        # But should be different instances
        assert request1 is not request2


class TestSmsRecipientsBuilderUpdateRequest:
    """Test build_update_request method."""

    def test_build_update_request_valid_active(self):
        """Test build_update_request with valid parameters for active status."""
        builder = SmsRecipientsBuilder().sms_recipient_id("recipient123")
        request = builder.build_update_request(SmsRecipientStatus.ACTIVE)

        assert isinstance(request, SmsRecipientUpdateRequest)
        assert request.sms_recipient_id == "recipient123"
        assert request.status == SmsRecipientStatus.ACTIVE

    def test_build_update_request_valid_opt_out(self):
        """Test build_update_request with valid parameters for opt_out status."""
        builder = SmsRecipientsBuilder().sms_recipient_id("recipient456")
        request = builder.build_update_request(SmsRecipientStatus.OPT_OUT)

        assert isinstance(request, SmsRecipientUpdateRequest)
        assert request.sms_recipient_id == "recipient456"
        assert request.status == SmsRecipientStatus.OPT_OUT

    def test_build_update_request_without_id_raises_error(self):
        """Test build_update_request raises error when sms_recipient_id is not set."""
        builder = SmsRecipientsBuilder()

        with pytest.raises(
            ValueError, match="SMS recipient ID is required for update request"
        ):
            builder.build_update_request(SmsRecipientStatus.ACTIVE)

    def test_build_update_request_with_other_params_set(self):
        """Test build_update_request ignores other parameters."""
        builder = (
            SmsRecipientsBuilder()
            .sms_recipient_id("recipient789")
            .status(SmsRecipientStatus.ACTIVE)  # This should be ignored
            .page(5)
            .limit(100)
        )
        request = builder.build_update_request(SmsRecipientStatus.OPT_OUT)

        assert request.sms_recipient_id == "recipient789"
        assert (
            request.status == SmsRecipientStatus.OPT_OUT
        )  # Should use the passed parameter

    def test_build_update_request_multiple_calls(self):
        """Test build_update_request can be called multiple times with different statuses."""
        builder = SmsRecipientsBuilder().sms_recipient_id("recipient999")

        request1 = builder.build_update_request(SmsRecipientStatus.ACTIVE)
        request2 = builder.build_update_request(SmsRecipientStatus.OPT_OUT)

        # Both requests should have the same ID but different statuses
        assert request1.sms_recipient_id == request2.sms_recipient_id
        assert request1.status == SmsRecipientStatus.ACTIVE
        assert request2.status == SmsRecipientStatus.OPT_OUT
        # But should be different instances
        assert request1 is not request2


class TestSmsRecipientsBuilderEdgeCases:
    """Test edge cases and special scenarios."""

    def test_builder_state_persistence(self):
        """Test that builder state persists across multiple build calls."""
        builder = (
            SmsRecipientsBuilder()
            .status(SmsRecipientStatus.ACTIVE)
            .sms_number_id("sms123")
            .page(3)
            .limit(50)
            .sms_recipient_id("recipient456")
        )

        # Build list request
        list_request = builder.build_list_request()
        assert list_request.query_params.status == SmsRecipientStatus.ACTIVE
        assert list_request.query_params.sms_number_id == "sms123"

        # Build get request - should still work with same builder
        get_request = builder.build_get_request()
        assert get_request.sms_recipient_id == "recipient456"

        # Build update request - should still work with same builder
        update_request = builder.build_update_request(SmsRecipientStatus.OPT_OUT)
        assert update_request.sms_recipient_id == "recipient456"
        assert update_request.status == SmsRecipientStatus.OPT_OUT

    def test_builder_parameter_override(self):
        """Test that parameters can be overridden."""
        builder = SmsRecipientsBuilder().status(SmsRecipientStatus.ACTIVE)

        # Override with different status
        builder.status(SmsRecipientStatus.OPT_OUT)
        request = builder.build_list_request()

        assert request.query_params.status == SmsRecipientStatus.OPT_OUT

    def test_builder_with_empty_strings(self):
        """Test builder with empty strings."""
        builder = SmsRecipientsBuilder().sms_number_id("").sms_recipient_id("")

        # Empty strings should still be set
        assert builder._sms_number_id == ""
        assert builder._sms_recipient_id == ""

        # Building get request with empty ID should raise error during validation
        with pytest.raises(ValueError):
            builder.build_get_request()

    def test_builder_reuse_for_different_operations(self):
        """Test that same builder can be used for different operations."""
        builder = SmsRecipientsBuilder()

        # Use for list operation
        list_request1 = builder.status(SmsRecipientStatus.ACTIVE).build_list_request()
        assert list_request1.query_params.status == SmsRecipientStatus.ACTIVE

        # Modify for different list operation
        list_request2 = (
            builder.status(SmsRecipientStatus.OPT_OUT).page(2).build_list_request()
        )
        assert list_request2.query_params.status == SmsRecipientStatus.OPT_OUT
        assert list_request2.query_params.page == 2

        # Use for get operation
        get_request = builder.sms_recipient_id("recipient123").build_get_request()
        assert get_request.sms_recipient_id == "recipient123"

        # Use for update operation
        update_request = builder.build_update_request(SmsRecipientStatus.ACTIVE)
        assert update_request.sms_recipient_id == "recipient123"
        assert update_request.status == SmsRecipientStatus.ACTIVE
