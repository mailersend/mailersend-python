"""Other endpoints resource"""

from .base import AsyncBaseResource, BaseResource
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

        response = self.client.request(method="GET", path="api-quota")

        return self._create_response(response)


class AsyncOther(AsyncBaseResource):
    """Async client for other MailerSend API endpoints."""

    async def get_quota(self) -> APIResponse:
        """
        Get API quota information.

        Returns:
            APIResponse with quota information including remaining requests
        """
        response = await self.client.request(method="GET", path="api-quota")
        return self._create_response(response)
