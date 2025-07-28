from typing import Dict, Any, Optional

from .base import BaseResource
from ..models.domains import (
    DomainListRequest, DomainCreateRequest, DomainDeleteRequest, DomainGetRequest,
    DomainUpdateSettingsRequest, DomainRecipientsRequest, DomainDnsRecordsRequest,
    DomainVerificationRequest, DomainListQueryParams
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
        
        # Use default query params if no request provided
        if not request:
            query_params = DomainListQueryParams()
            params = query_params.to_query_params()
        else:
            if not isinstance(request, DomainListRequest):
                self.logger.error("Invalid DomainListRequest object provided")
                raise ValidationError("DomainListRequest must be provided")
            params = request.to_query_params()
        
        self.logger.info("Requesting domains list")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", "domains", params=params)
        
        return self._create_response(response)

    def get_domain(self, request: DomainGetRequest) -> APIResponse:
        """
        Retrieve information about a single domain.
        
        Args:
            request: DomainGetRequest with domain ID
            
        Returns:
            APIResponse with domain information
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to get domain")

        if not request:
            self.logger.error("No DomainGetRequest object provided")
            raise ValidationError("DomainGetRequest must be provided")

        if not isinstance(request, DomainGetRequest):
            self.logger.error("Invalid DomainGetRequest object provided")
            raise ValidationError("DomainGetRequest must be provided")
        
        self.logger.debug(f"Retrieving domain: {request.domain_id}")
        self.logger.info(f"Requesting domain information for: {request.domain_id}")
        
        response = self.client.request("GET", f"domains/{request.domain_id}")
        
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
        self.logger.debug("Preparing to create domain")
        
        if not request:
            self.logger.error("No DomainCreateRequest object provided")
            raise ValidationError("DomainCreateRequest must be provided")

        if not isinstance(request, DomainCreateRequest):
            self.logger.error("Invalid DomainCreateRequest object provided")
            raise ValidationError("DomainCreateRequest must be provided")
        
        # Convert to request body
        body = request.model_dump(by_alias=True, exclude_none=True)
        
        self.logger.info(f"Creating domain: {request.name}")
        self.logger.debug(f"Request body: {body}")
        
        response = self.client.request("POST", "domains", body=body)
        
        return self._create_response(response)

    def delete_domain(self, request: DomainDeleteRequest) -> APIResponse:
        """
        Delete a domain.
        
        Args:
            request: DomainDeleteRequest with domain ID to delete
            
        Returns:
            APIResponse (204 No Content on success)
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to delete domain")

        if not request:
            self.logger.error("No DomainDeleteRequest object provided")
            raise ValidationError("DomainDeleteRequest must be provided")

        if not isinstance(request, DomainDeleteRequest):
            self.logger.error("Invalid DomainDeleteRequest object provided")
            raise ValidationError("DomainDeleteRequest must be provided")
        
        self.logger.debug(f"Deleting domain: {request.domain_id}")
        self.logger.info(f"Deleting domain: {request.domain_id}")
        
        response = self.client.request("DELETE", f"domains/{request.domain_id}")
        
        return self._create_response(response)

    def get_domain_recipients(self, request: DomainRecipientsRequest) -> APIResponse:
        """
        Retrieve recipients for a domain.
        
        Args:
            request: DomainRecipientsRequest with domain ID and pagination options
            
        Returns:
            APIResponse with list of domain recipients
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to get domain recipients")

        if not request:
            self.logger.error("No DomainRecipientsRequest object provided")
            raise ValidationError("DomainRecipientsRequest must be provided")

        if not isinstance(request, DomainRecipientsRequest):
            self.logger.error("Invalid DomainRecipientsRequest object provided")
            raise ValidationError("DomainRecipientsRequest must be provided")
        
        self.logger.debug(f"Retrieving recipients for domain: {request.domain_id}")
        
        # Convert to query parameters
        params = request.to_query_params()
        
        self.logger.info(f"Requesting recipients for domain: {request.domain_id}")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", f"domains/{request.domain_id}/recipients", params=params)
        
        return self._create_response(response)

    def update_domain_settings(self, request: DomainUpdateSettingsRequest) -> APIResponse:
        """
        Update domain settings.
        
        Args:
            request: DomainUpdateSettingsRequest with domain ID and settings to update
            
        Returns:
            APIResponse with updated domain information
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to update domain settings")

        if not request:
            self.logger.error("No DomainUpdateSettingsRequest object provided")
            raise ValidationError("DomainUpdateSettingsRequest must be provided")

        if not isinstance(request, DomainUpdateSettingsRequest):
            self.logger.error("Invalid DomainUpdateSettingsRequest object provided")
            raise ValidationError("DomainUpdateSettingsRequest must be provided")
        
        self.logger.debug(f"Updating settings for domain: {request.domain_id}")
        
        # Convert to request body, excluding domain_id which goes in URL path
        body = request.model_dump(by_alias=True, exclude_none=True, exclude={'domain_id'})
        
        self.logger.info(f"Updating settings for domain: {request.domain_id}")
        self.logger.debug(f"Request body: {body}")
        
        response = self.client.request("PUT", f"domains/{request.domain_id}/settings", body=body)
        
        return self._create_response(response)

    def get_domain_dns_records(self, request: DomainDnsRecordsRequest) -> APIResponse:
        """
        Retrieve DNS records for a domain.
        
        Args:
            request: DomainDnsRecordsRequest with domain ID
            
        Returns:
            APIResponse with domain DNS records
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to get domain DNS records")

        if not request:
            self.logger.error("No DomainDnsRecordsRequest object provided")
            raise ValidationError("DomainDnsRecordsRequest must be provided")

        if not isinstance(request, DomainDnsRecordsRequest):
            self.logger.error("Invalid DomainDnsRecordsRequest object provided")
            raise ValidationError("DomainDnsRecordsRequest must be provided")
        
        self.logger.debug(f"Retrieving DNS records for domain: {request.domain_id}")
        self.logger.info(f"Requesting DNS records for domain: {request.domain_id}")
        
        response = self.client.request("GET", f"domains/{request.domain_id}/dns-records")
        
        return self._create_response(response)

    def get_domain_verification_status(self, request: DomainVerificationRequest) -> APIResponse:
        """
        Retrieve verification status for a domain.
        
        Args:
            request: DomainVerificationRequest with domain ID
            
        Returns:
            APIResponse with domain verification status
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to get domain verification status")

        if not request:
            self.logger.error("No DomainVerificationRequest object provided")
            raise ValidationError("DomainVerificationRequest must be provided")

        if not isinstance(request, DomainVerificationRequest):
            self.logger.error("Invalid DomainVerificationRequest object provided")
            raise ValidationError("DomainVerificationRequest must be provided")
        
        self.logger.debug(f"Retrieving verification status for domain: {request.domain_id}")
        self.logger.info(f"Requesting verification status for domain: {request.domain_id}")
        
        response = self.client.request("GET", f"domains/{request.domain_id}/verify")
        
        return self._create_response(response) 