"""
API resource classes for interacting with specific MailerSend API endpoints.
"""

from .base import BaseResource
from .email import Email
from .activity import Activity
from .analytics import Analytics
from .domains import Domains

__all__ = [
    "BaseResource",
    "Email",
    "Activity",
    "Analytics",
    "Domains",
]