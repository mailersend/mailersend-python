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

__all__ = [
    "BaseModel",
    "EmailContact",
    "EmailAttachment",
    "EmailPersonalization", 
    "EmailRequest",
    "EmailTrackingSettings", 
    "EmailHeader"
]