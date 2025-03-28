"""
MailerSend Python SDK - Official Python library for interacting with the MailerSend API.
"""

from .client import MailerSendClient
from .constants import __version__

from .exceptions import (
    MailerSendError,
    ValidationError,
    AuthenticationError,
    ResourceNotFoundError,
    RateLimitExceeded,
    BadRequestError,
    ServerError,
)

__all__ = [
    # Main client
    "MailerSendClient",

    # Exceptions
    "MailerSendError",
    "ValidationError",
    "AuthenticationError",
    "ResourceNotFoundError",
    "RateLimitExceeded",
    "BadRequestError",
    "ServerError",
]