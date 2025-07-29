import logging
import json
import time
import uuid
from typing import Optional, Dict, Any, Set

# Sensitive fields that should be redacted in logs
SENSITIVE_FIELDS = {
    "authorization",
    "x-api-key",
    "api_key",
    "token",
    "password",
    "secret",
    "key",
    "auth",
    "bearer",
}


class DebugFilter(logging.Filter):
    """Filter that adds request context to log records."""

    def filter(self, record):
        # Add request ID if not present
        if not hasattr(record, "request_id"):
            record.request_id = getattr(self, "_current_request_id", "unknown")
        return True


class SensitiveDataFormatter(logging.Formatter):
    """Formatter that redacts sensitive information from log messages."""

    def format(self, record):
        # Create a copy of the record to avoid modifying the original
        record_copy = logging.makeLogRecord(record.__dict__)

        # Sanitize the message if it contains structured data
        if hasattr(record_copy, "args") and record_copy.args:
            record_copy.args = tuple(
                self._sanitize_value(arg) if isinstance(arg, (dict, str)) else arg
                for arg in record_copy.args
            )

        return super().format(record_copy)

    def _sanitize_value(self, value):
        """Sanitize sensitive data from values."""
        if isinstance(value, dict):
            return self._sanitize_dict(value)
        elif isinstance(value, str):
            return self._sanitize_string(value)
        return value

    def _sanitize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitize dictionary data."""
        if not isinstance(data, dict):
            return data

        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in SENSITIVE_FIELDS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_value(item) for item in value]
            else:
                sanitized[key] = value
        return sanitized

    def _sanitize_string(self, text: str) -> str:
        """Sanitize bearer tokens and other sensitive patterns in strings."""
        import re

        # Redact Bearer tokens
        text = re.sub(r"Bearer [^\s]+", "Bearer [REDACTED]", text)
        # Redact other common patterns
        text = re.sub(r'"api_key":\s*"[^"]*"', '"api_key": "[REDACTED]"', text)
        return text


def get_logger(name: Optional[str] = None, debug: bool = False) -> logging.Logger:
    """
    Get a logger instance configured for the MailerSend SDK.

    Args:
        name: Optional name for the logger, typically the module name.
              If not provided, it will use 'mailersend'.
        debug: Whether to enable debug mode with detailed logging

    Returns:
        A configured logger instance
    """
    logger_name = f"mailersend.{name}" if name else "mailersend"
    logger = logging.getLogger(logger_name)

    # Don't add handlers if they've already been added
    # This prevents duplicate log messages
    if not logger.handlers and not logging.root.handlers:
        # Set up a default handler if none exists
        handler = logging.StreamHandler()

        # Use sensitive data formatter
        if debug:
            formatter = SensitiveDataFormatter(
                "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s"
            )
            logger.setLevel(logging.DEBUG)
        else:
            formatter = SensitiveDataFormatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            logger.setLevel(logging.WARNING)

        handler.setFormatter(formatter)

        # Add debug filter for request context
        debug_filter = DebugFilter()
        handler.addFilter(debug_filter)

        logger.addHandler(handler)

    return logger


def setup_debug_logging():
    """
    Set up comprehensive debug logging for the entire SDK.

    This enables detailed request/response logging, timing information,
    and other debugging features across all SDK components.
    """
    # Set debug level for all mailersend loggers
    mailersend_logger = logging.getLogger("mailersend")
    mailersend_logger.setLevel(logging.DEBUG)

    # Enable debug logging for requests library (optional)
    requests_logger = logging.getLogger("urllib3.connectionpool")
    requests_logger.setLevel(logging.DEBUG)

    # Add a handler if none exists
    if not mailersend_logger.handlers:
        handler = logging.StreamHandler()
        formatter = SensitiveDataFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s"
        )
        handler.setFormatter(formatter)

        debug_filter = DebugFilter()
        handler.addFilter(debug_filter)

        mailersend_logger.addHandler(handler)


class RequestLogger:
    """Helper class for logging API requests with context and timing."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.request_id = None
        self.start_time = None

    def start_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
    ) -> str:
        """Start logging a new request."""
        self.request_id = str(uuid.uuid4())[:8]
        self.start_time = time.time()

        # Update the filter with current request ID
        for handler in self.logger.handlers:
            for filter_obj in handler.filters:
                if isinstance(filter_obj, DebugFilter):
                    filter_obj._current_request_id = self.request_id

        self.logger.info(
            f"🚀 Starting {method} request to {url}",
            extra={"request_id": self.request_id},
        )

        if params:
            sanitized_params = SensitiveDataFormatter()._sanitize_dict(params)
            self.logger.debug(
                f"📋 Query params: {json.dumps(sanitized_params, indent=2)}",
                extra={"request_id": self.request_id},
            )

        if body:
            sanitized_body = SensitiveDataFormatter()._sanitize_dict(body)
            self.logger.debug(
                f"📦 Request body: {json.dumps(sanitized_body, indent=2)}",
                extra={"request_id": self.request_id},
            )

        return self.request_id

    def log_response(self, response, duration: Optional[float] = None):
        """Log the response details."""
        if duration is None and self.start_time:
            duration = time.time() - self.start_time

        status_emoji = "✅" if 200 <= response.status_code < 300 else "❌"
        duration_str = f" ({duration:.3f}s)" if duration else ""

        self.logger.info(
            f"{status_emoji} Response {response.status_code}{duration_str}",
            extra={"request_id": self.request_id},
        )

        # Log important headers
        important_headers = {
            "x-request-id": response.headers.get("x-request-id"),
            "x-apiquota-remaining": response.headers.get("x-apiquota-remaining"),
            "retry-after": response.headers.get("retry-after"),
            "content-type": response.headers.get("content-type"),
        }
        filtered_headers = {k: v for k, v in important_headers.items() if v is not None}

        if filtered_headers:
            self.logger.debug(
                f"📄 Response headers: {json.dumps(filtered_headers, indent=2)}",
                extra={"request_id": self.request_id},
            )

        # Log response body for errors or debug level
        if response.status_code >= 400 or self.logger.isEnabledFor(logging.DEBUG):
            try:
                response_data = response.json()
                self.logger.debug(
                    f"📥 Response body: {json.dumps(response_data, indent=2)}",
                    extra={"request_id": self.request_id},
                )
            except Exception:
                self.logger.debug(
                    f"📥 Response body (text): {response.text[:500]}...",
                    extra={"request_id": self.request_id},
                )

    def log_error(self, error: Exception):
        """Log request errors."""
        self.logger.error(
            f"💥 Request failed: {str(error)}", extra={"request_id": self.request_id}
        )

    def log_retry(self, attempt: int, delay: float):
        """Log retry attempts."""
        self.logger.warning(
            f"🔄 Retrying request (attempt {attempt}) after {delay}s delay",
            extra={"request_id": self.request_id},
        )
