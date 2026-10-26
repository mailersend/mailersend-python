"""WhatsApp Templates builder for MailerSend SDK."""

from typing import Optional, Union

from ..models.whatsapp_templates import (
    WhatsAppTemplatesListRequest,
    WhatsAppTemplatesListQueryParams,
    WhatsAppTemplateGetRequest,
    WhatsAppTemplateStatus,
    WhatsAppTemplateCategory,
)


class WhatsAppTemplatesBuilder:
    """Builder for WhatsApp Templates API requests."""

    def __init__(self) -> None:
        """Initialize the WhatsAppTemplatesBuilder."""
        self._whatsapp_account_id: Optional[str] = None
        self._status: Optional[Union[WhatsAppTemplateStatus, str]] = None
        self._category: Optional[Union[WhatsAppTemplateCategory, str]] = None
        self._language: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._whatsapp_template_id: Optional[str] = None

    def whatsapp_account_id(
        self, whatsapp_account_id: str
    ) -> "WhatsAppTemplatesBuilder":
        """
        Set the WhatsApp account (sender) ID filter.

        Args:
            whatsapp_account_id: MailerSend sender ID the templates belong to

        Returns:
            WhatsAppTemplatesBuilder: Builder instance for method chaining
        """
        self._whatsapp_account_id = whatsapp_account_id
        return self

    def status(
        self, status: Union[WhatsAppTemplateStatus, str]
    ) -> "WhatsAppTemplatesBuilder":
        """
        Set the template status filter. Only approved templates can be sent.

        Args:
            status: Template review status (e.g. "approved")

        Returns:
            WhatsAppTemplatesBuilder: Builder instance for method chaining
        """
        self._status = status
        return self

    def category(
        self, category: Union[WhatsAppTemplateCategory, str]
    ) -> "WhatsAppTemplatesBuilder":
        """
        Set the template category filter.

        Args:
            category: UTILITY, AUTHENTICATION or MARKETING

        Returns:
            WhatsAppTemplatesBuilder: Builder instance for method chaining
        """
        self._category = category
        return self

    def language(self, language: str) -> "WhatsAppTemplatesBuilder":
        """
        Set the template language filter.

        Args:
            language: Template language code (e.g. "en_US")

        Returns:
            WhatsAppTemplatesBuilder: Builder instance for method chaining
        """
        self._language = language
        return self

    def page(self, page: int) -> "WhatsAppTemplatesBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number (1-100)

        Returns:
            WhatsAppTemplatesBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "WhatsAppTemplatesBuilder":
        """
        Set the limit for number of results per page.

        Args:
            limit: Number of results per page (1-100)

        Returns:
            WhatsAppTemplatesBuilder: Builder instance for method chaining
        """
        self._limit = limit
        return self

    def whatsapp_template_id(
        self, whatsapp_template_id: str
    ) -> "WhatsAppTemplatesBuilder":
        """
        Set the WhatsApp template ID for get operations.

        Args:
            whatsapp_template_id: WhatsApp template ID

        Returns:
            WhatsAppTemplatesBuilder: Builder instance for method chaining
        """
        self._whatsapp_template_id = whatsapp_template_id
        return self

    def build_list_request(self) -> WhatsAppTemplatesListRequest:
        """
        Build a request for listing WhatsApp templates.

        Returns:
            WhatsAppTemplatesListRequest: Request object for listing WhatsApp templates
        """
        params = {}

        if self._whatsapp_account_id is not None:
            params["whatsapp_account_id"] = self._whatsapp_account_id
        if self._status is not None:
            params["status"] = self._status
        if self._category is not None:
            params["category"] = self._category
        if self._language is not None:
            params["language"] = self._language
        if self._page is not None:
            params["page"] = self._page
        if self._limit is not None:
            params["limit"] = self._limit

        return WhatsAppTemplatesListRequest(
            query_params=WhatsAppTemplatesListQueryParams(**params)
        )

    def build_get_request(self) -> WhatsAppTemplateGetRequest:
        """
        Build a request for getting a single WhatsApp template.

        Returns:
            WhatsAppTemplateGetRequest: Request object for getting WhatsApp template

        Raises:
            ValueError: If WhatsApp template ID is not set
        """
        if self._whatsapp_template_id is None:
            raise ValueError("WhatsApp template ID is required for get request")

        return WhatsAppTemplateGetRequest(
            whatsapp_template_id=self._whatsapp_template_id
        )
