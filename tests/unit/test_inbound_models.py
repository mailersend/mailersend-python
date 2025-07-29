import pytest
from pydantic import ValidationError

from mailersend.models.inbound import (
    InboundListRequest,
    InboundListQueryParams,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
    InboundFilter,
    InboundFilterGroup,
    InboundForward,
)


class TestInboundFilter:
    """Test InboundFilter model."""

    def test_create_valid_filter(self):
        """Test creating a valid inbound filter."""
        filter_obj = InboundFilter(
            type="catch_all",
            key=None,
            comparer=None,
            value=None
        )
        assert filter_obj.type == "catch_all"
        assert filter_obj.key is None
        assert filter_obj.comparer is None
        assert filter_obj.value is None

    def test_create_filter_with_all_fields(self):
        """Test creating a filter with all fields."""
        filter_obj = InboundFilter(
            type="match_header",
            key="X-Custom-Header",
            comparer="equal",
            value="test-value"
        )
        assert filter_obj.type == "match_header"
        assert filter_obj.key == "X-Custom-Header"
        assert filter_obj.comparer == "equal"
        assert filter_obj.value == "test-value"

    def test_invalid_filter_type(self):
        """Test validation of invalid filter type."""
        with pytest.raises(ValidationError) as exc_info:
            InboundFilter(type="invalid_type")
        assert "Type must be one of" in str(exc_info.value)

    def test_invalid_comparer(self):
        """Test validation of invalid comparer."""
        with pytest.raises(ValidationError) as exc_info:
            InboundFilter(type="catch_recipient", comparer="invalid_comparer")
        assert "Comparer must be one of" in str(exc_info.value)

    def test_valid_comparers(self):
        """Test all valid comparers."""
        valid_comparers = [
            'equal', 'not-equal', 'contains', 'not-contains',
            'starts-with', 'ends-with', 'not-starts-with', 'not-ends-with'
        ]
        for comparer in valid_comparers:
            filter_obj = InboundFilter(type="catch_recipient", comparer=comparer, value="test")
            assert filter_obj.comparer == comparer

    def test_value_length_limit(self):
        """Test value length validation."""
        long_value = "x" * 192  # Exceeds 191 character limit
        with pytest.raises(ValidationError) as exc_info:
            InboundFilter(type="catch_recipient", value=long_value)
        assert "Value cannot exceed 191 characters" in str(exc_info.value)

    def test_key_length_limit(self):
        """Test key length validation."""
        long_key = "x" * 192  # Exceeds 191 character limit
        with pytest.raises(ValidationError) as exc_info:
            InboundFilter(type="match_header", key=long_key)
        assert "Key cannot exceed 191 characters" in str(exc_info.value)

    def test_value_trimming(self):
        """Test that values are trimmed."""
        filter_obj = InboundFilter(type="catch_recipient", value="  test  ")
        assert filter_obj.value == "test"

    def test_key_trimming(self):
        """Test that keys are trimmed."""
        filter_obj = InboundFilter(type="match_header", key="  header  ")
        assert filter_obj.key == "header"


class TestInboundFilterGroup:
    """Test InboundFilterGroup model."""

    def test_create_valid_filter_group(self):
        """Test creating a valid filter group."""
        group = InboundFilterGroup(type="catch_all")
        assert group.type == "catch_all"
        assert group.filters is None

    def test_create_filter_group_with_filters(self):
        """Test creating a filter group with filters."""
        filters = [{"comparer": "equal", "value": "test"}]
        group = InboundFilterGroup(type="catch_recipient", filters=filters)
        assert group.type == "catch_recipient"
        assert group.filters == filters

    def test_invalid_filter_group_type(self):
        """Test validation of invalid filter group type."""
        with pytest.raises(ValidationError) as exc_info:
            InboundFilterGroup(type="invalid_type")
        assert "Type must be one of" in str(exc_info.value)

    def test_filters_limit(self):
        """Test filters count limit."""
        filters = [{"comparer": "equal", "value": f"test{i}"} for i in range(6)]  # 6 filters, exceeds limit
        with pytest.raises(ValidationError) as exc_info:
            InboundFilterGroup(type="catch_recipient", filters=filters)
        assert "Maximum 5 filters allowed" in str(exc_info.value)


class TestInboundForward:
    """Test InboundForward model."""

    def test_create_email_forward(self):
        """Test creating an email forward."""
        forward = InboundForward(type="email", value="test@example.com")
        assert forward.type == "email"
        assert forward.value == "test@example.com"
        assert forward.id is None
        assert forward.secret is None

    def test_create_webhook_forward(self):
        """Test creating a webhook forward."""
        forward = InboundForward(
            type="webhook",
            value="https://example.com/webhook",
            secret="secret123"
        )
        assert forward.type == "webhook"
        assert forward.value == "https://example.com/webhook"
        assert forward.secret == "secret123"

    def test_invalid_forward_type(self):
        """Test validation of invalid forward type."""
        with pytest.raises(ValidationError) as exc_info:
            InboundForward(type="invalid", value="test")
        assert "Type must be either 'email' or 'webhook'" in str(exc_info.value)

    def test_empty_value(self):
        """Test validation of empty value."""
        with pytest.raises(ValidationError) as exc_info:
            InboundForward(type="email", value="")
        assert "Value is required" in str(exc_info.value)

    def test_value_length_limit(self):
        """Test value length validation."""
        long_value = "x" * 192  # Exceeds 191 character limit
        with pytest.raises(ValidationError) as exc_info:
            InboundForward(type="email", value=long_value)
        assert "Value cannot exceed 191 characters" in str(exc_info.value)

    def test_value_trimming(self):
        """Test that values are trimmed."""
        forward = InboundForward(type="email", value="  test@example.com  ")
        assert forward.value == "test@example.com"


class TestInboundDeleteRequest:
    """Test InboundDeleteRequest model."""

    def test_create_delete_request(self):
        """Test creating a delete request."""
        request = InboundDeleteRequest(inbound_id="test-id")
        assert request.inbound_id == "test-id"

    def test_validate_inbound_id_required(self):
        """Test that inbound_id is required."""
        with pytest.raises(ValidationError) as excinfo:
            InboundDeleteRequest(inbound_id="")
        assert "Inbound ID is required" in str(excinfo.value)

    def test_validate_inbound_id_trimmed(self):
        """Test that inbound_id is trimmed."""
        request = InboundDeleteRequest(inbound_id="  test-id  ")
        assert request.inbound_id == "test-id" 