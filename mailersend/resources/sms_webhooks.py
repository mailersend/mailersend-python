"""SMS Webhooks resource."""

from .base import BaseResource
from ..models.sms_webhooks import (
    SmsWebhooksListRequest,
    SmsWebhookGetRequest,
    SmsWebhookCreateRequest,
    SmsWebhookUpdateRequest,
    SmsWebhookDeleteRequest
)
from ..models.base import APIResponse


class SmsWebhooks(BaseResource):
    """SMS Webhooks resource for MailerSend API."""

    def list_sms_webhooks(self, request: SmsWebhooksListRequest) -> APIResponse:
        """
        List SMS webhooks.
        
        Args:
            request: SmsWebhooksListRequest object containing query parameters
            
        Returns:
            APIResponse: Response containing list of SMS webhooks
        """
        params = request.to_query_params()
        
        self.logger.info(f"Listing SMS webhooks for SMS number: {request.query_params.sms_number_id}")
        
        response = self.client.request(
            method='GET',
            endpoint='sms-webhooks',
            params=params
        )
        
        return self._create_response(response)

    def get_sms_webhook(self, request: SmsWebhookGetRequest) -> APIResponse:
        """
        Get a single SMS webhook.
        
        Args:
            request: SmsWebhookGetRequest object containing SMS webhook ID
            
        Returns:
            APIResponse: Response containing SMS webhook details
        """
        self.logger.info(f"Getting SMS webhook: {request.sms_webhook_id}")
        
        response = self.client.request(
            method='GET',
            endpoint=f'sms-webhooks/{request.sms_webhook_id}'
        )
        
        return self._create_response(response)

    def create_sms_webhook(self, request: SmsWebhookCreateRequest) -> APIResponse:
        """
        Create an SMS webhook.
        
        Args:
            request: SmsWebhookCreateRequest object containing webhook data
            
        Returns:
            APIResponse: Response containing created SMS webhook
        """
        self.logger.info(f"Creating SMS webhook: {request.name} for SMS number: {request.sms_number_id}")
        
        response = self.client.request(
            method='POST',
            endpoint='sms-webhooks',
            body=request.to_request_body()
        )
        
        return self._create_response(response)

    def update_sms_webhook(self, request: SmsWebhookUpdateRequest) -> APIResponse:
        """
        Update an SMS webhook.
        
        Args:
            request: SmsWebhookUpdateRequest object containing SMS webhook ID and update data
            
        Returns:
            APIResponse: Response containing updated SMS webhook
        """
        self.logger.info(f"Updating SMS webhook: {request.sms_webhook_id}")
        
        response = self.client.request(
            method='PUT',
            endpoint=f'sms-webhooks/{request.sms_webhook_id}',
            body=request.to_request_body()
        )
        
        return self._create_response(response)

    def delete_sms_webhook(self, request: SmsWebhookDeleteRequest) -> APIResponse:
        """
        Delete an SMS webhook.
        
        Args:
            request: SmsWebhookDeleteRequest object containing SMS webhook ID
            
        Returns:
            APIResponse: Response confirming deletion
        """
        self.logger.info(f"Deleting SMS webhook: {request.sms_webhook_id}")
        
        response = self.client.request(
            method='DELETE',
            endpoint=f'sms-webhooks/{request.sms_webhook_id}'
        )
        
        return self._create_response(response) 