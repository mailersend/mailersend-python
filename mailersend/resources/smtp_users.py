"""SMTP Users API resource."""

from .base import BaseResource
from ..models.base import APIResponse
from ..models.smtp_users import (
    SmtpUsersListRequest,
    SmtpUserGetRequest,
    SmtpUserCreateRequest,
    SmtpUserUpdateRequest,
    SmtpUserDeleteRequest,
)


class SmtpUsers(BaseResource):
    """SMTP Users API resource."""

    def list_smtp_users(self, request: SmtpUsersListRequest) -> APIResponse:
        """List SMTP users for a domain.

        Args:
            request: The list SMTP users request

        Returns:
            APIResponse: API response with SMTP users list data
        """
        self.logger.debug(
            "Listing SMTP users for domain: %s with limit: %s",
            request.domain_id,
            request.query_params.limit,
        )

        # Extract query parameters
        params = request.to_query_params()

        # Make API call
        response = self.client.request(
            method="GET",
            path=f"domains/{request.domain_id}/smtp-users",
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
        self.logger.debug(
            "Getting SMTP user: %s from domain: %s",
            request.smtp_user_id,
            request.domain_id,
        )

        # Make API call
        response = self.client.request(
            method="GET",
            path=f"domains/{request.domain_id}/smtp-users/{request.smtp_user_id}",
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
        self.logger.debug(
            "Creating SMTP user: %s for domain: %s", request.name, request.domain_id
        )

        # Make API call
        response = self.client.request(
            method="POST",
            path=f"domains/{request.domain_id}/smtp-users",
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
        self.logger.debug(
            "Updating SMTP user: %s in domain: %s",
            request.smtp_user_id,
            request.domain_id,
        )

        # Make API call
        response = self.client.request(
            method="PUT",
            path=f"domains/{request.domain_id}/smtp-users/{request.smtp_user_id}",
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
        self.logger.debug(
            "Deleting SMTP user: %s from domain: %s",
            request.smtp_user_id,
            request.domain_id,
        )

        # Make API call
        response = self.client.request(
            method="DELETE",
            path=f"domains/{request.domain_id}/smtp-users/{request.smtp_user_id}",
        )

        # Create standardized response
        return self._create_response(response)
