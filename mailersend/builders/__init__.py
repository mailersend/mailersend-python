"""
Builder patterns for constructing complex MailerSend requests.

The builder pattern provides a fluent, chainable API for constructing
complex email requests with intelligent defaults and validation.
"""

from .email import EmailBuilder
from .activity import ActivityBuilder, SingleActivityBuilder
from .analytics import AnalyticsBuilder
from .domains import DomainsBuilder
from .identities import IdentityBuilder
from .inbound import InboundBuilder
from .messages import MessagesBuilder
from .schedules import SchedulesBuilder
from .recipients import RecipientsBuilder
from .templates import TemplatesBuilder
from .tokens import TokensBuilder
from .webhooks import WebhooksBuilder
from .email_verification import EmailVerificationBuilder
from .users import UsersBuilder
from .sms_messages import SmsMessagesBuilder
from .sms_numbers import SmsNumbersBuilder
from .sms_activity import SmsActivityBuilder
from .sms_sending import SmsSendingBuilder
from .sms_recipients import SmsRecipientsBuilder

__all__ = [
    'EmailBuilder',
    'ActivityBuilder',
    'SingleActivityBuilder',
    'AnalyticsBuilder',
    'DomainsBuilder',
    'IdentityBuilder',
    'InboundBuilder',
    'MessagesBuilder',
    'SchedulesBuilder',
    'RecipientsBuilder',
    'TemplatesBuilder',
    'TokensBuilder',
    'WebhooksBuilder',
    'EmailVerificationBuilder',
    'UsersBuilder',
    'SmsMessagesBuilder',
    'SmsNumbersBuilder',
    'SmsActivityBuilder',
    'SmsSendingBuilder',
    'SmsRecipientsBuilder',
] 