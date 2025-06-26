"""
MailerSend Python SDK

A comprehensive Python SDK for the MailerSend API.
"""

from .client import MailerSendClient
from .builders.email import EmailBuilder
from .builders.activity import ActivityBuilder, SingleActivityBuilder
from .resources.email import Email
from .resources.activity import Activity
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
from .exceptions import (
    MailerSendError,
    AuthenticationError,
    RateLimitExceeded,
    ResourceNotFoundError,
    BadRequestError,
    ServerError,
    ValidationError
)

__version__ = "1.0.0"

__all__ = [
    # Core client
    "MailerSendClient",
    
    # Builders
    "EmailBuilder",
    "ActivityBuilder",
    "SingleActivityBuilder",
    
    # Resources
    "Email",
    "Activity",
    
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
    
    # Exceptions
    "MailerSendError",
    "AuthenticationError", 
    "RateLimitExceeded",
    "ResourceNotFoundError",
    "BadRequestError",
    "ServerError",
    "ValidationError",
]