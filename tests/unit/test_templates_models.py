"""Tests for Templates models."""

import pytest
from pydantic import ValidationError

from mailersend.models.templates import (
    TemplatesListRequest,
    TemplatesListQueryParams,
    TemplateGetRequest,
    TemplateDeleteRequest,
)


class TestTemplatesListQueryParams:
    """Test TemplatesListQueryParams model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        query_params = TemplatesListQueryParams()
        assert query_params.domain_id is None
        assert query_params.page == 1
        assert query_params.limit == 25

    def test_custom_values(self):
        """Test setting custom values."""
        query_params = TemplatesListQueryParams(
            domain_id="test-domain", page=2, limit=50
        )
        assert query_params.domain_id == "test-domain"
        assert query_params.page == 2
        assert query_params.limit == 50

    def test_domain_id_validation(self):
        """Test domain_id validation and trimming."""
        query_params = TemplatesListQueryParams(domain_id="  test-domain  ")
        assert query_params.domain_id == "test-domain"

    def test_page_validation(self):
        """Test page validation (must be >= 1)."""
        with pytest.raises(ValidationError):
            TemplatesListQueryParams(page=0)

        with pytest.raises(ValidationError):
            TemplatesListQueryParams(page=-1)

    def test_limit_validation(self):
        """Test limit validation (10-100)."""
        with pytest.raises(ValidationError):
            TemplatesListQueryParams(limit=9)

        with pytest.raises(ValidationError):
            TemplatesListQueryParams(limit=101)

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = TemplatesListQueryParams()
        result = query_params.to_query_params()
        expected = {"page": 1, "limit": 25}
        assert result == expected

    def test_to_query_params_with_all_values(self):
        """Test to_query_params with all values set."""
        query_params = TemplatesListQueryParams(
            domain_id="test-domain", page=3, limit=50
        )
        result = query_params.to_query_params()
        expected = {"domain_id": "test-domain", "page": 3, "limit": 50}
        assert result == expected

    def test_to_query_params_excludes_none(self):
        """Test to_query_params excludes None values."""
        query_params = TemplatesListQueryParams(page=2, limit=30)
        result = query_params.to_query_params()
        expected = {"page": 2, "limit": 30}
        assert result == expected
        # Verify no None values are included
        assert "domain_id" not in result or result["domain_id"] is not None


class TestTemplatesListRequest:
    """Test TemplatesListRequest model."""

    def test_create_request_with_query_params(self):
        """Test creating request with query params object."""
        query_params = TemplatesListQueryParams(
            domain_id="test-domain", page=2, limit=50
        )
        request = TemplatesListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_create_request_with_defaults(self):
        """Test creating request with default query params."""
        request = TemplatesListRequest()
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.query_params.domain_id is None

    def test_to_query_params_delegation(self):
        """Test that to_query_params delegates to query_params object."""
        query_params = TemplatesListQueryParams(
            domain_id="test-domain", page=3, limit=75
        )
        request = TemplatesListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {"domain_id": "test-domain", "page": 3, "limit": 75}
        assert result == expected

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        request = TemplatesListRequest()
        result = request.to_query_params()
        expected = {"page": 1, "limit": 25}
        assert result == expected


class TestTemplateGetRequest:
    """Test TemplateGetRequest model."""

    def test_valid_template_id(self):
        """Test with valid template ID."""
        request = TemplateGetRequest(template_id="template123")
        assert request.template_id == "template123"

    def test_template_id_validation(self):
        """Test template ID validation."""
        # Empty template ID
        with pytest.raises(ValidationError, match="Template ID is required"):
            TemplateGetRequest(template_id="")

        # Whitespace-only template ID
        with pytest.raises(ValidationError, match="Template ID is required"):
            TemplateGetRequest(template_id="   ")

    def test_template_id_trimming(self):
        """Test template ID is trimmed."""
        request = TemplateGetRequest(template_id="  template123  ")
        assert request.template_id == "template123"


class TestTemplateDeleteRequest:
    """Test TemplateDeleteRequest model."""

    def test_valid_template_id(self):
        """Test with valid template ID."""
        request = TemplateDeleteRequest(template_id="template123")
        assert request.template_id == "template123"

    def test_template_id_validation(self):
        """Test template ID validation."""
        # Empty template ID
        with pytest.raises(ValidationError, match="Template ID is required"):
            TemplateDeleteRequest(template_id="")

        # Whitespace-only template ID
        with pytest.raises(ValidationError, match="Template ID is required"):
            TemplateDeleteRequest(template_id="   ")

    def test_template_id_trimming(self):
        """Test template ID is trimmed."""
        request = TemplateDeleteRequest(template_id="  template123  ")
        assert request.template_id == "template123"
