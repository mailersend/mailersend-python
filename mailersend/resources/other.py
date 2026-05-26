"""Other endpoints resource"""

from .base import BaseResource
from ..models.base import APIResponse


class Other(BaseResource):
    """
    Client for interacting with other MailerSend API endpoints.

    Provides methods for accessing miscellaneous endpoints like API quota.
    """

    def get_quota(self) -> APIResponse:
        """
        Get API quota information.

        Returns:
            APIResponse with quota information including remaining requests
        """
        self.logger.debug("Retrieving API quota information")

        return self._request(method="GET", path="api-quota")


AsyncOther = Other
