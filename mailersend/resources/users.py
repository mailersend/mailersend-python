"""Users API resource."""

from .base import BaseResource
from ..models.base import APIResponse
from ..models.users import (
    UsersListRequest,
    UserGetRequest,
    UserInviteRequest,
    UserUpdateRequest,
    UserDeleteRequest,
    InvitesListRequest,
    InviteGetRequest,
    InviteResendRequest,
    InviteCancelRequest,
)


class Users(BaseResource):
    """Users API resource."""

    def list_users(self, request: UsersListRequest) -> APIResponse:
        """Get a list of account users.

        Args:
            request: The list users request

        Returns:
            APIResponse: API response with users list data
        """
        self.logger.debug(
            "Listing users with pagination: page=%s, limit=%s",
            request.query_params.page,
            request.query_params.limit,
        )

        # Extract query parameters
        params = request.to_query_params()

        # Make API call
        response = self.client.request(method="GET", path="users", params=params)

        # Create standardized response
        return self._create_response(response)

    def get_user(self, request: UserGetRequest) -> APIResponse:
        """Get a single account user.

        Args:
            request: The get user request

        Returns:
            APIResponse: API response with user data
        """
        self.logger.debug("Getting user: %s", request.user_id)

        # Make API call
        response = self.client.request(
            method="GET", path=f"users/{request.user_id}"
        )

        # Create standardized response
        return self._create_response(response)

    def invite_user(self, request: UserInviteRequest) -> APIResponse:
        """Invite a user to account.

        Args:
            request: The user invite request

        Returns:
            APIResponse: API response with invite data
        """
        self.logger.debug(
            "Inviting user: %s with role: %s", request.email, request.role
        )

        # Make API call
        response = self.client.request(
            method="POST", path="users", body=request.to_json()
        )

        # Create standardized response
        return self._create_response(response)

    def update_user(self, request: UserUpdateRequest) -> APIResponse:
        """Update account user.

        Args:
            request: The user update request

        Returns:
            APIResponse: API response with updated user data
        """
        self.logger.debug(
            "Updating user: %s with role: %s", request.user_id, request.role
        )

        # Make API call
        response = self.client.request(
            method="PUT", path=f"users/{request.user_id}", body=request.to_json()
        )

        # Create standardized response
        return self._create_response(response)

    def delete_user(self, request: UserDeleteRequest) -> APIResponse:
        """Delete account user.

        Args:
            request: The user delete request

        Returns:
            APIResponse: API response with delete confirmation
        """
        self.logger.debug("Deleting user: %s", request.user_id)

        # Make API call
        response = self.client.request(
            method="DELETE", path=f"users/{request.user_id}"
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
        self.logger.debug(
            "Listing invites with pagination: page=%s, limit=%s",
            request.query_params.page,
            request.query_params.limit,
        )

        # Extract query parameters
        params = request.to_query_params()

        # Make API call
        response = self.client.request(method="GET", path="invites", params=params)

        # Create standardized response
        return self._create_response(response)

    def get_invite(self, request: InviteGetRequest) -> APIResponse:
        """Get a single invite.

        Args:
            request: The get invite request

        Returns:
            APIResponse: API response with invite data
        """
        self.logger.debug("Getting invite: %s", request.invite_id)

        # Make API call
        response = self.client.request(
            method="GET", path=f"invites/{request.invite_id}"
        )

        # Create standardized response
        return self._create_response(response)

    def resend_invite(self, request: InviteResendRequest) -> APIResponse:
        """Resend an invite.

        Args:
            request: The invite resend request

        Returns:
            APIResponse: API response with resent invite data
        """
        self.logger.debug("Resending invite: %s", request.invite_id)

        # Make API call
        response = self.client.request(
            method="POST", path=f"invites/{request.invite_id}/resend"
        )

        # Create standardized response
        return self._create_response(response)

    def cancel_invite(self, request: InviteCancelRequest) -> APIResponse:
        """Cancel an invite.

        Args:
            request: The invite cancel request

        Returns:
            APIResponse: API response with cancel confirmation
        """
        self.logger.debug("Canceling invite: %s", request.invite_id)

        # Make API call
        response = self.client.request(
            method="DELETE", path=f"invites/{request.invite_id}"
        )

        # Create standardized response
        return self._create_response(response, None)
