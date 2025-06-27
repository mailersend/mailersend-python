from typing import List, Optional, Literal, Any
from pydantic import Field, field_validator

from .base import BaseModel as MailerSendBaseModel


class DomainListRequest(MailerSendBaseModel):
    """Request model for listing domains."""
    
    page: Optional[int] = None
    limit: Optional[int] = 25
    verified: Optional[bool] = None
    
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


class DomainCreateRequest(MailerSendBaseModel):
    """Request model for creating a new domain."""
    
    name: str
    return_path_subdomain: Optional[str] = None
    custom_tracking_subdomain: Optional[str] = None
    inbound_routing_subdomain: Optional[str] = None
    
    @field_validator('name')
    def validate_name(cls, v):
        """Validate domain name format and requirements."""
        if not v or not v.strip():
            raise ValueError("Domain name is required")
        
        # Must be lowercase
        if v != v.lower():
            raise ValueError("Domain name must be lowercase")
        
        # Basic domain validation
        if not '.' in v or ' ' in v:
            raise ValueError("Invalid domain name format")
        
        return v.strip()
    
    @field_validator('return_path_subdomain', 'custom_tracking_subdomain', 'inbound_routing_subdomain')
    def validate_subdomains(cls, v):
        """Validate subdomain is alphanumeric."""
        if v is not None:
            if not v.isalnum():
                raise ValueError("Subdomain must be alphanumeric")
        return v


class DomainDeleteRequest(MailerSendBaseModel):
    """Request model for deleting a domain."""
    
    domain_id: str
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()


class DomainGetRequest(MailerSendBaseModel):
    """Request model for getting a single domain."""
    
    domain_id: str
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()


class DomainSettings(MailerSendBaseModel):
    """Model for domain settings."""
    
    send_paused: bool = False
    track_clicks: bool = True
    track_opens: bool = True
    track_unsubscribe: bool = True
    track_unsubscribe_html: str = "<p>Click here to <a href=\"{{unsubscribe}}\">unsubscribe</a></p>"
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


class DomainUpdateSettingsRequest(MailerSendBaseModel):
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
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()
    
    @field_validator('custom_tracking_subdomain')
    def validate_custom_tracking_subdomain(cls, v):
        """Validate custom tracking subdomain is alphanumeric."""
        if v is not None and not v.isalnum():
            raise ValueError("Custom tracking subdomain must be alphanumeric")
        return v


class Domain(MailerSendBaseModel):
    """Model representing a domain."""
    
    id: str
    name: str
    dkim: Optional[bool] = None
    spf: Optional[bool] = None
    mx: Optional[bool] = None
    tracking: Optional[bool] = None
    is_verified: bool = False
    is_cname_verified: Optional[bool] = None
    is_dns_active: bool = False
    is_cname_active: Optional[bool] = None
    is_tracking_allowed: Optional[bool] = None
    has_not_queued_messages: Optional[bool] = None
    not_queued_messages_count: Optional[int] = None
    domain_settings: DomainSettings
    can: Optional[dict] = None
    totals: Optional[List[Any]] = None
    created_at: str
    updated_at: str


class DomainListResponse(MailerSendBaseModel):
    """Response model for domain list."""
    
    data: List[Domain]
    links: dict
    meta: dict


class DomainResponse(MailerSendBaseModel):
    """Response model for single domain."""
    
    data: Domain


class DomainRecipient(MailerSendBaseModel):
    """Model representing a domain recipient."""
    
    id: str
    email: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str] = None


class DomainRecipientsRequest(MailerSendBaseModel):
    """Request model for getting domain recipients."""
    
    domain_id: str
    page: Optional[int] = None
    limit: Optional[int] = 25
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()
    
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


class DomainRecipientsResponse(MailerSendBaseModel):
    """Response model for domain recipients."""
    
    data: List[DomainRecipient] 
    links: dict
    meta: dict


class DomainDnsRecord(MailerSendBaseModel):
    """Model for DNS record details."""
    
    hostname: str
    type: str
    value: str
    priority: Optional[str] = None


class DomainDnsRecords(MailerSendBaseModel):
    """Model for all DNS records of a domain."""
    
    id: str
    spf: Optional[DomainDnsRecord] = None
    dkim: Optional[DomainDnsRecord] = None
    return_path: Optional[DomainDnsRecord] = None
    custom_tracking: Optional[DomainDnsRecord] = None
    inbound_routing: Optional[DomainDnsRecord] = None


class DomainDnsRecordsResponse(MailerSendBaseModel):
    """Response model for domain DNS records."""
    
    data: DomainDnsRecords


class DomainDnsRecordsRequest(MailerSendBaseModel):
    """Request model for getting domain DNS records."""
    
    domain_id: str
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()


class DomainVerificationData(MailerSendBaseModel):
    """Model for domain verification status data."""
    
    dkim: bool = False
    spf: bool = False
    mx: bool = False
    tracking: bool = False
    cname: bool = False
    rp_cname: bool = False


class DomainVerificationResponse(MailerSendBaseModel):
    """Response model for domain verification status."""
    
    message: str
    data: DomainVerificationData


class DomainVerificationRequest(MailerSendBaseModel):
    """Request model for getting domain verification status."""
    
    domain_id: str
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip() 