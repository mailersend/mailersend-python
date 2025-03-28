"""
API resource classes for interacting with specific MailerSend API endpoints.
"""

from .base import BaseResource
from .email import Email

__all__ = [
    "BaseResource",
    "Email",
]