import asyncio
import logging
import os
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from .constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, USER_AGENT
from .exceptions import (
    AuthenticationError,
    BadRequestError,
    MailerSendError,
    RateLimitExceeded,
    ResourceNotFoundError,
    ServerError,
)
from .resources.activity import AsyncActivity
from .resources.analytics import AsyncAnalytics
from .resources.dmarc_monitoring import AsyncDmarcMonitoring
from .resources.domains import AsyncDomains
from .resources.email import AsyncEmail
from .resources.email_verification import AsyncEmailVerification
from .resources.identities import AsyncIdentitiesResource
from .resources.inbound import AsyncInboundResource
from .resources.messages import AsyncMessages
from .resources.other import AsyncOther
from .resources.recipients import AsyncRecipients
from .resources.schedules import AsyncSchedules
from .resources.sms_activity import AsyncSmsActivity
from .resources.sms_inbounds import AsyncSmsInbounds
from .resources.sms_messages import AsyncSmsMessages
from .resources.sms_numbers import AsyncSmsNumbers
from .resources.sms_recipients import AsyncSmsRecipients
from .resources.sms_sending import AsyncSmsSending
from .resources.sms_webhooks import AsyncSmsWebhooks
from .resources.smtp_users import AsyncSmtpUsers
from .resources.templates import AsyncTemplates
from .resources.tokens import AsyncTokens
from .resources.users import AsyncUsers
from .resources.webhooks import AsyncWebhooks
from .logging import get_logger, RequestLogger

_RETRY_STATUSES = frozenset([429, 500, 502, 503, 504])


class AsyncMailerSendClient:
    """
    Async client for the MailerSend API.

    Uses httpx.AsyncClient under the hood. Supports use as an async context
    manager (recommended) or manual lifecycle management via close().

    Examples:
        >>> # Using environment variable (recommended)
        >>> async with AsyncMailerSendClient() as client:
        ...     response = await client.emails.send(email_request)

        >>> # Using explicit API key
        >>> client = AsyncMailerSendClient(api_key="your_api_key")

        >>> # Enable debug logging for detailed request/response info
        >>> client = AsyncMailerSendClient(debug=True)
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
        """
        Initialize the async MailerSend client.

        Args:
            api_key: Your MailerSend API key. If not provided, will try to read
                    from MAILERSEND_API_KEY environment variable
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            debug: Enable detailed debug logging
            logger: Custom logger instance

        Raises:
            ValueError: If no API key is provided and MAILERSEND_API_KEY
                       environment variable is not set
        """
        resolved_api_key = api_key or os.getenv("MAILERSEND_API_KEY")

        if not resolved_api_key:
            raise ValueError(
                "API key is required. Either pass it as 'api_key' parameter or "
                "set the 'MAILERSEND_API_KEY' environment variable."
            )

        self.api_key = resolved_api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.debug = debug
        self.logger = logger or get_logger(debug=debug)
        self.request_logger = RequestLogger(self.logger)

        self._client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            },
            timeout=self.timeout,
        )

        self.emails = AsyncEmail(self)
        self.activities = AsyncActivity(self)
        self.analytics = AsyncAnalytics(self)
        self.domains = AsyncDomains(self)
        self.identities = AsyncIdentitiesResource(self)
        self.inbound = AsyncInboundResource(self)
        self.templates = AsyncTemplates(self)
        self.tokens = AsyncTokens(self)
        self.webhooks = AsyncWebhooks(self)
        self.email_verification = AsyncEmailVerification(self)
        self.users = AsyncUsers(self)
        self.messages = AsyncMessages(self)
        self.recipients = AsyncRecipients(self)
        self.schedules = AsyncSchedules(self)
        self.sms_messages = AsyncSmsMessages(self)
        self.smtp_users = AsyncSmtpUsers(self)
        self.sms_sending = AsyncSmsSending(self)
        self.sms_numbers = AsyncSmsNumbers(self)
        self.sms_activity = AsyncSmsActivity(self)
        self.sms_inbounds = AsyncSmsInbounds(self)
        self.sms_recipients = AsyncSmsRecipients(self)
        self.sms_webhooks = AsyncSmsWebhooks(self)
        self.api_quota = AsyncOther(self)
        self.dmarc_monitoring = AsyncDmarcMonitoring(self)

        self.logger.info("AsyncMailerSendClient initialized successfully")

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

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
    ) -> httpx.Response:
        """
        Make an async HTTP request to the MailerSend API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Query parameters
            body: Request body data

        Returns:
            Response object

        Raises:
            AuthenticationError: If authentication fails
            ResourceNotFoundError: If the requested resource is not found
            RateLimitExceeded: If API rate limits are exceeded
            BadRequestError: If the request was malformed
            ServerError: If a server error occurs
            MailerSendError: For other API errors
        """
        url = urljoin(self.base_url, path)
        request_id = self.request_logger.start_request(method, url, params, body)

        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=body,
                )

                self.request_logger.log_response(response)

                if 200 <= response.status_code < 300:
                    return response

                # Retry on transient errors (except on the last attempt)
                if (
                    response.status_code in _RETRY_STATUSES
                    and attempt < self.max_retries
                ):
                    if response.status_code == 429:
                        retry_after = response.headers.get("retry-after")
                        delay = (
                            float(retry_after) if retry_after else 0.3 * (2**attempt)
                        )
                    else:
                        delay = 0.3 * (2**attempt)
                    self.request_logger.log_retry(attempt + 1, delay)
                    await asyncio.sleep(delay)
                    continue

                error_message = self._get_error_message(response)
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
                        f"Rate limit exceeded. Retry after: {retry_after}s, Remaining: {remaining}",
                        extra={"request_id": request_id},
                    )
                    raise RateLimitExceeded(error_message, response)
                elif 400 <= response.status_code < 500:
                    raise BadRequestError(error_message, response)
                elif 500 <= response.status_code < 600:
                    raise ServerError(error_message, response)
                else:
                    raise MailerSendError(error_message, response)

            except (
                AuthenticationError,
                ResourceNotFoundError,
                RateLimitExceeded,
                BadRequestError,
                ServerError,
                MailerSendError,
            ):
                raise
            except httpx.RequestError as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = 0.3 * (2**attempt)
                    self.request_logger.log_retry(attempt + 1, delay)
                    await asyncio.sleep(delay)
                    continue
                self.request_logger.log_error(e)
                raise MailerSendError(f"Request failed: {str(e)}") from e

        # Should not be reached, but satisfies type checker
        if last_exception:
            raise MailerSendError(f"Request failed: {str(last_exception)}")
        raise MailerSendError("Request failed after retries")

    def _get_error_message(self, response: httpx.Response) -> str:
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
        return f"Error {response.status_code}: {response.text}"

    async def close(self) -> None:
        """Close the underlying httpx client and release resources."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncMailerSendClient":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()
