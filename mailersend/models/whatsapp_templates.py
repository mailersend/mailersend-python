"""WhatsApp Templates models."""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import Field, field_validator
from .base import BaseModel


class WhatsAppTemplateStatus(str, Enum):
    """WhatsApp template status options."""

    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"
    DELETED = "deleted"
    DISABLED = "disabled"
    FLAGGED = "flagged"
    IN_APPEAL = "in_appeal"
    LIMIT_EXCEEDED = "limit_exceeded"
    LOCKED = "locked"
    PAUSED = "paused"
    REINSTATED = "reinstated"
    PENDING_DELETION = "pending_deletion"


class WhatsAppTemplateCategory(str, Enum):
    """WhatsApp template category options."""

    UTILITY = "UTILITY"
    AUTHENTICATION = "AUTHENTICATION"
    MARKETING = "MARKETING"


class WhatsAppTemplatesListQueryParams(BaseModel):
    """Query parameters for listing WhatsApp templates."""

    whatsapp_account_id: Optional[str] = Field(
        None, description="WhatsApp account (sender) ID filter"
    )
    status: Optional[WhatsAppTemplateStatus] = Field(
        None, description="Template status filter"
    )
    category: Optional[WhatsAppTemplateCategory] = Field(
        None, description="Template category filter"
    )
    language: Optional[str] = Field(
        None, max_length=20, description="Template language code filter"
    )
    page: int = Field(default=1, ge=1, le=100, description="Page number")
    limit: int = Field(
        default=25, ge=1, le=100, description="Number of results per page"
    )

    @field_validator("whatsapp_account_id", "language")
    @classmethod
    def strip_filter(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from string filters."""
        if v is not None:
            return v.strip()
        return v

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict, excluding None and default values."""
        params = {}

        if self.whatsapp_account_id is not None:
            params["whatsapp_account_id"] = self.whatsapp_account_id
        if self.status is not None:
            params["status"] = self.status.value
        if self.category is not None:
            params["category"] = self.category.value
        if self.language is not None:
            params["language"] = self.language
        if self.page != 1:
            params["page"] = self.page
        if self.limit != 25:
            params["limit"] = self.limit

        return params


class WhatsAppTemplatesListRequest(BaseModel):
    """Request model for listing WhatsApp templates."""

    query_params: WhatsAppTemplatesListQueryParams = Field(
        default_factory=WhatsAppTemplatesListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()


class WhatsAppTemplateGetRequest(BaseModel):
    """Request model for getting a single WhatsApp template."""

    whatsapp_template_id: str = Field(
        ..., min_length=1, description="WhatsApp template ID"
    )

    @field_validator("whatsapp_template_id")
    @classmethod
    def validate_whatsapp_template_id(cls, v):
        """Validate WhatsApp template ID."""
        if not v or not v.strip():
            raise ValueError("WhatsApp template ID cannot be empty")
        return v.strip()
