import pytest
from pydantic import ValidationError

from mailersend.models.templates import (
    TemplatesListRequest, TemplateGetRequest, TemplateDeleteRequest,
    TemplateCategory, TemplateDomain, TemplatePersonalization, TemplateStats,
    Template, TemplatesListResponse, TemplateResponse
)


class TestTemplatesListRequest:
    """Test TemplatesListRequest model functionality"""
    
    def test_create_minimal_request(self):
        """Test creating a minimal templates list request"""
        request = TemplatesListRequest()
        
        assert request.domain_id is None
        assert request.page is None
        assert request.limit == 25
    
    def test_create_full_request(self):
        """Test creating a full templates list request"""
        request = TemplatesListRequest(
            domain_id="domain-123",
            page=2,
            limit=50
        )
        
        assert request.domain_id == "domain-123"
        assert request.page == 2
        assert request.limit == 50
    
    def test_validate_page_positive(self):
        """Test page validation requires positive number"""
        with pytest.raises(ValidationError) as exc_info:
            TemplatesListRequest(page=0)
        
        assert "Page must be greater than 0" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            TemplatesListRequest(page=-1)
        
        assert "Page must be greater than 0" in str(exc_info.value)
    
    def test_validate_limit_range(self):
        """Test limit validation enforces 10-100 range"""
        with pytest.raises(ValidationError) as exc_info:
            TemplatesListRequest(limit=5)
        
        assert "Limit must be between 10 and 100" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            TemplatesListRequest(limit=150)
        
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_validate_domain_id_not_empty(self):
        """Test domain_id validation rejects empty strings"""
        with pytest.raises(ValidationError) as exc_info:
            TemplatesListRequest(domain_id="")
        
        assert "Domain ID cannot be empty" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            TemplatesListRequest(domain_id="   ")
        
        assert "Domain ID cannot be empty" in str(exc_info.value)
    
    def test_domain_id_strips_whitespace(self):
        """Test domain_id strips whitespace"""
        request = TemplatesListRequest(domain_id="  domain-123  ")
        
        assert request.domain_id == "domain-123"


class TestTemplateGetRequest:
    """Test TemplateGetRequest model functionality"""
    
    def test_create_request(self):
        """Test creating a template get request"""
        request = TemplateGetRequest(template_id="template-123")
        
        assert request.template_id == "template-123"
    
    def test_validate_template_id_required(self):
        """Test template_id validation requires non-empty value"""
        with pytest.raises(ValidationError) as exc_info:
            TemplateGetRequest(template_id="")
        
        assert "Template ID is required" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            TemplateGetRequest(template_id="   ")
        
        assert "Template ID is required" in str(exc_info.value)
    
    def test_template_id_strips_whitespace(self):
        """Test template_id strips whitespace"""
        request = TemplateGetRequest(template_id="  template-123  ")
        
        assert request.template_id == "template-123"


class TestTemplateDeleteRequest:
    """Test TemplateDeleteRequest model functionality"""
    
    def test_create_request(self):
        """Test creating a template delete request"""
        request = TemplateDeleteRequest(template_id="template-123")
        
        assert request.template_id == "template-123"
    
    def test_validate_template_id_required(self):
        """Test template_id validation requires non-empty value"""
        with pytest.raises(ValidationError) as exc_info:
            TemplateDeleteRequest(template_id="")
        
        assert "Template ID is required" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            TemplateDeleteRequest(template_id="   ")
        
        assert "Template ID is required" in str(exc_info.value)
    
    def test_template_id_strips_whitespace(self):
        """Test template_id strips whitespace"""
        request = TemplateDeleteRequest(template_id="  template-123  ")
        
        assert request.template_id == "template-123"


class TestTemplateCategory:
    """Test TemplateCategory model functionality"""
    
    def test_create_category(self):
        """Test creating a template category"""
        category = TemplateCategory(
            id="category-123",
            name="Newsletter Templates"
        )
        
        assert category.id == "category-123"
        assert category.name == "Newsletter Templates"


class TestTemplateDomain:
    """Test TemplateDomain model functionality"""
    
    def test_create_minimal_domain(self):
        """Test creating a minimal template domain"""
        domain = TemplateDomain(
            id="domain-123",
            name="example.com"
        )
        
        assert domain.id == "domain-123"
        assert domain.name == "example.com"
        assert domain.domain_settings is None
        assert domain.totals is None
    
    def test_create_full_domain(self):
        """Test creating a full template domain"""
        domain = TemplateDomain(
            id="domain-123",
            name="example.com",
            domain_settings={"track_opens": True},
            totals={"sent": 100, "delivered": 95}
        )
        
        assert domain.id == "domain-123"
        assert domain.name == "example.com"
        assert domain.domain_settings == {"track_opens": True}
        assert domain.totals == {"sent": 100, "delivered": 95}


