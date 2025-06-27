from typing import List, Optional, Dict, Any
from pydantic import Field, field_validator

from .base import BaseModel as MailerSendBaseModel


class TemplatesListRequest(MailerSendBaseModel):
    """Request model for listing templates."""
    
    domain_id: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = 25
    
    @field_validator('limit')
    def validate_limit(cls, v):
        """Validate limit is within acceptable range."""
        if v is not None and (v < 10 or v > 100):
            raise ValueError("Limit must be between 10 and 100")
        return v
    
    @field_validator('page')
    def validate_page(cls, v):
        """Validate page is positive."""
        if v is not None and v < 1:
            raise ValueError("Page must be greater than 0")
        return v
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Domain ID cannot be empty")
        return v.strip() if v else v


class TemplateGetRequest(MailerSendBaseModel):
    """Request model for getting a single template."""
    
    template_id: str
    
    @field_validator('template_id')
    def validate_template_id(cls, v):
        """Validate template ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Template ID is required")
        return v.strip()


class TemplateDeleteRequest(MailerSendBaseModel):
    """Request model for deleting a template."""
    
    template_id: str
    
    @field_validator('template_id')
    def validate_template_id(cls, v):
        """Validate template ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Template ID is required")
        return v.strip()


class TemplateCategory(MailerSendBaseModel):
    """Model representing a template category."""
    
    id: str
    name: str


class TemplateDomain(MailerSendBaseModel):
    """Model representing a template domain."""
    
    id: str
    name: str
    domain_settings: Optional[Dict[str, Any]] = None
    totals: Optional[Dict[str, int]] = None


class TemplatePersonalization(MailerSendBaseModel):
    """Model representing template personalization data."""
    
    name: Optional[str] = None
    elements: Optional[List[Dict[str, str]]] = None
    license_key: Optional[str] = None
    account_name: Optional[str] = None
    product_name: Optional[str] = None
    renew_button: Optional[str] = None
    expiration_date: Optional[str] = None


class TemplateStats(MailerSendBaseModel):
    """Model representing template statistics."""
    
    total: int = 0
    queued: int = 0
    sent: int = 0
    rejected: int = 0
    delivered: int = 0
    last_email_sent_at: Optional[str] = None


class Template(MailerSendBaseModel):
    """Model representing a template."""
    
    id: str
    name: str
    type: str
    image_path: Optional[str] = None
    personalization: Optional[TemplatePersonalization] = None
    created_at: str
    category: Optional[TemplateCategory] = None
    domain: Optional[TemplateDomain] = None
    template_stats: Optional[TemplateStats] = None


class TemplatesListResponse(MailerSendBaseModel):
    """Response model for templates list."""
    
    data: List[Template]
    links: Dict[str, Optional[str]]
    meta: Dict[str, Any]


class TemplateResponse(MailerSendBaseModel):
    """Response model for single template."""
    
    data: Template 