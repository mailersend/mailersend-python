"""SMTP Users builder."""

from typing import Optional

from ..models.smtp_users import (
    SmtpUsersListRequest,
    SmtpUsersListQueryParams,
    SmtpUserGetRequest,
    SmtpUserCreateRequest,
    SmtpUserUpdateRequest,
    SmtpUserDeleteRequest,
)
from ..exceptions import ValidationError


class SmtpUsersBuilder:
    """Builder for SMTP Users requests."""

    def __init__(self):
        """Initialize the builder."""
        self._domain_id: Optional[str] = None
        self._smtp_user_id: Optional[str] = None
        self._name: Optional[str] = None
        self._enabled: Optional[bool] = None
        self._page: int = 1
        self._limit: int = 25

    def domain_id(self, domain_id: str) -> "SmtpUsersBuilder":
        """Set the domain ID.

        Args:
            domain_id: The domain ID

        Returns:
            Self for method chaining
        """
        self._domain_id = domain_id
        return self

    def smtp_user_id(self, smtp_user_id: str) -> "SmtpUsersBuilder":
        """Set the SMTP user ID.

        Args:
            smtp_user_id: The SMTP user ID

        Returns:
            Self for method chaining
        """
        self._smtp_user_id = smtp_user_id
        return self

    def name(self, name: str) -> "SmtpUsersBuilder":
        """Set the SMTP user name.

        Args:
            name: The SMTP user name

        Returns:
            Self for method chaining
        """
        self._name = name
        return self

    def enabled(self, enabled: bool) -> "SmtpUsersBuilder":
        """Set the enabled status.

        Args:
            enabled: Whether the SMTP user is enabled

        Returns:
            Self for method chaining
        """
        self._enabled = enabled
        return self

    def page(self, page: int) -> "SmtpUsersBuilder":
        """Set the page number for pagination.

        Args:
            page: The page number (minimum 1)

        Returns:
            Self for method chaining
        """
        if page < 1:
            raise ValidationError("Page must be >= 1")
        self._page = page
        return self

    def limit(self, limit: int) -> "SmtpUsersBuilder":
        """Set the limit for pagination.

        Args:
            limit: The limit (10-100)

        Returns:
            Self for method chaining
        """
        if limit < 10 or limit > 100:
            raise ValidationError("Limit must be between 10 and 100")
        self._limit = limit
        return self

    def build_smtp_users_list(self) -> SmtpUsersListRequest:
        """Build an SMTP users list request.

        Returns:
            SmtpUsersListRequest

        Raises:
            ValidationError: If domain_id is not set
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required")

        query_params = SmtpUsersListQueryParams(limit=self._limit)

        return SmtpUsersListRequest(
            domain_id=self._domain_id, query_params=query_params
        )

    def build_smtp_user_get(self) -> SmtpUserGetRequest:
        """Build an SMTP user get request.

        Returns:
            SmtpUserGetRequest

        Raises:
            ValidationError: If domain_id or smtp_user_id is not set
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required")
        if not self._smtp_user_id:
            raise ValidationError("SMTP User ID is required")

        return SmtpUserGetRequest(
            domain_id=self._domain_id, smtp_user_id=self._smtp_user_id
        )

    def build_smtp_user_create(self) -> SmtpUserCreateRequest:
        """Build an SMTP user create request.

        Returns:
            SmtpUserCreateRequest

        Raises:
            ValidationError: If domain_id or name is not set
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required")
        if not self._name:
            raise ValidationError("Name is required")

        return SmtpUserCreateRequest(
            domain_id=self._domain_id, name=self._name, enabled=self._enabled
        )

    def build_smtp_user_update(self) -> SmtpUserUpdateRequest:
        """Build an SMTP user update request.

        Returns:
            SmtpUserUpdateRequest

        Raises:
            ValidationError: If domain_id, smtp_user_id, or name is not set
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required")
        if not self._smtp_user_id:
            raise ValidationError("SMTP User ID is required")
        if not self._name:
            raise ValidationError("Name is required")

        return SmtpUserUpdateRequest(
            domain_id=self._domain_id,
            smtp_user_id=self._smtp_user_id,
            name=self._name,
            enabled=self._enabled,
        )

    def build_smtp_user_delete(self) -> SmtpUserDeleteRequest:
        """Build an SMTP user delete request.

        Returns:
            SmtpUserDeleteRequest

        Raises:
            ValidationError: If domain_id or smtp_user_id is not set
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required")
        if not self._smtp_user_id:
            raise ValidationError("SMTP User ID is required")

        return SmtpUserDeleteRequest(
            domain_id=self._domain_id, smtp_user_id=self._smtp_user_id
        )
