"""Shared base client for MailerSendClient and AsyncMailerSendClient."""

import logging
import os
from typing import Any, Dict, NoReturn, Optional

from .constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, USER_AGENT
from .exceptions import (
    AuthenticationError,
    BadRequestError,
    MailerSendError,
    RateLimitExceeded,
    ResourceNotFoundError,
    ServerError,
)
from .logging import get_logger, RequestLogger
from .resources.activity import Activity
from .resources.analytics import Analytics
from .resources.dmarc_monitoring import DmarcMonitoring
from .resources.domains import Domains
from .resources.email import Email
from .resources.email_verification import EmailVerification
from .resources.identities import IdentitiesResource
from .resources.inbound import InboundResource
from .resources.messages import Messages
from .resources.other import Other
from .resources.recipients import Recipients
from .resources.schedules import Schedules
from .resources.sms_activity import SmsActivity
from .resources.sms_inbounds import SmsInbounds
from .resources.sms_messages import SmsMessages
from .resources.sms_numbers import SmsNumbers
from .resources.sms_recipients import SmsRecipients
from .resources.sms_sending import SmsSending
from .resources.sms_webhooks import SmsWebhooks
from .resources.smtp_users import SmtpUsers
from .resources.templates import Templates
from .resources.tokens import Tokens
from .resources.users import Users
from .resources.webhooks import Webhooks

# HTTP status codes that warrant a retry
RETRY_STATUSES: frozenset = frozenset([429, 500, 502, 503, 504])


class _BaseMailerSendClient:
    """
    Shared base for MailerSendClient and AsyncMailerSendClient.

    Handles API key resolution, resource initialisation, debug helpers,
    and error parsing/dispatch. Subclasses provide the transport layer
    (requests vs httpx) and the request() method (sync vs async).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        debug: bool = False,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        resolved_api_key = api_key or os.getenv("MAILERSEND_API_KEY")
        if not resolved_api_key:
            raise ValueError(
                "API key is required. Either pass it as 'api_key' parameter or "
                "set the 'MAILERSEND_API_KEY' environment variable."
            )

        self.api_key = resolved_api_key
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.max_retries = max_retries
        self.debug = debug
        self.logger = logger or get_logger(debug=debug)
        self.request_logger = RequestLogger(self.logger)

        self._init_resources()

    def _init_resources(self) -> None:
        """Instantiate all API resource objects."""
        self.emails = Email(self)
        self.activities = Activity(self)
        self.analytics = Analytics(self)
        self.domains = Domains(self)
        self.identities = IdentitiesResource(self)
        self.inbound = InboundResource(self)
        self.templates = Templates(self)
        self.tokens = Tokens(self)
        self.webhooks = Webhooks(self)
        self.email_verification = EmailVerification(self)
        self.users = Users(self)
        self.messages = Messages(self)
        self.recipients = Recipients(self)
        self.schedules = Schedules(self)
        self.sms_messages = SmsMessages(self)
        self.smtp_users = SmtpUsers(self)
        self.sms_sending = SmsSending(self)
        self.sms_numbers = SmsNumbers(self)
        self.sms_activity = SmsActivity(self)
        self.sms_inbounds = SmsInbounds(self)
        self.sms_recipients = SmsRecipients(self)
        self.sms_webhooks = SmsWebhooks(self)
        self.api_quota = Other(self)
        self.dmarc_monitoring = DmarcMonitoring(self)

    @staticmethod
    def _get_error_message(response: Any) -> str:
        """Extract a human-readable error message from an HTTP response."""
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                message = error_data.get("message", "Unknown error")
                errors = error_data.get("errors", {})
                if errors:
                    error_details = "; ".join(
                        f"{key}: {', '.join(msgs)}" for key, msgs in errors.items()
                    )
                    return f"{message}: {error_details}"
                return message
        except Exception:
            pass
        try:
            return f"Error {response.status_code}: {response.text}"
        except Exception:
            return f"Error {response.status_code}: <unreadable response body>"

    def _raise_for_status(
        self, response: Any, error_message: str, request_id: str
    ) -> NoReturn:
        """Log and raise the appropriate SDK exception for a non-2xx response."""
        self.logger.error(
            f"API error {response.status_code}: {error_message}",
            extra={"request_id": request_id},
        )
        if response.status_code == 401:
            raise AuthenticationError(error_message, response)
        elif response.status_code == 404:
            raise ResourceNotFoundError(error_message, response)
        elif response.status_code == 429:
            retry_after = response.headers.get("retry-after")
            remaining = response.headers.get("x-apiquota-remaining")
            self.logger.warning(
                f"Rate limit exceeded. Retry after: {retry_after}s, "
                f"Remaining: {remaining}",
                extra={"request_id": request_id},
            )
            raise RateLimitExceeded(error_message, response)
        elif 400 <= response.status_code < 500:
            raise BadRequestError(error_message, response)
        elif 500 <= response.status_code < 600:
            raise ServerError(error_message, response)
        else:
            raise MailerSendError(error_message, response)

    def enable_debug(self) -> None:
        """Enable debug logging for this client instance."""
        self.debug = True
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("Debug mode enabled")

    def disable_debug(self) -> None:
        """Disable debug logging for this client instance."""
        self.debug = False
        self.logger.setLevel(logging.WARNING)
        self.logger.info("Debug mode disabled")

    def get_debug_info(self) -> Dict[str, Any]:
        """Get current debug and configuration information."""
        return {
            "debug_enabled": self.debug,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "user_agent": USER_AGENT,
            "logger_level": self.logger.level,
        }
