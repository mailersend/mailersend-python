"""Domains resource"""

from typing import Optional

from .base import BaseResource
from ..models.domains import (
    DomainListRequest,
    DomainCreateRequest,
    DomainDeleteRequest,
    DomainGetRequest,
    DomainUpdateSettingsRequest,
    DomainRecipientsRequest,
    DomainDnsRecordsRequest,
    DomainVerificationRequest,
    DomainListQueryParams,
)
from ..models.base import APIResponse


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
        """
        self.logger.debug("Retrieving domains list")

        # Use default query params if no request provided
        if not request:
            query_params = DomainListQueryParams()
            params = query_params.to_query_params()
        else:
            params = request.to_query_params()

        self.logger.debug("Query params: %s", params)

        response = self.client.request("GET", "domains", params=params)

        return self._create_response(response)

    def get_domain(self, request: DomainGetRequest) -> APIResponse:
        """
        Retrieve information about a single domain.

        Args:
            request: DomainGetRequest with domain ID

        Returns:
            APIResponse with domain information
        """
        self.logger.debug("Preparing to get domain")
        self.logger.debug("Requesting domain information for: %s", request.domain_id)

        response = self.client.request("GET", f"domains/{request.domain_id}")

        return self._create_response(response)

    def create_domain(self, request: DomainCreateRequest) -> APIResponse:
        """
        Create a new domain.

        Args:
            request: DomainCreateRequest with domain creation details

        Returns:
            APIResponse with created domain information
        """
        self.logger.debug("Creating domain: %s", request.name)

        # Convert to request body
        body = request.model_dump(by_alias=True, exclude_none=True)

        self.logger.debug("Request body: %s", body)

        response = self.client.request("POST", "domains", body=body)

        return self._create_response(response)

    def delete_domain(self, request: DomainDeleteRequest) -> APIResponse:
        """
        Delete a domain.

        Args:
            request: DomainDeleteRequest with domain ID to delete

        Returns:
            APIResponse (204 No Content on success)
        """
        self.logger.debug("Preparing to delete domain")
        self.logger.debug("Deleting domain: %s", request.domain_id)

        response = self.client.request("DELETE", f"domains/{request.domain_id}")

        return self._create_response(response)

    def get_domain_recipients(self, request: DomainRecipientsRequest) -> APIResponse:
        """
        Retrieve recipients for a domain.

        Args:
            request: DomainRecipientsRequest with domain ID and pagination options

        Returns:
            APIResponse with list of domain recipients
        """
        self.logger.debug("Preparing to get domain recipients")
        self.logger.debug("Retrieving recipients for domain: %s", request.domain_id)

        # Convert to query parameters
        params = request.to_query_params()

        self.logger.debug("Query params: %s", params)

        response = self.client.request(
            "GET", f"domains/{request.domain_id}/recipients", params=params
        )

        return self._create_response(response)

    def update_domain_settings(
        self, request: DomainUpdateSettingsRequest
    ) -> APIResponse:
        """
        Update domain settings.

        Args:
            request: DomainUpdateSettingsRequest with domain ID and settings to update

        Returns:
            APIResponse with updated domain information
        """
        self.logger.debug("Preparing to update domain settings")
        self.logger.debug("Updating settings for domain: %s", request.domain_id)

        # Convert to request body, excluding domain_id which goes in URL path
        body = request.model_dump(
            by_alias=True, exclude_none=True, exclude={"domain_id"}
        )

        self.logger.debug("Request body: %s", body)

        response = self.client.request(
            "PUT", f"domains/{request.domain_id}/settings", body=body
        )

        return self._create_response(response)

    def get_domain_dns_records(self, request: DomainDnsRecordsRequest) -> APIResponse:
        """
        Retrieve DNS records for a domain.

        Args:
            request: DomainDnsRecordsRequest with domain ID

        Returns:
            APIResponse with domain DNS records
        """
        self.logger.debug("Preparing to get domain DNS records")
        self.logger.debug("Retrieving DNS records for domain: %s", request.domain_id)

        response = self.client.request(
            "GET", f"domains/{request.domain_id}/dns-records"
        )

        return self._create_response(response)

    def get_domain_verification_status(
        self, request: DomainVerificationRequest
    ) -> APIResponse:
        """
        Retrieve verification status for a domain.

        Args:
            request: DomainVerificationRequest with domain ID

        Returns:
            APIResponse with domain verification status
        """
        self.logger.debug("Preparing to get domain verification status")
        self.logger.debug(
            "Retrieving verification status for domain: %s", request.domain_id
        )

        response = self.client.request("GET", f"domains/{request.domain_id}/verify")

        return self._create_response(response)
