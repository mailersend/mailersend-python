from typing import Optional, List, Any
from pydantic import field_validator, Field

from .base import BaseModel


class IdentityListQueryParams(BaseModel):
    """Model for identity list query parameters with validation."""

    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)
    domain_id: Optional[str] = None

    def to_query_params(self) -> dict:
        """Convert to query parameters for API request."""
        params = {"page": self.page, "limit": self.limit, "domain_id": self.domain_id}

        return {k: v for k, v in params.items() if v is not None}


class IdentityListRequest(BaseModel):
    """Request model for listing sender identities."""

    query_params: IdentityListQueryParams

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class IdentityCreateRequest(BaseModel):
    """Request model for creating a new sender identity."""

    domain_id: str
    name: str
    email: str
    reply_to_email: Optional[str] = None
    reply_to_name: Optional[str] = None
    add_note: Optional[bool] = None
    personal_note: Optional[str] = None

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()

    @field_validator("name")
    def validate_name(cls, v):
        """Validate name is provided and within length limits."""
        if not v or not v.strip():
            raise ValueError("Name is required")
        if len(v.strip()) > 191:
            raise ValueError("Name must be 191 characters or less")
        return v.strip()

    @field_validator("email")
    def validate_email(cls, v):
        """Validate email is provided and within length limits."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        if len(v.strip()) > 191:
            raise ValueError("Email must be 191 characters or less")
        # Basic email validation
        if "@" not in v.strip():
            raise ValueError("Invalid email format")
        return v.strip()

    @field_validator("reply_to_email")
    def validate_reply_to_email(cls, v):
        """Validate reply-to email format if provided."""
        if v is not None:
            v = v.strip()
            if v and "@" not in v:
                raise ValueError("Invalid reply-to email format")
            if len(v) > 191:
                raise ValueError("Reply-to email must be 191 characters or less")
        return v

    @field_validator("personal_note")
    def validate_personal_note(cls, v):
        """Validate personal note length."""
        if v is not None and len(v) > 250:
            raise ValueError("Personal note must be 250 characters or less")
        return v


class IdentityGetRequest(BaseModel):
    """Request model for getting a single identity by ID."""

    identity_id: str

    @field_validator("identity_id")
    def validate_identity_id(cls, v):
        """Validate identity ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Identity ID is required")
        return v.strip()


class IdentityGetByEmailRequest(BaseModel):
    """Request model for getting a single identity by email."""

    email: str

    @field_validator("email")
    def validate_email(cls, v):
        """Validate email is provided and has valid format."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        if "@" not in v.strip():
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

    @field_validator("identity_id")
    def validate_identity_id(cls, v):
        """Validate identity ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Identity ID is required")
        return v.strip()

    @field_validator("name")
    def validate_name(cls, v):
        """Validate name length if provided."""
        if v is not None:
            v = v.strip()
            if len(v) > 191:
                raise ValueError("Name must be 191 characters or less")
            if not v:
                raise ValueError("Name cannot be empty")
        return v

    @field_validator("reply_to_email")
    def validate_reply_to_email(cls, v):
        """Validate reply-to email format if provided."""
        if v is not None:
            v = v.strip()
            if v and "@" not in v:
                raise ValueError("Invalid reply-to email format")
            if len(v) > 191:
                raise ValueError("Reply-to email must be 191 characters or less")
        return v

    @field_validator("personal_note")
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

    @field_validator("email")
    def validate_email(cls, v):
        """Validate email is provided and has valid format."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        if "@" not in v.strip():
            raise ValueError("Invalid email format")
        return v.strip()

    @field_validator("name")
    def validate_name(cls, v):
        """Validate name length if provided."""
        if v is not None:
            v = v.strip()
            if len(v) > 191:
                raise ValueError("Name must be 191 characters or less")
            if not v:
                raise ValueError("Name cannot be empty")
        return v

    @field_validator("reply_to_email")
    def validate_reply_to_email(cls, v):
        """Validate reply-to email format if provided."""
        if v is not None:
            v = v.strip()
            if v and "@" not in v:
                raise ValueError("Invalid reply-to email format")
            if len(v) > 191:
                raise ValueError("Reply-to email must be 191 characters or less")
        return v

    @field_validator("personal_note")
    def validate_personal_note(cls, v):
        """Validate personal note length."""
        if v is not None and len(v) > 250:
            raise ValueError("Personal note must be 250 characters or less")
        return v


class IdentityDeleteRequest(BaseModel):
    """Request model for deleting an identity by ID."""

    identity_id: str

    @field_validator("identity_id")
    def validate_identity_id(cls, v):
        """Validate identity ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Identity ID is required")
        return v.strip()


class IdentityDeleteByEmailRequest(BaseModel):
    """Request model for deleting an identity by email."""

    email: str

    @field_validator("email")
    def validate_email(cls, v):
        """Validate email is provided and has valid format."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        if "@" not in v.strip():
            raise ValueError("Invalid email format")
        return v.strip()



