"""Tokens API resource."""

import logging

from .base import BaseResource
from ..models.base import APIResponse
from ..models.tokens import (
    TokensListRequest, TokenGetRequest, TokenCreateRequest, TokenUpdateRequest,
    TokenUpdateNameRequest, TokenDeleteRequest
)


logger = logging.getLogger(__name__)


class Tokens(BaseResource):
    """Tokens API resource."""

    def list_tokens(self, request: TokensListRequest) -> APIResponse:
        """List API tokens.
        
        Args:
            request: The list tokens request
            
        Returns:
            APIResponse: API response with tokens list data
        """
        logger.info(f"Listing tokens with pagination: page={request.query_params.page}, limit={request.query_params.limit}")
        
        # Extract query parameters
        params = request.to_query_params()
        
        # Make API call
        response = self.client.request(
            method="GET",
            endpoint="/v1/token",
            params=params
        )
        
        # Create standardized response
        return self._create_response(response)

    def get_token(self, request: TokenGetRequest) -> APIResponse:
        """Get a single API token.
        
        Args:
            request: The get token request
            
        Returns:
            APIResponse: API response with token data
        """
        logger.info(f"Getting token: {request.token_id}")
        
        # Make API call
        response = self.client.request(
            method="GET",
            endpoint=f"/v1/token/{request.token_id}"
        )
        
        # Create standardized response
        return self._create_response(response)

    def create_token(self, request: TokenCreateRequest) -> APIResponse:
        """Create an API token.
        
        Args:
            request: The create token request
            
        Returns:
            APIResponse: API response with token creation data
        """
        logger.info(f"Creating token: {request.name} for domain: {request.domain_id}")
        
        # Make API call
        response = self.client.request(
            method="POST",
            endpoint="/v1/token",
            json=request.to_json()
        )
        
        # Create standardized response
        return self._create_response(response)

    def update_token(self, request: TokenUpdateRequest) -> APIResponse:
        """Update an API token status.
        
        Args:
            request: The update token request
            
        Returns:
            APIResponse: API response with update confirmation
        """
        logger.info(f"Updating token: {request.token_id} to status: {request.status}")
        
        # Make API call
        response = self.client.request(
            method="PUT",
            endpoint=f"/v1/token/{request.token_id}/settings",
            json=request.to_json()
        )
        
        # Create standardized response
        return self._create_response(response)

    def update_token_name(self, request: TokenUpdateNameRequest) -> APIResponse:
        """Update an API token name.
        
        Args:
            request: The update token name request
            
        Returns:
            APIResponse: API response with update confirmation
        """
        logger.info(f"Updating token name: {request.token_id} to: {request.name}")
        
        # Make API call
        response = self.client.request(
            method="PUT",
            endpoint=f"/v1/token/{request.token_id}",
            json=request.to_json()
        )
        
        # Create standardized response
        return self._create_response(response)

    def delete_token(self, request: TokenDeleteRequest) -> APIResponse:
        """Delete an API token.
        
        Args:
            request: The delete token request
            
        Returns:
            APIResponse: API response with delete confirmation
        """
        logger.info(f"Deleting token: {request.token_id}")
        
        # Make API call
        response = self.client.request(
            method="DELETE",
            endpoint=f"/v1/token/{request.token_id}"
        )
        
        # Create standardized response
        return self._create_response(response) 