"""
API resource classes for interacting with specific MailerSend API endpoints.
"""

from .base import BaseResource
from .email import Email
from .activity import Activity
from .analytics import Analytics
from .domains import Domains
from .identities import IdentitiesResource
from .inbound import InboundResource
from .messages import Messages
from .schedules import Schedules
from .recipients import Recipients
from .templates import Templates
from .tokens import Tokens
from .webhooks import Webhooks
from .email_verification import EmailVerification
from .users import Users
from .sms_messages import SmsMessages
from .sms_numbers import SmsNumbers
from .sms_activity import SmsActivity
from .sms_sending import SmsSending
from .sms_recipients import SmsRecipients
from .sms_webhooks import SmsWebhooks

__all__ = [
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
]