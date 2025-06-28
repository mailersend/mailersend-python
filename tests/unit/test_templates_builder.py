"""Tests for Templates builder."""
import pytest

from mailersend.builders.templates import TemplatesBuilder  
from mailersend.models.templates import (
    TemplatesListQueryParams, TemplatesListRequest,
    TemplateGetRequest, TemplateDeleteRequest
)
from mailersend.exceptions import ValidationError


class TestTemplatesBuilder:
    """Test TemplatesBuilder functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.builder = TemplatesBuilder()
    
    def test_builder_initialization(self):
        """Test builder initializes with clean state."""
        builder = TemplatesBuilder()
        
        # Internal state should be None/empty
        assert builder._domain_id is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._template_id is None
    
    def test_domain_id_method(self):
        """Test domain_id method sets domain ID."""
        result = self.builder.domain_id("domain-123")
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._domain_id == "domain-123"
    
    def test_page_method(self):
        """Test page method sets page number."""
        result = self.builder.page(2)
        
        # Should return self for chaining  
        assert result is self.builder
        assert self.builder._page == 2
    
    def test_page_method_validates_positive(self):
        """Test page method validates positive numbers."""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.page(0)
        
        assert "Page must be greater than 0" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            self.builder.page(-1)
        
        assert "Page must be greater than 0" in str(exc_info.value)
    
    def test_limit_method(self):
        """Test limit method sets limit."""
        result = self.builder.limit(50)
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._limit == 50
    
    def test_limit_method_validates_range(self):
        """Test limit method validates 10-100 range."""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.limit(5)
        
        assert "Limit must be between 10 and 100" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            self.builder.limit(150)
        
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_template_id_method(self):
        """Test template_id method sets template ID."""
        result = self.builder.template_id("template-123")
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._template_id == "template-123"
    
    def test_template_id_method_validates_not_empty(self):
        """Test template_id method validates non-empty strings."""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.template_id("")
        
        assert "Template ID cannot be empty" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            self.builder.template_id("   ")
        
        assert "Template ID cannot be empty" in str(exc_info.value)
    
    def test_template_id_strips_whitespace(self):
        """Test template_id strips whitespace."""
        self.builder.template_id("  template-123  ")
        
        assert self.builder._template_id == "template-123"
    
    def test_all_method(self):
        """Test all method clears domain filter."""
        # Set domain ID first
        self.builder.domain_id("domain-123")
        assert self.builder._domain_id == "domain-123"
        
        # Call all() to clear it
        result = self.builder.all()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._domain_id is None
    
    def test_first_page_method(self):
        """Test first_page method sets page to 1."""
        result = self.builder.first_page()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._page == 1
    
    def test_default_limit_method(self):
        """Test default_limit method sets limit to 25."""
        result = self.builder.default_limit()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._limit == 25
    
    def test_max_limit_method(self):
        """Test max_limit method sets limit to 100."""
        result = self.builder.max_limit()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._limit == 100
    
    def test_min_limit_method(self):
        """Test min_limit method sets limit to 10."""
        result = self.builder.min_limit()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._limit == 10
    
    def test_method_chaining(self):
        """Test methods can be chained together."""
        result = (self.builder
                  .domain_id("domain-123")
                  .page(2)
                  .limit(50))
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._domain_id == "domain-123"
        assert self.builder._page == 2
        assert self.builder._limit == 50
    
    def test_build_templates_list_request_minimal(self):
        """Test building minimal templates list request."""
        request = self.builder.build_templates_list_request()
        
        assert isinstance(request, TemplatesListRequest)
        assert isinstance(request.query_params, TemplatesListQueryParams)
        # Should use defaults from query params model
        assert request.query_params.domain_id is None
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
    
    def test_build_templates_list_request_full(self):
        """Test building full templates list request."""
        request = (self.builder
                   .domain_id("domain-123")
                   .page(2)
                   .limit(50)
                   .build_templates_list_request())
        
        assert isinstance(request, TemplatesListRequest)
        assert isinstance(request.query_params, TemplatesListQueryParams)
        assert request.query_params.domain_id == "domain-123"
        assert request.query_params.page == 2
        assert request.query_params.limit == 50
    
    def test_build_templates_list_request_partial(self):
        """Test building templates list request with partial parameters."""
        request = (self.builder
                   .domain_id("domain-123")
                   .build_templates_list_request())
        
        assert isinstance(request, TemplatesListRequest)
        assert request.query_params.domain_id == "domain-123"
        # Should use defaults for unspecified values
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
    
    def test_build_templates_list_request_only_set_explicit_values(self):
        """Test builder only sets explicitly provided values in query params."""
        request = (self.builder
                   .page(3)
                   .build_templates_list_request())
        
        assert isinstance(request, TemplatesListRequest)
        assert request.query_params.domain_id is None
        assert request.query_params.page == 3
        # Should use default for limit
        assert request.query_params.limit == 25
    
    def test_build_template_get_request(self):
        """Test building template get request."""
        request = (self.builder
                   .template_id("template-123")
                   .build_template_get_request())
        
        assert isinstance(request, TemplateGetRequest)
        assert request.template_id == "template-123"
    
    def test_build_template_get_request_requires_template_id(self):
        """Test building template get request requires template_id."""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.build_template_get_request()
        
        assert "Template ID is required for get request" in str(exc_info.value)
    
    def test_build_template_delete_request(self):
        """Test building template delete request."""
        request = (self.builder
                   .template_id("template-123")
                   .build_template_delete_request())
        
        assert isinstance(request, TemplateDeleteRequest)
        assert request.template_id == "template-123"
    
    def test_build_template_delete_request_requires_template_id(self):
        """Test building template delete request requires template_id."""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.build_template_delete_request()
        
        assert "Template ID is required for delete request" in str(exc_info.value)
    
    def test_reset_method(self):
        """Test reset method clears all state."""
        # Set various values
        self.builder.domain_id("domain-123")
        self.builder.page(2)
        self.builder.limit(50)
        self.builder.template_id("template-123")
        
        # Verify state is set
        assert self.builder._domain_id == "domain-123"
        assert self.builder._page == 2
        assert self.builder._limit == 50
        assert self.builder._template_id == "template-123"
        
        # Reset
        result = self.builder.reset()
        
        # Should return self for chaining
        assert result is self.builder
        
        # All state should be cleared
        assert self.builder._domain_id is None
        assert self.builder._page is None
        assert self.builder._limit is None
        assert self.builder._template_id is None
    
    def test_copy_method(self):
        """Test copy method creates independent copy."""
        # Set up original builder
        original = (self.builder
                    .domain_id("domain-123")
                    .page(2)
                    .limit(50)
                    .template_id("template-123"))
        
        # Create copy
        copy = original.copy()
        
        # Should be different objects
        assert copy is not original
        assert isinstance(copy, TemplatesBuilder)
        
        # Should have same state
        assert copy._domain_id == "domain-123"
        assert copy._page == 2
        assert copy._limit == 50
        assert copy._template_id == "template-123"
        
        # Changes to copy should not affect original
        copy.domain_id("different-domain")
        assert original._domain_id == "domain-123"
        assert copy._domain_id == "different-domain"
    
    def test_state_isolation_between_requests(self):
        """Test builder state doesn't interfere between different request types."""
        # Set up for templates list
        self.builder.domain_id("domain-123").page(2).limit(50)
        
        # Build templates list request
        list_request = self.builder.build_templates_list_request()
        assert list_request.query_params.domain_id == "domain-123"
        assert list_request.query_params.page == 2
        assert list_request.query_params.limit == 50
        
        # Set template ID for get/delete requests
        self.builder.template_id("template-456")
        
        # Build get request
        get_request = self.builder.build_template_get_request()
        assert get_request.template_id == "template-456"
        
        # Build delete request
        delete_request = self.builder.build_template_delete_request()
        assert delete_request.template_id == "template-456"
        
        # List request should still work with previous state
        list_request2 = self.builder.build_templates_list_request()
        assert list_request2.query_params.domain_id == "domain-123"
        assert list_request2.query_params.page == 2
        assert list_request2.query_params.limit == 50
    
    def test_helper_methods_workflow(self):
        """Test using helper methods in a realistic workflow."""
        # Start with default settings
        builder = TemplatesBuilder()
        
        # Use helper methods to configure
        request = (builder
                   .first_page()
                   .max_limit()
                   .domain_id("production-domain")
                   .build_templates_list_request())
        
        assert request.query_params.page == 1
        assert request.query_params.limit == 100
        assert request.query_params.domain_id == "production-domain"
        
        # Reset and try different configuration
        request2 = (builder
                    .reset()
                    .min_limit()
                    .page(5)
                    .all()  # Clear domain filter
                    .build_templates_list_request())
        
        assert request2.query_params.page == 5
        assert request2.query_params.limit == 10
        assert request2.query_params.domain_id is None 