import pytest

from mailersend.builders.templates import TemplatesBuilder  
from mailersend.models.templates import (
    TemplatesListRequest, TemplateGetRequest, TemplateDeleteRequest
)
from mailersend.exceptions import ValidationError


class TestTemplatesBuilder:
    """Test TemplatesBuilder functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.builder = TemplatesBuilder()
    
    def test_builder_initialization(self):
        """Test builder initializes with clean state"""
        builder = TemplatesBuilder()
        
        # Internal state should be None/empty
        assert builder._domain_id is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._template_id is None
    
    def test_domain_id_method(self):
        """Test domain_id method sets domain ID"""
        result = self.builder.domain_id("domain-123")
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._domain_id == "domain-123"
    
    def test_page_method(self):
        """Test page method sets page number"""
        result = self.builder.page(2)
        
        # Should return self for chaining  
        assert result is self.builder
        assert self.builder._page == 2
    
    def test_page_method_validates_positive(self):
        """Test page method validates positive numbers"""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.page(0)
        
        assert "Page must be greater than 0" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            self.builder.page(-1)
        
        assert "Page must be greater than 0" in str(exc_info.value)
    
    def test_limit_method(self):
        """Test limit method sets limit"""
        result = self.builder.limit(50)
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._limit == 50
    
    def test_limit_method_validates_range(self):
        """Test limit method validates 10-100 range"""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.limit(5)
        
        assert "Limit must be between 10 and 100" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            self.builder.limit(150)
        
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_template_id_method(self):
        """Test template_id method sets template ID"""
        result = self.builder.template_id("template-123")
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._template_id == "template-123"
    
    def test_template_id_method_validates_not_empty(self):
        """Test template_id method validates non-empty strings"""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.template_id("")
        
        assert "Template ID cannot be empty" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            self.builder.template_id("   ")
        
        assert "Template ID cannot be empty" in str(exc_info.value)
    
    def test_template_id_strips_whitespace(self):
        """Test template_id strips whitespace"""
        self.builder.template_id("  template-123  ")
        
        assert self.builder._template_id == "template-123"
    
    def test_all_method(self):
        """Test all method clears domain filter"""
        # Set domain ID first
        self.builder.domain_id("domain-123")
        assert self.builder._domain_id == "domain-123"
        
        # Call all() to clear it
        result = self.builder.all()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._domain_id is None
    
    def test_first_page_method(self):
        """Test first_page method sets page to 1"""
        result = self.builder.first_page()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._page == 1
    
    def test_default_limit_method(self):
        """Test default_limit method sets limit to 25"""
        result = self.builder.default_limit()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._limit == 25
    
    def test_max_limit_method(self):
        """Test max_limit method sets limit to 100"""
        result = self.builder.max_limit()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._limit == 100
    
    def test_min_limit_method(self):
        """Test min_limit method sets limit to 10"""
        result = self.builder.min_limit()
        
        # Should return self for chaining
        assert result is self.builder
        assert self.builder._limit == 10
    
    def test_method_chaining(self):
        """Test methods can be chained together"""
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
        """Test building minimal templates list request"""
        request = self.builder.build_templates_list_request()
        
        assert isinstance(request, TemplatesListRequest)
        assert request.domain_id is None
        assert request.page is None
        assert request.limit is None  # Builder passes None, resource handles default
    
    def test_build_templates_list_request_full(self):
        """Test building full templates list request"""
        request = (self.builder
                   .domain_id("domain-123")
                   .page(2)
                   .limit(50)
                   .build_templates_list_request())
        
        assert isinstance(request, TemplatesListRequest)
        assert request.domain_id == "domain-123"
        assert request.page == 2
        assert request.limit == 50
    
    def test_build_template_get_request(self):
        """Test building template get request"""
        request = (self.builder
                   .template_id("template-123")
                   .build_template_get_request())
        
        assert isinstance(request, TemplateGetRequest)
        assert request.template_id == "template-123"
    
    def test_build_template_get_request_requires_template_id(self):
        """Test building template get request requires template_id"""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.build_template_get_request()
        
        assert "Template ID is required for get request" in str(exc_info.value)
    
    def test_build_template_delete_request(self):
        """Test building template delete request"""
        request = (self.builder
                   .template_id("template-123")
                   .build_template_delete_request())
        
        assert isinstance(request, TemplateDeleteRequest)
        assert request.template_id == "template-123"
    
    def test_build_template_delete_request_requires_template_id(self):
        """Test building template delete request requires template_id"""
        with pytest.raises(ValidationError) as exc_info:
            self.builder.build_template_delete_request()
        
        assert "Template ID is required for delete request" in str(exc_info.value)
    
    def test_reset_method(self):
        """Test reset method clears all state"""
        # Set all fields
        (self.builder
         .domain_id("domain-123")
         .page(2)
         .limit(50)
         .template_id("template-123"))
        
        # Verify fields are set
        assert self.builder._domain_id == "domain-123"
        assert self.builder._page == 2
        assert self.builder._limit == 50
        assert self.builder._template_id == "template-123"
        
        # Reset builder
        result = self.builder.reset()
        
        # Should return self for chaining
        assert result is self.builder
        
        # All fields should be reset
        assert self.builder._domain_id is None
        assert self.builder._page is None
        assert self.builder._limit is None
        assert self.builder._template_id is None
    
    def test_copy_method(self):
        """Test copy method creates builder with same state"""
        # Set up original builder
        (self.builder
         .domain_id("domain-123")
         .page(2)
         .limit(50)
         .template_id("template-123"))
        
        # Create copy
        copy_builder = self.builder.copy()
        
        # Should be different instances
        assert copy_builder is not self.builder
        
        # Should have same state
        assert copy_builder._domain_id == "domain-123"
        assert copy_builder._page == 2
        assert copy_builder._limit == 50
        assert copy_builder._template_id == "template-123"
        
        # Modifying copy should not affect original
        copy_builder.domain_id("different-domain")
        assert self.builder._domain_id == "domain-123"
        assert copy_builder._domain_id == "different-domain"
    
    def test_state_isolation_between_requests(self):
        """Test builder state isolation between different request types"""
        # Set up builder for list request
        self.builder.reset()
        list_request = (self.builder
                        .domain_id("domain-123")
                        .page(1)
                        .limit(25)
                        .build_templates_list_request())
        
        # Now set template_id for get request (should not affect list request)
        get_request = (self.builder
                       .template_id("template-456")
                       .build_template_get_request())
        
        # List request should be unaffected
        assert list_request.domain_id == "domain-123"
        assert list_request.page == 1
        assert list_request.limit == 25
        
        # Get request should work
        assert get_request.template_id == "template-456"
    
    def test_helper_methods_workflow(self):
        """Test realistic workflow using helper methods"""
        # Start with first page, max limit, all templates
        list_request = (self.builder
                        .all()
                        .first_page()
                        .max_limit()
                        .build_templates_list_request())
        
        assert list_request.domain_id is None
        assert list_request.page == 1
        assert list_request.limit == 100
        
        # Reset and try specific domain with min limit
        domain_request = (self.builder
                          .reset()
                          .domain_id("my-domain")
                          .min_limit()
                          .build_templates_list_request())
        
        assert domain_request.domain_id == "my-domain"
        assert domain_request.page is None
        assert domain_request.limit == 10 