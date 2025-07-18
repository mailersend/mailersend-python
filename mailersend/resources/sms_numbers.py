from .base import BaseResource
from ..models.sms_numbers import (
    SmsNumbersListRequest, SmsNumberGetRequest, SmsNumberUpdateRequest, SmsNumberDeleteRequest
)
from ..models.base import APIResponse
from ..exceptions import ValidationError


class SmsNumbers(BaseResource):
    """
    Client for interacting with the MailerSend SMS Phone Numbers API.
    """

    def list(self, request: SmsNumbersListRequest) -> APIResponse:
        """
        Get a list of SMS phone numbers.
        
        Args:
            request: SmsNumbersListRequest with query parameters
            
        Returns:
            APIResponse with SMS phone numbers list and metadata
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to list SMS phone numbers")
        
        if not request:
            self.logger.error("No SmsNumbersListRequest object provided")
            raise ValidationError("SmsNumbersListRequest must be provided")
        
        if not isinstance(request, SmsNumbersListRequest):
            self.logger.error("Invalid SmsNumbersListRequest object provided")
            raise ValidationError("SmsNumbersListRequest must be provided")
        
        # Convert to query parameters
        params = request.to_query_params()
        
        self.logger.info(f"Listing SMS phone numbers with params: {params}")
        
        response = self.client.request("GET", "sms-numbers", params=params)
        
        return self._create_response(response)

    def get(self, request: SmsNumberGetRequest) -> APIResponse:
        """
        Get a specific SMS phone number.
        
        Args:
            request: SmsNumberGetRequest with SMS number ID
            
        Returns:
            APIResponse with SMS phone number data and metadata
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to get SMS phone number")
        
        if not request:
            self.logger.error("No SmsNumberGetRequest object provided")
            raise ValidationError("SmsNumberGetRequest must be provided")
        
        if not isinstance(request, SmsNumberGetRequest):
            self.logger.error("Invalid SmsNumberGetRequest object provided")
            raise ValidationError("SmsNumberGetRequest must be provided")
        
        self.logger.info(f"Getting SMS phone number: {request.sms_number_id}")
        
        response = self.client.request("GET", f"sms-numbers/{request.sms_number_id}")
        
        return self._create_response(response)

    def update(self, request: SmsNumberUpdateRequest) -> APIResponse:
        """
        Update a specific SMS phone number.
        
        Args:
            request: SmsNumberUpdateRequest with SMS number ID and update data
            
        Returns:
            APIResponse with updated SMS phone number data and metadata
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to update SMS phone number")
        
        if not request:
            self.logger.error("No SmsNumberUpdateRequest object provided")
            raise ValidationError("SmsNumberUpdateRequest must be provided")
        
        if not isinstance(request, SmsNumberUpdateRequest):
            self.logger.error("Invalid SmsNumberUpdateRequest object provided")
            raise ValidationError("SmsNumberUpdateRequest must be provided")
        
        # Convert to JSON payload
        payload = request.to_json()
        
        self.logger.info(f"Updating SMS phone number: {request.sms_number_id}")
        self.logger.debug(f"Update payload: {payload}")
        
        response = self.client.request("PUT", f"sms-numbers/{request.sms_number_id}", body=payload)
        
        return self._create_response(response)

    def delete(self, request: SmsNumberDeleteRequest) -> APIResponse:
        """
        Delete a specific SMS phone number.
        
        Args:
            request: SmsNumberDeleteRequest with SMS number ID
            
        Returns:
            APIResponse with deletion confirmation and metadata
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to delete SMS phone number")
        
        if not request:
            self.logger.error("No SmsNumberDeleteRequest object provided")
            raise ValidationError("SmsNumberDeleteRequest must be provided")
        
        if not isinstance(request, SmsNumberDeleteRequest):
            self.logger.error("Invalid SmsNumberDeleteRequest object provided")
            raise ValidationError("SmsNumberDeleteRequest must be provided")
        
        self.logger.info(f"Deleting SMS phone number: {request.sms_number_id}")
        
        response = self.client.request("DELETE", f"sms-numbers/{request.sms_number_id}")
        
        return self._create_response(response)