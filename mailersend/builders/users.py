"""Builder for Users API."""

from typing import List, Optional, Dict, Any
from copy import deepcopy

from ..models.users import (
    UsersListRequest,
    UsersListQueryParams,
    UserGetRequest,
    UserInviteRequest,
    UserUpdateRequest,
    UserDeleteRequest,
    InvitesListRequest,
    InvitesListQueryParams,
    InviteGetRequest,
    InviteResendRequest,
    InviteCancelRequest,
)


class UsersBuilder:
    """Builder for Users API requests."""

    def __init__(self):
        """Initialize the builder."""
        self._user_id: Optional[str] = None
        self._invite_id: Optional[str] = None
        self._email: Optional[str] = None
        self._role: Optional[str] = None
        self._permissions: List[str] = []
        self._templates: List[str] = []
        self._domains: List[str] = []
        self._requires_periodic_password_change: Optional[bool] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None

    def user_id(self, user_id: str) -> "UsersBuilder":
        """Set the user ID.

        Args:
            user_id: The user ID

        Returns:
            Self for method chaining
        """
        self._user_id = user_id
        return self

    def invite_id(self, invite_id: str) -> "UsersBuilder":
        """Set the invite ID.

        Args:
            invite_id: The invite ID

        Returns:
            Self for method chaining
        """
        self._invite_id = invite_id
        return self

    def email(self, email: str) -> "UsersBuilder":
        """Set the email.

        Args:
            email: The email address

        Returns:
            Self for method chaining
        """
        self._email = email
        return self

    def role(self, role: str) -> "UsersBuilder":
        """Set the role.

        Args:
            role: The role name

        Returns:
            Self for method chaining
        """
        self._role = role
        return self

    def permissions(self, permissions: List[str]) -> "UsersBuilder":
        """Set the permissions list.

        Args:
            permissions: List of permission names

        Returns:
            Self for method chaining
        """
        self._permissions = permissions[:]
        return self

    def add_permission(self, permission: str) -> "UsersBuilder":
        """Add a permission to the list.

        Args:
            permission: The permission name

        Returns:
            Self for method chaining
        """
        if permission not in self._permissions:
            self._permissions.append(permission)
        return self

    def templates(self, templates: List[str]) -> "UsersBuilder":
        """Set the templates list.

        Args:
            templates: List of template IDs

        Returns:
            Self for method chaining
        """
        self._templates = templates[:]
        return self

    def add_template(self, template_id: str) -> "UsersBuilder":
        """Add a template to the list.

        Args:
            template_id: The template ID

        Returns:
            Self for method chaining
        """
        if template_id not in self._templates:
            self._templates.append(template_id)
        return self

    def domains(self, domains: List[str]) -> "UsersBuilder":
        """Set the domains list.

        Args:
            domains: List of domain IDs

        Returns:
            Self for method chaining
        """
        self._domains = domains[:]
        return self

    def add_domain(self, domain_id: str) -> "UsersBuilder":
        """Add a domain to the list.

        Args:
            domain_id: The domain ID

        Returns:
            Self for method chaining
        """
        if domain_id not in self._domains:
            self._domains.append(domain_id)
        return self

    def requires_periodic_password_change(self, requires: bool) -> "UsersBuilder":
        """Set whether periodic password change is required.

        Args:
            requires: Whether periodic password change is required

        Returns:
            Self for method chaining
        """
        self._requires_periodic_password_change = requires
        return self

    def page(self, page: int) -> "UsersBuilder":
        """Set the page number for pagination.

        Args:
            page: The page number (must be >= 1)

        Returns:
            Self for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "UsersBuilder":
        """Set the limit for pagination.

        Args:
            limit: The number of items per page (10-100)

        Returns:
            Self for method chaining
        """
        self._limit = limit
        return self

    # Helper methods for common roles
    def admin_role(self) -> "UsersBuilder":
        """Set role to Admin.

        Returns:
            Self for method chaining
        """
        return self.role("Admin")

    def manager_role(self) -> "UsersBuilder":
        """Set role to Manager.

        Returns:
            Self for method chaining
        """
        return self.role("Manager")

    def designer_role(self) -> "UsersBuilder":
        """Set role to Designer.

        Returns:
            Self for method chaining
        """
        return self.role("Designer")

    def accountant_role(self) -> "UsersBuilder":
        """Set role to Accountant.

        Returns:
            Self for method chaining
        """
        return self.role("Accountant")

    def custom_user_role(self) -> "UsersBuilder":
        """Set role to Custom User.

        Returns:
            Self for method chaining
        """
        return self.role("Custom User")

    # Helper methods for common permission groups
    def template_permissions(self) -> "UsersBuilder":
        """Add common template permissions.

        Returns:
            Self for method chaining
        """
        template_perms = [
            "read-all-templates",
            "read-own-templates",
            "manage-template",
            "read-filemanager",
        ]
        for perm in template_perms:
            self.add_permission(perm)
        return self

    def domain_permissions(self) -> "UsersBuilder":
        """Add common domain permissions.

        Returns:
            Self for method chaining
        """
        domain_perms = [
            "manage-domain",
            "manage-inbound",
            "manage-webhook",
            "control-sendings",
            "control-tracking-options",
            "access-smtp-credentials",
            "view-smtp-users",
            "manage-smtp-users",
        ]
        for perm in domain_perms:
            self.add_permission(perm)
        return self

    def analytics_permissions(self) -> "UsersBuilder":
        """Add analytics and activity permissions.

        Returns:
            Self for method chaining
        """
        analytics_perms = [
            "read-recipient",
            "read-activity",
            "read-email",
            "read-analytics",
        ]
        for perm in analytics_perms:
            self.add_permission(perm)
        return self

    def account_permissions(self) -> "UsersBuilder":
        """Add account management permissions.

        Returns:
            Self for method chaining
        """
        account_perms = [
            "manage-account",
            "read-invoice",
            "manage-api-token",
            "read-suppressions",
            "manage-suppressions",
            "read-ip-addresses",
            "manage-ip-addresses",
            "read-error-log",
        ]
        for perm in account_perms:
            self.add_permission(perm)
        return self

    def reset(self) -> "UsersBuilder":
        """Reset the builder state.

        Returns:
            Self for method chaining
        """
        self._user_id = None
        self._invite_id = None
        self._email = None
        self._role = None
        self._permissions = []
        self._templates = []
        self._domains = []
        self._requires_periodic_password_change = None
        self._page = None
        self._limit = None
        return self

    def copy(self) -> "UsersBuilder":
        """Create a copy of the current builder state.

        Returns:
            New UsersBuilder instance with copied state
        """
        new_builder = UsersBuilder()
        new_builder._user_id = self._user_id
        new_builder._invite_id = self._invite_id
        new_builder._email = self._email
        new_builder._role = self._role
        new_builder._permissions = self._permissions[:]
        new_builder._templates = self._templates[:]
        new_builder._domains = self._domains[:]
        new_builder._requires_periodic_password_change = (
            self._requires_periodic_password_change
        )
        new_builder._page = self._page
        new_builder._limit = self._limit
        return new_builder

    # Build methods for each API operation
    def build_users_list(self) -> UsersListRequest:
        """Build a request for listing users.

        Returns:
            UsersListRequest object
        """
        query_params = UsersListQueryParams()
        if self._page is not None:
            query_params.page = self._page
        if self._limit is not None:
            query_params.limit = self._limit

        return UsersListRequest(query_params=query_params)

    def build_user_get(self) -> UserGetRequest:
        """Build a request for getting a single user.

        Returns:
            UserGetRequest object

        Raises:
            ValueError: If user_id is not set
        """
        if not self._user_id:
            raise ValueError("user_id is required for getting a user")

        return UserGetRequest(user_id=self._user_id)

    def build_user_invite(self) -> UserInviteRequest:
        """Build a request for inviting a user.

        Returns:
            UserInviteRequest object

        Raises:
            ValueError: If required fields are missing
        """
        if not self._email:
            raise ValueError("email is required for inviting a user")
        if not self._role:
            raise ValueError("role is required for inviting a user")

        return UserInviteRequest(
            email=self._email,
            role=self._role,
            permissions=self._permissions,
            templates=self._templates,
            domains=self._domains,
            requires_periodic_password_change=self._requires_periodic_password_change,
        )

    def build_user_update(self) -> UserUpdateRequest:
        """Build a request for updating a user.

        Returns:
            UserUpdateRequest object

        Raises:
            ValueError: If required fields are missing
        """
        if not self._user_id:
            raise ValueError("user_id is required for updating a user")
        if not self._role:
            raise ValueError("role is required for updating a user")

        return UserUpdateRequest(
            user_id=self._user_id,
            role=self._role,
            permissions=self._permissions,
            templates=self._templates,
            domains=self._domains,
            requires_periodic_password_change=self._requires_periodic_password_change,
        )

    def build_user_delete(self) -> UserDeleteRequest:
        """Build a request for deleting a user.

        Returns:
            UserDeleteRequest object

        Raises:
            ValueError: If user_id is not set
        """
        if not self._user_id:
            raise ValueError("user_id is required for deleting a user")

        return UserDeleteRequest(user_id=self._user_id)

    def build_invites_list(self) -> InvitesListRequest:
        """Build a request for listing invites.

        Returns:
            InvitesListRequest object
        """
        query_params = InvitesListQueryParams()
        if self._page is not None:
            query_params.page = self._page
        if self._limit is not None:
            query_params.limit = self._limit

        return InvitesListRequest(query_params=query_params)

    def build_invite_get(self) -> InviteGetRequest:
        """Build a request for getting a single invite.

        Returns:
            InviteGetRequest object

        Raises:
            ValueError: If invite_id is not set
        """
        if not self._invite_id:
            raise ValueError("invite_id is required for getting an invite")

        return InviteGetRequest(invite_id=self._invite_id)

    def build_invite_resend(self) -> InviteResendRequest:
        """Build a request for resending an invite.

        Returns:
            InviteResendRequest object

        Raises:
            ValueError: If invite_id is not set
        """
        if not self._invite_id:
            raise ValueError("invite_id is required for resending an invite")

        return InviteResendRequest(invite_id=self._invite_id)

    def build_invite_cancel(self) -> InviteCancelRequest:
        """Build a request for canceling an invite.

        Returns:
            InviteCancelRequest object

        Raises:
            ValueError: If invite_id is not set
        """
        if not self._invite_id:
            raise ValueError("invite_id is required for canceling an invite")

        return InviteCancelRequest(invite_id=self._invite_id)
