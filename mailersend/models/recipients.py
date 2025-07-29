"""Recipients API models for MailerSend SDK."""

from datetime import datetime
from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field, field_validator


# Query Parameters Models
class RecipientsListQueryParams(BaseModel):
    """Query parameters for listing recipients."""

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
        params["page"] = self.page
        params["limit"] = self.limit
        return params


class SuppressionListQueryParams(BaseModel):
    """Query parameters for listing suppression entries."""

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
        params["page"] = self.page
        params["limit"] = self.limit
        return params


# Request Models
class RecipientsListRequest(BaseModel):
    """Request model for listing recipients."""

    query_params: RecipientsListQueryParams = Field(
        default_factory=RecipientsListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class RecipientGetRequest(BaseModel):
    """Request model for getting a single recipient."""

    recipient_id: str

    @field_validator("recipient_id")
    @classmethod
    def validate_recipient_id(cls, v: str) -> str:
        """Validate and clean recipient_id."""
        if not v or not v.strip():
            raise ValueError("recipient_id cannot be empty")
        return v.strip()


class RecipientDeleteRequest(BaseModel):
    """Request model for deleting a recipient."""

    recipient_id: str

    @field_validator("recipient_id")
    @classmethod
    def validate_recipient_id(cls, v: str) -> str:
        """Validate and clean recipient_id."""
        if not v or not v.strip():
            raise ValueError("recipient_id cannot be empty")
        return v.strip()


class SuppressionListRequest(BaseModel):
    """Request model for listing suppression entries."""

    query_params: SuppressionListQueryParams = Field(
        default_factory=SuppressionListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class SuppressionAddRequest(BaseModel):
    """Request model for adding recipients to suppression lists."""

    domain_id: str
    recipients: Optional[List[str]] = None
    patterns: Optional[List[str]] = None

    @field_validator("domain_id")
    @classmethod
    def validate_domain_id(cls, v: str) -> str:
        """Validate and clean domain_id."""
        if not v or not v.strip():
            raise ValueError("domain_id cannot be empty")
        return v.strip()

    @field_validator("recipients")
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

    @field_validator("patterns")
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

    @field_validator("domain_id")
    @classmethod
    def validate_domain_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean domain_id."""
        if v is not None:
            return v.strip()
        return v

    @field_validator("ids")
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



