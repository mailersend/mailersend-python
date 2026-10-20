"""WhatsApp Activities resource."""

from .base import BaseResource
from ..models.whatsapp_activities import WhatsAppActivitiesListRequest
from ..models.base import APIResponse


class WhatsAppActivities(BaseResource):
    """WhatsApp Activities resource for MailerSend API."""

    def list_whatsapp_activities(
        self, request: WhatsAppActivitiesListRequest
    ) -> APIResponse:
        """
        List WhatsApp activities, the status events of your WhatsApp messages.

        Args:
            request: WhatsAppActivitiesListRequest object containing query parameters

        Returns:
            APIResponse: Response containing list of WhatsApp activities
        """
        params = request.to_query_params()

        self.logger.debug(
            "Listing WhatsApp activities with page: %s, limit: %s",
            request.query_params.page,
            request.query_params.limit,
        )

        return self._request(method="GET", path="whatsapp/activities", params=params)
