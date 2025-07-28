from typing import Union

from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.inbound import (
    InboundListRequest,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
    InboundListResponse,
    InboundResponse
)
from mailersend.models.base import APIResponse
from mailersend.resources.base import BaseResource


class InboundResource(BaseResource):
    """Resource for managing inbound routes."""

    def list(self, request: InboundListRequest) -> APIResponse:
        """
        Get a list of inbound routes.
        
        Args:
            request: The inbound list request containing filtering and pagination parameters
            
        Returns:
            APIResponse containing the inbound routes list response
            
        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, InboundListRequest):
            raise MailerSendValidationError("Request must be an instance of InboundListRequest")
        
        self.logger.debug("Preparing to list inbound routes with query parameters")
        
        # Extract query parameters
        params = request.to_query_params()
        
        self.logger.debug(f"Making API request to list inbound routes with params: {params}")
        
        # Make API request
        response = self.client.request(
            method='GET',
            endpoint='inbound',
            params=params if params else None
        )
        
        return self._create_response(response, InboundListResponse)

    def get(self, request: InboundGetRequest) -> APIResponse:
        """
        Get a single inbound route by ID.
        
        Args:
            request: The inbound get request with inbound ID
            
        Returns:
            APIResponse containing the inbound route data
            
        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, InboundGetRequest):
            raise MailerSendValidationError("Request must be an instance of InboundGetRequest")
        
        self.logger.debug(f"Preparing to get inbound route with ID: {request.inbound_id}")
        
        # Make API request
        response = self.client.request(
            method='GET',
            endpoint=f'inbound/{request.inbound_id}'
        )
        
        return self._create_response(response, InboundResponse)

    def create(self, request: InboundCreateRequest) -> APIResponse:
        """
        Create a new inbound route.
        
        Args:
            request: The inbound create request with all required data
            
        Returns:
            APIResponse containing the created inbound route response
            
        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, InboundCreateRequest):
            raise MailerSendValidationError("Request must be an instance of InboundCreateRequest")
        
        self.logger.debug("Preparing to create inbound route")
        
        # Build request body with special handling for complex fields
        data = request.model_dump(by_alias=True, exclude_none=True)
        
        # Handle complex nested objects that need special serialization
        if 'catch_filter' in data:
            data['catch_filter'] = [filter_group for filter_group in data['catch_filter']]
        if 'match_filter' in data:
            data['match_filter'] = [filter_group for filter_group in data['match_filter']]
        if 'forwards' in data:
            # Exclude 'id' from forwards for creation
            data['forwards'] = [
                {k: v for k, v in forward.items() if k != 'id'}
                for forward in data['forwards']
            ]
        
        self.logger.debug(f"Making API request to create inbound route with data keys: {list(data.keys())}")
        
        # Make API request
        response = self.client.request(
            method='POST',
            endpoint='inbound',
            json=data
        )
        
        return self._create_response(response, InboundResponse)

    def update(self, request: InboundUpdateRequest) -> APIResponse:
        """
        Update an existing inbound route.
        
        Args:
            request: The inbound update request with inbound ID and update data
            
        Returns:
            APIResponse containing the updated inbound route response
            
        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, InboundUpdateRequest):
            raise MailerSendValidationError("Request must be an instance of InboundUpdateRequest")
        
        self.logger.debug(f"Preparing to update inbound route with ID: {request.inbound_id}")
        
        # Build request body, excluding inbound_id (goes in URL)
        data = request.model_dump(by_alias=True, exclude_none=True, exclude={'inbound_id'})
        
        # Handle complex nested objects that need special serialization
        if 'catch_filter' in data:
            data['catch_filter'] = [filter_group for filter_group in data['catch_filter']]
        if 'match_filter' in data:
            data['match_filter'] = [filter_group for filter_group in data['match_filter']]
        if 'forwards' in data:
            # Exclude 'id' from forwards for update
            data['forwards'] = [
                {k: v for k, v in forward.items() if k != 'id'}
                for forward in data['forwards']
            ]
        
        self.logger.debug(f"Making API request to update inbound route with data keys: {list(data.keys())}")
        
        # Make API request
        response = self.client.request(
            method='PUT',
            endpoint=f'inbound/{request.inbound_id}',
            json=data
        )
        
        return self._create_response(response, InboundResponse)

    def delete(self, request: InboundDeleteRequest) -> APIResponse:
        """
        Delete an inbound route.
        
        Args:
            request: The inbound delete request with inbound ID
            
        Returns:
            APIResponse containing the deletion result
            
        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, InboundDeleteRequest):
            raise MailerSendValidationError("Request must be an instance of InboundDeleteRequest")
        
        self.logger.debug(f"Preparing to delete inbound route with ID: {request.inbound_id}")
        
        # Make API request
        response = self.client.request(
            method='DELETE',
            endpoint=f'inbound/{request.inbound_id}'
        )
        
        return self._create_response(response) 