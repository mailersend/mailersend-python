import pytest
from pydantic import ValidationError

from mailersend.models.messages import (
    MessagesListRequest,
    MessagesListQueryParams,
    MessageGetRequest,
)


class TestMessagesListQueryParams:
    """Test MessagesListQueryParams model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        query_params = MessagesListQueryParams()
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test setting custom values."""
        query_params = MessagesListQueryParams(page=2, limit=50)
        assert query_params.page == 2
        assert query_params.limit == 50

    def test_page_validation(self):
        """Test page validation (must be >= 1)."""
        with pytest.raises(ValidationError):
            MessagesListQueryParams(page=0)

        with pytest.raises(ValidationError):
            MessagesListQueryParams(page=-1)

    def test_limit_validation(self):
        """Test limit validation (10-100)."""
        with pytest.raises(ValidationError):
            MessagesListQueryParams(limit=9)

        with pytest.raises(ValidationError):
            MessagesListQueryParams(limit=101)

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = MessagesListQueryParams()
        result = query_params.to_query_params()
        expected = {"page": 1, "limit": 25}
        assert result == expected

    def test_to_query_params_with_custom_values(self):
        """Test to_query_params with custom values."""
        query_params = MessagesListQueryParams(page=3, limit=50)
        result = query_params.to_query_params()
        expected = {"page": 3, "limit": 50}
        assert result == expected

    def test_to_query_params_excludes_none(self):
        """Test to_query_params excludes None values."""
        query_params = MessagesListQueryParams(page=2, limit=30)
        result = query_params.to_query_params()
        expected = {"page": 2, "limit": 30}
        assert result == expected
        # Verify no None values are included
        for key, value in result.items():
            assert value is not None


class TestMessagesListRequest:
    """Test MessagesListRequest model."""

    def test_create_request_with_query_params(self):
        """Test creating request with query params object."""
        query_params = MessagesListQueryParams(page=2, limit=50)
        request = MessagesListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_create_request_with_defaults(self):
        """Test creating request with default query params."""
        query_params = MessagesListQueryParams()
        request = MessagesListRequest(query_params=query_params)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params object."""
        query_params = MessagesListQueryParams(page=3, limit=75)
        request = MessagesListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {"page": 3, "limit": 75}
        assert result == expected

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = MessagesListQueryParams()
        request = MessagesListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {"page": 1, "limit": 25}
        assert result == expected

    def test_serialization(self):
        """Test model serialization."""
        query_params = MessagesListQueryParams(page=2, limit=40)
        request = MessagesListRequest(query_params=query_params)
        data = request.model_dump()
        assert "query_params" in data
        assert data["query_params"]["page"] == 2
        assert data["query_params"]["limit"] == 40


class TestMessageGetRequest:
    """Test MessageGetRequest model."""

    def test_valid_message_id(self):
        """Test with valid message ID."""
        request = MessageGetRequest(message_id="message123")
        assert request.message_id == "message123"

    def test_message_id_validation(self):
        """Test message ID validation."""
        # Empty message ID
        with pytest.raises(ValidationError, match="Message ID is required"):
            MessageGetRequest(message_id="")

        # Whitespace-only message ID
        with pytest.raises(ValidationError, match="Message ID is required"):
            MessageGetRequest(message_id="   ")

    def test_message_id_trimming(self):
        """Test message ID is trimmed."""
        request = MessageGetRequest(message_id="  message123  ")
        assert request.message_id == "message123"

    def test_serialization(self):
        """Test model serialization."""
        request = MessageGetRequest(message_id="message123")
        data = request.model_dump()
        assert data == {"message_id": "message123"}
