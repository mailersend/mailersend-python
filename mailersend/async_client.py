import asyncio
import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from .base_client import _BaseMailerSendClient, RETRY_STATUSES
from .constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, USER_AGENT
from .exceptions import (
    AuthenticationError,
    BadRequestError,
    MailerSendError,
    RateLimitExceeded,
    ResourceNotFoundError,
    ServerError,
)


class AsyncMailerSendClient(_BaseMailerSendClient):
    """
    Async client for the MailerSend API.

    Uses httpx.AsyncClient under the hood. Supports use as an async context
    manager (recommended) or manual lifecycle management via close().

    Examples:
        >>> # Using environment variable (recommended)
        >>> async with AsyncMailerSendClient() as client:
        ...     response = await client.emails.send(email_request)

        >>> # Using explicit API key (remember to close when done)
        >>> client = AsyncMailerSendClient(api_key="your_api_key")
        >>> response = await client.emails.send(email_request)
        >>> await client.close()

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
        super().__init__(api_key, base_url, timeout, max_retries, debug, logger)

        self._client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            },
            timeout=self.timeout,
        )

        self.logger.info(f"{self.__class__.__name__} initialized successfully")

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

                if (
                    response.status_code in RETRY_STATUSES
                    and attempt < self.max_retries
                ):
                    if response.status_code == 429:
                        retry_after = response.headers.get("retry-after")
                        try:
                            delay = (
                                float(retry_after)
                                if retry_after
                                else 0.3 * (2**attempt)
                            )
                        except ValueError:
                            delay = 0.3 * (2**attempt)
                    else:
                        delay = 0.3 * (2**attempt)
                    self.request_logger.log_retry(attempt + 1, delay)
                    await asyncio.sleep(delay)
                    continue

                self._raise_for_status(
                    response, self._get_error_message(response), request_id
                )

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
                if attempt < self.max_retries:
                    delay = 0.3 * (2**attempt)
                    self.request_logger.log_retry(attempt + 1, delay)
                    await asyncio.sleep(delay)
                    continue
                self.request_logger.log_error(e)
                raise MailerSendError(f"Request failed: {str(e)}") from e

    async def close(self) -> None:
        """Close the underlying httpx client and release resources."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncMailerSendClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        await self.close()
