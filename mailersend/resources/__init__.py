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
from .webhooks import Webhooks

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
    "Webhooks",
]