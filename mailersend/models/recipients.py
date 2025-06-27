"""Recipients API models for MailerSend SDK."""
from datetime import datetime
from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field, field_validator


# Request Models
class RecipientsListRequest(BaseModel):
    """Request model for listing recipients."""
    
    domain_id: Optional[str] = None
    page: Optional[int] = Field(default=None, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)
    
    @field_validator('domain_id')
    @classmethod
    def validate_domain_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean domain_id."""
        if v is not None:
            return v.strip()
        return v


class RecipientGetRequest(BaseModel):
    """Request model for getting a single recipient."""
    
    recipient_id: str
    
    @field_validator('recipient_id')
    @classmethod
    def validate_recipient_id(cls, v: str) -> str:
        """Validate and clean recipient_id."""
        if not v or not v.strip():
            raise ValueError("recipient_id cannot be empty")
        return v.strip()


class RecipientDeleteRequest(BaseModel):
    """Request model for deleting a recipient."""
    
    recipient_id: str
    
    @field_validator('recipient_id')
    @classmethod
    def validate_recipient_id(cls, v: str) -> str:
        """Validate and clean recipient_id."""
        if not v or not v.strip():
            raise ValueError("recipient_id cannot be empty")
        return v.strip()


class SuppressionListRequest(BaseModel):
    """Request model for listing suppression entries."""
    
    domain_id: Optional[str] = None
    page: Optional[int] = Field(default=None, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)
    
    @field_validator('domain_id')
    @classmethod
    def validate_domain_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean domain_id."""
        if v is not None:
            return v.strip()
        return v


class SuppressionAddRequest(BaseModel):
    """Request model for adding recipients to suppression lists."""
    
    domain_id: str
    recipients: Optional[List[str]] = None
    patterns: Optional[List[str]] = None
    
    @field_validator('domain_id')
    @classmethod
    def validate_domain_id(cls, v: str) -> str:
        """Validate and clean domain_id."""
        if not v or not v.strip():
            raise ValueError("domain_id cannot be empty")
        return v.strip()
    
    @field_validator('recipients')
    @classmethod
    def validate_recipients(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate recipients list."""
        if v is not None:
            if not v:
                raise ValueError("recipients list cannot be empty if provided")
            # Clean and validate each email
            cleaned = []
            for email in v:
                if not email or not email.strip():
                    raise ValueError("recipient email cannot be empty")
                cleaned.append(email.strip())
            return cleaned
        return v
    
    @field_validator('patterns')
    @classmethod
    def validate_patterns(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate patterns list."""
        if v is not None:
            if not v:
                raise ValueError("patterns list cannot be empty if provided")
            # Clean each pattern
            cleaned = []
            for pattern in v:
                if not pattern or not pattern.strip():
                    raise ValueError("pattern cannot be empty")
                cleaned.append(pattern.strip())
            return cleaned
        return v


class SuppressionDeleteRequest(BaseModel):
    """Request model for deleting from suppression lists."""
    
    domain_id: Optional[str] = None
    ids: Optional[List[str]] = None
    all: Optional[bool] = None
    
    @field_validator('domain_id')
    @classmethod
    def validate_domain_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean domain_id."""
        if v is not None:
            return v.strip()
        return v
    
    @field_validator('ids')
    @classmethod
    def validate_ids(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate ids list."""
        if v is not None:
            if not v:
                raise ValueError("ids list cannot be empty if provided")
            # Clean each id
            cleaned = []
            for id_val in v:
                if not id_val or not id_val.strip():
                    raise ValueError("id cannot be empty")
                cleaned.append(id_val.strip())
            return cleaned
        return v


# Response Models
class RecipientDomain(BaseModel):
    """Domain information for recipients."""
    
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    dkim: Optional[bool] = None
    spf: Optional[bool] = None
    mx: Optional[bool] = None
    tracking: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_cname_verified: Optional[bool] = None
    is_dns_active: Optional[bool] = None
    is_cname_active: Optional[bool] = None
    is_tracking_allowed: Optional[bool] = None
    has_not_queued_messages: Optional[bool] = None
    not_queued_messages_count: Optional[int] = None
    domain_settings: Optional[Dict[str, Any]] = None


class Recipient(BaseModel):
    """Recipient model."""
    
    id: str
    email: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[str] = None
    emails: Optional[List[Dict[str, Any]]] = None
    domain: Optional[RecipientDomain] = None


class BlocklistEntry(BaseModel):
    """Blocklist entry model."""
    
    id: str
    type: str  # "exact" or "pattern"
    pattern: str
    domain: Optional[RecipientDomain] = None
    created_at: datetime
    updated_at: datetime


class HardBounce(BaseModel):
    """Hard bounce model."""
    
    id: str
    reason: Optional[str] = None
    created_at: datetime
    recipient: Recipient


class SpamComplaint(BaseModel):
    """Spam complaint model."""
    
    id: str
    created_at: datetime
    recipient: Recipient


class Unsubscribe(BaseModel):
    """Unsubscribe model."""
    
    id: str
    reason: Optional[str] = None
    readable_reason: Optional[str] = None
    created_at: datetime
    recipient: Recipient


class OnHoldEntry(BaseModel):
    """On hold list entry model."""
    
    id: str
    created_at: datetime
    on_hold_until: datetime
    email: str
    recipient: Recipient


# Response Wrapper Models
class RecipientsListResponse(BaseModel):
    """Response model for recipients list."""
    
    data: List[Recipient]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None


class RecipientResponse(BaseModel):
    """Response model for single recipient."""
    
    data: Recipient


class BlocklistResponse(BaseModel):
    """Response model for blocklist entries."""
    
    data: List[BlocklistEntry]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None


class HardBouncesResponse(BaseModel):
    """Response model for hard bounces."""
    
    data: List[HardBounce]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None


class SpamComplaintsResponse(BaseModel):
    """Response model for spam complaints."""
    
    data: List[SpamComplaint]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None


class UnsubscribesResponse(BaseModel):
    """Response model for unsubscribes."""
    
    data: List[Unsubscribe]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None


class OnHoldResponse(BaseModel):
    """Response model for on hold entries."""
    
    data: List[OnHoldEntry]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None


class SuppressionAddResponse(BaseModel):
    """Response model for adding to suppression lists."""
    
    data: List[Union[BlocklistEntry, HardBounce, SpamComplaint, Unsubscribe]] 