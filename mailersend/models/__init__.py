"""
Data models used for communicating with the MailerSend API.
"""

from .email import (
    EmailRequest,
    EmailFrom,
    EmailRecipient,
    Attachment,
    Personalization,
    Variable,
)

__all__ = [
    "EmailRequest",
    "EmailFrom",
    "EmailRecipient",
    "Attachment",
    "Personalization",
    "Variable",
]