class TestTemplatePersonalization:
    """Test TemplatePersonalization model functionality"""
    
    def test_create_minimal_personalization(self):
        """Test creating minimal template personalization"""
        personalization = TemplatePersonalization()
        
        assert personalization.name is None
        assert personalization.elements is None
        assert personalization.license_key is None
        assert personalization.account_name is None
        assert personalization.product_name is None
        assert personalization.renew_button is None
        assert personalization.expiration_date is None
    
    def test_create_full_personalization(self):
        """Test creating full template personalization"""
        personalization = TemplatePersonalization(
            name="John Doe",
            elements=[{"name": "Product A", "price": "$99"}],
            license_key="LICENSE-123",
            account_name="Acme Corp",
            product_name="Premium Plan",
            renew_button="Renew Now",
            expiration_date="2024-12-31"
        )
        
        assert personalization.name == "John Doe"
        assert personalization.elements == [{"name": "Product A", "price": "$99"}]
        assert personalization.license_key == "LICENSE-123"
        assert personalization.account_name == "Acme Corp"
        assert personalization.product_name == "Premium Plan"
        assert personalization.renew_button == "Renew Now"
        assert personalization.expiration_date == "2024-12-31"


class TestTemplateStats:
    """Test TemplateStats model functionality"""
    
    def test_create_default_stats(self):
        """Test creating default template stats"""
        stats = TemplateStats()
        
        assert stats.total == 0
        assert stats.queued == 0
        assert stats.sent == 0
        assert stats.rejected == 0
        assert stats.delivered == 0
        assert stats.last_email_sent_at is None
    
    def test_create_full_stats(self):
        """Test creating full template stats"""
        stats = TemplateStats(
            total=100,
            queued=5,
            sent=95,
            rejected=2,
            delivered=93,
            last_email_sent_at="2024-01-15T10:30:00Z"
        )
        
        assert stats.total == 100
        assert stats.queued == 5
        assert stats.sent == 95
        assert stats.rejected == 2
        assert stats.delivered == 93
        assert stats.last_email_sent_at == "2024-01-15T10:30:00Z"


class TestTemplate:
    """Test Template model functionality"""
    
    def test_create_minimal_template(self):
        """Test creating a minimal template"""
        template = Template(
            id="template-123",
            name="Welcome Email",
            type="html",
            created_at="2024-01-15T10:30:00Z"
        )
        
        assert template.id == "template-123"
        assert template.name == "Welcome Email"
        assert template.type == "html"
        assert template.created_at == "2024-01-15T10:30:00Z"
        assert template.image_path is None
        assert template.personalization is None
        assert template.category is None
        assert template.domain is None
        assert template.template_stats is None
    
    def test_create_full_template(self):
        """Test creating a full template"""
        category = TemplateCategory(id="cat-1", name="Marketing")
        domain = TemplateDomain(id="domain-1", name="example.com")
        personalization = TemplatePersonalization(name="John")
        stats = TemplateStats(total=50, sent=48)
        
        template = Template(
            id="template-123",
            name="Welcome Email",
            type="html",
            image_path="https://example.com/image.jpg",
            personalization=personalization,
            created_at="2024-01-15T10:30:00Z",
            category=category,
            domain=domain,
            template_stats=stats
        )
        
        assert template.id == "template-123"
        assert template.name == "Welcome Email"
        assert template.type == "html"
        assert template.image_path == "https://example.com/image.jpg"
        assert template.personalization == personalization
        assert template.created_at == "2024-01-15T10:30:00Z"
        assert template.category == category
        assert template.domain == domain
        assert template.template_stats == stats


class TestTemplatesListResponse:
    """Test TemplatesListResponse model functionality"""
    
    def test_create_response(self):
        """Test creating a templates list response"""
        template = Template(
            id="template-123",
            name="Welcome Email",
            type="html",
            created_at="2024-01-15T10:30:00Z"
        )
        
        response = TemplatesListResponse(
            data=[template],
            links={"first": "page1", "last": "page2", "prev": None, "next": "page2"},
            meta={"current_page": 1, "total": 1}
        )
        
        assert len(response.data) == 1
        assert response.data[0] == template
        assert response.links["first"] == "page1"
        assert response.meta["total"] == 1


class TestTemplateResponse:
    """Test TemplateResponse model functionality"""
    
    def test_create_response(self):
        """Test creating a template response"""
        template = Template(
            id="template-123",
            name="Welcome Email",
            type="html",
            created_at="2024-01-15T10:30:00Z"
        )
        
        response = TemplateResponse(data=template)
        
        assert response.data == template 