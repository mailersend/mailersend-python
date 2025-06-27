"""Email Verification API resource for MailerSend SDK."""

import logging
from typing import Any, Dict, Optional

from mailersend.models.base import APIResponse
from mailersend.models.email_verification import (
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationAsyncStatusRequest,
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
)


logger = logging.getLogger(__name__)


class EmailVerification:
    """Resource for managing email verification through the MailerSend API."""

    def __init__(self, client: Any) -> None:
        """Initialize the EmailVerification resource.
        
        Args:
            client: The MailerSend API client instance.
        """
        self.client = client

    def verify_email(self, request: EmailVerifyRequest) -> APIResponse:
        """Verify a single email address (synchronous).
        
        Args:
            request: The email verification request data.
            
        Returns:
            APIResponse: The API response containing verification status.
        """
        logger.info(f"Verifying email address: {request.email}")
        
        endpoint = "email-verification/verify"
        payload = {"email": request.email}
        
        return self.client.request("POST", endpoint, json=payload)

    def verify_email_async(self, request: EmailVerifyAsyncRequest) -> APIResponse:
        """Verify a single email address (asynchronous).
        
        Args:
            request: The async email verification request data.
            
        Returns:
            APIResponse: The API response containing verification ID and status.
        """
        logger.info(f"Starting async verification for email: {request.email}")
        
        endpoint = "email-verification/verify-async"
        payload = {"email": request.email}
        
        return self.client.request("POST", endpoint, json=payload)

    def get_async_status(self, request: EmailVerificationAsyncStatusRequest) -> APIResponse:
        """Get the status of an async email verification.
        
        Args:
            request: The async status request data.
            
        Returns:
            APIResponse: The API response containing verification status and result.
        """
        logger.info(f"Getting async verification status for ID: {request.email_verification_id}")
        
        endpoint = f"email-verification/verify-async/{request.email_verification_id}"
        
        return self.client.request("GET", endpoint)

    def list_verifications(self, request: EmailVerificationListsRequest) -> APIResponse:
        """List all email verification lists.
        
        Args:
            request: The list request data with pagination options.
            
        Returns:
            APIResponse: The API response containing verification lists.
        """
        logger.info("Listing email verification lists")
        
        endpoint = "email-verification"
        params: Dict[str, Any] = {}
        
        if request.page is not None:
            params["page"] = request.page
        if request.limit is not None:
            params["limit"] = request.limit
        
        return self.client.request("GET", endpoint, params=params)

    def get_verification(self, request: EmailVerificationGetRequest) -> APIResponse:
        """Get a single email verification list.
        
        Args:
            request: The get verification request data.
            
        Returns:
            APIResponse: The API response containing verification list details.
        """
        logger.info(f"Getting email verification list: {request.email_verification_id}")
        
        endpoint = f"email-verification/{request.email_verification_id}"
        
        return self.client.request("GET", endpoint)

    def create_verification(self, request: EmailVerificationCreateRequest) -> APIResponse:
        """Create a new email verification list.
        
        Args:
            request: The create verification request data.
            
        Returns:
            APIResponse: The API response containing created verification list.
        """
        logger.info(f"Creating email verification list: {request.name} with {len(request.emails)} emails")
        
        endpoint = "email-verification"
        payload = {
            "name": request.name,
            "emails": request.emails
        }
        
        return self.client.request("POST", endpoint, json=payload)

    def verify_list(self, request: EmailVerificationVerifyRequest) -> APIResponse:
        """Start verification of an email verification list.
        
        Args:
            request: The verify list request data.
            
        Returns:
            APIResponse: The API response containing updated verification list.
        """
        logger.info(f"Starting verification for list: {request.email_verification_id}")
        
        endpoint = f"email-verification/{request.email_verification_id}/verify"
        
        return self.client.request("GET", endpoint)

    def get_results(self, request: EmailVerificationResultsRequest) -> APIResponse:
        """Get verification results for an email verification list.
        
        Args:
            request: The results request data with optional filters.
            
        Returns:
            APIResponse: The API response containing verification results.
        """
        logger.info(f"Getting verification results for list: {request.email_verification_id}")
        
        endpoint = f"email-verification/{request.email_verification_id}/results"
        params: Dict[str, Any] = {}
        
        if request.page is not None:
            params["page"] = request.page
        if request.limit is not None:
            params["limit"] = request.limit
        if request.results is not None and request.results:
            params["results"] = request.results
        
        return self.client.request("GET", endpoint, params=params) 