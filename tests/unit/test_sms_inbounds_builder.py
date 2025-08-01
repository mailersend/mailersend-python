"""Tests for SMS Inbounds builder."""

import pytest

from mailersend.builders.sms_inbounds import SmsInboundsBuilder
from mailersend.models.sms_inbounds import (
    SmsInboundsListRequest,
    SmsInboundGetRequest,
    SmsInboundCreateRequest,
    SmsInboundUpdateRequest,
    SmsInboundDeleteRequest,
    FilterComparer,
    SmsInboundFilter,
)


class TestSmsInboundsBuilderBasicMethods:
    """Test basic SmsInboundsBuilder methods."""

    def test_initialization(self):
        """Test SmsInboundsBuilder initialization."""
        builder = SmsInboundsBuilder()

        # Query parameters
        assert builder._sms_number_id is None
        assert builder._enabled is None
        assert builder._page is None
        assert builder._limit is None

        # Resource identifiers
        assert builder._sms_inbound_id is None

        # Create/Update fields
        assert builder._name is None
        assert builder._forward_url is None
        assert builder._filter_comparer is None
        assert builder._filter_value is None

    def test_sms_number_id_method(self):
        """Test sms_number_id method."""
        builder = SmsInboundsBuilder()
        result = builder.sms_number_id("sms123")

        assert result is builder  # Method chaining
        assert builder._sms_number_id == "sms123"

    def test_enabled_method(self):
        """Test enabled method."""
        builder = SmsInboundsBuilder()
        result = builder.enabled(True)

        assert result is builder  # Method chaining
        assert builder._enabled is True

        # Test with False
        builder.enabled(False)
        assert builder._enabled is False

    def test_page_method(self):
        """Test page method."""
        builder = SmsInboundsBuilder()
        result = builder.page(2)

        assert result is builder  # Method chaining
        assert builder._page == 2

    def test_limit_method(self):
        """Test limit method."""
        builder = SmsInboundsBuilder()
        result = builder.limit(50)

        assert result is builder  # Method chaining
        assert builder._limit == 50

    def test_sms_inbound_id_method(self):
        """Test sms_inbound_id method."""
        builder = SmsInboundsBuilder()
        result = builder.sms_inbound_id("inbound456")

        assert result is builder  # Method chaining
        assert builder._sms_inbound_id == "inbound456"

    def test_name_method(self):
        """Test name method."""
        builder = SmsInboundsBuilder()
        result = builder.name("Test Inbound")

        assert result is builder  # Method chaining
        assert builder._name == "Test Inbound"

    def test_forward_url_method(self):
        """Test forward_url method."""
        builder = SmsInboundsBuilder()
        result = builder.forward_url("https://example.com/webhook")

        assert result is builder  # Method chaining
        assert builder._forward_url == "https://example.com/webhook"

    def test_filter_method(self):
        """Test filter method."""
        builder = SmsInboundsBuilder()
        result = builder.filter(FilterComparer.STARTS_WITH, "START")

        assert result is builder  # Method chaining
        assert builder._filter_comparer == FilterComparer.STARTS_WITH
        assert builder._filter_value == "START"


