"""Account resource"""

from .base import BaseResource
from ..models.base import APIResponse


class AccountResource(BaseResource):
    """Client for interacting with the MailerSend Account API."""

    def get_account(self) -> APIResponse:
        """
        Get the account behind the API token.

        Returns:
            APIResponse with the account plan, usage, limits and add-ons
        """
        self.logger.debug("Retrieving account information")

        return self._request(method="GET", path="account")
