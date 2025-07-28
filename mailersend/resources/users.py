"""Users API resource."""

import logging
from typing import Optional, List

from .base import BaseResource
from ..models.base import APIResponse
from ..models.users import (
    UsersListRequest, UserGetRequest, UserInviteRequest, UserUpdateRequest, UserDeleteRequest,
    InvitesListRequest, InviteGetRequest, InviteResendRequest, InviteCancelRequest,
    UsersListResponse, UserResponse, UserInviteResponse, UserUpdateResponse,
    InvitesListResponse, InviteResponse, InviteResendResponse
)
from ..builders.users import UsersBuilder


logger = logging.getLogger(__name__)


class Users(BaseResource):
    """Users API resource."""

    def list_users(self, request: UsersListRequest) -> APIResponse:
        """Get a list of account users.

        Args:
            request: The list users request

        Returns:
            APIResponse: API response with users list data
        """
        logger.info(f"Listing users with pagination: page={request.query_params.page}, limit={request.query_params.limit}")

        # Extract query parameters
        params = request.to_query_params()

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint="/v1/users",
            params=params
        )

        # Create standardized response
        return self._create_response(response, UsersListResponse(**response.json()))

    def get_user(self, request: UserGetRequest) -> APIResponse:
        """Get a single account user.

        Args:
            request: The get user request

        Returns:
            APIResponse: API response with user data
        """
        logger.info(f"Getting user: {request.user_id}")

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint=f"/v1/users/{request.user_id}"
        )

        # Create standardized response
        return self._create_response(response, UserResponse(**response.json()))

    def invite_user(self, request: UserInviteRequest) -> APIResponse:
        """Invite a user to account.

        Args:
            request: The user invite request

        Returns:
            APIResponse: API response with invite data
        """
        logger.info(f"Inviting user: {request.email} with role: {request.role}")

        # Make API call
        response = self.client.request(
            method="POST",
            endpoint="/v1/users",
            json=request.to_json()
        )

        # Create standardized response
        return self._create_response(response, UserInviteResponse(**response.json()))

    def update_user(self, request: UserUpdateRequest) -> APIResponse:
        """Update account user.

        Args:
            request: The user update request

        Returns:
            APIResponse: API response with updated user data
        """
        logger.info(f"Updating user: {request.user_id} with role: {request.role}")

        # Make API call
        response = self.client.request(
            method="PUT",
            endpoint=f"/v1/users/{request.user_id}",
            json=request.to_json()
        )

        # Create standardized response
        return self._create_response(response, UserUpdateResponse(**response.json()))

    def delete_user(self, request: UserDeleteRequest) -> APIResponse:
        """Delete account user.

        Args:
            request: The user delete request

        Returns:
            APIResponse: API response with delete confirmation
        """
        logger.info(f"Deleting user: {request.user_id}")

        # Make API call
        response = self.client.request(
            method="DELETE",
            endpoint=f"/v1/users/{request.user_id}"
        )

        # Create standardized response
        return self._create_response(response, None)

    def list_invites(self, request: InvitesListRequest) -> APIResponse:
        """Get a list of invites.

        Args:
            request: The list invites request

        Returns:
            APIResponse: API response with invites list data
        """
        logger.info(f"Listing invites with pagination: page={request.query_params.page}, limit={request.query_params.limit}")

        # Extract query parameters
        params = request.to_query_params()

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint="/v1/invites",
            params=params
        )

        # Create standardized response
        return self._create_response(response, InvitesListResponse(**response.json()))

    def get_invite(self, request: InviteGetRequest) -> APIResponse:
        """Get a single invite.

        Args:
            request: The get invite request

        Returns:
            APIResponse: API response with invite data
        """
        logger.info(f"Getting invite: {request.invite_id}")

        # Make API call
        response = self.client.request(
            method="GET",
            endpoint=f"/v1/invites/{request.invite_id}"
        )

        # Create standardized response
        return self._create_response(response, InviteResponse(**response.json()))

    def resend_invite(self, request: InviteResendRequest) -> APIResponse:
        """Resend an invite.

        Args:
            request: The invite resend request

        Returns:
            APIResponse: API response with resent invite data
        """
        logger.info(f"Resending invite: {request.invite_id}")

        # Make API call
        response = self.client.request(
            method="POST",
            endpoint=f"/v1/invites/{request.invite_id}/resend"
        )

        # Create standardized response
        return self._create_response(response, InviteResendResponse(**response.json()))

    def cancel_invite(self, request: InviteCancelRequest) -> APIResponse:
        """Cancel an invite.

        Args:
            request: The invite cancel request

        Returns:
            APIResponse: API response with cancel confirmation
        """
        logger.info(f"Canceling invite: {request.invite_id}")

        # Make API call
        response = self.client.request(
            method="DELETE",
            endpoint=f"/v1/invites/{request.invite_id}"
        )

        # Create standardized response
        return self._create_response(response, None) 