class TestSmsInboundsBuilderChaining:
    """Test method chaining functionality."""

    def test_method_chaining_all_parameters(self):
        """Test chaining all methods together."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms123")
            .enabled(True)
            .page(2)
            .limit(50)
            .sms_inbound_id("inbound456")
            .name("Chained Inbound")
            .forward_url("https://example.com/chained")
            .filter(FilterComparer.CONTAINS, "TEST")
        )

        assert builder._sms_number_id == "sms123"
        assert builder._enabled is True
        assert builder._page == 2
        assert builder._limit == 50
        assert builder._sms_inbound_id == "inbound456"
        assert builder._name == "Chained Inbound"
        assert builder._forward_url == "https://example.com/chained"
        assert builder._filter_comparer == FilterComparer.CONTAINS
        assert builder._filter_value == "TEST"

    def test_method_chaining_query_params_only(self):
        """Test chaining query parameter methods."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms789")
            .enabled(False)
            .page(1)
            .limit(25)
        )

        assert builder._sms_number_id == "sms789"
        assert builder._enabled is False
        assert builder._page == 1
        assert builder._limit == 25

    def test_method_chaining_create_params_only(self):
        """Test chaining create parameter methods."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms999")
            .name("Create Only")
            .forward_url("https://example.com/create")
            .filter(FilterComparer.EQUAL, "EXACT")
        )

        assert builder._sms_number_id == "sms999"
        assert builder._name == "Create Only"
        assert builder._forward_url == "https://example.com/create"
        assert builder._filter_comparer == FilterComparer.EQUAL
        assert builder._filter_value == "EXACT"


class TestSmsInboundsBuilderListRequest:
    """Test build_list_request method."""

    def test_build_list_request_empty(self):
        """Test build_list_request with no parameters."""
        builder = SmsInboundsBuilder()
        request = builder.build_list_request()

        assert isinstance(request, SmsInboundsListRequest)
        assert request.query_params.sms_number_id is None
        assert request.query_params.enabled is None
        assert request.query_params.page is None
        assert request.query_params.limit is None

    def test_build_list_request_with_all_params(self):
        """Test build_list_request with all query parameters."""
        builder = (
            SmsInboundsBuilder().sms_number_id("sms123").enabled(True).page(3).limit(75)
        )
        request = builder.build_list_request()

        assert isinstance(request, SmsInboundsListRequest)
        assert request.query_params.sms_number_id == "sms123"
        assert request.query_params.enabled is True
        assert request.query_params.page == 3
        assert request.query_params.limit == 75

    def test_build_list_request_partial_params(self):
        """Test build_list_request with some query parameters."""
        builder = SmsInboundsBuilder().sms_number_id("sms456").page(2)
        request = builder.build_list_request()

        assert isinstance(request, SmsInboundsListRequest)
        assert request.query_params.sms_number_id == "sms456"
        assert request.query_params.enabled is None
        assert request.query_params.page == 2
        assert request.query_params.limit is None

    def test_build_list_request_ignores_non_query_params(self):
        """Test build_list_request ignores non-query parameters."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms789")
            .sms_inbound_id("inbound123")
            .name("Test")
            .forward_url("https://example.com")
        )
        request = builder.build_list_request()

        assert request.query_params.sms_number_id == "sms789"
        assert isinstance(request, SmsInboundsListRequest)


class TestSmsInboundsBuilderGetRequest:
    """Test build_get_request method."""

    def test_build_get_request_valid(self):
        """Test build_get_request with valid SMS inbound ID."""
        builder = SmsInboundsBuilder().sms_inbound_id("inbound123")
        request = builder.build_get_request()

        assert isinstance(request, SmsInboundGetRequest)
        assert request.sms_inbound_id == "inbound123"

    def test_build_get_request_without_inbound_id_raises_error(self):
        """Test build_get_request raises error when SMS inbound ID is not set."""
        builder = SmsInboundsBuilder()

        with pytest.raises(
            ValueError, match="SMS inbound ID is required for get request"
        ):
            builder.build_get_request()

    def test_build_get_request_ignores_other_params(self):
        """Test build_get_request ignores other parameters."""
        builder = (
            SmsInboundsBuilder()
            .sms_inbound_id("inbound456")
            .sms_number_id("sms123")
            .name("Test")
            .enabled(True)
        )
        request = builder.build_get_request()

        assert request.sms_inbound_id == "inbound456"
        assert isinstance(request, SmsInboundGetRequest)


