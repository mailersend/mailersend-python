"""Test cases for Recipients API builder."""
import pytest

from mailersend.builders.recipients import RecipientsBuilder
from mailersend.models.recipients import (
    RecipientsListRequest,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
)


class TestRecipientsBuilder:
    """Test RecipientsBuilder class."""

    def test_init(self):
        """Test builder initialization."""
        builder = RecipientsBuilder()

        assert builder._domain_id is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._recipient_id is None
        assert builder._recipients is None
        assert builder._patterns is None
        assert builder._ids is None
        assert builder._all is None

    def test_domain_id(self):
        """Test setting domain_id."""
        builder = RecipientsBuilder()
        result = builder.domain_id("domain123")

        assert result is builder
        assert builder._domain_id == "domain123"

    def test_page(self):
        """Test setting page."""
        builder = RecipientsBuilder()
        result = builder.page(2)

        assert result is builder
        assert builder._page == 2

    def test_page_validation(self):
        """Test page validation."""
        builder = RecipientsBuilder()

        with pytest.raises(ValueError) as exc_info:
            builder.page(0)
        assert "Page must be >= 1" in str(exc_info.value)

    def test_limit(self):
        """Test setting limit."""
        builder = RecipientsBuilder()
        result = builder.limit(50)

        assert result is builder
        assert builder._limit == 50

    def test_limit_validation(self):
        """Test limit validation."""
        builder = RecipientsBuilder()

        # Test minimum limit
        with pytest.raises(ValueError) as exc_info:
            builder.limit(9)
        assert "Limit must be between 10 and 100" in str(exc_info.value)

        # Test maximum limit
        with pytest.raises(ValueError) as exc_info:
            builder.limit(101)
        assert "Limit must be between 10 and 100" in str(exc_info.value)

    def test_recipient_id(self):
        """Test setting recipient_id."""
        builder = RecipientsBuilder()
        result = builder.recipient_id("recipient123")

        assert result is builder
        assert builder._recipient_id == "recipient123"

    def test_recipients(self):
        """Test setting recipients list."""
        builder = RecipientsBuilder()
        recipients = ["test@example.com", "user@example.com"]
        result = builder.recipients(recipients)

        assert result is builder
        assert builder._recipients == recipients

    def test_add_recipient(self):
        """Test adding single recipient."""
        builder = RecipientsBuilder()
        
        # Add first recipient
        result = builder.add_recipient("test@example.com")
        assert result is builder
        assert builder._recipients == ["test@example.com"]

        # Add second recipient
        builder.add_recipient("user@example.com")
        assert builder._recipients == ["test@example.com", "user@example.com"]

    def test_patterns(self):
        """Test setting patterns list."""
        builder = RecipientsBuilder()
        patterns = [".*@example.com", ".*@test.com"]
        result = builder.patterns(patterns)

        assert result is builder
        assert builder._patterns == patterns

    def test_add_pattern(self):
        """Test adding single pattern."""
        builder = RecipientsBuilder()
        
        # Add first pattern
        result = builder.add_pattern(".*@example.com")
        assert result is builder
        assert builder._patterns == [".*@example.com"]

        # Add second pattern
        builder.add_pattern(".*@test.com")
        assert builder._patterns == [".*@example.com", ".*@test.com"]

    def test_ids(self):
        """Test setting ids list."""
        builder = RecipientsBuilder()
        ids = ["id1", "id2", "id3"]
        result = builder.ids(ids)

        assert result is builder
        assert builder._ids == ids

    def test_add_id(self):
        """Test adding single id."""
        builder = RecipientsBuilder()
        
        # Add first id
        result = builder.add_id("id1")
        assert result is builder
        assert builder._ids == ["id1"]

        # Add second id
        builder.add_id("id2")
        assert builder._ids == ["id1", "id2"]

    def test_all(self):
        """Test setting all flag."""
        builder = RecipientsBuilder()
        
        # Test setting to True
        result = builder.all(True)
        assert result is builder
        assert builder._all is True

        # Test setting to False
        builder.all(False)
        assert builder._all is False

        # Test default (True)
        builder.all()
        assert builder._all is True

    def test_build_recipients_list_request(self):
        """Test building recipients list request."""
        builder = RecipientsBuilder()

        # Test with defaults
        request = builder.build_recipients_list_request()
        assert isinstance(request, RecipientsListRequest)
        assert request.query_params.domain_id is None
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

        # Test with all parameters
        builder.domain_id("domain123").page(2).limit(50)
        request = builder.build_recipients_list_request()
        assert request.query_params.domain_id == "domain123"
        assert request.query_params.page == 2
        assert request.query_params.limit == 50

    def test_build_recipient_get_request(self):
        """Test building recipient get request."""
        builder = RecipientsBuilder()

        # Test without recipient_id
        with pytest.raises(ValueError) as exc_info:
            builder.build_recipient_get_request()
        assert "recipient_id is required for get_recipient operations" in str(exc_info.value)

        # Test with recipient_id
        builder.recipient_id("recipient123")
        request = builder.build_recipient_get_request()
        assert isinstance(request, RecipientGetRequest)
        assert request.recipient_id == "recipient123"

    def test_build_recipient_delete_request(self):
        """Test building recipient delete request."""
        builder = RecipientsBuilder()

        # Test without recipient_id
        with pytest.raises(ValueError) as exc_info:
            builder.build_recipient_delete_request()
        assert "recipient_id is required for delete_recipient operations" in str(exc_info.value)

        # Test with recipient_id
        builder.recipient_id("recipient123")
        request = builder.build_recipient_delete_request()
        assert isinstance(request, RecipientDeleteRequest)
        assert request.recipient_id == "recipient123"

    def test_build_suppression_list_request(self):
        """Test building suppression list request."""
        builder = RecipientsBuilder()

        # Test with defaults
        request = builder.build_suppression_list_request()
        assert isinstance(request, SuppressionListRequest)
        assert request.query_params.domain_id is None
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

        # Test with all parameters
        builder.domain_id("domain123").page(3).limit(75)
        request = builder.build_suppression_list_request()
        assert request.query_params.domain_id == "domain123"
        assert request.query_params.page == 3
        assert request.query_params.limit == 75

    def test_build_suppression_add_request(self):
        """Test building suppression add request."""
        builder = RecipientsBuilder()

        # Test without domain_id
        with pytest.raises(ValueError) as exc_info:
            builder.recipients(["test@example.com"]).build_suppression_add_request()
        assert "domain_id is required for suppression add operations" in str(exc_info.value)

        # Test without recipients or patterns
        builder.reset().domain_id("domain123")
        with pytest.raises(ValueError) as exc_info:
            builder.build_suppression_add_request()
        assert "Either recipients or patterns must be provided for suppression add operations" in str(exc_info.value)

        # Test with recipients only
        builder.recipients(["test@example.com"])
        request = builder.build_suppression_add_request()
        assert isinstance(request, SuppressionAddRequest)
        assert request.domain_id == "domain123"
        assert request.recipients == ["test@example.com"]
        assert request.patterns is None

        # Test with patterns only
        builder.reset().domain_id("domain123").patterns([".*@example.com"])
        request = builder.build_suppression_add_request()
        assert request.domain_id == "domain123"
        assert request.recipients is None
        assert request.patterns == [".*@example.com"]

        # Test with both
        builder.recipients(["test@example.com"])
        request = builder.build_suppression_add_request()
        assert request.domain_id == "domain123"
        assert request.recipients == ["test@example.com"]
        assert request.patterns == [".*@example.com"]

    def test_build_suppression_delete_request(self):
        """Test building suppression delete request."""
        builder = RecipientsBuilder()

        # Test without ids or all flag
        with pytest.raises(ValueError) as exc_info:
            builder.build_suppression_delete_request()
        assert "Either ids or all flag must be provided for suppression delete operations" in str(exc_info.value)

        # Test with ids only
        builder.ids(["id1", "id2"])
        request = builder.build_suppression_delete_request()
        assert isinstance(request, SuppressionDeleteRequest)
        assert request.domain_id is None
        assert request.ids == ["id1", "id2"]
        assert request.all is None

        # Test with all flag only
        builder.reset().all(True)
        request = builder.build_suppression_delete_request()
        assert request.domain_id is None
        assert request.ids is None
        assert request.all is True

        # Test with domain_id
        builder.domain_id("domain123")
        request = builder.build_suppression_delete_request()
        assert request.domain_id == "domain123"
        assert request.ids is None
        assert request.all is True

    def test_reset(self):
        """Test reset method."""
        builder = RecipientsBuilder()

        # Set some values
        builder.domain_id("domain123").page(2).limit(50).recipient_id("recipient123")
        builder.recipients(["test@example.com"]).patterns([".*@example.com"])
        builder.ids(["id1", "id2"]).all(True)

        # Reset
        result = builder.reset()
        assert result is builder

        # Check all values are reset
        assert builder._domain_id is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._recipient_id is None
        assert builder._recipients is None
        assert builder._patterns is None
        assert builder._ids is None
        assert builder._all is None

    def test_copy(self):
        """Test copy method."""
        builder = RecipientsBuilder()

        # Set some values
        builder.domain_id("domain123").page(2).limit(50).recipient_id("recipient123")
        builder.recipients(["test@example.com"]).patterns([".*@example.com"])
        builder.ids(["id1", "id2"]).all(True)

        # Create copy
        copy_builder = builder.copy()

        # Verify it's a different instance
        assert copy_builder is not builder

        # Verify all values are copied
        assert copy_builder._domain_id == "domain123"
        assert copy_builder._page == 2
        assert copy_builder._limit == 50
        assert copy_builder._recipient_id == "recipient123"
        assert copy_builder._recipients == ["test@example.com"]
        assert copy_builder._patterns == [".*@example.com"]
        assert copy_builder._ids == ["id1", "id2"]
        assert copy_builder._all is True

        # Verify lists are separate instances
        assert copy_builder._recipients is not builder._recipients
        assert copy_builder._patterns is not builder._patterns
        assert copy_builder._ids is not builder._ids

    def test_copy_with_none_values(self):
        """Test copy method with None values."""
        builder = RecipientsBuilder()

        # Don't set any values (leave as None)
        copy_builder = builder.copy()

        # Check all values are None
        assert copy_builder._domain_id is None
        assert copy_builder._page is None
        assert copy_builder._limit is None
        assert copy_builder._recipient_id is None
        assert copy_builder._recipients is None
        assert copy_builder._patterns is None
        assert copy_builder._ids is None
        assert copy_builder._all is None

    def test_method_chaining(self):
        """Test that all methods return self for chaining."""
        builder = RecipientsBuilder()

        result = (builder
                  .domain_id("domain123")
                  .page(2)
                  .limit(50)
                  .recipient_id("recipient123")
                  .recipients(["test@example.com"])
                  .add_recipient("user@example.com")
                  .patterns([".*@example.com"])
                  .add_pattern(".*@test.com")
                  .ids(["id1"])
                  .add_id("id2")
                  .all(True)
                  .reset())

        assert result is builder

    def test_build_multiple_requests(self):
        """Test building multiple requests from same builder."""
        builder = RecipientsBuilder()

        # Set common parameters
        builder.domain_id("domain123").page(1).limit(25)

        # Build list request
        list_request = builder.build_recipients_list_request()
        assert list_request.query_params.domain_id == "domain123"
        assert list_request.query_params.page == 1
        assert list_request.query_params.limit == 25

        # Build suppression list request with same parameters
        suppression_request = builder.build_suppression_list_request()
        assert suppression_request.query_params.domain_id == "domain123"
        assert suppression_request.query_params.page == 1
        assert suppression_request.query_params.limit == 25

        # Add recipient_id and build get request
        builder.recipient_id("recipient123")
        get_request = builder.build_recipient_get_request()
        assert get_request.recipient_id == "recipient123"

        # Original requests should be unchanged
        assert list_request.query_params.domain_id == "domain123"
        assert suppression_request.query_params.domain_id == "domain123" 