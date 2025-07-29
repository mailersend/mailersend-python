"""Models for Tokens API."""

from datetime import datetime
from typing import List, Optional, Literal, Dict, Any

from pydantic import BaseModel, Field, field_validator


# Token scope constants
TOKEN_SCOPES = [
    "email_full",
    "domains_read",
    "domains_full",
    "activity_read",
    "activity_full",
    "analytics_read",
    "analytics_full",
    "tokens_full",
    "webhooks_full",
    "templates_full",
    "suppressions_read",
    "suppressions_full",
    "sms_full",
    "sms_read",
    "email_verification_read",
    "email_verification_full",
    "inbounds_full",
    "recipients_read",
    "recipients_full",
    "sender_identity_read",
    "sender_identity_full",
    "users_read",
    "users_full",
    "smtp_users_read",
    "smtp_users_full",
]

# Token status types
TokenStatus = Literal["pause", "unpause"]


# Query parameters models
class TokensListQueryParams(BaseModel):
    """Query parameters for tokens list request."""

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=25, ge=10, le=100)

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        params = {}
        if self.page != 1:  # Only include if not default
            params["page"] = self.page
        if self.limit != 25:  # Only include if not default
            params["limit"] = self.limit
        return params


# Request models
class TokensListRequest(BaseModel):
    """Request model for listing tokens."""

    query_params: TokensListQueryParams = Field(default_factory=TokensListQueryParams)

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class TokenGetRequest(BaseModel):
    """Request model for getting a single token."""

    token_id: str


class TokenCreateRequest(BaseModel):
    """Request model for creating a token."""

    name: str = Field(max_length=50)
    domain_id: str
    scopes: List[str] = Field(min_length=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate token name."""
        if not v.strip():
            raise ValueError("Token name cannot be empty")
        return v.strip()

    @field_validator("domain_id")
    @classmethod
    def validate_domain_id(cls, v: str) -> str:
        """Validate domain ID."""
        if not v.strip():
            raise ValueError("Domain ID cannot be empty")
        return v.strip()

    @field_validator("scopes")
    @classmethod
    def validate_scopes(cls, v: List[str]) -> List[str]:
        """Validate scopes."""
        if not v:
            raise ValueError("At least one scope is required")

        invalid_scopes = [scope for scope in v if scope not in TOKEN_SCOPES]
        if invalid_scopes:
            raise ValueError(
                f"Invalid scopes: {invalid_scopes}. Valid scopes: {TOKEN_SCOPES}"
            )

        return v

    def to_json(self) -> Dict[str, Any]:
        """Convert request to JSON data for API call."""
        return {"name": self.name, "domain_id": self.domain_id, "scopes": self.scopes}


class TokenUpdateRequest(BaseModel):
    """Request model for updating a token status."""

    token_id: str
    status: TokenStatus

    def to_json(self) -> Dict[str, Any]:
        """Convert request to JSON data for API call."""
        return {"status": self.status}


class TokenUpdateNameRequest(BaseModel):
    """Request model for updating a token name."""

    token_id: str
    name: str = Field(max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate token name."""
        if not v.strip():
            raise ValueError("Token name cannot be empty")
        return v.strip()

    def to_json(self) -> Dict[str, Any]:
        """Convert request to JSON data for API call."""
        return {"name": self.name}


class TokenDeleteRequest(BaseModel):
    """Request model for deleting a token."""

    token_id: str
