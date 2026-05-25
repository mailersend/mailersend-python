"""
API resource classes for interacting with specific MailerSend API endpoints.
"""

from .base import AsyncBaseResource, BaseResource
from .email import AsyncEmail, Email
from .activity import AsyncActivity, Activity
from .analytics import AsyncAnalytics, Analytics
from .domains import AsyncDomains, Domains
from .identities import AsyncIdentitiesResource, IdentitiesResource
from .inbound import AsyncInboundResource, InboundResource
from .messages import AsyncMessages, Messages
from .schedules import AsyncSchedules, Schedules
from .recipients import AsyncRecipients, Recipients
from .templates import AsyncTemplates, Templates
from .tokens import AsyncTokens, Tokens
from .webhooks import AsyncWebhooks, Webhooks
from .email_verification import AsyncEmailVerification, EmailVerification
from .users import AsyncUsers, Users
from .sms_messages import AsyncSmsMessages, SmsMessages
from .sms_numbers import AsyncSmsNumbers, SmsNumbers
from .sms_activity import AsyncSmsActivity, SmsActivity
from .sms_sending import AsyncSmsSending, SmsSending
from .sms_recipients import AsyncSmsRecipients, SmsRecipients
from .sms_webhooks import AsyncSmsWebhooks, SmsWebhooks
from .sms_inbounds import AsyncSmsInbounds, SmsInbounds
from .other import AsyncOther, Other
from .dmarc_monitoring import AsyncDmarcMonitoring, DmarcMonitoring
from .smtp_users import AsyncSmtpUsers, SmtpUsers

__all__ = [
    # Sync resources
    "BaseResource",
    "Email",
    "Activity",
    "Analytics",
    "Domains",
    "IdentitiesResource",
    "InboundResource",
    "Messages",
    "Schedules",
    "Recipients",
    "Templates",
    "Tokens",
    "Webhooks",
    "EmailVerification",
    "Users",
    "SmsMessages",
    "SmsNumbers",
    "SmsActivity",
    "SmsSending",
    "SmsRecipients",
    "SmsWebhooks",
    "SmsInbounds",
    "SmtpUsers",
    "Other",
    "DmarcMonitoring",
    # Async resources
    "AsyncBaseResource",
    "AsyncEmail",
    "AsyncActivity",
    "AsyncAnalytics",
    "AsyncDomains",
    "AsyncIdentitiesResource",
    "AsyncInboundResource",
    "AsyncMessages",
    "AsyncSchedules",
    "AsyncRecipients",
    "AsyncTemplates",
    "AsyncTokens",
    "AsyncWebhooks",
    "AsyncEmailVerification",
    "AsyncUsers",
    "AsyncSmsMessages",
    "AsyncSmsNumbers",
    "AsyncSmsActivity",
    "AsyncSmsSending",
    "AsyncSmsRecipients",
    "AsyncSmsWebhooks",
    "AsyncSmsInbounds",
    "AsyncSmtpUsers",
    "AsyncOther",
    "AsyncDmarcMonitoring",
]
