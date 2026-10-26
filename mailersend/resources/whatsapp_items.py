"""WhatsApp Items resource."""

from .base import BaseResource
from ..models.whatsapp_items import (
    WhatsAppItemsListRequest,
    WhatsAppItemGetRequest,
)
from ..models.base import APIResponse


class WhatsAppItems(BaseResource):
    """WhatsApp Items resource for MailerSend API."""

    def list_whatsapp_items(self, request: WhatsAppItemsListRequest) -> APIResponse:
        """
        List WhatsApp items, one per recipient of each message.

        Args:
            request: WhatsAppItemsListRequest object containing query parameters

        Returns:
            APIResponse: Response containing list of WhatsApp items
        """
        params = request.to_query_params()

        self.logger.debug(
            "Listing WhatsApp items with page: %s, limit: %s",
            request.query_params.page,
            request.query_params.limit,
        )

        return self._request(method="GET", path="whatsapp/items", params=params)

    def get_whatsapp_item(self, request: WhatsAppItemGetRequest) -> APIResponse:
        """
        Get a single WhatsApp item with its recipient and status timeline.

        Args:
            request: WhatsAppItemGetRequest object containing WhatsApp item ID

        Returns:
            APIResponse: Response containing WhatsApp item details
        """
        self.logger.debug("Getting WhatsApp item: %s", request.whatsapp_item_id)

        return self._request(
            method="GET", path=f"whatsapp/items/{request.whatsapp_item_id}"
        )
