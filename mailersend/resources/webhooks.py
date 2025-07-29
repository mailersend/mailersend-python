"""Webhooks resource for MailerSend SDK."""

import logging
from typing import Optional, Dict, Any

from .base import BaseResource
from ..models.base import APIResponse
from ..models.webhooks import (
    WebhooksListRequest,
    WebhookGetRequest,
    WebhookCreateRequest,
    WebhookUpdateRequest,
    WebhookDeleteRequest,
    WebhooksListResponse,
    WebhookResponse,
)
from ..exceptions import ValidationError

logger = logging.getLogger(__name__)


class Webhooks(BaseResource):
    """Webhooks API resource for managing webhooks."""

    def list_webhooks(self, request: WebhooksListRequest) -> APIResponse:
        """List webhooks for a domain.

        Args:
            request: The webhooks list request

        Returns:
            APIResponse with WebhooksListResponse data

        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting list_webhooks operation")

        # Validate request
        if not request:
            logger.error("WebhooksListRequest is required")
            raise ValidationError("WebhooksListRequest must be provided")

        if not isinstance(request, WebhooksListRequest):
            logger.error(f"Expected WebhooksListRequest, got {type(request).__name__}")
            raise ValidationError("request must be a WebhooksListRequest instance")

        logger.debug(f"Webhooks list request: {request}")

        # Extract query parameters
        params = request.to_query_params()

        logger.info(f"Listing webhooks with params: {params}")

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

        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting get_webhook operation")

        # Validate request
        if not request:
            logger.error("WebhookGetRequest is required")
            raise ValidationError("WebhookGetRequest must be provided")

        if not isinstance(request, WebhookGetRequest):
            logger.error(f"Expected WebhookGetRequest, got {type(request).__name__}")
            raise ValidationError("request must be a WebhookGetRequest instance")

        logger.debug(f"Webhook get request: {request}")

        logger.info(f"Getting webhook: {request.webhook_id}")

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

        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting create_webhook operation")

        # Validate request
        if not request:
            logger.error("WebhookCreateRequest is required")
            raise ValidationError("WebhookCreateRequest must be provided")

        if not isinstance(request, WebhookCreateRequest):
            logger.error(f"Expected WebhookCreateRequest, got {type(request).__name__}")
            raise ValidationError("request must be a WebhookCreateRequest instance")

        logger.debug(f"Webhook create request: {request}")

        # Prepare request body
        data: Dict[str, Any] = {
            "url": request.url,
            "name": request.name,
            "events": request.events,
            "domain_id": request.domain_id,
        }

        if request.enabled is not None:
            data["enabled"] = request.enabled

        logger.info(f"Creating webhook: {request.name}")

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

        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting update_webhook operation")

        # Validate request
        if not request:
            logger.error("WebhookUpdateRequest is required")
            raise ValidationError("WebhookUpdateRequest must be provided")

        if not isinstance(request, WebhookUpdateRequest):
            logger.error(f"Expected WebhookUpdateRequest, got {type(request).__name__}")
            raise ValidationError("request must be a WebhookUpdateRequest instance")

        logger.debug(f"Webhook update request: {request}")

        # Prepare request body - only include non-None fields
        data: Dict[str, Any] = {}

        if request.url is not None:
            data["url"] = request.url
        if request.name is not None:
            data["name"] = request.name
        if request.events is not None:
            data["events"] = request.events
        if request.enabled is not None:
            data["enabled"] = request.enabled

        logger.info(f"Updating webhook: {request.webhook_id}")

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

        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting delete_webhook operation")

        # Validate request
        if not request:
            logger.error("WebhookDeleteRequest is required")
            raise ValidationError("WebhookDeleteRequest must be provided")

        if not isinstance(request, WebhookDeleteRequest):
            logger.error(f"Expected WebhookDeleteRequest, got {type(request).__name__}")
            raise ValidationError("request must be a WebhookDeleteRequest instance")

        logger.debug(f"Webhook delete request: {request}")

        logger.info(f"Deleting webhook: {request.webhook_id}")

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint=f"webhooks/{request.webhook_id}"
        )

        # Create standardized response
        return self._create_response(response)
