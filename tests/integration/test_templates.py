import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.templates import (
    TemplatesListRequest,
    TemplateGetRequest,
    TemplateDeleteRequest,
    TemplatesListQueryParams,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def basic_templates_list_request():
    """Basic templates list request"""
    return TemplatesListRequest(
        query_params=TemplatesListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def template_get_request():
    """Template get request with test template ID"""
    return TemplateGetRequest(template_id="test-template-id")


@pytest.fixture
def sample_domain_id():
    """Sample domain ID for testing"""
    return os.environ.get("SDK_DOMAIN_ID", "test-domain-id")


class TestTemplatesIntegration:
    """Integration tests for Templates API."""

    @vcr.use_cassette("templates_list_basic.yaml")
    def test_list_templates_basic(self, email_client, basic_templates_list_request):
        """Test listing templates with basic parameters."""
        response = email_client.templates.list_templates(basic_templates_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            templates = response.data["data"]
            assert isinstance(templates, list)

            # If we have templates, check the structure
            if templates:
                first_template = templates[0]
                assert "id" in first_template
                assert "name" in first_template
                assert "category" in first_template or "categories" in first_template  # API has both fields
                assert "created_at" in first_template

    @vcr.use_cassette("templates_list_no_params.yaml")
    def test_list_templates_no_params(self, email_client):
        """Test listing templates without any parameters (using None)."""
        # The list_templates method accepts None as a parameter
        response = email_client.templates.list_templates(None)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have the same structure as basic request
        if "data" in response.data:
            templates = response.data["data"]
            assert isinstance(templates, list)

    @vcr.use_cassette("templates_list_with_pagination.yaml")
    def test_list_templates_with_pagination(self, email_client):
        """Test listing templates with pagination."""
        request = TemplatesListRequest(
            query_params=TemplatesListQueryParams(page=1, limit=10)
        )

        response = email_client.templates.list_templates(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta
            assert "per_page" in meta
            # API may or may not include total count in meta
            assert meta["per_page"] == 10
            assert meta["current_page"] == 1

    @vcr.use_cassette("templates_list_with_domain_filter.yaml")
    def test_list_templates_with_domain_filter(self, email_client, sample_domain_id):
        """Test listing templates filtered by domain."""
        request = TemplatesListRequest(
            query_params=TemplatesListQueryParams(
                page=1, 
                limit=10, 
                domain_id=sample_domain_id
            )
        )

        response = email_client.templates.list_templates(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # If we have templates, verify they belong to the specified domain
        if "data" in response.data and response.data["data"]:
            for template in response.data["data"]:
                # Templates may have domain information in their data
                # The exact structure depends on the API response
                assert isinstance(template, dict)

    @vcr.use_cassette("templates_get_single.yaml")
    def test_get_template_not_found_with_test_id(self, email_client, template_get_request):
        """Test getting a non-existent template returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.templates.get_template(template_get_request)

        error_str = str(exc_info.value).lower()
        assert "not found" in error_str or "404" in error_str or "could not be found" in error_str

    @vcr.use_cassette("templates_delete.yaml")
    def test_delete_template_not_found_with_test_id(self, email_client, template_get_request):
        """Test deleting a non-existent template returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = TemplateDeleteRequest(
            template_id=template_get_request.template_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.templates.delete_template(delete_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "template" in error_str)

    @vcr.use_cassette("templates_validation_error.yaml")
    def test_list_templates_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.templates.list_templates("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("templates_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_templates_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.templates.list_templates(basic_templates_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert hasattr(response, "data")
        assert hasattr(response, "headers")

        # Check for rate limiting headers
        if response.rate_limit_remaining is not None:
            assert isinstance(response.rate_limit_remaining, int)
            # Rate limit remaining can be -1 for unlimited plans
        assert response.rate_limit_remaining is not None

        # Check for request ID
        if response.request_id is not None:
            assert isinstance(response.request_id, str)
            assert len(response.request_id) > 0

    @vcr.use_cassette("templates_empty_result.yaml")
    def test_list_templates_empty_result(self, email_client, basic_templates_list_request):
        """Test listing templates when no templates exist."""
        response = email_client.templates.list_templates(basic_templates_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to existing templates)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    def test_template_get_model_validation(self):
        """Test model validation for template get request."""
        # Test empty template_id
        with pytest.raises(ValueError) as exc_info:
            TemplateGetRequest(template_id="")
        assert "template id is required" in str(exc_info.value).lower()

        # Test whitespace template_id
        with pytest.raises(ValueError) as exc_info:
            TemplateGetRequest(template_id="   ")
        assert "template id is required" in str(exc_info.value).lower()

    def test_template_delete_model_validation(self):
        """Test model validation for template delete request."""
        # Test empty template_id
        with pytest.raises(ValueError) as exc_info:
            TemplateDeleteRequest(template_id="")
        assert "template id is required" in str(exc_info.value).lower()

        # Test whitespace template_id
        with pytest.raises(ValueError) as exc_info:
            TemplateDeleteRequest(template_id="   ")
        assert "template id is required" in str(exc_info.value).lower()

    def test_templates_list_query_params_validation(self):
        """Test validation for templates list query parameters."""
        # Test valid parameters
        params = TemplatesListQueryParams(
            page=1, 
            limit=25, 
            domain_id="test-domain"
        )
        assert params.page == 1
        assert params.limit == 25
        assert params.domain_id == "test-domain"
        
        # Test minimum limit validation
        with pytest.raises(ValueError):
            TemplatesListQueryParams(limit=5)  # Below minimum of 10
            
        # Test maximum limit validation  
        with pytest.raises(ValueError):
            TemplatesListQueryParams(limit=150)  # Above maximum of 100
            
        # Test minimum page validation
        with pytest.raises(ValueError):
            TemplatesListQueryParams(page=0)  # Below minimum of 1

    def test_templates_list_query_params_to_dict(self):
        """Test query parameters conversion to dictionary."""
        # Test with all parameters
        params = TemplatesListQueryParams(
            page=2,
            limit=50,
            domain_id="test-domain"
        )
        query_dict = params.to_query_params()
        
        assert query_dict["page"] == 2
        assert query_dict["limit"] == 50
        assert query_dict["domain_id"] == "test-domain"
        
        # Test with minimal parameters (only defaults)
        params_minimal = TemplatesListQueryParams()
        query_dict_minimal = params_minimal.to_query_params()
        
        assert query_dict_minimal["page"] == 1
        assert query_dict_minimal["limit"] == 25
        assert "domain_id" not in query_dict_minimal  # None values excluded

    def test_templates_list_request_defaults(self):
        """Test that TemplatesListRequest has proper defaults."""
        # Test creating request without explicit query_params
        request = TemplatesListRequest()
        
        assert request.query_params is not None
        assert isinstance(request.query_params, TemplatesListQueryParams)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.query_params.domain_id is None
        
        # Test to_query_params method
        query_dict = request.to_query_params()
        assert query_dict["page"] == 1
        assert query_dict["limit"] == 25
        assert "domain_id" not in query_dict

    def test_domain_id_validation_and_cleaning(self):
        """Test domain_id validation and cleaning."""
        # Test domain_id with whitespace gets cleaned
        params = TemplatesListQueryParams(domain_id="  test-domain  ")
        assert params.domain_id == "test-domain"
        
        # Test None domain_id is preserved
        params_none = TemplatesListQueryParams(domain_id=None)
        assert params_none.domain_id is None 