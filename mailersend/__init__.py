"""
MailerSend Python SDK

A comprehensive Python SDK for the MailerSend API.
"""

from .client import MailerSendClient
from .builders.email import EmailBuilder
from .builders.activity import ActivityBuilder, SingleActivityBuilder
from .builders.analytics import AnalyticsBuilder
from .resources.email import Email
from .resources.activity import Activity
from .resources.analytics import Analytics
from .models.email import (
    EmailContact, 
    EmailAttachment,
    EmailPersonalization, 
    EmailRequest,
    EmailTrackingSettings, 
    EmailHeader
)
from .models.activity import (
    ActivityRecipient,
    ActivityEmail,
    Activity as ActivityModel,
    ActivityQueryParams,
    SingleActivityRequest
)
from .models.analytics import (
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
from .exceptions import (
    MailerSendError,
    AuthenticationError,
    RateLimitExceeded,
    ResourceNotFoundError,
    BadRequestError,
    ServerError,
    ValidationError
)

__version__ = "1.0.0"

__all__ = [
    # Core client
    "MailerSendClient",
    
    # Builders
    "EmailBuilder",
    "ActivityBuilder",
    "SingleActivityBuilder",
    "AnalyticsBuilder",
    
    # Resources
    "Email",
    "Activity",
    "Analytics",
    
    # Email models
    "EmailContact",
    "EmailAttachment", 
    "EmailPersonalization",
    "EmailRequest",
    "EmailTrackingSettings",
    "EmailHeader",
    
    # Activity models
    "ActivityRecipient",
    "ActivityEmail",
    "ActivityModel",
    "ActivityQueryParams",
    "SingleActivityRequest",
    
    # Analytics models
    "AnalyticsRequest",
    "AnalyticsDateStats",
    "AnalyticsDateResponse",
    "AnalyticsCountryStats",
    "AnalyticsCountryResponse",
    "AnalyticsUserAgentStats",
    "AnalyticsUserAgentResponse",
    "AnalyticsReadingEnvironmentStats",
    "AnalyticsReadingEnvironmentResponse",
    
    # Exceptions
    "MailerSendError",
    "AuthenticationError", 
    "RateLimitExceeded",
    "ResourceNotFoundError",
    "BadRequestError",
    "ServerError",
    "ValidationError",
]