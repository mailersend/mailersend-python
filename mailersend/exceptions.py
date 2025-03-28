from typing import Optional
import requests


class MailerSendError(Exception):
    """Base exception for all MailerSend API errors."""
    
    def __init__(self, message: str, response: Optional[requests.Response] = None):
        self.message = message
        self.response = response
        super().__init__(self.message)


class AuthenticationError(MailerSendError):
    """Raised when authentication fails."""
    pass


class ResourceNotFoundError(MailerSendError):
    """Raised when a requested resource is not found."""
    pass


class RateLimitExceeded(MailerSendError):
    """Raised when API rate limits are exceeded."""
    
    @property
    def retry_after(self) -> Optional[int]:
        """Get the recommended retry time in seconds."""
        if self.response and "Retry-After" in self.response.headers:
            try:
                return int(self.response.headers["Retry-After"])
            except (ValueError, TypeError):
                pass
        return None


class BadRequestError(MailerSendError):
    """Raised when the request was malformed."""
    pass


class ServerError(MailerSendError):
    """Raised when a server-side error occurs."""
    pass


class ValidationError(MailerSendError):
    """Raised when request validation fails."""
    pass