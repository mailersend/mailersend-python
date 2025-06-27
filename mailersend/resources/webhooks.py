"""Webhooks API resource for MailerSend SDK."""

import logging
from typing import Dict, Any

from pydantic import ValidationError

from ..models.base import APIResponse
from ..models.webhooks import (
    WebhookCreateRequest,
    WebhookDeleteRequest,
    WebhookGetRequest,
    WebhookUpdateRequest,
    WebhooksListRequest,
)

logger = logging.getLogger(__name__)


class Webhooks:
    """Webhooks API resource for managing webhooks."""
    
    def __init__(self, client) -> None:
        """Initialize the Webhooks resource.
        
        Args:
            client: The MailerSend client instance
        """
        self.client = client
    
    def list_webhooks(self, request: WebhooksListRequest) -> APIResponse:
        """List webhooks for a domain.
        
        Args:
            request: The webhooks list request
            
        Returns:
            APIResponse: The API response
            
        Raises:
            ValidationError: If request validation fails
        """
        try:
            logger.info("Listing webhooks for domain: %s", request.domain_id)
            
            params = {"domain_id": request.domain_id}
            
            return self.client.request(
                method="GET",
                endpoint="webhooks",
                params=params
            )
            
        except ValidationError as e:
            logger.error("Validation error in list_webhooks: %s", e)
            raise
    
    def get_webhook(self, request: WebhookGetRequest) -> APIResponse:
        """Get a single webhook by ID.
        
        Args:
            request: The webhook get request
            
        Returns:
            APIResponse: The API response
            
        Raises:
            ValidationError: If request validation fails
        """
        try:
            logger.info("Getting webhook: %s", request.webhook_id)
            
            return self.client.request(
                method="GET",
                endpoint=f"webhooks/{request.webhook_id}"
            )
            
        except ValidationError as e:
            logger.error("Validation error in get_webhook: %s", e)
            raise
    
    def create_webhook(self, request: WebhookCreateRequest) -> APIResponse:
        """Create a new webhook.
        
        Args:
            request: The webhook create request
            
        Returns:
            APIResponse: The API response
            
        Raises:
            ValidationError: If request validation fails
        """
        try:
            logger.info("Creating webhook: %s", request.name)
            
            data: Dict[str, Any] = {
                "url": request.url,
                "name": request.name,
                "events": request.events,
                "domain_id": request.domain_id,
            }
            
            if request.enabled is not None:
                data["enabled"] = request.enabled
            
            return self.client.request(
                method="POST",
                endpoint="webhooks",
                json=data
            )
            
        except ValidationError as e:
            logger.error("Validation error in create_webhook: %s", e)
            raise
    
    def update_webhook(self, request: WebhookUpdateRequest) -> APIResponse:
        """Update an existing webhook.
        
        Args:
            request: The webhook update request
            
        Returns:
            APIResponse: The API response
            
        Raises:
            ValidationError: If request validation fails
        """
        try:
            logger.info("Updating webhook: %s", request.webhook_id)
            
            data: Dict[str, Any] = {}
            
            if request.url is not None:
                data["url"] = request.url
            if request.name is not None:
                data["name"] = request.name
            if request.events is not None:
                data["events"] = request.events
            if request.enabled is not None:
                data["enabled"] = request.enabled
            
            return self.client.request(
                method="PUT",
                endpoint=f"webhooks/{request.webhook_id}",
                json=data
            )
            
        except ValidationError as e:
            logger.error("Validation error in update_webhook: %s", e)
            raise
    
    def delete_webhook(self, request: WebhookDeleteRequest) -> APIResponse:
        """Delete a webhook.
        
        Args:
            request: The webhook delete request
            
        Returns:
            APIResponse: The API response
            
        Raises:
            ValidationError: If request validation fails
        """
        try:
            logger.info("Deleting webhook: %s", request.webhook_id)
            
            return self.client.request(
                method="DELETE",
                endpoint=f"webhooks/{request.webhook_id}"
            )
            
        except ValidationError as e:
            logger.error("Validation error in delete_webhook: %s", e)
            raise 