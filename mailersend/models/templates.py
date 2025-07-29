"""Templates API models for MailerSend SDK."""

from typing import List, Optional, Dict, Any
from pydantic import Field, field_validator

from .base import BaseModel as MailerSendBaseModel


# Query Parameters Models
class TemplatesListQueryParams(MailerSendBaseModel):
    """Query parameters for listing templates."""

    domain_id: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=25, ge=10, le=100)

    @field_validator("domain_id")
    @classmethod
    def validate_domain_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean domain_id."""
        if v is not None:
            return v.strip()
        return v

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary, excluding None values."""
        params = {}

        if self.domain_id is not None:
            params["domain_id"] = self.domain_id

        # Always include page and limit (they have defaults)
        params["page"] = self.page
        params["limit"] = self.limit

        return params


# Request Models
class TemplatesListRequest(MailerSendBaseModel):
    """Request model for listing templates."""

    query_params: TemplatesListQueryParams = Field(
        default_factory=TemplatesListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class TemplateGetRequest(MailerSendBaseModel):
    """Request model for getting a single template."""

    template_id: str

    @field_validator("template_id")
    @classmethod
    def validate_template_id(cls, v: str) -> str:
        """Validate template ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Template ID is required")
        return v.strip()


class TemplateDeleteRequest(MailerSendBaseModel):
    """Request model for deleting a template."""

    template_id: str

    @field_validator("template_id")
    @classmethod
    def validate_template_id(cls, v: str) -> str:
        """Validate template ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Template ID is required")
        return v.strip()


# Response Models
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