class TestSmsInboundsBuilderCreateRequest:
    """Test build_create_request method."""

    def test_build_create_request_valid_minimal(self):
        """Test build_create_request with minimal required fields."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms123")
            .name("Test Inbound")
            .forward_url("https://example.com/webhook")
        )
        request = builder.build_create_request()

        assert isinstance(request, SmsInboundCreateRequest)
        assert request.sms_number_id == "sms123"
        assert request.name == "Test Inbound"
        assert request.forward_url == "https://example.com/webhook"
        assert request.filter is None
        assert request.enabled is True  # Default value

    def test_build_create_request_valid_with_filter(self):
        """Test build_create_request with filter."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms456")
            .name("Filtered Inbound")
            .forward_url("https://example.com/filtered")
            .filter(FilterComparer.STARTS_WITH, "START")
            .enabled(False)
        )
        request = builder.build_create_request()

        assert isinstance(request, SmsInboundCreateRequest)
        assert request.sms_number_id == "sms456"
        assert request.name == "Filtered Inbound"
        assert request.forward_url == "https://example.com/filtered"
        assert isinstance(request.filter, SmsInboundFilter)
        assert request.filter.comparer == FilterComparer.STARTS_WITH
        assert request.filter.value == "START"
        assert request.enabled is False

    def test_build_create_request_without_filter_comparer(self):
        """Test build_create_request when only filter value is set."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms789")
            .name("No Comparer")
            .forward_url("https://example.com/no-comparer")
        )
        # Manually set only filter value without comparer
        builder._filter_value = "TEST"
        request = builder.build_create_request()

        # Should not include filter if comparer is missing
        assert request.filter is None

    def test_build_create_request_without_filter_value(self):
        """Test build_create_request when only filter comparer is set."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms999")
            .name("No Value")
            .forward_url("https://example.com/no-value")
        )
        # Manually set only filter comparer without value
        builder._filter_comparer = FilterComparer.CONTAINS
        request = builder.build_create_request()

        # Should not include filter if value is missing
        assert request.filter is None

    def test_build_create_request_missing_sms_number_id_raises_error(self):
        """Test build_create_request raises error when SMS number ID is not set."""
        builder = SmsInboundsBuilder().name("Test").forward_url("https://example.com")

        with pytest.raises(
            ValueError, match="SMS number ID is required for create request"
        ):
            builder.build_create_request()

    def test_build_create_request_missing_name_raises_error(self):
        """Test build_create_request raises error when name is not set."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms123")
            .forward_url("https://example.com")
        )

        with pytest.raises(ValueError, match="Name is required for create request"):
            builder.build_create_request()

    def test_build_create_request_missing_forward_url_raises_error(self):
        """Test build_create_request raises error when forward URL is not set."""
        builder = SmsInboundsBuilder().sms_number_id("sms123").name("Test")

        with pytest.raises(
            ValueError, match="Forward URL is required for create request"
        ):
            builder.build_create_request()


class TestSmsInboundsBuilderUpdateRequest:
    """Test build_update_request method."""

    def test_build_update_request_valid_partial(self):
        """Test build_update_request with partial fields."""
        builder = SmsInboundsBuilder().sms_inbound_id("inbound123").name("Updated Name")
        request = builder.build_update_request()

        assert isinstance(request, SmsInboundUpdateRequest)
        assert request.sms_inbound_id == "inbound123"
        assert request.name == "Updated Name"
        assert request.sms_number_id is None
        assert request.forward_url is None
        assert request.filter is None
        assert request.enabled is None

    def test_build_update_request_valid_full(self):
        """Test build_update_request with all fields."""
        builder = (
            SmsInboundsBuilder()
            .sms_inbound_id("inbound456")
            .sms_number_id("sms789")
            .name("Fully Updated")
            .forward_url("https://example.com/updated")
            .filter(FilterComparer.ENDS_WITH, "END")
            .enabled(True)
        )
        request = builder.build_update_request()

        assert isinstance(request, SmsInboundUpdateRequest)
        assert request.sms_inbound_id == "inbound456"
        assert request.sms_number_id == "sms789"
        assert request.name == "Fully Updated"
        assert request.forward_url == "https://example.com/updated"
        assert isinstance(request.filter, SmsInboundFilter)
        assert request.filter.comparer == FilterComparer.ENDS_WITH
        assert request.filter.value == "END"
        assert request.enabled is True

    def test_build_update_request_with_filter_partial(self):
        """Test build_update_request with incomplete filter."""
        builder = (
            SmsInboundsBuilder().sms_inbound_id("inbound789").name("Partial Filter")
        )
        # Set only comparer, not value
        builder._filter_comparer = FilterComparer.EQUAL
        request = builder.build_update_request()

        # Should not include filter if incomplete
        assert request.filter is None
        assert request.name == "Partial Filter"

    def test_build_update_request_without_inbound_id_raises_error(self):
        """Test build_update_request raises error when SMS inbound ID is not set."""
        builder = SmsInboundsBuilder().name("Test")

        with pytest.raises(
            ValueError, match="SMS inbound ID is required for update request"
        ):
            builder.build_update_request()


class TestSmsInboundsBuilderDeleteRequest:
    """Test build_delete_request method."""

    def test_build_delete_request_valid(self):
        """Test build_delete_request with valid SMS inbound ID."""
        builder = SmsInboundsBuilder().sms_inbound_id("inbound123")
        request = builder.build_delete_request()

        assert isinstance(request, SmsInboundDeleteRequest)
        assert request.sms_inbound_id == "inbound123"

    def test_build_delete_request_without_inbound_id_raises_error(self):
        """Test build_delete_request raises error when SMS inbound ID is not set."""
        builder = SmsInboundsBuilder()

        with pytest.raises(
            ValueError, match="SMS inbound ID is required for delete request"
        ):
            builder.build_delete_request()

    def test_build_delete_request_ignores_other_params(self):
        """Test build_delete_request ignores other parameters."""
        builder = (
            SmsInboundsBuilder()
            .sms_inbound_id("inbound789")
            .name("To Be Deleted")
            .forward_url("https://example.com")
            .enabled(True)
        )
        request = builder.build_delete_request()

        assert request.sms_inbound_id == "inbound789"
        assert isinstance(request, SmsInboundDeleteRequest)


class TestSmsInboundsBuilderFilterComparers:
    """Test builder with all filter comparers."""

    def test_build_create_request_equal_comparer(self):
        """Test build_create_request with EQUAL comparer."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms123")
            .name("Equal Test")
            .forward_url("https://example.com/equal")
            .filter(FilterComparer.EQUAL, "EXACT")
        )
        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.EQUAL
        assert request.filter.value == "EXACT"

    def test_build_create_request_not_equal_comparer(self):
        """Test build_create_request with NOT_EQUAL comparer."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms456")
            .name("Not Equal Test")
            .forward_url("https://example.com/not-equal")
            .filter(FilterComparer.NOT_EQUAL, "IGNORE")
        )
        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.NOT_EQUAL
        assert request.filter.value == "IGNORE"

    def test_build_create_request_contains_comparer(self):
        """Test build_create_request with CONTAINS comparer."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms789")
            .name("Contains Test")
            .forward_url("https://example.com/contains")
            .filter(FilterComparer.CONTAINS, "STOP")
        )
        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.CONTAINS
        assert request.filter.value == "STOP"

    def test_build_create_request_not_contains_comparer(self):
        """Test build_create_request with NOT_CONTAINS comparer."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms999")
            .name("Not Contains Test")
            .forward_url("https://example.com/not-contains")
            .filter(FilterComparer.NOT_CONTAINS, "SPAM")
        )
        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.NOT_CONTAINS
        assert request.filter.value == "SPAM"

    def test_build_create_request_starts_with_comparer(self):
        """Test build_create_request with STARTS_WITH comparer."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms111")
            .name("Starts With Test")
            .forward_url("https://example.com/starts-with")
            .filter(FilterComparer.STARTS_WITH, "START")
        )
        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.STARTS_WITH
        assert request.filter.value == "START"

    def test_build_create_request_ends_with_comparer(self):
        """Test build_create_request with ENDS_WITH comparer."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms222")
            .name("Ends With Test")
            .forward_url("https://example.com/ends-with")
            .filter(FilterComparer.ENDS_WITH, "END")
        )
        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.ENDS_WITH
        assert request.filter.value == "END"

    def test_build_create_request_not_starts_with_comparer(self):
        """Test build_create_request with NOT_STARTS_WITH comparer."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms333")
            .name("Not Starts With Test")
            .forward_url("https://example.com/not-starts-with")
            .filter(FilterComparer.NOT_STARTS_WITH, "AVOID")
        )
        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.NOT_STARTS_WITH
        assert request.filter.value == "AVOID"

    def test_build_create_request_not_ends_with_comparer(self):
        """Test build_create_request with NOT_ENDS_WITH comparer."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms444")
            .name("Not Ends With Test")
            .forward_url("https://example.com/not-ends-with")
            .filter(FilterComparer.NOT_ENDS_WITH, "EXCLUDE")
        )
        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.NOT_ENDS_WITH
        assert request.filter.value == "EXCLUDE"


class TestSmsInboundsBuilderEdgeCases:
    """Test edge cases and special scenarios."""

    def test_builder_state_persistence(self):
        """Test that builder state persists across multiple build calls."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms123")
            .sms_inbound_id("inbound456")
            .name("Persistent Inbound")
            .forward_url("https://example.com/persistent")
            .filter(FilterComparer.CONTAINS, "KEEP")
            .enabled(True)
            .page(2)
            .limit(50)
        )

        # Build list request
        list_request = builder.build_list_request()
        assert list_request.query_params.sms_number_id == "sms123"
        assert list_request.query_params.page == 2

        # Build get request - should still work with same builder
        get_request = builder.build_get_request()
        assert get_request.sms_inbound_id == "inbound456"

        # Build create request - should still work with same builder
        create_request = builder.build_create_request()
        assert create_request.name == "Persistent Inbound"
        assert create_request.filter.value == "KEEP"

        # Build update request - should still work with same builder
        update_request = builder.build_update_request()
        assert update_request.sms_inbound_id == "inbound456"
        assert update_request.enabled is True

        # Build delete request - should still work with same builder
        delete_request = builder.build_delete_request()
        assert delete_request.sms_inbound_id == "inbound456"

    def test_builder_parameter_override(self):
        """Test that parameters can be overridden."""
        builder = SmsInboundsBuilder().name("Original Name")

        # Override with different name
        builder.name("New Name")
        create_request = (
            builder.sms_number_id("sms123")
            .forward_url("https://example.com")
            .build_create_request()
        )

        assert create_request.name == "New Name"

    def test_builder_filter_override(self):
        """Test that filter can be overridden."""
        builder = SmsInboundsBuilder().filter(FilterComparer.EQUAL, "OLD")

        # Override with different filter
        builder.filter(FilterComparer.CONTAINS, "NEW")
        create_request = (
            builder.sms_number_id("sms789")
            .name("Filter Test")
            .forward_url("https://example.com")
            .build_create_request()
        )

        assert create_request.filter.comparer == FilterComparer.CONTAINS
        assert create_request.filter.value == "NEW"

    def test_builder_reuse_for_different_operations(self):
        """Test that same builder can be used for different operations."""
        builder = SmsInboundsBuilder()

        # Use for list operation
        list_request = (
            builder.sms_number_id("sms123").enabled(True).page(1).build_list_request()
        )
        assert list_request.query_params.sms_number_id == "sms123"

        # Modify for create operation
        create_request = (
            builder.name("Reused Builder")
            .forward_url("https://example.com/reused")
            .filter(FilterComparer.STARTS_WITH, "BEGIN")
            .build_create_request()
        )
        assert create_request.name == "Reused Builder"
        assert create_request.sms_number_id == "sms123"  # Preserved from list operation

        # Use for get operation
        get_request = builder.sms_inbound_id("inbound789").build_get_request()
        assert get_request.sms_inbound_id == "inbound789"

        # Use for update operation
        update_request = builder.enabled(False).build_update_request()
        assert update_request.sms_inbound_id == "inbound789"
        assert update_request.enabled is False

        # Use for delete operation
        delete_request = builder.build_delete_request()
        assert delete_request.sms_inbound_id == "inbound789"

    def test_multiple_calls_to_same_build_method(self):
        """Test that multiple calls to the same build method work correctly."""
        builder = (
            SmsInboundsBuilder()
            .sms_inbound_id("inbound123")
            .sms_number_id("sms456")
            .name("Multi-call Inbound")
            .forward_url("https://example.com/multi")
            .filter(FilterComparer.EQUAL, "EXACT")
            .enabled(True)
        )

        # Multiple calls should create separate request instances
        request1 = builder.build_update_request()
        request2 = builder.build_update_request()

        # Both should have same values but be different instances
        assert request1.sms_inbound_id == request2.sms_inbound_id == "inbound123"
        assert request1.name == request2.name == "Multi-call Inbound"
        assert request1 is not request2

    def test_create_request_with_enabled_none_uses_default(self):
        """Test that create request uses model default when enabled is not set."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms555")
            .name("Default Enabled")
            .forward_url("https://example.com/default")
        )

        request = builder.build_create_request()

        # Should use model default (True) when not explicitly set
        assert request.enabled is True

    def test_filter_edge_cases(self):
        """Test filter with edge case values."""
        builder = (
            SmsInboundsBuilder()
            .sms_number_id("sms666")
            .name("Edge Case Filter")
            .forward_url("https://example.com/edge")
            .filter(FilterComparer.CONTAINS, "!@#$%^&*()")
        )

        request = builder.build_create_request()

        assert request.filter.comparer == FilterComparer.CONTAINS
        assert request.filter.value == "!@#$%^&*()"

    def test_query_params_edge_values(self):
        """Test query parameters with edge values."""
        builder = (
            SmsInboundsBuilder()
            .page(1)  # Minimum page
            .limit(10)  # Minimum limit
            .enabled(False)
        )  # Explicit False

        request = builder.build_list_request()

        assert request.query_params.page == 1
        assert request.query_params.limit == 10
        assert request.query_params.enabled is False
