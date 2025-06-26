"""
Builder patterns for constructing complex MailerSend requests.

The builder pattern provides a fluent, chainable API for constructing
complex email requests with intelligent defaults and validation.
"""

from .email import EmailBuilder
from .activity import ActivityBuilder, SingleActivityBuilder

__all__ = [
    'EmailBuilder',
    'ActivityBuilder',
    'SingleActivityBuilder',
] 