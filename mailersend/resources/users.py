"""Users API resource."""

import logging
from typing import Optional

from ..models.base import APIResponse
from ..builders.users import UsersBuilder


logger = logging.getLogger(__name__)


class Users:
    """Users API resource."""

    def __init__(self, client):
        """Initialize the Users resource.
        
        Args:
            client: The MailerSend client instance
        """
        self.client = client

    def list_users(self) -> APIResponse:
        """Get a list of account users.
        
        Returns:
            APIResponse: Raw API response
        """
        logger.info("Listing account users")
        
        builder = UsersBuilder()
        request_data = builder.build_users_list()
        
        return self.client.request(
            method="GET",
            endpoint="/v1/users"
        )

    def get_user(self, user_id: str) -> APIResponse:
        """Get a single account user.
        
        Args:
            user_id: The user ID
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Getting user: {user_id}")
        
        builder = UsersBuilder()
        request_data = builder.user_id(user_id).build_user_get()
        
        return self.client.request(
            method="GET",
            endpoint=f"/v1/users/{request_data.user_id}"
        )

    def invite_user(
        self, 
        email: str, 
        role: str, 
        permissions: Optional[list] = None,
        templates: Optional[list] = None,
        domains: Optional[list] = None,
        requires_periodic_password_change: Optional[bool] = None
    ) -> APIResponse:
        """Invite a user to account.
        
        Args:
            email: The email address
            role: The role name
            permissions: List of permission names (required for Custom User role)
            templates: List of template IDs
            domains: List of domain IDs
            requires_periodic_password_change: Whether periodic password change is required
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Inviting user: {email} with role: {role}")
        
        builder = UsersBuilder()
        builder.email(email).role(role)
        
        if permissions:
            builder.permissions(permissions)
        if templates:
            builder.templates(templates)
        if domains:
            builder.domains(domains)
        if requires_periodic_password_change is not None:
            builder.requires_periodic_password_change(requires_periodic_password_change)
        
        request_data = builder.build_user_invite()
        
        json_data = {
            "email": request_data.email,
            "role": request_data.role,
            "permissions": request_data.permissions,
            "templates": request_data.templates,
            "domains": request_data.domains,
        }
        
        if request_data.requires_periodic_password_change is not None:
            json_data["requires_periodic_password_change"] = request_data.requires_periodic_password_change
        
        return self.client.request(
            method="POST",
            endpoint="/v1/users",
            json=json_data
        )

    def update_user(
        self, 
        user_id: str, 
        role: str, 
        permissions: Optional[list] = None,
        templates: Optional[list] = None,
        domains: Optional[list] = None,
        requires_periodic_password_change: Optional[bool] = None
    ) -> APIResponse:
        """Update account user.
        
        Args:
            user_id: The user ID
            role: The role name
            permissions: List of permission names (required for Custom User role)
            templates: List of template IDs
            domains: List of domain IDs
            requires_periodic_password_change: Whether periodic password change is required
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Updating user: {user_id} with role: {role}")
        
        builder = UsersBuilder()
        builder.user_id(user_id).role(role)
        
        if permissions:
            builder.permissions(permissions)
        if templates:
            builder.templates(templates)
        if domains:
            builder.domains(domains)
        if requires_periodic_password_change is not None:
            builder.requires_periodic_password_change(requires_periodic_password_change)
        
        request_data = builder.build_user_update()
        
        json_data = {
            "role": request_data.role,
            "permissions": request_data.permissions,
            "templates": request_data.templates,
            "domains": request_data.domains,
        }
        
        if request_data.requires_periodic_password_change is not None:
            json_data["requires_periodic_password_change"] = request_data.requires_periodic_password_change
        
        return self.client.request(
            method="PUT",
            endpoint=f"/v1/users/{request_data.user_id}",
            json=json_data
        )

    def delete_user(self, user_id: str) -> APIResponse:
        """Delete a user from account.
        
        Args:
            user_id: The user ID
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Deleting user: {user_id}")
        
        builder = UsersBuilder()
        request_data = builder.user_id(user_id).build_user_delete()
        
        return self.client.request(
            method="DELETE",
            endpoint=f"/v1/users/{request_data.user_id}"
        )

    def list_invites(self) -> APIResponse:
        """Get a list of invites.
        
        Returns:
            APIResponse: Raw API response
        """
        logger.info("Listing account invites")
        
        builder = UsersBuilder()
        request_data = builder.build_invites_list()
        
        return self.client.request(
            method="GET",
            endpoint="/v1/invites"
        )

    def get_invite(self, invite_id: str) -> APIResponse:
        """Get a single invite.
        
        Args:
            invite_id: The invite ID
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Getting invite: {invite_id}")
        
        builder = UsersBuilder()
        request_data = builder.invite_id(invite_id).build_invite_get()
        
        return self.client.request(
            method="GET",
            endpoint=f"/v1/invites/{request_data.invite_id}"
        )

    def resend_invite(self, invite_id: str) -> APIResponse:
        """Resend an invite.
        
        Args:
            invite_id: The invite ID
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Resending invite: {invite_id}")
        
        builder = UsersBuilder()
        request_data = builder.invite_id(invite_id).build_invite_resend()
        
        return self.client.request(
            method="POST",
            endpoint=f"/v1/invites/{request_data.invite_id}/resend"
        )

    def cancel_invite(self, invite_id: str) -> APIResponse:
        """Cancel an invite.
        
        Args:
            invite_id: The invite ID
            
        Returns:
            APIResponse: Raw API response
        """
        logger.info(f"Canceling invite: {invite_id}")
        
        builder = UsersBuilder()
        request_data = builder.invite_id(invite_id).build_invite_cancel()
        
        return self.client.request(
            method="DELETE",
            endpoint=f"/v1/invites/{request_data.invite_id}"
        ) 