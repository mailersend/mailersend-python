from typing import Union

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
    IdentityResponse,
)
from ..models.base import APIResponse
from .base import BaseResource


class IdentitiesResource(BaseResource):
    """Resource for managing sender identities."""

    def list_identities(self, request: IdentityListRequest) -> APIResponse:
        """
        Get a list of sender identities.

        Args:
            request: The identity list request containing filtering and pagination parameters

        Returns:
            APIResponse containing the identities list response

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, IdentityListRequest):
            raise MailerSendValidationError(
                "Request must be an instance of IdentityListRequest"
            )

        self.logger.debug("Preparing to list identities with query parameters")

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(
            f"Making API request to list identities with params: {params}"
        )

        # Make API request
        response = self.client.request(
            method="GET", endpoint="/identities", params=params if params else None
        )

        return self._create_response(response, IdentityListResponse)

    def create_identity(self, request: IdentityCreateRequest) -> APIResponse:
        """
        Create a new sender identity.

        Args:
            request: The identity creation request with all required data

        Returns:
            APIResponse containing the created identity response

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, IdentityCreateRequest):
            raise MailerSendValidationError(
                "Request must be an instance of IdentityCreateRequest"
            )

        self.logger.debug("Preparing to create identity")

        # Build request body
        data = request.model_dump(by_alias=True, exclude_none=True)

        self.logger.debug(
            f"Making API request to create identity with data keys: {list(data.keys())}"
        )

        # Make API request
        response = self.client.request(method="POST", endpoint="/identities", body=data)

        return self._create_response(response, IdentityResponse)

    def get_identity(self, request: IdentityGetRequest) -> APIResponse:
        """
        Get a single sender identity by ID.

        Args:
            request: The identity get request with identity ID

        Returns:
            APIResponse containing the identity data

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, IdentityGetRequest):
            raise MailerSendValidationError(
                "Request must be an instance of IdentityGetRequest"
            )

        self.logger.debug(f"Preparing to get identity with ID: {request.identity_id}")

        # Make API request
        response = self.client.request(
            method="GET", endpoint=f"/identities/{request.identity_id}"
        )

        return self._create_response(response, IdentityResponse)

    def get_identity_by_email(self, request: IdentityGetByEmailRequest) -> APIResponse:
        """
        Get a single sender identity by email.

        Args:
            request: The identity get by email request

        Returns:
            APIResponse containing the identity data

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, IdentityGetByEmailRequest):
            raise MailerSendValidationError(
                "Request must be an instance of IdentityGetByEmailRequest"
            )

        self.logger.debug(f"Preparing to get identity by email: {request.email}")

        # Make API request
        response = self.client.request(
            method="GET", endpoint=f"/identities/email/{request.email}"
        )

        return self._create_response(response, IdentityResponse)

    def update_identity(self, request: IdentityUpdateRequest) -> APIResponse:
        """
        Update a sender identity by ID.

        Args:
            request: The identity update request with identity ID and update data

        Returns:
            APIResponse containing the updated identity

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, IdentityUpdateRequest):
            raise MailerSendValidationError(
                "Request must be an instance of IdentityUpdateRequest"
            )

        self.logger.debug(
            f"Preparing to update identity with ID: {request.identity_id}"
        )

        # Build request body, excluding identity_id (goes in URL)
        data = request.model_dump(
            by_alias=True, exclude_none=True, exclude={"identity_id"}
        )

        self.logger.debug(
            f"Making API request to update identity with data keys: {list(data.keys())}"
        )

        # Make API request
        response = self.client.request(
            method="PUT",
            endpoint=f"/identities/{request.identity_id}",
            body=data if data else None,
        )

        return self._create_response(response, IdentityResponse)

    def update_identity_by_email(
        self, request: IdentityUpdateByEmailRequest
    ) -> APIResponse:
        """
        Update a sender identity by email.

        Args:
            request: The identity update by email request

        Returns:
            APIResponse containing the updated identity

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, IdentityUpdateByEmailRequest):
            raise MailerSendValidationError(
                "Request must be an instance of IdentityUpdateByEmailRequest"
            )

        self.logger.debug(f"Preparing to update identity by email: {request.email}")

        # Build request body, excluding email (goes in URL)
        data = request.model_dump(by_alias=True, exclude_none=True, exclude={"email"})

        self.logger.debug(
            f"Making API request to update identity by email with data keys: {list(data.keys())}"
        )

        # Make API request
        response = self.client.request(
            method="PUT",
            endpoint=f"/identities/email/{request.email}",
            body=data if data else None,
        )

        return self._create_response(response, IdentityResponse)

    def delete_identity(self, request: IdentityDeleteRequest) -> APIResponse:
        """
        Delete a sender identity by ID.

        Args:
            request: The identity delete request with identity ID

        Returns:
            APIResponse containing the deletion result

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, IdentityDeleteRequest):
            raise MailerSendValidationError(
                "Request must be an instance of IdentityDeleteRequest"
            )

        self.logger.debug(
            f"Preparing to delete identity with ID: {request.identity_id}"
        )

        # Make API request
        response = self.client.request(
            method="DELETE", endpoint=f"/identities/{request.identity_id}"
        )

        return self._create_response(response)

    def delete_identity_by_email(
        self, request: IdentityDeleteByEmailRequest
    ) -> APIResponse:
        """
        Delete a sender identity by email.

        Args:
            request: The identity delete by email request

        Returns:
            APIResponse containing the deletion result

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, IdentityDeleteByEmailRequest):
            raise MailerSendValidationError(
                "Request must be an instance of IdentityDeleteByEmailRequest"
            )

        self.logger.debug(f"Preparing to delete identity by email: {request.email}")

        # Make API request
        response = self.client.request(
            method="DELETE", endpoint=f"/identities/email/{request.email}"
        )

        return self._create_response(response)
