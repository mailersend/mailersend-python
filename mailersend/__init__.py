"""
MailerSend Python SDK

A comprehensive Python SDK for the MailerSend API.
"""

from .client import MailerSendClient

# Import all builders for better UX - users can import everything from main module
from .builders.email import EmailBuilder
from .builders.activity import ActivityBuilder, SingleActivityBuilder
from .builders.analytics import AnalyticsBuilder
from .builders.domains import DomainsBuilder
from .builders.identities import IdentityBuilder
from .builders.inbound import InboundBuilder
from .builders.messages import MessagesBuilder
from .builders.schedules import SchedulesBuilder
from .builders.recipients import RecipientsBuilder
from .builders.templates import TemplatesBuilder
from .builders.tokens import TokensBuilder
from .builders.smtp_users import SmtpUsersBuilder
from .builders.webhooks import WebhooksBuilder
from .builders.email_verification import EmailVerificationBuilder
from .builders.users import UsersBuilder
from .builders.sms_messages import SmsMessagesBuilder
from .builders.sms_numbers import SmsNumbersBuilder
from .builders.sms_activity import SmsActivityBuilder
from .builders.sms_sending import SmsSendingBuilder
from .builders.sms_recipients import SmsRecipientsBuilder
from .builders.sms_webhooks import SmsWebhooksBuilder
from .builders.sms_inbounds import SmsInboundsBuilder
from .resources.email import Email
from .resources.activity import Activity
from .resources.analytics import Analytics
from .resources.domains import Domains
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

__version__ = "2.0.0"

__all__ = [
    # Core client
    "MailerSendClient",
    
    # Builders - All available from main module for better UX
    "EmailBuilder",
    "ActivityBuilder", 
    "SingleActivityBuilder",
    "AnalyticsBuilder",
    "DomainsBuilder",
    "IdentityBuilder",
    "InboundBuilder", 
    "MessagesBuilder",
    "SchedulesBuilder",
    "RecipientsBuilder",
    "TemplatesBuilder",
    "TokensBuilder", 
    "SmtpUsersBuilder",
    "WebhooksBuilder",
    "EmailVerificationBuilder",
    "UsersBuilder",
    "SmsMessagesBuilder",
    "SmsNumbersBuilder", 
    "SmsActivityBuilder",
    "SmsSendingBuilder",
    "SmsRecipientsBuilder",
    "SmsWebhooksBuilder",
    "SmsInboundsBuilder",
    
    # Resources
    "Email",
    "Activity",
    "Analytics",
    "Domains",
    
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
    
    # Exceptions
    "MailerSendError",
    "AuthenticationError", 
    "RateLimitExceeded",
    "ResourceNotFoundError",
    "BadRequestError",
    "ServerError",
    "ValidationError",
]
