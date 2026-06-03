import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base_client import _BaseMailerSendClient, RETRY_STATUSES
from .constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, USER_AGENT
from .exceptions import MailerSendError


class MailerSendClient(_BaseMailerSendClient):
    """
    Main client for the MailerSend API.

    This client provides access to all MailerSend API resources and handles
    authentication, request formatting, and error handling.

    Examples:
        >>> # Using environment variable (recommended)
        >>> client = MailerSendClient()  # Reads from MAILERSEND_API_KEY
        >>> response = client.emails.send(email_request)

        >>> # Using explicit API key
        >>> client = MailerSendClient(api_key="your_api_key")

        >>> # Use as a context manager to ensure the session is closed
        >>> with MailerSendClient() as client:
        ...     response = client.emails.send(email_request)
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
        Initialize the MailerSend client.

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

        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=sorted(RETRY_STATUSES),
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            }
        )

        self.logger.info(f"{self.__class__.__name__} initialized successfully")
        if debug:
            self.logger.info("Debug mode enabled")

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Make an HTTP request to the MailerSend API.

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

        try:
            response = self.session.request(
                method=method, url=url, params=params, json=body, timeout=self.timeout
            )
            self.request_logger.log_response(response)

            if 200 <= response.status_code < 300:
                return response

            self._raise_for_status(
                response, self._get_error_message(response), request_id
            )

        except requests.RequestException as e:
            self.request_logger.log_error(e)
            raise MailerSendError(f"Request failed: {str(e)}") from e

    def get_debug_info(self) -> Dict[str, Any]:
        """Get current debug and configuration information."""
        info = super().get_debug_info()
        info["session_adapters"] = list(self.session.adapters.keys())
        return info

    def __enter__(self) -> "MailerSendClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.session.close()
