from typing import Dict, Any, Optional

from .base import BaseResource
from ..models.domains import (
    DomainListRequest, DomainCreateRequest, DomainUpdateSettingsRequest,
    DomainRecipientsRequest
)
from ..models.base import APIResponse
from ..exceptions import ValidationError


class Domains(BaseResource):
    """
    Client for interacting with the MailerSend Domains API.
    
    Provides methods for managing domains, their settings, recipients,
    DNS records, and verification status.
    """

    def list_domains(self, request: Optional[DomainListRequest] = None) -> APIResponse:
        """
        Retrieve a list of domains.
        
        Args:
            request: Optional DomainListRequest with filtering and pagination options
            
        Returns:
            APIResponse with list of domains
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Retrieving domains list")
        
        # Convert to query parameters
        params = {}
        if request:
            params = self._build_query_params(request)
        
        self.logger.info("Requesting domains list")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", "domains", params=params)
        
        return self._create_response(response)

    def get_domain(self, domain_id: str) -> APIResponse:
        """
        Retrieve information about a single domain.
        
        Args:
            domain_id: The domain ID
            
        Returns:
            APIResponse with domain information
            
        Raises:
            ValidationError: If domain_id is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug(f"Retrieving domain: {domain_id}")
        
        if not domain_id or not domain_id.strip():
            self.logger.error("No domain ID provided")
            raise ValidationError("Domain ID must be provided")
        
        self.logger.info(f"Requesting domain information for: {domain_id}")
        
        response = self.client.request("GET", f"domains/{domain_id}")
        
        return self._create_response(response)

    def create_domain(self, request: DomainCreateRequest) -> APIResponse:
        """
        Create a new domain.
        
        Args:
            request: DomainCreateRequest with domain creation details
            
        Returns:
            APIResponse with created domain information
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Creating new domain")
        
        if not request:
            self.logger.error("No DomainCreateRequest object provided")
            raise ValidationError("DomainCreateRequest must be provided")
        
        # Convert to request body
        body = self._build_request_body(request)
        
        self.logger.info(f"Creating domain: {request.name}")
        self.logger.debug(f"Request body: {body}")
        
        response = self.client.request("POST", "domains", body=body)
        
        return self._create_response(response)

    def delete_domain(self, domain_id: str) -> APIResponse:
        """
        Delete a domain.
        
        Args:
            domain_id: The domain ID to delete
            
        Returns:
            APIResponse (204 No Content on success)
            
        Raises:
            ValidationError: If domain_id is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug(f"Deleting domain: {domain_id}")
        
        if not domain_id or not domain_id.strip():
            self.logger.error("No domain ID provided")
            raise ValidationError("Domain ID must be provided")
        
        self.logger.info(f"Deleting domain: {domain_id}")
        
        response = self.client.request("DELETE", f"domains/{domain_id}")
        
        return self._create_response(response)

    def get_domain_recipients(self, domain_id: str, request: Optional[DomainRecipientsRequest] = None) -> APIResponse:
        """
        Retrieve recipients for a domain.
        
        Args:
            domain_id: The domain ID
            request: Optional DomainRecipientsRequest with pagination options
            
        Returns:
            APIResponse with list of domain recipients
            
        Raises:
            ValidationError: If domain_id is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug(f"Retrieving recipients for domain: {domain_id}")
        
        if not domain_id or not domain_id.strip():
            self.logger.error("No domain ID provided")
            raise ValidationError("Domain ID must be provided")
        
        # Convert to query parameters
        params = {}
        if request:
            params = self._build_query_params(request)
        
        self.logger.info(f"Requesting recipients for domain: {domain_id}")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", f"domains/{domain_id}/recipients", params=params)
        
        return self._create_response(response)

    def update_domain_settings(self, domain_id: str, request: DomainUpdateSettingsRequest) -> APIResponse:
        """
        Update domain settings.
        
        Args:
            domain_id: The domain ID
            request: DomainUpdateSettingsRequest with settings to update
            
        Returns:
            APIResponse with updated domain information
            
        Raises:
            ValidationError: If domain_id or request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug(f"Updating settings for domain: {domain_id}")
        
        if not domain_id or not domain_id.strip():
            self.logger.error("No domain ID provided")
            raise ValidationError("Domain ID must be provided")
        
        if not request:
            self.logger.error("No DomainUpdateSettingsRequest object provided")
            raise ValidationError("DomainUpdateSettingsRequest must be provided")
        
        # Convert to request body
        body = self._build_request_body(request)
        
        self.logger.info(f"Updating settings for domain: {domain_id}")
        self.logger.debug(f"Request body: {body}")
        
        response = self.client.request("PUT", f"domains/{domain_id}/settings", body=body)
        
        return self._create_response(response)

    def get_domain_dns_records(self, domain_id: str) -> APIResponse:
        """
        Retrieve DNS records for a domain.
        
        Args:
            domain_id: The domain ID
            
        Returns:
            APIResponse with domain DNS records
            
        Raises:
            ValidationError: If domain_id is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug(f"Retrieving DNS records for domain: {domain_id}")
        
        if not domain_id or not domain_id.strip():
            self.logger.error("No domain ID provided")
            raise ValidationError("Domain ID must be provided")
        
        self.logger.info(f"Requesting DNS records for domain: {domain_id}")
        
        response = self.client.request("GET", f"domains/{domain_id}/dns-records")
        
        return self._create_response(response)

    def get_domain_verification_status(self, domain_id: str) -> APIResponse:
        """
        Retrieve verification status for a domain.
        
        Args:
            domain_id: The domain ID
            
        Returns:
            APIResponse with domain verification status
            
        Raises:
            ValidationError: If domain_id is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug(f"Retrieving verification status for domain: {domain_id}")
        
        if not domain_id or not domain_id.strip():
            self.logger.error("No domain ID provided")
            raise ValidationError("Domain ID must be provided")
        
        self.logger.info(f"Requesting verification status for domain: {domain_id}")
        
        response = self.client.request("GET", f"domains/{domain_id}/verify")
        
        return self._create_response(response)

    def _build_query_params(self, request) -> Dict[str, Any]:
        """
        Build query parameters from request object.
        
        Args:
            request: Request object with query parameters
            
        Returns:
            Dictionary of query parameters
        """
        # Convert model to dict, excluding None values
        params = request.model_dump(exclude_none=True)
        
        return params

    def _build_request_body(self, request) -> Dict[str, Any]:
        """
        Build request body from request object.
        
        Args:
            request: Request object
            
        Returns:
            Dictionary for request body
        """
        # Convert model to dict, excluding None values
        body = request.model_dump(exclude_none=True)
        
        return body 