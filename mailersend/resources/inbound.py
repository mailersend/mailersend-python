from typing import Optional, Dict, Any

from pydantic import ValidationError as PydanticValidationError

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
from mailersend.resources.base import BaseResource


class InboundResource(BaseResource):
    """Resource for managing inbound routes."""

    def list(self, request: InboundListRequest) -> InboundListResponse:
        """
        Get a list of inbound routes.
        
        Args:
            request: The inbound list request
            
        Returns:
            InboundListResponse: The response containing inbound routes list
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request cannot be None")
        
        try:
            # Build parameters, excluding None values
            params = {}
            if request.domain_id is not None:
                params['domain_id'] = request.domain_id
            if request.page is not None:
                params['page'] = request.page
            if request.limit is not None:
                params['limit'] = request.limit
            
            response = self.client.get("inbound", params=params)
            return InboundListResponse(**response.json())
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid response format: {e}")

    def get(self, request: InboundGetRequest) -> InboundResponse:
        """
        Get a single inbound route by ID.
        
        Args:
            request: The inbound get request
            
        Returns:
            InboundResponse: The response containing inbound route data
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request cannot be None")
        
        try:
            response = self.client.get(f"inbound/{request.inbound_id}")
            return InboundResponse(**response.json())
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid response format: {e}")

    def create(self, request: InboundCreateRequest) -> InboundResponse:
        """
        Create a new inbound route.
        
        Args:
            request: The inbound create request
            
        Returns:
            InboundResponse: The response containing created inbound route data
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request cannot be None")
        
        try:
            # Build request data, excluding None values and ID fields
            data = {}
            if request.domain_id is not None:
                data['domain_id'] = request.domain_id
            if request.name is not None:
                data['name'] = request.name
            if request.domain_enabled is not None:
                data['domain_enabled'] = request.domain_enabled
            if request.inbound_domain is not None:
                data['inbound_domain'] = request.inbound_domain
            if request.inbound_priority is not None:
                data['inbound_priority'] = request.inbound_priority
            if request.catch_filter is not None:
                data['catch_filter'] = [filter_group.model_dump() for filter_group in request.catch_filter]
            if request.catch_type is not None:
                data['catch_type'] = request.catch_type
            if request.match_filter is not None:
                data['match_filter'] = [filter_group.model_dump() for filter_group in request.match_filter]
            if request.match_type is not None:
                data['match_type'] = request.match_type
            if request.forwards is not None:
                data['forwards'] = [forward.model_dump(exclude={'id'}) for forward in request.forwards]
            
            response = self.client.post("inbound", json=data)
            return InboundResponse(**response.json())
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid response format: {e}")

    def update(self, request: InboundUpdateRequest) -> InboundResponse:
        """
        Update an existing inbound route.
        
        Args:
            request: The inbound update request
            
        Returns:
            InboundResponse: The response containing updated inbound route data
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request cannot be None")
        
        try:
            # Build request data, excluding None values and ID fields
            data = {}
            if request.name is not None:
                data['name'] = request.name
            if request.domain_enabled is not None:
                data['domain_enabled'] = request.domain_enabled
            if request.inbound_domain is not None:
                data['inbound_domain'] = request.inbound_domain
            if request.inbound_priority is not None:
                data['inbound_priority'] = request.inbound_priority
            if request.catch_filter is not None:
                data['catch_filter'] = [filter_group.model_dump() for filter_group in request.catch_filter]
            if request.catch_type is not None:
                data['catch_type'] = request.catch_type
            if request.match_filter is not None:
                data['match_filter'] = [filter_group.model_dump() for filter_group in request.match_filter]
            if request.match_type is not None:
                data['match_type'] = request.match_type
            if request.forwards is not None:
                data['forwards'] = [forward.model_dump(exclude={'id'}) for forward in request.forwards]
            
            response = self.client.put(f"inbound/{request.inbound_id}", json=data)
            return InboundResponse(**response.json())
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid response format: {e}")

    def delete(self, request: InboundDeleteRequest) -> None:
        """
        Delete an inbound route.
        
        Args:
            request: The inbound delete request
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request cannot be None")
        
        self.client.delete(f"inbound/{request.inbound_id}") 