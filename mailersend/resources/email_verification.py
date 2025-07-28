"""Email Verification resource for MailerSend SDK."""
import logging
from typing import Any, Dict, Optional

from .base import BaseResource
from ..models.base import APIResponse
from ..models.email_verification import (
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationAsyncStatusRequest,
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
    EmailVerifyResponse,
    EmailVerifyAsyncResponse,
    EmailVerificationAsyncStatusResponse,
    EmailVerificationListsResponse,
    EmailVerificationResponse,
    EmailVerificationResultsResponse,
)
from ..exceptions import ValidationError

logger = logging.getLogger(__name__)


class EmailVerification(BaseResource):
    """Resource for managing email verification through the MailerSend API."""

    def verify_email(self, request: EmailVerifyRequest) -> APIResponse:
        """Verify a single email address (synchronous).
        
        Args:
            request: The email verification request data.
            
        Returns:
            APIResponse with EmailVerifyResponse data
            
        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting verify_email operation")
        
        # Validate request
        if not request:
            logger.error("EmailVerifyRequest is required")
            raise ValidationError("EmailVerifyRequest must be provided")
        
        if not isinstance(request, EmailVerifyRequest):
            logger.error(f"Expected EmailVerifyRequest, got {type(request).__name__}")
            raise ValidationError("request must be an EmailVerifyRequest instance")
        
        logger.debug(f"Email verify request: {request}")
        
        # Prepare request body
        payload = {"email": request.email}
        
        logger.info(f"Verifying email address: {request.email}")
        
        # Make API call
        response = self.client.request("POST", "email-verification/verify", json=payload)
        
        # Create standardized response
        return self._create_response(
            response,
            EmailVerifyResponse(**response.json())
        )

    def verify_email_async(self, request: EmailVerifyAsyncRequest) -> APIResponse:
        """Verify a single email address (asynchronous).
        
        Args:
            request: The async email verification request data.
            
        Returns:
            APIResponse with EmailVerifyAsyncResponse data
            
        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting verify_email_async operation")
        
        # Validate request
        if not request:
            logger.error("EmailVerifyAsyncRequest is required")
            raise ValidationError("EmailVerifyAsyncRequest must be provided")
        
        if not isinstance(request, EmailVerifyAsyncRequest):
            logger.error(f"Expected EmailVerifyAsyncRequest, got {type(request).__name__}")
            raise ValidationError("request must be an EmailVerifyAsyncRequest instance")
        
        logger.debug(f"Async email verify request: {request}")
        
        # Prepare request body
        payload = {"email": request.email}
        
        logger.info(f"Starting async verification for email: {request.email}")
        
        # Make API call
        response = self.client.request("POST", "email-verification/verify-async", json=payload)
        
        # Create standardized response
        return self._create_response(
            response,
            EmailVerifyAsyncResponse(**response.json())
        )

    def get_async_status(self, request: EmailVerificationAsyncStatusRequest) -> APIResponse:
        """Get the status of an async email verification.
        
        Args:
            request: The async status request data.
            
        Returns:
            APIResponse with EmailVerificationAsyncStatusResponse data
            
        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting get_async_status operation")
        
        # Validate request
        if not request:
            logger.error("EmailVerificationAsyncStatusRequest is required")
            raise ValidationError("EmailVerificationAsyncStatusRequest must be provided")
        
        if not isinstance(request, EmailVerificationAsyncStatusRequest):
            logger.error(f"Expected EmailVerificationAsyncStatusRequest, got {type(request).__name__}")
            raise ValidationError("request must be an EmailVerificationAsyncStatusRequest instance")
        
        logger.debug(f"Async status request: {request}")
        
        # Prepare API call
        url = f"email-verification/verify-async/{request.email_verification_id}"
        logger.info(f"Getting async verification status for ID: {request.email_verification_id}")
        
        # Make API call
        response = self.client.request("GET", url)
        
        # Create standardized response
        return self._create_response(
            response,
            EmailVerificationAsyncStatusResponse(**response.json())
        )

    def list_verifications(self, request: EmailVerificationListsRequest) -> APIResponse:
        """List all email verification lists.
        
        Args:
            request: The list request data with pagination options.
            
        Returns:
            APIResponse with EmailVerificationListsResponse data
            
        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting list_verifications operation")
        
        # Validate request
        if not request:
            logger.error("EmailVerificationListsRequest is required")
            raise ValidationError("EmailVerificationListsRequest must be provided")
        
        if not isinstance(request, EmailVerificationListsRequest):
            logger.error(f"Expected EmailVerificationListsRequest, got {type(request).__name__}")
            raise ValidationError("request must be an EmailVerificationListsRequest instance")
        
        logger.debug(f"List verifications request: {request}")
        
        # Extract query parameters
        params = request.to_query_params()
        
        logger.info(f"Listing email verification lists with params: {params}")
        
        # Make API call
        response = self.client.request("GET", "email-verification", params=params)
        
        # Create standardized response
        return self._create_response(
            response,
            EmailVerificationListsResponse(**response.json())
        )

    def get_verification(self, request: EmailVerificationGetRequest) -> APIResponse:
        """Get a single email verification list.
        
        Args:
            request: The get verification request data.
            
        Returns:
            APIResponse with EmailVerificationResponse data
            
        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting get_verification operation")
        
        # Validate request
        if not request:
            logger.error("EmailVerificationGetRequest is required")
            raise ValidationError("EmailVerificationGetRequest must be provided")
        
        if not isinstance(request, EmailVerificationGetRequest):
            logger.error(f"Expected EmailVerificationGetRequest, got {type(request).__name__}")
            raise ValidationError("request must be an EmailVerificationGetRequest instance")
        
        logger.debug(f"Get verification request: {request}")
        
        # Prepare API call
        url = f"email-verification/{request.email_verification_id}"
        logger.info(f"Getting email verification list: {request.email_verification_id}")
        
        # Make API call
        response = self.client.request("GET", url)
        
        # Create standardized response
        return self._create_response(
            response,
            EmailVerificationResponse(**response.json())
        )

    def create_verification(self, request: EmailVerificationCreateRequest) -> APIResponse:
        """Create a new email verification list.
        
        Args:
            request: The create verification request data.
            
        Returns:
            APIResponse with EmailVerificationResponse data
            
        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting create_verification operation")
        
        # Validate request
        if not request:
            logger.error("EmailVerificationCreateRequest is required")
            raise ValidationError("EmailVerificationCreateRequest must be provided")
        
        if not isinstance(request, EmailVerificationCreateRequest):
            logger.error(f"Expected EmailVerificationCreateRequest, got {type(request).__name__}")
            raise ValidationError("request must be an EmailVerificationCreateRequest instance")
        
        logger.debug(f"Create verification request: {request}")
        
        # Prepare request body
        payload = {
            "name": request.name,
            "emails": request.emails
        }
        
        logger.info(f"Creating email verification list: {request.name} with {len(request.emails)} emails")
        
        # Make API call
        response = self.client.request("POST", "email-verification", json=payload)
        
        # Create standardized response
        return self._create_response(
            response,
            EmailVerificationResponse(**response.json())
        )

    def verify_list(self, request: EmailVerificationVerifyRequest) -> APIResponse:
        """Start verification of an email verification list.
        
        Args:
            request: The verify list request data.
            
        Returns:
            APIResponse with EmailVerificationResponse data
            
        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting verify_list operation")
        
        # Validate request
        if not request:
            logger.error("EmailVerificationVerifyRequest is required")
            raise ValidationError("EmailVerificationVerifyRequest must be provided")
        
        if not isinstance(request, EmailVerificationVerifyRequest):
            logger.error(f"Expected EmailVerificationVerifyRequest, got {type(request).__name__}")
            raise ValidationError("request must be an EmailVerificationVerifyRequest instance")
        
        logger.debug(f"Verify list request: {request}")
        
        # Prepare API call
        url = f"email-verification/{request.email_verification_id}/verify"
        logger.info(f"Starting verification for list: {request.email_verification_id}")
        
        # Make API call
        response = self.client.request("GET", url)
        
        # Create standardized response
        return self._create_response(
            response,
            EmailVerificationResponse(**response.json())
        )

    def get_results(self, request: EmailVerificationResultsRequest) -> APIResponse:
        """Get verification results for an email verification list.
        
        Args:
            request: The results request data with optional filters.
            
        Returns:
            APIResponse with EmailVerificationResultsResponse data
            
        Raises:
            ValidationError: If request validation fails
        """
        logger.debug("Starting get_results operation")
        
        # Validate request
        if not request:
            logger.error("EmailVerificationResultsRequest is required")
            raise ValidationError("EmailVerificationResultsRequest must be provided")
        
        if not isinstance(request, EmailVerificationResultsRequest):
            logger.error(f"Expected EmailVerificationResultsRequest, got {type(request).__name__}")
            raise ValidationError("request must be an EmailVerificationResultsRequest instance")
        
        logger.debug(f"Get results request: {request}")
        
        # Extract query parameters
        params = request.to_query_params()
        
        # Prepare API call
        url = f"email-verification/{request.email_verification_id}/results"
        logger.info(f"Getting verification results for list: {request.email_verification_id} with params: {params}")
        
        # Make API call
        response = self.client.request("GET", url, params=params)
        
        # Create standardized response
        return self._create_response(
            response,
            EmailVerificationResultsResponse(**response.json())
        ) 