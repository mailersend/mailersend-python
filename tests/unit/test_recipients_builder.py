"""Unit tests for RecipientsBuilder."""
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
    """Test RecipientsBuilder."""

    def test_init(self):
        """Test builder initialization."""
        builder = RecipientsBuilder()
        
        assert builder._domain_id is None
        assert builder._page is None
        assert builder._limit == 25
        assert builder._recipient_id is None
        assert builder._recipients is None
        assert builder._patterns is None
        assert builder._ids is None
        assert builder._all is None

    def test_domain_id(self):
        """Test domain_id method."""
        builder = RecipientsBuilder()
        result = builder.domain_id("domain123")
        
        assert result is builder  # fluent interface
        assert builder._domain_id == "domain123"

    def test_page(self):
        """Test page method."""
        builder = RecipientsBuilder()
        result = builder.page(5)
        
        assert result is builder
        assert builder._page == 5

    def test_page_validation(self):
        """Test page validation."""
        builder = RecipientsBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.page(0)
        assert "Page must be >= 1" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            builder.page(-1)
        assert "Page must be >= 1" in str(exc_info.value)

    def test_limit(self):
        """Test limit method."""
        builder = RecipientsBuilder()
        result = builder.limit(50)
        
        assert result is builder
        assert builder._limit == 50

    def test_limit_validation(self):
        """Test limit validation."""
        builder = RecipientsBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.limit(5)
        assert "Limit must be between 10 and 100" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            builder.limit(150)
        assert "Limit must be between 10 and 100" in str(exc_info.value)

    def test_recipient_id(self):
        """Test recipient_id method."""
        builder = RecipientsBuilder()
        result = builder.recipient_id("recipient123")
        
        assert result is builder
        assert builder._recipient_id == "recipient123"

    def test_recipients(self):
        """Test recipients method."""
        builder = RecipientsBuilder()
        recipients = ["test@example.com", "user@example.com"]
        result = builder.recipients(recipients)
        
        assert result is builder
        assert builder._recipients == recipients

    def test_add_recipient(self):
        """Test add_recipient method."""
        builder = RecipientsBuilder()
        
        # First recipient
        result = builder.add_recipient("test@example.com")
        assert result is builder
        assert builder._recipients == ["test@example.com"]
        
        # Second recipient
        builder.add_recipient("user@example.com")
        assert builder._recipients == ["test@example.com", "user@example.com"]

    def test_patterns(self):
        """Test patterns method."""
        builder = RecipientsBuilder()
        patterns = [".*@example.com", ".*@test.com"]
        result = builder.patterns(patterns)
        
        assert result is builder
        assert builder._patterns == patterns

    def test_add_pattern(self):
        """Test add_pattern method."""
        builder = RecipientsBuilder()
        
        # First pattern
        result = builder.add_pattern(".*@example.com")
        assert result is builder
        assert builder._patterns == [".*@example.com"]
        
        # Second pattern
        builder.add_pattern(".*@test.com")
        assert builder._patterns == [".*@example.com", ".*@test.com"]

    def test_ids(self):
        """Test ids method."""
        builder = RecipientsBuilder()
        ids = ["id1", "id2", "id3"]
        result = builder.ids(ids)
        
        assert result is builder
        assert builder._ids == ids

    def test_add_id(self):
        """Test add_id method."""
        builder = RecipientsBuilder()
        
        # First ID
        result = builder.add_id("id1")
        assert result is builder
        assert builder._ids == ["id1"]
        
        # Second ID
        builder.add_id("id2")
        assert builder._ids == ["id1", "id2"]

    def test_all(self):
        """Test all method."""
        builder = RecipientsBuilder()
        
        # Default True
        result = builder.all()
        assert result is builder
        assert builder._all is True
        
        # Explicit False
        builder.all(False)
        assert builder._all is False

    def test_build_recipients_list_request(self):
        """Test building recipients list request."""
        builder = RecipientsBuilder()
        
        # Test with defaults
        request = builder.build_recipients_list_request()
        assert isinstance(request, RecipientsListRequest)
        assert request.domain_id is None
        assert request.page is None
        assert request.limit == 25
        
        # Test with all parameters
        request = (
            builder
            .domain_id("domain123")
            .page(2)
            .limit(50)
            .build_recipients_list_request()
        )
        assert request.domain_id == "domain123"
        assert request.page == 2
        assert request.limit == 50

    def test_build_recipient_get_request(self):
        """Test building recipient get request."""
        builder = RecipientsBuilder()
        
        # Test without recipient_id
        with pytest.raises(ValueError) as exc_info:
            builder.build_recipient_get_request()
        assert "recipient_id must be set for get request" in str(exc_info.value)
        
        # Test with recipient_id
        request = builder.recipient_id("recipient123").build_recipient_get_request()
        assert isinstance(request, RecipientGetRequest)
        assert request.recipient_id == "recipient123"

    def test_build_recipient_delete_request(self):
        """Test building recipient delete request."""
        builder = RecipientsBuilder()
        
        # Test without recipient_id
        with pytest.raises(ValueError) as exc_info:
            builder.build_recipient_delete_request()
        assert "recipient_id must be set for delete request" in str(exc_info.value)
        
        # Test with recipient_id
        request = builder.recipient_id("recipient123").build_recipient_delete_request()
        assert isinstance(request, RecipientDeleteRequest)
        assert request.recipient_id == "recipient123"

    def test_build_suppression_list_request(self):
        """Test building suppression list request."""
        builder = RecipientsBuilder()
        
        # Test with defaults
        request = builder.build_suppression_list_request()
        assert isinstance(request, SuppressionListRequest)
        assert request.domain_id is None
        assert request.page is None
        assert request.limit == 25
        
        # Test with all parameters
        request = (
            builder
            .domain_id("domain123")
            .page(3)
            .limit(75)
            .build_suppression_list_request()
        )
        assert request.domain_id == "domain123"
        assert request.page == 3
        assert request.limit == 75

    def test_build_suppression_add_request(self):
        """Test building suppression add request."""
        builder = RecipientsBuilder()
        
        # Test without domain_id
        with pytest.raises(ValueError) as exc_info:
            builder.recipients(["test@example.com"]).build_suppression_add_request()
        assert "domain_id must be set for suppression add request" in str(exc_info.value)
        
        # Test without recipients or patterns
        builder.reset()  # Reset to clear previous state
        with pytest.raises(ValueError) as exc_info:
            builder.domain_id("domain123").build_suppression_add_request()
        assert "Either recipients or patterns must be provided" in str(exc_info.value)
        
        # Test with recipients
        request = (
            builder
            .domain_id("domain123")
            .recipients(["test@example.com"])
            .build_suppression_add_request()
        )
        assert isinstance(request, SuppressionAddRequest)
        assert request.domain_id == "domain123"
        assert request.recipients == ["test@example.com"]
        assert request.patterns is None
        
        # Test with patterns
        builder.reset()
        request = (
            builder
            .domain_id("domain123")
            .patterns([".*@example.com"])
            .build_suppression_add_request()
        )
        assert request.domain_id == "domain123"
        assert request.patterns == [".*@example.com"]
        assert request.recipients is None
        
        # Test with both
        builder.reset()
        request = (
            builder
            .domain_id("domain123")
            .recipients(["test@example.com"])
            .patterns([".*@example.com"])
            .build_suppression_add_request()
        )
        assert request.recipients == ["test@example.com"]
        assert request.patterns == [".*@example.com"]

    def test_build_suppression_delete_request(self):
        """Test building suppression delete request."""
        builder = RecipientsBuilder()
        
        # Test without ids or all
        with pytest.raises(ValueError) as exc_info:
            builder.build_suppression_delete_request()
        assert "Either ids or all flag must be provided" in str(exc_info.value)
        
        # Test with ids
        request = (
            builder
            .domain_id("domain123")
            .ids(["id1", "id2"])
            .build_suppression_delete_request()
        )
        assert isinstance(request, SuppressionDeleteRequest)
        assert request.domain_id == "domain123"
        assert request.ids == ["id1", "id2"]
        assert request.all is None
        
        # Test with all flag
        builder.reset()
        request = (
            builder
            .domain_id("domain123")
            .all(True)
            .build_suppression_delete_request()
        )
        assert request.domain_id == "domain123"
        assert request.all is True
        assert request.ids is None
        
        # Test without domain_id (for on-hold)
        builder.reset()
        request = builder.ids(["id1", "id2"]).build_suppression_delete_request()
        assert request.domain_id is None
        assert request.ids == ["id1", "id2"]

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
        assert builder._limit == 25
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
        
        # Copy
        copy_builder = builder.copy()
        
        # Check it's a different instance
        assert copy_builder is not builder
        
        # Check all values are copied
        assert copy_builder._domain_id == "domain123"
        assert copy_builder._page == 2
        assert copy_builder._limit == 50
        assert copy_builder._recipient_id == "recipient123"
        assert copy_builder._recipients == ["test@example.com"]
        assert copy_builder._patterns == [".*@example.com"]
        assert copy_builder._ids == ["id1", "id2"]
        assert copy_builder._all is True
        
        # Check lists are separate instances
        assert copy_builder._recipients is not builder._recipients
        assert copy_builder._patterns is not builder._patterns
        assert copy_builder._ids is not builder._ids
        
        # Modify original and check copy is unaffected
        builder._recipients.append("new@example.com")
        assert copy_builder._recipients == ["test@example.com"]

    def test_copy_with_none_values(self):
        """Test copy method with None values."""
        builder = RecipientsBuilder()
        
        # Don't set any values (leave as None)
        copy_builder = builder.copy()
        
        # Check all values are None
        assert copy_builder._domain_id is None
        assert copy_builder._page is None
        assert copy_builder._limit == 25
        assert copy_builder._recipient_id is None
        assert copy_builder._recipients is None
        assert copy_builder._patterns is None
        assert copy_builder._ids is None
        assert copy_builder._all is None

    def test_method_chaining(self):
        """Test method chaining works correctly."""
        builder = RecipientsBuilder()
        
        # Chain multiple methods
        result = (
            builder
            .domain_id("domain123")
            .page(2)
            .limit(50)
            .recipient_id("recipient123")
            .recipients(["test@example.com"])
            .add_recipient("user@example.com")
            .patterns([".*@example.com"])
            .add_pattern(".*@test.com")
            .ids(["id1", "id2"])
            .add_id("id3")
            .all(True)
        )
        
        # Check chaining works
        assert result is builder
        
        # Check all values are set
        assert builder._domain_id == "domain123"
        assert builder._page == 2
        assert builder._limit == 50
        assert builder._recipient_id == "recipient123"
        assert builder._recipients == ["test@example.com", "user@example.com"]
        assert builder._patterns == [".*@example.com", ".*@test.com"]
        assert builder._ids == ["id1", "id2", "id3"]
        assert builder._all is True

    def test_state_independence(self):
        """Test that different builders maintain independent state."""
        builder1 = RecipientsBuilder()
        builder2 = RecipientsBuilder()
        
        # Set different values
        builder1.domain_id("domain1").page(1).limit(10)
        builder2.domain_id("domain2").page(2).limit(20)
        
        # Check independence
        assert builder1._domain_id == "domain1"
        assert builder1._page == 1
        assert builder1._limit == 10
        
        assert builder2._domain_id == "domain2"
        assert builder2._page == 2
        assert builder2._limit == 20

    def test_build_multiple_requests(self):
        """Test building multiple requests from same builder."""
        builder = RecipientsBuilder()
        
        # Set common parameters
        builder.domain_id("domain123").page(1).limit(25)
        
        # Build list request
        list_request = builder.build_recipients_list_request()
        assert list_request.domain_id == "domain123"
        assert list_request.page == 1
        assert list_request.limit == 25
        
        # Build suppression list request
        suppression_request = builder.build_suppression_list_request()
        assert suppression_request.domain_id == "domain123"
        assert suppression_request.page == 1
        assert suppression_request.limit == 25
        
        # Set recipient_id and build get request
        builder.recipient_id("recipient123")
        get_request = builder.build_recipient_get_request()
        assert get_request.recipient_id == "recipient123"
        
        # Previous requests should be unaffected
        assert list_request.domain_id == "domain123"
        assert suppression_request.domain_id == "domain123" 