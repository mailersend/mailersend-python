"""SMS Messages resource."""

import logging
from typing import TYPE_CHECKING

from mailersend.models.sms_messages import (
    SmsMessagesListRequest, SmsMessageGetRequest,
    SmsMessagesListResponse, SmsMessageResponse
)
from mailersend.models.base import APIResponse
from .base import BaseResource

if TYPE_CHECKING:
    from mailersend.client import Client

logger = logging.getLogger(__name__)


class SmsMessages(BaseResource):
    """SMS Messages resource for MailerSend API."""

    def list_sms_messages(self, request: SmsMessagesListRequest) -> APIResponse:
        """
        List SMS messages.
        
        Args:
            request: SmsMessagesListRequest object containing query parameters
            
        Returns:
            APIResponse: Response containing list of SMS messages
        """
        params = request.to_query_params()
        
        logger.info(f"Listing SMS messages with page: {request.query_params.page}, limit: {request.query_params.limit}")
        
        response = self.client.request(
            method="GET",
            path="sms-messages",
            params=params
        )
        
        return self._create_response(response, SmsMessagesListResponse)

    def get_sms_message(self, request: SmsMessageGetRequest) -> APIResponse:
        """
        Get a single SMS message.
        
        Args:
            request: SmsMessageGetRequest object containing SMS message ID
            
        Returns:
            APIResponse: Response containing SMS message details
        """
        logger.info(f"Getting SMS message: {request.sms_message_id}")
        
        response = self.client.request(
            method="GET",
            path=f"sms-messages/{request.sms_message_id}"
        )
        
        return self._create_response(response, SmsMessageResponse) 