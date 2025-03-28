"""
Data models used for communicating with the MailerSend API.
"""
from .base import BaseModel
from .email import (
    EmailRequest,
    EmailFrom,
    EmailRecipient,
    EmailReplyTo,
    EmailAttachment,
    EmailContent,
    EmailPersonalization,
    EmailTrackingSettings,
    EmailHeader
)

__all__ = [
    "BaseModel",
    "EmailRequest",
    "EmailFrom",
    "EmailRecipient",
    "EmailReplyTo",
    "EmailAttachment",
    "EmailContent",
    "EmailPersonalization",
    "EmailTrackingSettings",
    "EmailHeader",
]