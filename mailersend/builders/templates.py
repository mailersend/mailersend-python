"""Templates builder for MailerSend SDK."""
from typing import Optional
from copy import deepcopy

from ..models.templates import (
    TemplatesListRequest, TemplatesListQueryParams,
    TemplateGetRequest, TemplateDeleteRequest
)
from ..exceptions import ValidationError


class TemplatesBuilder:
    """
    Builder for creating template-related requests using a fluent interface.
    
    Supports building requests for:
    - Listing templates
    - Getting single template
    - Deleting templates
    """
    
    def __init__(self):
        """Initialize a new TemplatesBuilder."""
        self._reset()
    
    def _reset(self):
        """Reset all builder state."""
        # List templates parameters
        self._domain_id: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        
        # Template ID for get/delete operations
        self._template_id: Optional[str] = None
    
    def domain_id(self, domain_id: str) -> 'TemplatesBuilder':
        """
        Set the domain ID for filtering templates.
        
        Args:
            domain_id: Domain ID to filter by
            
        Returns:
            Self for method chaining
        """
        self._domain_id = domain_id
        return self
    
    def page(self, page: int) -> 'TemplatesBuilder':
        """
        Set the page number for pagination.
        
        Args:
            page: Page number (must be > 0)
            
        Returns:
            Self for method chaining
        """
        if page < 1:
            raise ValidationError("Page must be greater than 0")
        self._page = page
        return self
    
    def limit(self, limit: int) -> 'TemplatesBuilder':
        """
        Set the number of items per page.
        
        Args:
            limit: Items per page (10-100)
            
        Returns:
            Self for method chaining
        """
        if limit < 10 or limit > 100:
            raise ValidationError("Limit must be between 10 and 100")
        self._limit = limit
        return self
    
    def template_id(self, template_id: str) -> 'TemplatesBuilder':
        """
        Set the template ID for get/delete operations.
        
        Args:
            template_id: Template ID
            
        Returns:
            Self for method chaining
        """
        if not template_id or not template_id.strip():
            raise ValidationError("Template ID cannot be empty")
        self._template_id = template_id.strip()
        return self
    
    def all(self) -> 'TemplatesBuilder':
        """
        Configure to retrieve all templates (no filters).
        
        Returns:
            Self for method chaining
        """
        self._domain_id = None
        return self
    
    def first_page(self) -> 'TemplatesBuilder':
        """
        Set to the first page.
        
        Returns:
            Self for method chaining
        """
        return self.page(1)
    
    def default_limit(self) -> 'TemplatesBuilder':
        """
        Set to default limit (25 items per page).
        
        Returns:
            Self for method chaining
        """
        return self.limit(25)
    
    def max_limit(self) -> 'TemplatesBuilder':
        """
        Set to maximum limit (100 items per page).
        
        Returns:
            Self for method chaining
        """
        return self.limit(100)
    
    def min_limit(self) -> 'TemplatesBuilder':
        """
        Set to minimum limit (10 items per page).
        
        Returns:
            Self for method chaining
        """
        return self.limit(10)
    
    def build_templates_list_request(self) -> TemplatesListRequest:
        """
        Build a request for listing templates.
        
        Returns:
            Validated TemplatesListRequest instance
        """
        # Create query params - only set values that were explicitly provided
        query_params_dict = {}
        
        if self._domain_id is not None:
            query_params_dict["domain_id"] = self._domain_id
        if self._page is not None:
            query_params_dict["page"] = self._page
        if self._limit is not None:
            query_params_dict["limit"] = self._limit
        
        query_params = TemplatesListQueryParams(**query_params_dict)
        
        return TemplatesListRequest(query_params=query_params)
    
    def build_template_get_request(self) -> TemplateGetRequest:
        """
        Build a request for getting a single template.
        
        Returns:
            Validated TemplateGetRequest instance
            
        Raises:
            ValidationError: If template_id is not set
        """
        if not self._template_id:
            raise ValidationError("Template ID is required for get request")
        
        return TemplateGetRequest(template_id=self._template_id)
    
    def build_template_delete_request(self) -> TemplateDeleteRequest:
        """
        Build a request for deleting a template.
        
        Returns:
            Validated TemplateDeleteRequest instance
            
        Raises:
            ValidationError: If template_id is not set
        """
        if not self._template_id:
            raise ValidationError("Template ID is required for delete request")
        
        return TemplateDeleteRequest(template_id=self._template_id)
    
    def reset(self) -> 'TemplatesBuilder':
        """
        Reset the builder to initial state.
        
        Returns:
            Self for method chaining
        """
        self._reset()
        return self
    
    def copy(self) -> 'TemplatesBuilder':
        """
        Create a copy of the current builder state.
        
        Returns:
            New TemplatesBuilder instance with copied state
        """
        new_builder = TemplatesBuilder()
        new_builder._domain_id = self._domain_id
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._template_id = self._template_id
        return new_builder 