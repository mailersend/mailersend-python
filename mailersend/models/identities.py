from typing import Optional, List, Any
from pydantic import field_validator

from .base import BaseModel


class IdentityListRequest(BaseModel):
    """Request model for listing sender identities."""
    
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


class IdentityCreateRequest(BaseModel):
    """Request model for creating a new sender identity."""
    
    domain_id: str
    name: str
    email: str
    reply_to_email: Optional[str] = None
    reply_to_name: Optional[str] = None
    add_note: Optional[bool] = None
    personal_note: Optional[str] = None
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()
    
    @field_validator('name')
    def validate_name(cls, v):
        """Validate name is provided and within length limits."""
        if not v or not v.strip():
            raise ValueError("Name is required")
        if len(v.strip()) > 191:
            raise ValueError("Name must be 191 characters or less")
        return v.strip()
    
    @field_validator('email')
    def validate_email(cls, v):
        """Validate email is provided and within length limits."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        if len(v.strip()) > 191:
            raise ValueError("Email must be 191 characters or less")
        # Basic email validation
        if '@' not in v.strip():
            raise ValueError("Invalid email format")
        return v.strip()
    
    @field_validator('reply_to_email')
    def validate_reply_to_email(cls, v):
        """Validate reply-to email format if provided."""
        if v is not None:
            v = v.strip()
            if v and '@' not in v:
                raise ValueError("Invalid reply-to email format")
            if len(v) > 191:
                raise ValueError("Reply-to email must be 191 characters or less")
        return v
    
    @field_validator('personal_note')
    def validate_personal_note(cls, v):
        """Validate personal note length."""
        if v is not None and len(v) > 250:
            raise ValueError("Personal note must be 250 characters or less")
        return v


class IdentityGetRequest(BaseModel):
    """Request model for getting a single identity by ID."""
    
    identity_id: str
    
    @field_validator('identity_id')
    def validate_identity_id(cls, v):
        """Validate identity ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Identity ID is required")
        return v.strip()


class IdentityGetByEmailRequest(BaseModel):
    """Request model for getting a single identity by email."""
    
    email: str
    
    @field_validator('email')
    def validate_email(cls, v):
        """Validate email is provided and has valid format."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        if '@' not in v.strip():
            raise ValueError("Invalid email format")
        return v.strip()


class IdentityUpdateRequest(BaseModel):
    """Request model for updating an identity by ID."""
    
    identity_id: str
    name: Optional[str] = None
    reply_to_email: Optional[str] = None
    reply_to_name: Optional[str] = None
    add_note: Optional[bool] = None
    personal_note: Optional[str] = None
    
    @field_validator('identity_id')
    def validate_identity_id(cls, v):
        """Validate identity ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Identity ID is required")
        return v.strip()
    
    @field_validator('name')
    def validate_name(cls, v):
        """Validate name length if provided."""
        if v is not None:
            v = v.strip()
            if len(v) > 191:
                raise ValueError("Name must be 191 characters or less")
            if not v:
                raise ValueError("Name cannot be empty")
        return v
    
    @field_validator('reply_to_email')
    def validate_reply_to_email(cls, v):
        """Validate reply-to email format if provided."""
        if v is not None:
            v = v.strip()
            if v and '@' not in v:
                raise ValueError("Invalid reply-to email format")
            if len(v) > 191:
                raise ValueError("Reply-to email must be 191 characters or less")
        return v
    
    @field_validator('personal_note')
    def validate_personal_note(cls, v):
        """Validate personal note length."""
        if v is not None and len(v) > 250:
            raise ValueError("Personal note must be 250 characters or less")
        return v


class IdentityUpdateByEmailRequest(BaseModel):
    """Request model for updating an identity by email."""
    
    email: str
    name: Optional[str] = None
    reply_to_email: Optional[str] = None
    reply_to_name: Optional[str] = None
    add_note: Optional[bool] = None
    personal_note: Optional[str] = None
    
    @field_validator('email')
    def validate_email(cls, v):
        """Validate email is provided and has valid format."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        if '@' not in v.strip():
            raise ValueError("Invalid email format")
        return v.strip()
    
    @field_validator('name')
    def validate_name(cls, v):
        """Validate name length if provided."""
        if v is not None:
            v = v.strip()
            if len(v) > 191:
                raise ValueError("Name must be 191 characters or less")
            if not v:
                raise ValueError("Name cannot be empty")
        return v
    
    @field_validator('reply_to_email')
    def validate_reply_to_email(cls, v):
        """Validate reply-to email format if provided."""
        if v is not None:
            v = v.strip()
            if v and '@' not in v:
                raise ValueError("Invalid reply-to email format")
            if len(v) > 191:
                raise ValueError("Reply-to email must be 191 characters or less")
        return v
    
    @field_validator('personal_note')
    def validate_personal_note(cls, v):
        """Validate personal note length."""
        if v is not None and len(v) > 250:
            raise ValueError("Personal note must be 250 characters or less")
        return v


class IdentityDeleteRequest(BaseModel):
    """Request model for deleting an identity by ID."""
    
    identity_id: str
    
    @field_validator('identity_id')
    def validate_identity_id(cls, v):
        """Validate identity ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Identity ID is required")
        return v.strip()


class IdentityDeleteByEmailRequest(BaseModel):
    """Request model for deleting an identity by email."""
    
    email: str
    
    @field_validator('email')
    def validate_email(cls, v):
        """Validate email is provided and has valid format."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        if '@' not in v.strip():
            raise ValueError("Invalid email format")
        return v.strip()


class IdentityDomain(BaseModel):
    """Model representing a domain associated with an identity."""
    
    id: str
    name: str
    created_at: str
    updated_at: str


class Identity(BaseModel):
    """Model representing a sender identity."""
    
    id: str
    email: str
    name: str
    reply_to_email: Optional[str] = None
    reply_to_name: Optional[str] = None
    is_verified: bool = False
    resends: int = 0
    add_note: bool = False
    personal_note: Optional[str] = None
    domain: IdentityDomain


class IdentityListResponse(BaseModel):
    """Response model for identity list."""
    
    data: List[Identity]
    links: Optional[dict] = None
    meta: Optional[dict] = None


class IdentityResponse(BaseModel):
    """Response model for single identity."""
    
    data: Identity 