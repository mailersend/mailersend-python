"""Email Verification API models for MailerSend SDK."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class EmailVerifyRequest(BaseModel):
    """Request model for single email verification."""
    
    email: str = Field(..., description="Email address to verify")
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email is not empty."""
        if not v or not v.strip():
            raise ValueError("email cannot be empty")
        return v.strip()


class EmailVerifyAsyncRequest(BaseModel):
    """Request model for async single email verification."""
    
    email: str = Field(..., description="Email address to verify asynchronously")
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email is not empty."""
        if not v or not v.strip():
            raise ValueError("email cannot be empty")
        return v.strip()


class EmailVerificationAsyncStatusRequest(BaseModel):
    """Request model for getting async email verification status."""
    
    email_verification_id: str = Field(..., description="Email verification ID")
    
    @field_validator("email_verification_id")
    @classmethod
    def validate_email_verification_id(cls, v: str) -> str:
        """Validate email_verification_id is not empty."""
        if not v or not v.strip():
            raise ValueError("email_verification_id cannot be empty")
        return v.strip()


class EmailVerificationListsRequest(BaseModel):
    """Request model for listing email verification lists."""
    
    page: Optional[int] = Field(None, ge=1, description="Page number")
    limit: Optional[int] = Field(None, ge=10, le=100, description="Items per page")
    
    @field_validator("page")
    @classmethod
    def validate_page(cls, v: Optional[int]) -> Optional[int]:
        """Validate page is positive."""
        if v is not None and v < 1:
            raise ValueError("page must be greater than 0")
        return v
    
    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: Optional[int]) -> Optional[int]:
        """Validate limit is within range."""
        if v is not None:
            if v < 10:
                raise ValueError("limit must be at least 10")
            if v > 100:
                raise ValueError("limit cannot exceed 100")
        return v


class EmailVerificationGetRequest(BaseModel):
    """Request model for getting a single email verification list."""
    
    email_verification_id: str = Field(..., description="Email verification ID")
    
    @field_validator("email_verification_id")
    @classmethod
    def validate_email_verification_id(cls, v: str) -> str:
        """Validate email_verification_id is not empty."""
        if not v or not v.strip():
            raise ValueError("email_verification_id cannot be empty")
        return v.strip()


class EmailVerificationCreateRequest(BaseModel):
    """Request model for creating an email verification list."""
    
    name: str = Field(..., description="Name of the verification list")
    emails: List[str] = Field(..., min_length=1, description="List of email addresses to verify")
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name is not empty."""
        if not v or not v.strip():
            raise ValueError("name cannot be empty")
        return v.strip()
    
    @field_validator("emails")
    @classmethod
    def validate_emails(cls, v: List[str]) -> List[str]:
        """Validate emails list is not empty and all emails are valid."""
        if not v:
            raise ValueError("emails list cannot be empty")
        
        validated_emails = []
        for email in v:
            if not email or not email.strip():
                raise ValueError("email addresses cannot be empty")
            if len(email.strip()) > 191:
                raise ValueError("email addresses cannot exceed 191 characters")
            validated_emails.append(email.strip())
        
        return validated_emails


class EmailVerificationVerifyRequest(BaseModel):
    """Request model for verifying an email verification list."""
    
    email_verification_id: str = Field(..., description="Email verification ID")
    
    @field_validator("email_verification_id")
    @classmethod
    def validate_email_verification_id(cls, v: str) -> str:
        """Validate email_verification_id is not empty."""
        if not v or not v.strip():
            raise ValueError("email_verification_id cannot be empty")
        return v.strip()


