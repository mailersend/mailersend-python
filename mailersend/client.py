import logging
from typing import Optional, Dict, Any, Type, cast, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, USER_AGENT
from .exceptions import (
    MailerSendError, AuthenticationError, RateLimitExceeded, 
    ResourceNotFoundError, BadRequestError, ServerError
)
from .resources.email import Email
from .logging import get_logger, RequestLogger


class MailerSendClient:
    """
    Main client for the MailerSend API.
    
    This client provides access to all MailerSend API resources and handles
    authentication, request formatting, and error handling.
    
    Examples:
        >>> client = MailerSendClient(api_key="your_api_key")
        >>> response = client.emails.send(email_request)
        
        # Enable debug logging for detailed request/response info
        >>> client = MailerSendClient(api_key="your_api_key", debug=True)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        debug: bool = False,
        logger: Optional[logging.Logger] = None
    ) -> None:
        """
        Initialize the MailerSend client.
        
        Args:
            api_key: Your MailerSend API key
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            debug: Enable detailed debug logging
            logger: Custom logger instance
        
        Raises:
            ValueError: If api_key is empty
        """
        if not api_key:
            raise ValueError("API key cannot be empty")
            
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.debug = debug
        self.logger = logger or get_logger(debug=debug)
        self.request_logger = RequestLogger(self.logger)
        
        # Initialize session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT
        })
        
        # Initialize resources
        self.emails = Email(self)
        
        self.logger.info("MailerSend client initialized successfully")
        if debug:
            self.logger.info("🐛 Debug mode enabled - detailed logging active")

        
    def request(
        self, 
        method: str, 
        path: str, 
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None
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
        
        # Start request logging
        request_id = self.request_logger.start_request(method, url, params, body)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=body,
                timeout=self.timeout
            )
            
            # Log response details
            self.request_logger.log_response(response)
            
            # Handle different response status codes
            if 200 <= response.status_code < 300:
                return response
                
            # Handle error responses
            error_message = self._get_error_message(response)
            
            # Log the error details before raising
            self.logger.error(f"API error {response.status_code}: {error_message}", 
                            extra={'request_id': request_id})
            
            if response.status_code == 401:
                raise AuthenticationError(error_message, response)
            elif response.status_code == 404:
                raise ResourceNotFoundError(error_message, response)
            elif response.status_code == 429:
                # Log rate limit details
                retry_after = response.headers.get('retry-after')
                remaining = response.headers.get('x-apiquota-remaining')
                self.logger.warning(f"⚠️ Rate limit exceeded. Retry after: {retry_after}s, Remaining: {remaining}", 
                                  extra={'request_id': request_id})
                raise RateLimitExceeded(error_message, response)
            elif 400 <= response.status_code < 500:
                raise BadRequestError(error_message, response)
            elif 500 <= response.status_code < 600:
                raise ServerError(error_message, response)
            else:
                raise MailerSendError(error_message, response)
                
        except requests.RequestException as e:
            self.request_logger.log_error(e)
            raise MailerSendError(f"Request failed: {str(e)}")
    
    def _get_error_message(self, response: requests.Response) -> str:
        """Extract error message from response."""
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                message = error_data.get("message", "Unknown error")
                errors = error_data.get("errors", {})
                if errors:
                    error_details = "; ".join(
                        f"{key}: {', '.join(msgs)}" 
                        for key, msgs in errors.items()
                    )
                    return f"{message}: {error_details}"
                return message
        except Exception:
            pass
        
        return f"Error {response.status_code}: {response.text}"
    
    def enable_debug(self):
        """Enable debug logging for this client instance."""
        self.debug = True
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("🐛 Debug mode enabled")
    
    def disable_debug(self):
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
            "user_agent": USER_AGENT,
            "logger_level": self.logger.level,
            "session_adapters": list(self.session.adapters.keys())
        }