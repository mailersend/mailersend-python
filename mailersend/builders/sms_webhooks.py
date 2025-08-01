"""SMS Webhooks builder for MailerSend SDK."""

from typing import Optional, List

from ..models.sms_webhooks import (
    SmsWebhooksListRequest,
    SmsWebhooksListQueryParams,
    SmsWebhookGetRequest,
    SmsWebhookCreateRequest,
    SmsWebhookUpdateRequest,
    SmsWebhookDeleteRequest,
    SmsWebhookEvent,
)


class SmsWebhooksBuilder:
    """Builder for SMS Webhooks API requests."""

    def __init__(self) -> None:
        """Initialize the SmsWebhooksBuilder."""
        self._sms_number_id: Optional[str] = None
        self._sms_webhook_id: Optional[str] = None
        self._url: Optional[str] = None
        self._name: Optional[str] = None
        self._events: Optional[List[SmsWebhookEvent]] = None
        self._enabled: Optional[bool] = None

    def sms_number_id(self, sms_number_id: str) -> "SmsWebhooksBuilder":
        """
        Set the SMS number ID for listing or creating webhooks.

        Args:
            sms_number_id: SMS number ID

        Returns:
            SmsWebhooksBuilder: Builder instance for method chaining
        """
        self._sms_number_id = sms_number_id
        return self

    def sms_webhook_id(self, sms_webhook_id: str) -> "SmsWebhooksBuilder":
        """
        Set the SMS webhook ID for get, update, and delete operations.

        Args:
            sms_webhook_id: SMS webhook ID

        Returns:
            SmsWebhooksBuilder: Builder instance for method chaining
        """
        self._sms_webhook_id = sms_webhook_id
        return self

    def url(self, url: str) -> "SmsWebhooksBuilder":
        """
        Set the webhook URL for create and update operations.

        Args:
            url: Webhook URL

        Returns:
            SmsWebhooksBuilder: Builder instance for method chaining
        """
        self._url = url
        return self

    def name(self, name: str) -> "SmsWebhooksBuilder":
        """
        Set the webhook name for create and update operations.

        Args:
            name: Webhook name

        Returns:
            SmsWebhooksBuilder: Builder instance for method chaining
        """
        self._name = name
        return self

    def events(self, events: List[SmsWebhookEvent]) -> "SmsWebhooksBuilder":
        """
        Set the events list for create and update operations.

        Args:
            events: List of SMS webhook events

        Returns:
            SmsWebhooksBuilder: Builder instance for method chaining
        """
        self._events = events
        return self

    def add_event(self, event: SmsWebhookEvent) -> "SmsWebhooksBuilder":
        """
        Add a single event to the events list.

        Args:
            event: SMS webhook event to add

        Returns:
            SmsWebhooksBuilder: Builder instance for method chaining
        """
        if self._events is None:
            self._events = []
        if event not in self._events:
            self._events.append(event)
        return self

    def enabled(self, enabled: bool) -> "SmsWebhooksBuilder":
        """
        Set the enabled status for create and update operations.

        Args:
            enabled: Whether webhook is enabled

        Returns:
            SmsWebhooksBuilder: Builder instance for method chaining
        """
        self._enabled = enabled
        return self

    def build_list_request(self) -> SmsWebhooksListRequest:
        """
        Build a request for listing SMS webhooks.

        Returns:
            SmsWebhooksListRequest: Request object for listing SMS webhooks

        Raises:
            ValueError: If SMS number ID is not set
        """
        if self._sms_number_id is None:
            raise ValueError("SMS number ID is required for list request")

        query_params = SmsWebhooksListQueryParams(sms_number_id=self._sms_number_id)
        return SmsWebhooksListRequest(query_params=query_params)

    def build_get_request(self) -> SmsWebhookGetRequest:
        """
        Build a request for getting a single SMS webhook.

        Returns:
            SmsWebhookGetRequest: Request object for getting SMS webhook

        Raises:
            ValueError: If SMS webhook ID is not set
        """
        if self._sms_webhook_id is None:
            raise ValueError("SMS webhook ID is required for get request")

        return SmsWebhookGetRequest(sms_webhook_id=self._sms_webhook_id)

    def build_create_request(self) -> SmsWebhookCreateRequest:
        """
        Build a request for creating an SMS webhook.

        Returns:
            SmsWebhookCreateRequest: Request object for creating SMS webhook

        Raises:
            ValueError: If required fields are not set
        """
        if self._url is None:
            raise ValueError("URL is required for create request")
        if self._name is None:
            raise ValueError("Name is required for create request")
        if self._events is None or len(self._events) == 0:
            raise ValueError("Events list is required for create request")
        if self._sms_number_id is None:
            raise ValueError("SMS number ID is required for create request")

        # Only include enabled if it's explicitly set
        kwargs = {
            "url": self._url,
            "name": self._name,
            "events": self._events,
            "sms_number_id": self._sms_number_id,
        }
        if self._enabled is not None:
            kwargs["enabled"] = self._enabled

        return SmsWebhookCreateRequest(**kwargs)

    def build_update_request(self) -> SmsWebhookUpdateRequest:
        """
        Build a request for updating an SMS webhook.

        Returns:
            SmsWebhookUpdateRequest: Request object for updating SMS webhook

        Raises:
            ValueError: If SMS webhook ID is not set
        """
        if self._sms_webhook_id is None:
            raise ValueError("SMS webhook ID is required for update request")

        return SmsWebhookUpdateRequest(
            sms_webhook_id=self._sms_webhook_id,
            url=self._url,
            name=self._name,
            events=self._events,
            enabled=self._enabled,
        )

    def build_delete_request(self) -> SmsWebhookDeleteRequest:
        """
        Build a request for deleting an SMS webhook.

        Returns:
            SmsWebhookDeleteRequest: Request object for deleting SMS webhook

        Raises:
            ValueError: If SMS webhook ID is not set
        """
        if self._sms_webhook_id is None:
            raise ValueError("SMS webhook ID is required for delete request")

        return SmsWebhookDeleteRequest(sms_webhook_id=self._sms_webhook_id)
