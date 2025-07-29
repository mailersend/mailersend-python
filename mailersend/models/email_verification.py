"""Email Verification API models for MailerSend SDK."""

from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, field_validator


# Query Parameters Models
class EmailVerificationListsQueryParams(BaseModel):
    """Query parameters for listing email verification lists."""

    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=25, ge=10, le=100, description="Items per page")

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        params = {}
        if self.page is not None:
            params["page"] = self.page
        if self.limit is not None:
            params["limit"] = self.limit
        return params


class EmailVerificationResultsQueryParams(BaseModel):
    """Query parameters for getting email verification results."""

    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=25, ge=10, le=100, description="Items per page")
    results: Optional[List[str]] = Field(
        None, description="Filter by specific verification results"
    )

    @field_validator("results")
    @classmethod
    def validate_results(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate results filter values."""
        if v is not None:
            valid_results = {
                "valid",
                "catch_all",
                "mailbox_full",
                "role_based",
                "unknown",
                "failed",
                "syntax_error",
                "typo",
                "mailbox_not_found",
                "disposable",
                "mailbox_blocked",
            }
            for result in v:
                if result not in valid_results:
                    raise ValueError(f"Invalid result filter: {result}")
        return v

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        params = {}
        if self.page is not None:
            params["page"] = self.page
        if self.limit is not None:
            params["limit"] = self.limit
        if self.results is not None and self.results:
            params["results"] = self.results
        return params


# Request Models
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

    query_params: EmailVerificationListsQueryParams

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


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
    emails: List[str] = Field(
        ..., min_length=1, description="List of email addresses to verify"
    )

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
    query_params: EmailVerificationResultsQueryParams

    @field_validator("email_verification_id")
    @classmethod
    def validate_email_verification_id(cls, v: str) -> str:
        """Validate email_verification_id is not empty."""
        if not v or not v.strip():
            raise ValueError("email_verification_id cannot be empty")
        return v.strip()

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()



