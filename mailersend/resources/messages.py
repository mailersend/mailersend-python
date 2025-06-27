from typing import Dict, Any, Optional

from .base import BaseResource
from ..models.messages import MessagesListRequest, MessageGetRequest
from ..models.base import APIResponse
from ..exceptions import ValidationError


class Messages(BaseResource):
    """
    Client for interacting with the MailerSend Messages API.
    
    Provides methods for retrieving message information.
    """

    def list_messages(self, request: Optional[MessagesListRequest] = None) -> APIResponse:
        """
        Retrieve a list of messages.
        
        Args:
            request: Optional MessagesListRequest with pagination options
            
        Returns:
            APIResponse with list of messages
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Retrieving messages list")
        
        # Convert to query parameters
        params = {}
        if request:
            params = self._build_query_params(request)
        
        self.logger.info("Requesting messages list")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", "messages", params=params)
        
        return self._create_response(response)

    def get_message(self, request: MessageGetRequest) -> APIResponse:
        """
        Retrieve information about a single message.
        
        Args:
            request: MessageGetRequest with message ID
            
        Returns:
            APIResponse with message information
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        if not request:
            self.logger.error("No MessageGetRequest object provided")
            raise ValidationError("MessageGetRequest must be provided")
        
        self.logger.debug(f"Retrieving message: {request.message_id}")
        self.logger.info(f"Requesting message information for: {request.message_id}")
        
        response = self.client.request("GET", f"messages/{request.message_id}")
        
        return self._create_response(response)

    def _build_query_params(self, request) -> Dict[str, Any]:
        """
        Convert request model to query parameters dictionary.
        
        Args:
            request: Request model to convert
            
        Returns:
            Dictionary of query parameters
        """
        params = {}
        
        # Handle pagination parameters
        if hasattr(request, 'page') and request.page is not None:
            params['page'] = request.page
        if hasattr(request, 'limit') and request.limit is not None:
            params['limit'] = request.limit
            
        return params 