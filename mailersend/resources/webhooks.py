"""Webhooks resource for MailerSend SDK."""

from .base import BaseResource
from ..models.base import APIResponse
from ..models.webhooks import (
    WebhooksListRequest,
    WebhookGetRequest,
    WebhookCreateRequest,
    WebhookUpdateRequest,
    WebhookDeleteRequest,
)

class Webhooks(BaseResource):
    """Webhooks API resource for managing webhooks."""

    def list_webhooks(self, request: WebhooksListRequest) -> APIResponse:
        """List webhooks for a domain.

        Args:
            request: The webhooks list request

        Returns:
            APIResponse with WebhooksListResponse data
        """
        self.logger.debug("Starting list_webhooks operation")
        self.logger.debug("Webhooks list request: %s", request)

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug("Listing webhooks with params: %s", params)

        # Make API call
        response = self.client.request(method="GET", endpoint="webhooks", params=params)

        # Create standardized response
        return self._create_response(response)

    def get_webhook(self, request: WebhookGetRequest) -> APIResponse:
        """Get a single webhook by ID.

        Args:
            request: The webhook get request

        Returns:
            APIResponse with WebhookResponse data
        """
        self.logger.debug("Starting get_webhook operation")
        self.logger.debug("Webhook get request: %s", request)

        # Make API call
        response = self.client.request(
            method="GET", endpoint=f"webhooks/{request.webhook_id}"
        )

        # Create standardized response
        return self._create_response(response)

    def create_webhook(self, request: WebhookCreateRequest) -> APIResponse:
        """Create a new webhook.

        Args:
            request: The webhook create request

        Returns:
            APIResponse with WebhookResponse data
        """
        self.logger.debug("Starting create_webhook operation")

        # Prepare request body
        data = request.model_dump(exclude_none=True)

        self.logger.debug("Creating webhook: %s", request.name)

        # Make API call
        response = self.client.request(method="POST", endpoint="webhooks", body=data)

        # Create standardized response
        return self._create_response(response)

    def update_webhook(self, request: WebhookUpdateRequest) -> APIResponse:
        """Update an existing webhook.

        Args:
            request: The webhook update request

        Returns:
            APIResponse with WebhookResponse data
        """
        self.logger.debug("Starting update_webhook operation")
        self.logger.debug("Webhook update request: %s", request)

        # Prepare request body - exclude webhook_id (goes in URL) and None fields
        data = request.model_dump(exclude_none=True, exclude={"webhook_id"})

        self.logger.debug("Updating webhook: %s", data)

        # Make API call
        response = self.client.request(
            method="PUT", endpoint=f"webhooks/{request.webhook_id}", body=data
        )

        # Create standardized response
        return self._create_response(response)

    def delete_webhook(self, request: WebhookDeleteRequest) -> APIResponse:
        """Delete a webhook.

        Args:
            request: The webhook delete request

        Returns:
            APIResponse with empty data
        """
        self.logger.debug("Starting delete_webhook operation")
        self.logger.debug("Webhook delete request: %s", request)

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint=f"webhooks/{request.webhook_id}"
        )

        # Create standardized response
        return self._create_response(response)
