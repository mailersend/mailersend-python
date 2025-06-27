"""
Data models used for communicating with the MailerSend API.
"""
from .base import BaseModel
from .email import (
    EmailContact, 
    EmailAttachment,
    EmailPersonalization, 
    EmailRequest,
    EmailTrackingSettings, 
    EmailHeader
)
from .activity import (
    ActivityRecipient,
    ActivityEmail,
    Activity,
    ActivityQueryParams,
    ActivityRequest,
    SingleActivityRequest
)
from .analytics import (
    AnalyticsRequest,
    AnalyticsDateStats,
    AnalyticsDateResponse,
    AnalyticsCountryStats,
    AnalyticsCountryResponse,
    AnalyticsUserAgentStats,
    AnalyticsUserAgentResponse,
    AnalyticsReadingEnvironmentStats,
    AnalyticsReadingEnvironmentResponse
)
from .domains import (
    DomainListRequest,
    DomainCreateRequest,
    DomainUpdateSettingsRequest,
    DomainSettings,
    Domain,
    DomainListResponse,
    DomainResponse,
    DomainRecipient,
    DomainRecipientsRequest,
    DomainRecipientsResponse,
    DomainDnsRecord,
    DomainDnsRecords,
    DomainDnsRecordsResponse,
    DomainVerificationData,
    DomainVerificationResponse
)

__all__ = [
    "BaseModel",
    "EmailContact",
    "EmailAttachment",
    "EmailPersonalization", 
    "EmailRequest",
    "EmailTrackingSettings", 
    "EmailHeader",
    "ActivityRecipient",
    "ActivityEmail",
    "Activity",
    "ActivityQueryParams",
    "ActivityRequest",
    "AnalyticsRequest",
    "AnalyticsDateStats",
    "AnalyticsDateResponse",
    "AnalyticsCountryStats",
    "AnalyticsCountryResponse",
    "AnalyticsUserAgentStats",
    "AnalyticsUserAgentResponse",
    "AnalyticsReadingEnvironmentStats",
    "AnalyticsReadingEnvironmentResponse",
    "DomainListRequest",
    "DomainCreateRequest",
    "DomainUpdateSettingsRequest",
    "DomainSettings",
    "Domain",
    "DomainListResponse",
    "DomainResponse",
    "DomainRecipient",
    "DomainRecipientsRequest",
    "DomainRecipientsResponse",
    "DomainDnsRecord",
    "DomainDnsRecords",
    "DomainDnsRecordsResponse",
    "DomainVerificationData",
    "DomainVerificationResponse"
]