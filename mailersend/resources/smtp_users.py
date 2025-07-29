"""SMTP Users API resource."""

import logging

from .base import BaseResource
from ..models.base import APIResponse
from ..models.smtp_users import (
    SmtpUsersListRequest,
    SmtpUserGetRequest,
    SmtpUserCreateRequest,
    SmtpUserUpdateRequest,
    SmtpUserDeleteRequest,
)


logger = logging.getLogger(__name__)


class SmtpUsers(BaseResource):
    """SMTP Users API resource."""

    def list_smtp_users(self, request: SmtpUsersListRequest) -> APIResponse:
        """List SMTP users for a domain.

        Args:
            request: The list SMTP users request

        Returns:
            APIResponse: API response with SMTP users list data
        """
        logger.info(
            f"Listing SMTP users for domain: {request.domain_id} with limit: {request.query_params.limit}"
        )

        # Extract query parameters
        params = request.to_query_params()

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint=f"domains/{request.domain_id}/smtp-users",
            params=params,
        )

        # Create standardized response
        return self._create_response(response)

    def get_smtp_user(self, request: SmtpUserGetRequest) -> APIResponse:
        """Get a single SMTP user.

        Args:
            request: The get SMTP user request

        Returns:
            APIResponse: API response with SMTP user data
        """
        logger.info(
            f"Getting SMTP user: {request.smtp_user_id} from domain: {request.domain_id}"
        )

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint=f"domains/{request.domain_id}/smtp-users/{request.smtp_user_id}",
        )

        # Create standardized response
        return self._create_response(response)

    def create_smtp_user(self, request: SmtpUserCreateRequest) -> APIResponse:
        """Create an SMTP user.

        Args:
            request: The create SMTP user request

        Returns:
            APIResponse: API response with SMTP user creation data
        """
        logger.info(
            f"Creating SMTP user: {request.name} for domain: {request.domain_id}"
        )

        # Make API call
        response = self.client.request(
            method="POST",
            endpoint=f"domains/{request.domain_id}/smtp-users",
            body=request.to_json(),
        )

        # Create standardized response
        return self._create_response(response)

    def update_smtp_user(self, request: SmtpUserUpdateRequest) -> APIResponse:
        """Update an SMTP user.

        Args:
            request: The update SMTP user request

        Returns:
            APIResponse: API response with updated SMTP user data
        """
        logger.info(
            f"Updating SMTP user: {request.smtp_user_id} in domain: {request.domain_id}"
        )

        # Make API call
        response = self.client.request(
            method="PUT",
            endpoint=f"domains/{request.domain_id}/smtp-users/{request.smtp_user_id}",
            body=request.to_json(),
        )

        # Create standardized response
        return self._create_response(response)

    def delete_smtp_user(self, request: SmtpUserDeleteRequest) -> APIResponse:
        """Delete an SMTP user.

        Args:
            request: The delete SMTP user request

        Returns:
            APIResponse: API response with delete confirmation
        """
        logger.info(
            f"Deleting SMTP user: {request.smtp_user_id} from domain: {request.domain_id}"
        )

        # Make API call
        response = self.client.request(
            method="DELETE",
            endpoint=f"domains/{request.domain_id}/smtp-users/{request.smtp_user_id}",
        )

        # Create standardized response
        return self._create_response(response)
