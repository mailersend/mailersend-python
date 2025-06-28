"""Tokens API resource."""

import logging
from typing import Optional, List

from ..models.base import APIResponse
from ..builders.tokens import TokensBuilder


logger = logging.getLogger(__name__)


class Tokens:
    """Tokens API resource."""

    def __init__(self, client):
        """Initialize the Tokens resource.
        
        Args:
            client: The MailerSend client instance
        """
        self.client = client

    def list_tokens(self, page: Optional[int] = None, limit: Optional[int] = None) -> APIResponse:
        """List API tokens.
        
        Args:
            page: Page number for pagination (default: None)
            limit: Number of tokens per page (10-100, default: 25)
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info("Listing API tokens")
        
        builder = TokensBuilder()
        if page is not None:
            builder.page(page)
        if limit is not None:
            builder.limit(limit)
        
        request_data = builder.build_tokens_list()
        
        params = {}
        if request_data.page is not None:
            params['page'] = request_data.page
        if request_data.limit is not None:
            params['limit'] = request_data.limit
        
        return self.client.request(
            method="GET",
            endpoint="/v1/token",
            params=params
        )

    def get_token(self, token_id: str) -> APIResponse:
        """Get a single API token.
        
        Args:
            token_id: The token ID
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Getting token: {token_id}")
        
        builder = TokensBuilder()
        request_data = builder.token_id(token_id).build_token_get()
        
        return self.client.request(
            method="GET",
            endpoint=f"/v1/token/{request_data.token_id}"
        )

    def create_token(self, name: str, domain_id: str, scopes: List[str]) -> APIResponse:
        """Create an API token.
        
        Args:
            name: The token name (max 50 characters)
            domain_id: The domain ID
            scopes: List of scopes for the token
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Creating token: {name} for domain: {domain_id}")
        
        builder = TokensBuilder()
        request_data = (builder
                       .name(name)
                       .domain_id(domain_id)
                       .scopes(scopes)
                       .build_token_create())
        
        json_data = {
            "name": request_data.name,
            "domain_id": request_data.domain_id,
            "scopes": request_data.scopes
        }
        
        return self.client.request(
            method="POST",
            endpoint="/v1/token",
            json=json_data
        )

    def update_token(self, token_id: str, status: str) -> APIResponse:
        """Update an API token status.
        
        Args:
            token_id: The token ID
            status: The token status ('pause' or 'unpause')
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Updating token: {token_id} to status: {status}")
        
        builder = TokensBuilder()
        request_data = (builder
                       .token_id(token_id)
                       .status(status)
                       .build_token_update())
        
        json_data = {
            "status": request_data.status
        }
        
        return self.client.request(
            method="PUT",
            endpoint=f"/v1/token/{request_data.token_id}/settings",
            json=json_data
        )

    def update_token_name(self, token_id: str, name: str) -> APIResponse:
        """Update an API token name.
        
        Args:
            token_id: The token ID
            name: The new token name (max 50 characters)
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Updating token name: {token_id} to: {name}")
        
        builder = TokensBuilder()
        request_data = (builder
                       .token_id(token_id)
                       .name(name)
                       .build_token_update_name())
        
        json_data = {
            "name": request_data.name
        }
        
        return self.client.request(
            method="PUT",
            endpoint=f"/v1/token/{request_data.token_id}",
            json=json_data
        )

    def delete_token(self, token_id: str) -> APIResponse:
        """Delete an API token.
        
        Args:
            token_id: The token ID
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Deleting token: {token_id}")
        
        builder = TokensBuilder()
        request_data = builder.token_id(token_id).build_token_delete()
        
        return self.client.request(
            method="DELETE",
            endpoint=f"/v1/token/{request_data.token_id}"
        ) 