class EmailVerificationResultsRequest(BaseModel):
    """Request model for getting email verification results."""
    
    email_verification_id: str = Field(..., description="Email verification ID")
    page: Optional[int] = Field(None, ge=1, description="Page number")
    limit: Optional[int] = Field(None, ge=10, le=100, description="Items per page")
    results: Optional[List[str]] = Field(None, description="Filter by specific verification results")
    
    @field_validator("email_verification_id")
    @classmethod
    def validate_email_verification_id(cls, v: str) -> str:
        """Validate email_verification_id is not empty."""
        if not v or not v.strip():
            raise ValueError("email_verification_id cannot be empty")
        return v.strip()
    
    @field_validator("page")
    @classmethod
    def validate_page(cls, v: Optional[int]) -> Optional[int]:
        """Validate page is positive."""
        if v is not None and v < 1:
            raise ValueError("page must be greater than 0")
        return v
    
    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: Optional[int]) -> Optional[int]:
        """Validate limit is within range."""
        if v is not None:
            if v < 10:
                raise ValueError("limit must be at least 10")
            if v > 100:
                raise ValueError("limit cannot exceed 100")
        return v
    
    @field_validator("results")
    @classmethod
    def validate_results(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate results filter values."""
        if v is not None:
            valid_results = {
                "valid", "catch_all", "mailbox_full", "role_based", "unknown", "failed",
                "syntax_error", "typo", "mailbox_not_found", "disposable", "mailbox_blocked"
            }
            for result in v:
                if result not in valid_results:
                    raise ValueError(f"Invalid result filter: {result}")
        return v


class EmailVerifyResponse(BaseModel):
    """Response model for single email verification."""
    
    status: str = Field(..., description="Verification status")


class EmailVerifyAsyncResponse(BaseModel):
    """Response model for async single email verification."""
    
    id: str = Field(..., description="Verification ID")
    address: str = Field(..., description="Email address")
    status: str = Field(..., description="Verification status")
    result: Optional[str] = Field(None, description="Verification result")
    error: Optional[str] = Field(None, description="Error message if any")


class EmailVerificationAsyncStatusResponse(BaseModel):
    """Response model for async email verification status."""
    
    id: str = Field(..., description="Verification ID")
    address: str = Field(..., description="Email address")
    status: str = Field(..., description="Verification status")
    result: Optional[str] = Field(None, description="Verification result")
    error: Optional[str] = Field(None, description="Error message if any")


class EmailVerificationStatus(BaseModel):
    """Email verification status model."""
    
    name: str = Field(..., description="Status name")
    count: int = Field(..., description="Number of verified emails")


class EmailVerificationStatistics(BaseModel):
    """Email verification statistics model."""
    
    valid: int = Field(..., description="Number of valid emails")
    catch_all: int = Field(..., description="Number of catch-all emails")
    mailbox_full: int = Field(..., description="Number of mailbox full emails")
    role_based: int = Field(..., description="Number of role-based emails")
    unknown: int = Field(..., description="Number of unknown emails")
    syntax_error: int = Field(..., description="Number of syntax error emails")
    typo: int = Field(..., description="Number of typo emails")
    mailbox_not_found: int = Field(..., description="Number of mailbox not found emails")
    disposable: int = Field(..., description="Number of disposable emails")
    mailbox_blocked: int = Field(..., description="Number of mailbox blocked emails")
    failed: int = Field(..., description="Number of failed verifications")


class EmailVerification(BaseModel):
    """Email verification list model."""
    
    id: str = Field(..., description="Verification list ID")
    name: str = Field(..., description="Verification list name")
    total: int = Field(..., description="Total number of emails")
    verification_started: Optional[datetime] = Field(None, description="Verification start time")
    verification_ended: Optional[datetime] = Field(None, description="Verification end time")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    status: EmailVerificationStatus = Field(..., description="Verification status")
    source: str = Field(..., description="Source of the verification list")
    statistics: EmailVerificationStatistics = Field(..., description="Verification statistics")


class EmailVerificationLinks(BaseModel):
    """Pagination links model."""
    
    first: Optional[str] = Field(None, description="First page URL")
    last: Optional[str] = Field(None, description="Last page URL")
    prev: Optional[str] = Field(None, description="Previous page URL")
    next: Optional[str] = Field(None, description="Next page URL")


class EmailVerificationMeta(BaseModel):
    """Pagination metadata model."""
    
    current_page: int = Field(..., description="Current page number")
    from_: Optional[int] = Field(None, alias="from", description="First item number")
    path: str = Field(..., description="Request path")
    per_page: str = Field(..., description="Items per page")
    to: Optional[int] = Field(None, description="Last item number")


class EmailVerificationListsResponse(BaseModel):
    """Response model for email verification lists."""
    
    data: List[EmailVerification] = Field(..., description="List of email verifications")
    links: EmailVerificationLinks = Field(..., description="Pagination links")
    meta: EmailVerificationMeta = Field(..., description="Pagination metadata")


class EmailVerificationResponse(BaseModel):
    """Response model for single email verification list."""
    
    data: EmailVerification = Field(..., description="Email verification data")


class EmailVerificationResult(BaseModel):
    """Email verification result model."""
    
    address: str = Field(..., description="Email address")
    result: str = Field(..., description="Verification result")


class EmailVerificationResultsResponse(BaseModel):
    """Response model for email verification results."""
    
    data: List[EmailVerificationResult] = Field(..., description="List of verification results")
    links: EmailVerificationLinks = Field(..., description="Pagination links")
    meta: EmailVerificationMeta = Field(..., description="Pagination metadata") 