"""Email Verification resource"""

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
)
from ..exceptions import ValidationError


class EmailVerification(BaseResource):
    """Resource for managing email verification through the MailerSend API."""

    def verify_email(self, request: EmailVerifyRequest) -> APIResponse:
        """Verify a single email address (synchronous).

        Args:
            request: The email verification request data.

        Returns:
            APIResponse with verification result
        """
        self.logger.debug("Starting verify_email operation")

        # Prepare request body
        body = request.model_dump(exclude_none=True)

        self.logger.debug("Verifying email address: %s", body)

        # Make API call
        response = self.client.request("POST", "email-verification/verify", body=body)

        # Create standardized response
        return self._create_response(response)

    def verify_email_async(self, request: EmailVerifyAsyncRequest) -> APIResponse:
        """Verify a single email address (asynchronous).

        Args:
            request: The async email verification request data.

        Returns:
            APIResponse with verification result
        """
        self.logger.debug("Starting verify_email_async operation")
        self.logger.debug("Async email verify request: %s", request)

        # Prepare request body
        body = request.model_dump(exclude_none=True)

        self.logger.debug("Starting async verification for email: %s", body)

        # Make API call
        response = self.client.request(
            "POST", "email-verification/verify-async", body=body
        )

        # Create standardized response
        return self._create_response(response)

    def get_async_status(
        self, request: EmailVerificationAsyncStatusRequest
    ) -> APIResponse:
        """Get the status of an async email verification.

        Args:
            request: The async status request data.

        Returns:
            APIResponse with EmailVerificationAsyncStatusResponse data
        """
        self.logger.debug("Starting get_async_status operation")

        # Prepare API call
        self.logger.debug(
            "Getting async verification status for ID: %s",
            request.email_verification_id,
        )

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint=f"email-verification/verify-async/{request.email_verification_id}",
        )

        # Create standardized response
        return self._create_response(response)

    def list_verifications(self, request: EmailVerificationListsRequest) -> APIResponse:
        """List all email verification lists.

        Args:
            request: The list request data with pagination options.

        Returns:
            APIResponse with list of email verification lists
        """
        self.logger.debug("Starting list_verifications operation")

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug("Listing email verification lists with params: %s", params)

        # Make API call
        response = self.client.request(
            method="GET", endpoint="email-verification", params=params
        )

        # Create standardized response
        return self._create_response(response)

    def get_verification(self, request: EmailVerificationGetRequest) -> APIResponse:
        """Get a single email verification list.

        Args:
            request: The get verification request data.

        Returns:
            APIResponse with email verification list data
        """
        self.logger.debug("Starting get_verification operation")

        # Prepare API call
        self.logger.debug(
            "Getting email verification list: %s", request.email_verification_id
        )

        # Make API call
        response = self.client.request(
            method="GET", endpoint=f"email-verification/{request.email_verification_id}"
        )

        # Create standardized response
        return self._create_response(response)

    def create_verification(
        self, request: EmailVerificationCreateRequest
    ) -> APIResponse:
        """Create a new email verification list.

        Args:
            request: The create verification request data.

        Returns:
            APIResponse with email verification list data
        """
        self.logger.debug("Starting create_verification operation")

        # Prepare request body
        body = request.model_dump(exclude_none=True)

        self.logger.debug(
            "Creating email verification list: %s with %s emails",
            request.name,
            len(request.emails),
        )

        # Make API call
        response = self.client.request("POST", "email-verification", body=body)

        # Create standardized response
        return self._create_response(response)

    def verify_list(self, request: EmailVerificationVerifyRequest) -> APIResponse:
        """Start verification of an email verification list.

        Args:
            request: The verify list request data.

        Returns:
            APIResponse with verification result
        """
        self.logger.debug("Starting verify_list operation")
        self.logger.debug(
            "Starting verification for list: %s", request.email_verification_id
        )

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint=f"email-verification/{request.email_verification_id}/verify",
        )

        # Create standardized response
        return self._create_response(response)

    def get_results(self, request: EmailVerificationResultsRequest) -> APIResponse:
        """Get verification results for an email verification list.

        Args:
            request: The results request data with optional filters.

        Returns:
            APIResponse with verification results
        """
        self.logger.debug("Starting get_results operation")

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(
            "Getting verification results for list: %s with params: %s",
            request.email_verification_id,
            params,
        )

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint=f"email-verification/{request.email_verification_id}/results",
            params=params,
        )

        # Create standardized response
        return self._create_response(response)
