"""Unit tests for Recipients models."""
import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.recipients import (
    # Query Parameters Models
    RecipientsListQueryParams,
    SuppressionListQueryParams,
    # Request Models
    RecipientsListRequest,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
)


class TestRecipientsListQueryParams:
    """Test RecipientsListQueryParams model."""

    def test_default_values(self):
        """Test default values."""
        query_params = RecipientsListQueryParams()
        assert query_params.domain_id is None
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test custom values."""
        query_params = RecipientsListQueryParams(
            domain_id="test-domain",
            page=2,
            limit=50
        )
        assert query_params.domain_id == "test-domain"
        assert query_params.page == 2
        assert query_params.limit == 50

    def test_domain_id_validation(self):
        """Test domain_id validation."""
        # Test trimming
        query_params = RecipientsListQueryParams(domain_id="  test-domain  ")
        assert query_params.domain_id == "test-domain"

    def test_page_validation(self):
        """Test page validation."""
        with pytest.raises(ValidationError):
            RecipientsListQueryParams(page=0)

        with pytest.raises(ValidationError):
            RecipientsListQueryParams(page=-1)

    def test_limit_validation(self):
        """Test limit validation."""
        with pytest.raises(ValidationError):
            RecipientsListQueryParams(limit=9)

        with pytest.raises(ValidationError):
            RecipientsListQueryParams(limit=101)

    def test_to_query_params(self):
        """Test to_query_params method."""
        query_params = RecipientsListQueryParams(
            domain_id="test-domain",
            page=2,
            limit=50
        )
        result = query_params.to_query_params()
        expected = {
            "domain_id": "test-domain",
            "page": 2,
            "limit": 50
        }
        assert result == expected

    def test_to_query_params_excludes_none(self):
        """Test to_query_params excludes None values."""
        query_params = RecipientsListQueryParams(page=2, limit=30)
        result = query_params.to_query_params()
        expected = {"page": 2, "limit": 30}
        assert result == expected
        assert "domain_id" not in result


class TestSuppressionListQueryParams:
    """Test SuppressionListQueryParams model."""

    def test_default_values(self):
        """Test default values."""
        query_params = SuppressionListQueryParams()
        assert query_params.domain_id is None
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test custom values."""
        query_params = SuppressionListQueryParams(
            domain_id="test-domain",
            page=3,
            limit=75
        )
        assert query_params.domain_id == "test-domain"
        assert query_params.page == 3
        assert query_params.limit == 75

    def test_to_query_params(self):
        """Test to_query_params method."""
        query_params = SuppressionListQueryParams(
            domain_id="test-domain",
            page=3,
            limit=75
        )
        result = query_params.to_query_params()
        expected = {
            "domain_id": "test-domain",
            "page": 3,
            "limit": 75
        }
        assert result == expected


class TestRecipientsListRequest:
    """Test RecipientsListRequest model."""

    def test_default_request(self):
        """Test request with default query params."""
        request = RecipientsListRequest()
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.query_params.domain_id is None

    def test_custom_query_params(self):
        """Test request with custom query params."""
        query_params = RecipientsListQueryParams(
            domain_id="test-domain",
            page=2,
            limit=50
        )
        request = RecipientsListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params."""
        query_params = RecipientsListQueryParams(
            domain_id="test-domain",
            page=2,
            limit=50
        )
        request = RecipientsListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {
            "domain_id": "test-domain",
            "page": 2,
            "limit": 50
        }
        assert result == expected


class TestRecipientGetRequest:
    """Test RecipientGetRequest model."""

    def test_valid_request(self):
        """Test valid request."""
        request = RecipientGetRequest(recipient_id="test-recipient")
        assert request.recipient_id == "test-recipient"

    def test_recipient_id_validation(self):
        """Test recipient_id validation."""
        with pytest.raises(ValidationError, match="recipient_id cannot be empty"):
            RecipientGetRequest(recipient_id="")

        with pytest.raises(ValidationError, match="recipient_id cannot be empty"):
            RecipientGetRequest(recipient_id="   ")

    def test_recipient_id_trimming(self):
        """Test recipient_id trimming."""
        request = RecipientGetRequest(recipient_id="  test-recipient  ")
        assert request.recipient_id == "test-recipient"


class TestRecipientDeleteRequest:
    """Test RecipientDeleteRequest model."""

    def test_valid_request(self):
        """Test valid request."""
        request = RecipientDeleteRequest(recipient_id="test-recipient")
        assert request.recipient_id == "test-recipient"

    def test_recipient_id_validation(self):
        """Test recipient_id validation."""
        with pytest.raises(ValidationError, match="recipient_id cannot be empty"):
            RecipientDeleteRequest(recipient_id="")

        with pytest.raises(ValidationError, match="recipient_id cannot be empty"):
            RecipientDeleteRequest(recipient_id="   ")

    def test_recipient_id_trimming(self):
        """Test recipient_id trimming."""
        request = RecipientDeleteRequest(recipient_id="  test-recipient  ")
        assert request.recipient_id == "test-recipient"


class TestSuppressionListRequest:
    """Test SuppressionListRequest model."""

    def test_default_request(self):
        """Test request with default query params."""
        request = SuppressionListRequest()
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.query_params.domain_id is None

    def test_custom_query_params(self):
        """Test request with custom query params."""
        query_params = SuppressionListQueryParams(
            domain_id="test-domain",
            page=3,
            limit=75
        )
        request = SuppressionListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params."""
        query_params = SuppressionListQueryParams(
            domain_id="test-domain",
            page=3,
            limit=75
        )
        request = SuppressionListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {
            "domain_id": "test-domain",
            "page": 3,
            "limit": 75
        }
        assert result == expected


