"""
MailerSend Python SDK - Official Python library for interacting with the MailerSend API.
"""

from .client import MailerSendClient
from .constants import __version__
from .models.base import APIResponse
from .logging import setup_debug_logging, get_logger
from .builders import EmailBuilder

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
    
    # Response object
    "APIResponse",

    # Exceptions
    "MailerSendError",
    "ValidationError",
    "AuthenticationError",
    "ResourceNotFoundError",
    "RateLimitExceeded",
    "BadRequestError",
    "ServerError",

    # Logging
    "setup_debug_logging",
    "get_logger",

    # Builders
    "EmailBuilder"
]