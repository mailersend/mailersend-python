from typing import Dict, Any, Optional

from .base import BaseResource
from ..models.schedules import SchedulesListRequest, ScheduleGetRequest, ScheduleDeleteRequest
from ..models.base import APIResponse
from ..exceptions import ValidationError


class Schedules(BaseResource):
    """
    Client for interacting with the MailerSend Message Schedules API.
    
    Provides methods for managing scheduled messages.
    """

    def list_schedules(self, request: Optional[SchedulesListRequest] = None) -> APIResponse:
        """
        Retrieve a list of scheduled messages.
        
        Args:
            request: Optional SchedulesListRequest with filtering and pagination options
            
        Returns:
            APIResponse with list of scheduled messages
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Retrieving scheduled messages list")
        
        # Convert to query parameters
        params = {}
        if request:
            params = self._build_query_params(request)
        
        self.logger.info("Requesting scheduled messages list")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", "message-schedules", params=params)
        
        return self._create_response(response)

    def get_schedule(self, request: ScheduleGetRequest) -> APIResponse:
        """
        Retrieve information about a single scheduled message.
        
        Args:
            request: ScheduleGetRequest with message ID
            
        Returns:
            APIResponse with scheduled message information
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        if not request:
            self.logger.error("No ScheduleGetRequest object provided")
            raise ValidationError("ScheduleGetRequest must be provided")
        
        self.logger.debug(f"Retrieving scheduled message: {request.message_id}")
        self.logger.info(f"Requesting scheduled message information for: {request.message_id}")
        
        response = self.client.request("GET", f"message-schedules/{request.message_id}")
        
        return self._create_response(response)

    def delete_schedule(self, request: ScheduleDeleteRequest) -> APIResponse:
        """
        Delete a scheduled message.
        
        Args:
            request: ScheduleDeleteRequest with message ID to delete
            
        Returns:
            APIResponse (204 No Content on success)
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        if not request:
            self.logger.error("No ScheduleDeleteRequest object provided")
            raise ValidationError("ScheduleDeleteRequest must be provided")
        
        self.logger.debug(f"Deleting scheduled message: {request.message_id}")
        self.logger.info(f"Deleting scheduled message: {request.message_id}")
        
        response = self.client.request("DELETE", f"message-schedules/{request.message_id}")
        
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
        
        # Handle filtering parameters
        if hasattr(request, 'domain_id') and request.domain_id is not None:
            params['domain_id'] = request.domain_id
        if hasattr(request, 'status') and request.status is not None:
            params['status'] = request.status
            
        # Handle pagination parameters
        if hasattr(request, 'page') and request.page is not None:
            params['page'] = request.page
        if hasattr(request, 'limit') and request.limit is not None:
            params['limit'] = request.limit
            
        return params 