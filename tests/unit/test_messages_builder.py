import pytest

from mailersend.builders.messages import MessagesBuilder
from mailersend.models.messages import (
    MessagesListRequest,
    MessagesListQueryParams,
    MessageGetRequest,
)
from mailersend.exceptions import ValidationError


class TestMessagesBuilder:
    """Test MessagesBuilder class."""

    def test_initialization(self):
        """Test builder initialization."""
        builder = MessagesBuilder()
        assert builder is not None
        assert builder._page is None
        assert builder._limit is None
        assert builder._message_id is None

    def test_page_method(self):
        """Test page method."""
        builder = MessagesBuilder()
        result = builder.page(2)
        assert result is builder  # Test fluent interface
        assert builder._page == 2

    def test_page_validation_zero(self):
        """Test page validation with zero."""
        builder = MessagesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.page(0)
        assert "Page must be greater than 0" in str(exc_info.value)

    def test_page_validation_negative(self):
        """Test page validation with negative number."""
        builder = MessagesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.page(-1)
        assert "Page must be greater than 0" in str(exc_info.value)

    def test_limit_method(self):
        """Test limit method."""
        builder = MessagesBuilder()
        result = builder.limit(50)
        assert result is builder  # Test fluent interface
        assert builder._limit == 50

    def test_limit_validation_min(self):
        """Test limit validation - minimum value."""
        builder = MessagesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.limit(5)
        assert "Limit must be between 10 and 100" in str(exc_info.value)

    def test_limit_validation_max(self):
        """Test limit validation - maximum value."""
        builder = MessagesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.limit(150)
        assert "Limit must be between 10 and 100" in str(exc_info.value)

    def test_limit_boundaries(self):
        """Test limit boundaries."""
        builder = MessagesBuilder()

        # Test minimum valid value
        builder.limit(10)
        assert builder._limit == 10

        # Test maximum valid value
        builder.limit(100)
        assert builder._limit == 100

    def test_message_id_method(self):
        """Test message_id method."""
        builder = MessagesBuilder()
        result = builder.message_id("5ee0b183b251345e407c936a")
        assert result is builder  # Test fluent interface
        assert builder._message_id == "5ee0b183b251345e407c936a"

    def test_message_id_validation_empty(self):
        """Test message_id validation with empty string."""
        builder = MessagesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.message_id("")
        assert "Message ID cannot be empty" in str(exc_info.value)

    def test_message_id_validation_whitespace(self):
        """Test message_id validation with whitespace."""
        builder = MessagesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.message_id("   ")
        assert "Message ID cannot be empty" in str(exc_info.value)

    def test_message_id_trimming(self):
        """Test message_id trimming."""
        builder = MessagesBuilder()
        builder.message_id("  5ee0b183b251345e407c936a  ")
        assert builder._message_id == "5ee0b183b251345e407c936a"

    def test_build_list_request_default(self):
        """Test building list request with default values."""
        builder = MessagesBuilder()
        request = builder.build_list_request()

        # Verify request structure
        assert isinstance(request, MessagesListRequest)
        assert isinstance(request.query_params, MessagesListQueryParams)

        # Verify default values are used
        assert request.query_params.page == 1  # Default value
        assert request.query_params.limit == 25  # Default value

    def test_build_list_request_with_parameters(self):
        """Test building list request with custom parameters."""
        builder = MessagesBuilder()
        request = builder.page(2).limit(50).build_list_request()

        # Verify request structure
        assert isinstance(request, MessagesListRequest)
        assert isinstance(request.query_params, MessagesListQueryParams)

        # Verify custom values
        assert request.query_params.page == 2
        assert request.query_params.limit == 50

    def test_build_list_request_partial_params(self):
        """Test building list request with partial parameters."""
        builder = MessagesBuilder()
        request = builder.page(3).build_list_request()

        # Verify request structure
        assert isinstance(request, MessagesListRequest)
        assert isinstance(request.query_params, MessagesListQueryParams)

        # Verify mixed values (custom page, default limit)
        assert request.query_params.page == 3
        assert request.query_params.limit == 25  # Default

    def test_build_list_request_only_limit(self):
        """Test building list request with only limit set."""
        builder = MessagesBuilder()
        request = builder.limit(75).build_list_request()

        # Verify request structure
        assert isinstance(request, MessagesListRequest)
        assert isinstance(request.query_params, MessagesListQueryParams)

        # Verify mixed values (default page, custom limit)
        assert request.query_params.page == 1  # Default
        assert request.query_params.limit == 75

    def test_build_get_request(self):
        """Test building get request."""
        builder = MessagesBuilder()
        request = builder.message_id("5ee0b183b251345e407c936a").build_get_request()

        assert isinstance(request, MessageGetRequest)
        assert request.message_id == "5ee0b183b251345e407c936a"

    def test_build_get_request_without_message_id(self):
        """Test building get request without message ID."""
        builder = MessagesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.build_get_request()
        assert "Message ID must be set to build get request" in str(exc_info.value)

    def test_reset_method(self):
        """Test reset method."""
        builder = MessagesBuilder()
        builder.page(2).limit(50).message_id("test-id")

        result = builder.reset()
        assert result is builder  # Test fluent interface
        assert builder._page is None
        assert builder._limit is None
        assert builder._message_id is None

    def test_copy_method(self):
        """Test copy method."""
        builder = MessagesBuilder()
        builder.page(3).limit(75).message_id("test-message-id")

        copied_builder = builder.copy()

        # Verify it's a different instance
        assert copied_builder is not builder

        # Verify same configuration
        assert copied_builder._page == 3
        assert copied_builder._limit == 75
        assert copied_builder._message_id == "test-message-id"

        # Verify modifications to copy don't affect original
        copied_builder.page(5)
        assert builder._page == 3
        assert copied_builder._page == 5

    def test_method_chaining(self):
        """Test method chaining with multiple calls."""
        builder = MessagesBuilder()
        result = builder.page(1).limit(25).message_id("test-id").reset().page(2)

        assert result is builder  # All methods return self
        assert builder._page == 2
        assert builder._limit is None  # Reset cleared this
        assert builder._message_id is None  # Reset cleared this

    def test_fluent_interface_with_build(self):
        """Test complete fluent interface workflow."""
        builder = MessagesBuilder()

        # Test list request workflow
        list_request = builder.page(1).limit(10).build_list_request()
        assert list_request.query_params.page == 1
        assert list_request.query_params.limit == 10

        # Test get request workflow (after reset)
        get_request = builder.reset().message_id("abc123").build_get_request()
        assert get_request.message_id == "abc123"

    def test_query_params_to_dict(self):
        """Test that built query params can be converted to dict."""
        builder = MessagesBuilder()
        request = builder.page(2).limit(50).build_list_request()

        params = request.to_query_params()
        expected = {"page": 2, "limit": 50}
        assert params == expected