class TestSuppressionAddRequest:
    """Test SuppressionAddRequest model."""

    def test_valid_request_with_recipients(self):
        """Test valid request with recipients."""
        request = SuppressionAddRequest(
            domain_id="test-domain",
            recipients=["test@example.com", "test2@example.com"]
        )
        assert request.domain_id == "test-domain"
        assert request.recipients == ["test@example.com", "test2@example.com"]
        assert request.patterns is None

    def test_valid_request_with_patterns(self):
        """Test valid request with patterns."""
        request = SuppressionAddRequest(
            domain_id="test-domain",
            patterns=["@spam.com", "@blocked.net"]
        )
        assert request.domain_id == "test-domain"
        assert request.patterns == ["@spam.com", "@blocked.net"]
        assert request.recipients is None

    def test_domain_id_validation(self):
        """Test domain_id validation."""
        with pytest.raises(ValidationError, match="domain_id cannot be empty"):
            SuppressionAddRequest(domain_id="", recipients=["test@example.com"])

        with pytest.raises(ValidationError, match="domain_id cannot be empty"):
            SuppressionAddRequest(domain_id="   ", recipients=["test@example.com"])

    def test_domain_id_trimming(self):
        """Test domain_id trimming."""
        request = SuppressionAddRequest(
            domain_id="  test-domain  ",
            recipients=["test@example.com"]
        )
        assert request.domain_id == "test-domain"

    def test_recipients_validation(self):
        """Test recipients validation."""
        # Empty list
        with pytest.raises(ValidationError, match="recipients list cannot be empty if provided"):
            SuppressionAddRequest(domain_id="test-domain", recipients=[])

        # Empty recipient
        with pytest.raises(ValidationError, match="recipient email cannot be empty"):
            SuppressionAddRequest(domain_id="test-domain", recipients=["test@example.com", ""])

        # Whitespace recipient
        with pytest.raises(ValidationError, match="recipient email cannot be empty"):
            SuppressionAddRequest(domain_id="test-domain", recipients=["test@example.com", "   "])

    def test_recipients_trimming(self):
        """Test recipients trimming."""
        request = SuppressionAddRequest(
            domain_id="test-domain",
            recipients=["  test@example.com  ", "  test2@example.com  "]
        )
        assert request.recipients == ["test@example.com", "test2@example.com"]

    def test_patterns_validation(self):
        """Test patterns validation."""
        # Empty list
        with pytest.raises(ValidationError, match="patterns list cannot be empty if provided"):
            SuppressionAddRequest(domain_id="test-domain", patterns=[])

        # Empty pattern
        with pytest.raises(ValidationError, match="pattern cannot be empty"):
            SuppressionAddRequest(domain_id="test-domain", patterns=["@spam.com", ""])

        # Whitespace pattern
        with pytest.raises(ValidationError, match="pattern cannot be empty"):
            SuppressionAddRequest(domain_id="test-domain", patterns=["@spam.com", "   "])

    def test_patterns_trimming(self):
        """Test patterns trimming."""
        request = SuppressionAddRequest(
            domain_id="test-domain",
            patterns=["  @spam.com  ", "  @blocked.net  "]
        )
        assert request.patterns == ["@spam.com", "@blocked.net"]


class TestSuppressionDeleteRequest:
    """Test SuppressionDeleteRequest model."""

    def test_valid_request_with_ids(self):
        """Test valid request with ids."""
        request = SuppressionDeleteRequest(
            domain_id="test-domain",
            ids=["id1", "id2"]
        )
        assert request.domain_id == "test-domain"
        assert request.ids == ["id1", "id2"]
        assert request.all is None

    def test_valid_request_with_all(self):
        """Test valid request with all flag."""
        request = SuppressionDeleteRequest(
            domain_id="test-domain",
            all=True
        )
        assert request.domain_id == "test-domain"
        assert request.all is True
        assert request.ids is None

    def test_domain_id_trimming(self):
        """Test domain_id trimming."""
        request = SuppressionDeleteRequest(
            domain_id="  test-domain  ",
            all=True
        )
        assert request.domain_id == "test-domain"

    def test_ids_validation(self):
        """Test ids validation."""
        # Empty list
        with pytest.raises(ValidationError, match="ids list cannot be empty if provided"):
            SuppressionDeleteRequest(domain_id="test-domain", ids=[])

        # Empty id
        with pytest.raises(ValidationError, match="id cannot be empty"):
            SuppressionDeleteRequest(domain_id="test-domain", ids=["id1", ""])

        # Whitespace id
        with pytest.raises(ValidationError, match="id cannot be empty"):
            SuppressionDeleteRequest(domain_id="test-domain", ids=["id1", "   "])

    def test_ids_trimming(self):
        """Test ids trimming."""
        request = SuppressionDeleteRequest(
            domain_id="test-domain",
            ids=["  id1  ", "  id2  "]
        )
        assert request.ids == ["id1", "id2"] 