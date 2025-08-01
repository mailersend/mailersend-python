import pytest

from mailersend.builders.inbound import InboundBuilder
from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.inbound import (
    InboundListRequest,
    InboundListQueryParams,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
    InboundFilterGroup,
    InboundForward,
)


class TestInboundBuilder:
    """Test InboundBuilder functionality."""

    def test_builder_initialization(self):
        """Test builder initialization."""
        builder = InboundBuilder()
        assert builder._domain_id is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._inbound_id is None
        assert builder._name is None
        assert builder._domain_enabled is None
        assert builder._inbound_domain is None
        assert builder._inbound_priority is None
        assert builder._catch_filter == []
        assert builder._catch_type is None
        assert builder._match_filter == []
        assert builder._match_type is None
        assert builder._forwards == []

    def test_reset_method(self):
        """Test reset method."""
        builder = InboundBuilder()
        builder.domain_id("test").page(2).name("Test")
        builder.reset()
        assert builder._domain_id is None
        assert builder._page is None
        assert builder._name is None

    def test_copy_method(self):
        """Test copy method."""
        builder = InboundBuilder()
        builder.domain_id("test").page(2).name("Test Route")

        copy_builder = builder.copy()
        assert copy_builder._domain_id == "test"
        assert copy_builder._page == 2
        assert copy_builder._name == "Test Route"

        # Verify it's a separate instance
        copy_builder.domain_id("different")
        assert builder._domain_id == "test"
        assert copy_builder._domain_id == "different"

    def test_fluent_api_chaining(self):
        """Test fluent API method chaining."""
        builder = InboundBuilder()
        result = builder.domain_id("test").page(1).limit(50).name("Test Route")
        assert result is builder  # Should return self for chaining
        assert builder._domain_id == "test"
        assert builder._page == 1
        assert builder._limit == 50
        assert builder._name == "Test Route"

    def test_pagination_methods(self):
        """Test pagination methods."""
        builder = InboundBuilder()
        builder.page(3).limit(25)
        assert builder._page == 3
        assert builder._limit == 25

    def test_filtering_methods(self):
        """Test filtering methods."""
        builder = InboundBuilder()
        builder.domain_id("domain123")
        assert builder._domain_id == "domain123"

    def test_identification_methods(self):
        """Test identification methods."""
        builder = InboundBuilder()
        builder.inbound_id("inbound123")
        assert builder._inbound_id == "inbound123"

    def test_basic_configuration_methods(self):
        """Test basic configuration methods."""
        builder = InboundBuilder()
        builder.name("Test Route").domain_enabled(True).inbound_domain(
            "inbound.example.com"
        ).inbound_priority(50)
        assert builder._name == "Test Route"
        assert builder._domain_enabled is True
        assert builder._inbound_domain == "inbound.example.com"
        assert builder._inbound_priority == 50

    def test_catch_and_match_type_methods(self):
        """Test catch and match type methods."""
        builder = InboundBuilder()
        builder.catch_type("all").match_type("one")
        assert builder._catch_type == "all"
        assert builder._match_type == "one"

    def test_filter_management_methods(self):
        """Test filter management methods."""
        builder = InboundBuilder()

        # Add catch filter
        builder.add_catch_filter("catch_all")
        assert len(builder._catch_filter) == 1
        assert builder._catch_filter[0].type == "catch_all"

        # Add match filter with conditions
        filters = [{"comparer": "equal", "value": "test"}]
        builder.add_match_filter("match_sender", filters)
        assert len(builder._match_filter) == 1
        assert builder._match_filter[0].type == "match_sender"
        assert builder._match_filter[0].filters == filters

        # Clear filters
        builder.clear_catch_filters()
        builder.clear_match_filters()
        assert builder._catch_filter == []
        assert builder._match_filter == []

    def test_forward_management_methods(self):
        """Test forward management methods."""
        builder = InboundBuilder()

        # Add generic forward
        builder.add_forward("email", "test@example.com", forward_id="id123")
        assert len(builder._forwards) == 1
        assert builder._forwards[0].type == "email"
        assert builder._forwards[0].value == "test@example.com"
        assert builder._forwards[0].id == "id123"

        # Add email forward
        builder.add_email_forward("test2@example.com")
        assert len(builder._forwards) == 2
        assert builder._forwards[1].type == "email"
        assert builder._forwards[1].value == "test2@example.com"

        # Add webhook forward
        builder.add_webhook_forward("https://example.com/webhook", "secret123")
        assert len(builder._forwards) == 3
        assert builder._forwards[2].type == "webhook"
        assert builder._forwards[2].value == "https://example.com/webhook"
        assert builder._forwards[2].secret == "secret123"

        # Clear forwards
        builder.clear_forwards()
        assert builder._forwards == []

    def test_convenience_filter_methods(self):
        """Test convenience methods for common filter configurations."""
        builder = InboundBuilder()

        # Catch all
        builder.catch_all()
        assert len(builder._catch_filter) == 1
        assert builder._catch_filter[0].type == "catch_all"

        # Catch recipient
        filters = [{"comparer": "equal", "value": "test"}]
        builder.catch_recipient(filters, "one")
        assert len(builder._catch_filter) == 2  # Added to existing
        assert builder._catch_filter[1].type == "catch_recipient"
        assert builder._catch_type == "one"

        # Match all
        builder.match_all()
        assert len(builder._match_filter) == 1
        assert builder._match_filter[0].type == "match_all"

        # Match sender
        builder.match_sender(filters, "all")
        assert len(builder._match_filter) == 2
        assert builder._match_filter[1].type == "match_sender"
        assert builder._match_type == "all"

        # Match domain
        builder.match_domain(filters, "one")
        assert len(builder._match_filter) == 3
        assert builder._match_filter[2].type == "match_domain"
        assert builder._match_type == "one"

        # Match header
        builder.match_header(filters, "all")
        assert len(builder._match_filter) == 4
        assert builder._match_filter[3].type == "match_header"
        assert builder._match_type == "all"

    def test_domain_convenience_methods(self):
        """Test convenience methods for domain configuration."""
        builder = InboundBuilder()

        # Enable domain
        builder.enable_domain("inbound.example.com", 75)
        assert builder._domain_enabled is True
        assert builder._inbound_domain == "inbound.example.com"
        assert builder._inbound_priority == 75

        # Disable domain
        builder.disable_domain()
        assert builder._domain_enabled is False
        assert builder._inbound_domain is None
        assert builder._inbound_priority is None

    def test_build_list_request(self):
        """Test building list request."""
        builder = InboundBuilder()
        builder.domain_id("domain123").page(2).limit(50)

        request = builder.build_list_request()
        assert isinstance(request, InboundListRequest)
        assert isinstance(request.query_params, InboundListQueryParams)
        assert request.query_params.domain_id == "domain123"
        assert request.query_params.page == 2
        assert request.query_params.limit == 50

    def test_build_list_request_minimal(self):
        """Test building minimal list request with defaults."""
        builder = InboundBuilder()

        request = builder.build_list_request()
        assert isinstance(request, InboundListRequest)
        assert isinstance(request.query_params, InboundListQueryParams)
        # Uses defaults when builder values are None
        assert request.query_params.page == 1  # Default
        assert request.query_params.limit == 25  # Default
        assert request.query_params.domain_id is None

    def test_build_list_request_partial_params(self):
        """Test building list request with only some parameters set."""
        builder = InboundBuilder()
        builder.page(3)  # Only set page, leave others as None/default

        request = builder.build_list_request()
        assert isinstance(request, InboundListRequest)
        assert request.query_params.page == 3
        assert request.query_params.limit == 25  # Uses default
        assert request.query_params.domain_id is None

    def test_build_get_request(self):
        """Test building get request."""
        builder = InboundBuilder()
        builder.inbound_id("inbound123")

        request = builder.build_get_request()
        assert isinstance(request, InboundGetRequest)
        assert request.inbound_id == "inbound123"

    def test_build_get_request_missing_id(self):
        """Test building get request without ID raises error."""
        builder = InboundBuilder()
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_get_request()
        assert "Inbound ID is required for get request" in str(exc_info.value)

    def test_build_create_request(self):
        """Test building create request."""
        builder = InboundBuilder()
        builder.domain_id("domain123").name("Test Route").domain_enabled(False)
        builder.catch_all().match_all()
        builder.add_email_forward("test@example.com")

        request = builder.build_create_request()
        assert isinstance(request, InboundCreateRequest)
        assert request.domain_id == "domain123"
        assert request.name == "Test Route"
        assert request.domain_enabled is False
        assert request.catch_filter.type == "catch_all"
        assert request.catch_filter.filters is None  # catch_all doesn't need specific filters
        assert request.match_filter.type == "match_all"
        assert request.match_filter.filters is None  # match_all doesn't need specific filters
        assert len(request.forwards) == 1

    def test_build_create_request_with_domain_enabled(self):
        """Test building create request with domain enabled."""
        builder = InboundBuilder()
        builder.domain_id("domain123").name("Test Route")
        builder.enable_domain("inbound.example.com", 50)
        builder.catch_all().match_all()
        builder.add_email_forward("test@example.com")

        request = builder.build_create_request()
        assert request.domain_enabled is True
        assert request.inbound_domain == "inbound.example.com"
        assert request.inbound_priority == 50

    def test_build_create_request_missing_required_fields(self):
        """Test building create request with missing required fields."""
        builder = InboundBuilder()

        # Missing domain_id
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_create_request()
        assert "Domain ID is required for create request" in str(exc_info.value)

        # Missing name
        builder.domain_id("domain123")
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_create_request()
        assert "Name is required for create request" in str(exc_info.value)

        # Missing domain_enabled
        builder.name("Test Route")
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_create_request()
        assert "Domain enabled flag is required for create request" in str(
            exc_info.value
        )

        # Missing catch_filter
        builder.domain_enabled(False)
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_create_request()
        assert "At least one catch filter is required for create request" in str(
            exc_info.value
        )

        # Missing match_filter
        builder.catch_all()
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_create_request()
        assert "At least one match filter is required for create request" in str(
            exc_info.value
        )

        # Missing forwards
        builder.match_all()
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_create_request()
        assert "At least one forward is required for create request" in str(
            exc_info.value
        )

    def test_build_update_request(self):
        """Test building update request."""
        builder = InboundBuilder()
        builder.inbound_id("inbound123").name("Updated Route").domain_enabled(True)
        builder.enable_domain("inbound.example.com", 75)
        builder.catch_all().match_all()
        builder.add_email_forward("test@example.com")

        request = builder.build_update_request()
        assert isinstance(request, InboundUpdateRequest)
        assert request.inbound_id == "inbound123"
        assert request.name == "Updated Route"
        assert request.domain_enabled is True
        assert request.inbound_domain == "inbound.example.com"
        assert request.inbound_priority == 75

    def test_build_update_request_missing_required_fields(self):
        """Test building update request with missing required fields."""
        builder = InboundBuilder()

        # Missing inbound_id
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_update_request()
        assert "Inbound ID is required for update request" in str(exc_info.value)

        # Missing name
        builder.inbound_id("inbound123")
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_update_request()
        assert "Name is required for update request" in str(exc_info.value)

        # Missing domain_enabled
        builder.name("Test Route")
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_update_request()
        assert "Domain enabled flag is required for update request" in str(
            exc_info.value
        )

    def test_build_delete_request(self):
        """Test building delete request."""
        builder = InboundBuilder()
        builder.inbound_id("inbound123")

        request = builder.build_delete_request()
        assert isinstance(request, InboundDeleteRequest)
        assert request.inbound_id == "inbound123"

    def test_build_delete_request_missing_id(self):
        """Test building delete request without ID raises error."""
        builder = InboundBuilder()
        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_delete_request()
        assert "Inbound ID is required for delete request" in str(exc_info.value)

    def test_complex_filter_configuration(self):
        """Test building complex filter configurations."""
        builder = InboundBuilder()
        builder.domain_id("domain123").name("Complex Route").domain_enabled(False)

        # Complex catch configuration
        catch_filters = [
            {"comparer": "equal", "value": "support"},
            {"comparer": "contains", "value": "help"},
        ]
        builder.catch_recipient(catch_filters, "one")

        # Complex match configuration
        match_filters = [
            {"comparer": "starts-with", "value": "urgent"},
            {"comparer": "ends-with", "value": "priority"},
        ]
        builder.match_sender(match_filters, "all")

        # Multiple forwards
        builder.add_email_forward("support@example.com")
        builder.add_webhook_forward("https://api.example.com/webhook", "secret123")

        request = builder.build_create_request()
        assert request.catch_filter is not None
        assert request.catch_filter.type == "catch_recipient"
        assert request.catch_filter.filters == catch_filters
        assert request.catch_type == "one"

        assert request.match_filter is not None
        assert request.match_filter.type == "match_sender"
        assert request.match_filter.filters == match_filters
        assert request.match_type == "all"

        assert len(request.forwards) == 2
        assert request.forwards[0].type == "email"
        assert request.forwards[1].type == "webhook"

    def test_state_isolation_between_builds(self):
        """Test that multiple builds don't interfere with each other."""
        builder = InboundBuilder()

        # Build list request
        builder.domain_id("domain123").page(1)
        list_request = builder.build_list_request()

        # Build get request (should work with same builder)
        builder.inbound_id("inbound123")
        get_request = builder.build_get_request()

        # Verify both requests are correct
        assert list_request.query_params.domain_id == "domain123"
        assert list_request.query_params.page == 1
        assert get_request.inbound_id == "inbound123"

    def test_builder_reuse_with_reset(self):
        """Test reusing builder after reset."""
        builder = InboundBuilder()

        # First configuration
        builder.domain_id("domain1").page(1).name("Route 1")
        first_request = builder.build_list_request()

        # Reset and new configuration
        builder.reset()
        builder.domain_id("domain2").page(2).name("Route 2")
        second_request = builder.build_list_request()

        # Verify they're different
        assert first_request.query_params.domain_id == "domain1"
        assert first_request.query_params.page == 1
        assert second_request.query_params.domain_id == "domain2"
        assert second_request.query_params.page == 2
