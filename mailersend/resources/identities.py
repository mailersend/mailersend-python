from typing import Dict, Any, Optional

from ..exceptions import ValidationError as MailerSendValidationError
from ..models.identities import (
    IdentityListRequest,
    IdentityCreateRequest,
    IdentityGetRequest,
    IdentityGetByEmailRequest,
    IdentityUpdateRequest,
    IdentityUpdateByEmailRequest,
    IdentityDeleteRequest,
    IdentityDeleteByEmailRequest,
    IdentityListResponse,
    IdentityResponse
)
from .base import BaseResource


class IdentitiesResource(BaseResource):
    """Resource for managing sender identities."""

    def list_identities(self, request: IdentityListRequest) -> Dict[str, Any]:
        """
        Get a list of sender identities.
        
        Args:
            request: The identity list request containing filtering and pagination parameters
            
        Returns:
            Dict containing the API response with identities list
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request is required")
        
        # Build query parameters, excluding None values
        params = {}
        if request.domain_id is not None:
            params['domain_id'] = request.domain_id
        if request.page is not None:
            params['page'] = request.page
        if request.limit is not None:
            params['limit'] = request.limit
        
        return self.client.request(
            method='GET',
            endpoint='/identities',
            params=params if params else None
        )

    def create_identity(self, request: IdentityCreateRequest) -> Dict[str, Any]:
        """
        Create a new sender identity.
        
        Args:
            request: The identity creation request with all required data
            
        Returns:
            Dict containing the API response with created identity
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request is required")
        
        # Build request body, excluding None values
        data = {
            'domain_id': request.domain_id,
            'name': request.name,
            'email': request.email
        }
        
        if request.reply_to_email is not None:
            data['reply_to_email'] = request.reply_to_email
        if request.reply_to_name is not None:
            data['reply_to_name'] = request.reply_to_name
        if request.add_note is not None:
            data['add_note'] = request.add_note
        if request.personal_note is not None:
            data['personal_note'] = request.personal_note
        
        return self.client.request(
            method='POST',
            endpoint='/identities',
            json=data
        )

    def get_identity(self, request: IdentityGetRequest) -> Dict[str, Any]:
        """
        Get a single sender identity by ID.
        
        Args:
            request: The identity get request with identity ID
            
        Returns:
            Dict containing the API response with identity data
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request is required")
        
        return self.client.request(
            method='GET',
            endpoint=f'/identities/{request.identity_id}'
        )

    def get_identity_by_email(self, request: IdentityGetByEmailRequest) -> Dict[str, Any]:
        """
        Get a single sender identity by email.
        
        Args:
            request: The identity get by email request
            
        Returns:
            Dict containing the API response with identity data
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request is required")
        
        return self.client.request(
            method='GET',
            endpoint=f'/identities/email/{request.email}'
        )

    def update_identity(self, request: IdentityUpdateRequest) -> Dict[str, Any]:
        """
        Update a sender identity by ID.
        
        Args:
            request: The identity update request with identity ID and update data
            
        Returns:
            Dict containing the API response with updated identity
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request is required")
        
        # Build request body, excluding None values and identity_id (goes in URL)
        data = {}
        if request.name is not None:
            data['name'] = request.name
        if request.reply_to_email is not None:
            data['reply_to_email'] = request.reply_to_email
        if request.reply_to_name is not None:
            data['reply_to_name'] = request.reply_to_name
        if request.add_note is not None:
            data['add_note'] = request.add_note
        if request.personal_note is not None:
            data['personal_note'] = request.personal_note
        
        return self.client.request(
            method='PUT',
            endpoint=f'/identities/{request.identity_id}',
            json=data if data else None
        )

    def update_identity_by_email(self, request: IdentityUpdateByEmailRequest) -> Dict[str, Any]:
        """
        Update a sender identity by email.
        
        Args:
            request: The identity update by email request
            
        Returns:
            Dict containing the API response with updated identity
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request is required")
        
        # Build request body, excluding None values and email (goes in URL)
        data = {}
        if request.name is not None:
            data['name'] = request.name
        if request.reply_to_email is not None:
            data['reply_to_email'] = request.reply_to_email
        if request.reply_to_name is not None:
            data['reply_to_name'] = request.reply_to_name
        if request.add_note is not None:
            data['add_note'] = request.add_note
        if request.personal_note is not None:
            data['personal_note'] = request.personal_note
        
        return self.client.request(
            method='PUT',
            endpoint=f'/identities/email/{request.email}',
            json=data if data else None
        )

    def delete_identity(self, request: IdentityDeleteRequest) -> Dict[str, Any]:
        """
        Delete a sender identity by ID.
        
        Args:
            request: The identity delete request with identity ID
            
        Returns:
            Dict containing the API response
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request is required")
        
        return self.client.request(
            method='DELETE',
            endpoint=f'/identities/{request.identity_id}'
        )

    def delete_identity_by_email(self, request: IdentityDeleteByEmailRequest) -> Dict[str, Any]:
        """
        Delete a sender identity by email.
        
        Args:
            request: The identity delete by email request
            
        Returns:
            Dict containing the API response
            
        Raises:
            MailerSendValidationError: If the request is invalid
        """
        if request is None:
            raise MailerSendValidationError("Request is required")
        
        return self.client.request(
            method='DELETE',
            endpoint=f'/identities/email/{request.email}'
        ) 