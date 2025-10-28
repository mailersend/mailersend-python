"""Domains models."""

from typing import Optional
from pydantic import Field, field_validator

from .base import BaseModel


class DomainListQueryParams(BaseModel):
    """Model for domain list query parameters with validation."""

    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)
    verified: Optional[bool] = None

    def to_query_params(self) -> dict:
        """Convert to query parameters for API request."""
        params = {"page": self.page, "limit": self.limit}
        
        # Convert boolean to lowercase string for API compatibility
        if self.verified is not None:
            params["verified"] = str(self.verified).lower()

        return {k: v for k, v in params.items() if v is not None}


class DomainListRequest(BaseModel):
    """Request model for listing domains."""

    query_params: DomainListQueryParams

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class DomainRecipientsQueryParams(BaseModel):
    """Model for domain recipients query parameters with validation."""

    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)

    def to_query_params(self) -> dict:
        """Convert to query parameters for API request."""
        params = {"page": self.page, "limit": self.limit}

        return {k: v for k, v in params.items() if v is not None}


class DomainRecipientsRequest(BaseModel):
    """Request model for getting domain recipients."""

    domain_id: str  # Path parameter
    query_params: DomainRecipientsQueryParams  # Query parameters

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class DomainCreateRequest(BaseModel):
    """Request model for creating a new domain."""

    name: str
    return_path_subdomain: Optional[str] = None
    custom_tracking_subdomain: Optional[str] = None
    inbound_routing_subdomain: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, v):
        """Validate domain name format and requirements."""
        if not v or not v.strip():
            raise ValueError("Domain name is required")

        # Must be lowercase
        if v != v.lower():
            raise ValueError("Domain name must be lowercase")

        # Basic domain validation
        if not "." in v or " " in v:
            raise ValueError("Invalid domain name format")

        return v.strip()

    @field_validator(
        "return_path_subdomain",
        "custom_tracking_subdomain",
        "inbound_routing_subdomain",
    )
    def validate_subdomains(cls, v):
        """Validate subdomain is alphanumeric."""
        if v is not None:
            if not v.isalnum():
                raise ValueError("Subdomain must be alphanumeric")
        return v


class DomainDeleteRequest(BaseModel):
    """Request model for deleting a domain."""

    domain_id: str

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()


class DomainGetRequest(BaseModel):
    """Request model for getting a single domain."""

    domain_id: str

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()


class DomainSettings(BaseModel):
    """Model for domain settings."""

    send_paused: bool = False
    track_clicks: bool = True
    track_opens: bool = True
    track_unsubscribe: bool = True
    track_unsubscribe_html: str = (
        '<p>Click here to <a href="{{unsubscribe}}">unsubscribe</a></p>'
    )
    track_unsubscribe_plain: str = "Click here to unsubscribe: {{unsubscribe}}"
    track_content: bool = True
    custom_tracking_enabled: bool = False
    custom_tracking_subdomain: str = "email"
    return_path_subdomain: Optional[str] = "mta"
    inbound_routing_enabled: Optional[bool] = False
    inbound_routing_subdomain: Optional[str] = "inbound"
    track_unsubscribe_html_enabled: Optional[bool] = None
    track_unsubscribe_plain_enabled: Optional[bool] = None
    precedence_bulk: bool = False
    ignore_duplicated_recipients: bool = False


class DomainUpdateSettingsRequest(BaseModel):
    """Request model for updating domain settings."""

    domain_id: str
    send_paused: Optional[bool] = None
    track_clicks: Optional[bool] = None
    track_opens: Optional[bool] = None
    track_unsubscribe: Optional[bool] = None
    track_content: Optional[bool] = None
    track_unsubscribe_html: Optional[str] = None
    track_unsubscribe_plain: Optional[str] = None
    custom_tracking_enabled: Optional[bool] = None
    custom_tracking_subdomain: Optional[str] = None
    precedence_bulk: Optional[bool] = None
    ignore_duplicated_recipients: Optional[bool] = None

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()

    @field_validator("custom_tracking_subdomain")
    def validate_custom_tracking_subdomain(cls, v):
        """Validate custom tracking subdomain is alphanumeric."""
        if v is not None and not v.isalnum():
            raise ValueError("Custom tracking subdomain must be alphanumeric")
        return v


class DomainDnsRecordsRequest(BaseModel):
    """Request model for getting domain DNS records."""

    domain_id: str

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()


class DomainVerificationRequest(BaseModel):
    """Request model for getting domain verification status."""

    domain_id: str

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()
