"""WhatsApp Templates resource."""

from .base import BaseResource
from ..models.whatsapp_templates import (
    WhatsAppTemplatesListRequest,
    WhatsAppTemplateGetRequest,
)
from ..models.base import APIResponse


class WhatsAppTemplates(BaseResource):
    """WhatsApp Templates resource for MailerSend API."""

    def list_whatsapp_templates(
        self, request: WhatsAppTemplatesListRequest
    ) -> APIResponse:
        """
        List WhatsApp templates.

        Args:
            request: WhatsAppTemplatesListRequest object containing query parameters

        Returns:
            APIResponse: Response containing list of WhatsApp templates
        """
        params = request.to_query_params()

        self.logger.debug(
            "Listing WhatsApp templates with page: %s, limit: %s",
            request.query_params.page,
            request.query_params.limit,
        )

        return self._request(method="GET", path="whatsapp/templates", params=params)

    def get_whatsapp_template(self, request: WhatsAppTemplateGetRequest) -> APIResponse:
        """
        Get a single WhatsApp template.

        Args:
            request: WhatsAppTemplateGetRequest object containing WhatsApp template ID

        Returns:
            APIResponse: Response containing WhatsApp template details
        """
        self.logger.debug("Getting WhatsApp template: %s", request.whatsapp_template_id)

        return self._request(
            method="GET", path=f"whatsapp/templates/{request.whatsapp_template_id}"
        )
