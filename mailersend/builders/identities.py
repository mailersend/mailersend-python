from typing import Optional
from copy import deepcopy

from ..exceptions import ValidationError as MailerSendValidationError
from ..models.identities import (
    IdentityListRequest,
    IdentityListQueryParams,
    IdentityCreateRequest,
    IdentityGetRequest,
    IdentityGetByEmailRequest,
    IdentityUpdateRequest,
    IdentityUpdateByEmailRequest,
    IdentityDeleteRequest,
    IdentityDeleteByEmailRequest,
)


class IdentityBuilder:
    """Builder class for constructing identity-related requests."""

    def __init__(self):
        """Initialize the builder with default values."""
        self.reset()

    def reset(self):
        """Reset builder to initial state."""
        # List parameters
        self._domain_id: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None

        # Identity parameters
        self._identity_id: Optional[str] = None
        self._email: Optional[str] = None
        self._name: Optional[str] = None
        self._reply_to_email: Optional[str] = None
        self._reply_to_name: Optional[str] = None
        self._add_note: Optional[bool] = None
        self._personal_note: Optional[str] = None

        return self

    def copy(self):
        """Create a copy of the current builder."""
        new_builder = IdentityBuilder()
        new_builder._domain_id = self._domain_id
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._identity_id = self._identity_id
        new_builder._email = self._email
        new_builder._name = self._name
        new_builder._reply_to_email = self._reply_to_email
        new_builder._reply_to_name = self._reply_to_name
        new_builder._add_note = self._add_note
        new_builder._personal_note = self._personal_note
        return new_builder

    # Pagination methods
    def page(self, page: int):
        """Set the page number for pagination."""
        self._page = page
        return self

    def limit(self, limit: int):
        """Set the limit for pagination."""
        self._limit = limit
        return self

    # Filtering methods
    def domain_id(self, domain_id: str):
        """Set the domain ID for filtering or creation."""
        self._domain_id = domain_id
        return self

    # Identity identification methods
    def identity_id(self, identity_id: str):
        """Set the identity ID."""
        self._identity_id = identity_id
        return self

    def email(self, email: str):
        """Set the email address."""
        self._email = email
        return self

    # Identity data methods
    def name(self, name: str):
        """Set the identity name."""
        self._name = name
        return self

    def reply_to_email(self, reply_to_email: str):
        """Set the reply-to email address."""
        self._reply_to_email = reply_to_email
        return self

    def reply_to_name(self, reply_to_name: str):
        """Set the reply-to name."""
        self._reply_to_name = reply_to_name
        return self

    def add_note(self, add_note: bool):
        """Set whether to add a personal note."""
        self._add_note = add_note
        return self

    def personal_note(self, personal_note: str):
        """Set the personal note content."""
        self._personal_note = personal_note
        return self

    # Convenience methods
    def enable_personal_note(self, note: str):
        """Enable personal note with content."""
        self._add_note = True
        self._personal_note = note
        return self

    def disable_personal_note(self):
        """Disable personal note."""
        self._add_note = False
        self._personal_note = None
        return self

    def with_reply_to(self, email: str, name: Optional[str] = None):
        """Set reply-to email and optionally name."""
        self._reply_to_email = email
        if name is not None:
            self._reply_to_name = name
        return self

    def clear_reply_to(self):
        """Clear reply-to settings."""
        self._reply_to_email = None
        self._reply_to_name = None
        return self

    # Build methods
    def build_list_request(self) -> IdentityListRequest:
        """Build a request for listing identities."""
        query_params = IdentityListQueryParams()

        # Only set values if they were explicitly set by the user
        if self._page is not None:
            query_params.page = self._page
        if self._limit is not None:
            query_params.limit = self._limit
        if self._domain_id is not None:
            query_params.domain_id = self._domain_id

        return IdentityListRequest(query_params=query_params)

    def build_create_request(self) -> IdentityCreateRequest:
        """Build a request for creating an identity."""
        if not self._domain_id:
            raise MailerSendValidationError(
                "Domain ID is required for creating an identity"
            )
        if not self._name:
            raise MailerSendValidationError("Name is required for creating an identity")
        if not self._email:
            raise MailerSendValidationError(
                "Email is required for creating an identity"
            )

        return IdentityCreateRequest(
            domain_id=self._domain_id,
            name=self._name,
            email=self._email,
            reply_to_email=self._reply_to_email,
            reply_to_name=self._reply_to_name,
            add_note=self._add_note,
            personal_note=self._personal_note,
        )

    def build_get_request(self) -> IdentityGetRequest:
        """Build a request for getting an identity by ID."""
        if not self._identity_id:
            raise MailerSendValidationError(
                "Identity ID is required for getting an identity"
            )

        return IdentityGetRequest(identity_id=self._identity_id)

    def build_get_by_email_request(self) -> IdentityGetByEmailRequest:
        """Build a request for getting an identity by email."""
        if not self._email:
            raise MailerSendValidationError(
                "Email is required for getting an identity by email"
            )

        return IdentityGetByEmailRequest(email=self._email)

    def build_update_request(self) -> IdentityUpdateRequest:
        """Build a request for updating an identity by ID."""
        if not self._identity_id:
            raise MailerSendValidationError(
                "Identity ID is required for updating an identity"
            )

        return IdentityUpdateRequest(
            identity_id=self._identity_id,
            name=self._name,
            reply_to_email=self._reply_to_email,
            reply_to_name=self._reply_to_name,
            add_note=self._add_note,
            personal_note=self._personal_note,
        )

    def build_update_by_email_request(self) -> IdentityUpdateByEmailRequest:
        """Build a request for updating an identity by email."""
        if not self._email:
            raise MailerSendValidationError(
                "Email is required for updating an identity by email"
            )

        return IdentityUpdateByEmailRequest(
            email=self._email,
            name=self._name,
            reply_to_email=self._reply_to_email,
            reply_to_name=self._reply_to_name,
            add_note=self._add_note,
            personal_note=self._personal_note,
        )

    def build_delete_request(self) -> IdentityDeleteRequest:
        """Build a request for deleting an identity by ID."""
        if not self._identity_id:
            raise MailerSendValidationError(
                "Identity ID is required for deleting an identity"
            )

        return IdentityDeleteRequest(identity_id=self._identity_id)

    def build_delete_by_email_request(self) -> IdentityDeleteByEmailRequest:
        """Build a request for deleting an identity by email."""
        if not self._email:
            raise MailerSendValidationError(
                "Email is required for deleting an identity by email"
            )

        return IdentityDeleteByEmailRequest(email=self._email)
