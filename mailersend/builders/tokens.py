"""Builder for Tokens API."""

from typing import List, Optional, Dict, Any
from copy import deepcopy

from ..models.tokens import (
    TOKEN_SCOPES,
    TokensListRequest,
    TokenGetRequest,
    TokenCreateRequest,
    TokenUpdateRequest,
    TokenUpdateNameRequest,
    TokenDeleteRequest,
)


class TokensBuilder:
    """Builder for Tokens API requests."""

    def __init__(self):
        """Initialize the builder."""
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._token_id: Optional[str] = None
        self._name: Optional[str] = None
        self._domain_id: Optional[str] = None
        self._scopes: List[str] = []
        self._status: Optional[str] = None

    def page(self, page: int) -> "TokensBuilder":
        """Set the page number for pagination.

        Args:
            page: The page number (must be >= 1)

        Returns:
            Self for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "TokensBuilder":
        """Set the limit for pagination.

        Args:
            limit: The number of items per page (10-100)

        Returns:
            Self for method chaining
        """
        self._limit = limit
        return self

    def token_id(self, token_id: str) -> "TokensBuilder":
        """Set the token ID.

        Args:
            token_id: The token ID

        Returns:
            Self for method chaining
        """
        self._token_id = token_id
        return self

    def name(self, name: str) -> "TokensBuilder":
        """Set the token name.

        Args:
            name: The token name (max 50 characters)

        Returns:
            Self for method chaining
        """
        self._name = name
        return self

    def domain_id(self, domain_id: str) -> "TokensBuilder":
        """Set the domain ID.

        Args:
            domain_id: The domain ID

        Returns:
            Self for method chaining
        """
        self._domain_id = domain_id
        return self

    def scopes(self, scopes: List[str]) -> "TokensBuilder":
        """Set the scopes list.

        Args:
            scopes: List of scope names

        Returns:
            Self for method chaining
        """
        self._scopes = scopes[:]
        return self

    def add_scope(self, scope: str) -> "TokensBuilder":
        """Add a scope to the list.

        Args:
            scope: The scope name

        Returns:
            Self for method chaining
        """
        if scope not in self._scopes:
            self._scopes.append(scope)
        return self

    def status(self, status: str) -> "TokensBuilder":
        """Set the token status.

        Args:
            status: The token status ('pause' or 'unpause')

        Returns:
            Self for method chaining
        """
        self._status = status
        return self

    # Helper methods for token status
    def pause(self) -> "TokensBuilder":
        """Set token status to pause.

        Returns:
            Self for method chaining
        """
        return self.status("pause")

    def unpause(self) -> "TokensBuilder":
        """Set token status to unpause.

        Returns:
            Self for method chaining
        """
        return self.status("unpause")

    # Helper methods for scope groups
    def email_scopes(self) -> "TokensBuilder":
        """Add email-related scopes.

        Returns:
            Self for method chaining
        """
        email_scopes = ["email_full"]
        for scope in email_scopes:
            self.add_scope(scope)
        return self

    def domains_read_scope(self) -> "TokensBuilder":
        """Add domains read scope.

        Returns:
            Self for method chaining
        """
        return self.add_scope("domains_read")

    def domains_full_scope(self) -> "TokensBuilder":
        """Add domains full scope.

        Returns:
            Self for method chaining
        """
        return self.add_scope("domains_full")

    def activity_scopes(self) -> "TokensBuilder":
        """Add activity-related scopes.

        Returns:
            Self for method chaining
        """
        activity_scopes = ["activity_read", "activity_full"]
        for scope in activity_scopes:
            self.add_scope(scope)
        return self

    def analytics_scopes(self) -> "TokensBuilder":
        """Add analytics-related scopes.

        Returns:
            Self for method chaining
        """
        analytics_scopes = ["analytics_read", "analytics_full"]
        for scope in analytics_scopes:
            self.add_scope(scope)
        return self

    def tokens_scope(self) -> "TokensBuilder":
        """Add tokens full scope.

        Returns:
            Self for method chaining
        """
        return self.add_scope("tokens_full")

    def webhooks_scope(self) -> "TokensBuilder":
        """Add webhooks full scope.

        Returns:
            Self for method chaining
        """
        return self.add_scope("webhooks_full")

    def templates_scope(self) -> "TokensBuilder":
        """Add templates full scope.

        Returns:
            Self for method chaining
        """
        return self.add_scope("templates_full")

    def suppressions_scopes(self) -> "TokensBuilder":
        """Add suppressions-related scopes.

        Returns:
            Self for method chaining
        """
        suppressions_scopes = ["suppressions_read", "suppressions_full"]
        for scope in suppressions_scopes:
            self.add_scope(scope)
        return self

    def sms_scopes(self) -> "TokensBuilder":
        """Add SMS-related scopes.

        Returns:
            Self for method chaining
        """
        sms_scopes = ["sms_full", "sms_read"]
        for scope in sms_scopes:
            self.add_scope(scope)
        return self

    def email_verification_scopes(self) -> "TokensBuilder":
        """Add email verification-related scopes.

        Returns:
            Self for method chaining
        """
        verification_scopes = ["email_verification_read", "email_verification_full"]
        for scope in verification_scopes:
            self.add_scope(scope)
        return self

    def inbound_scope(self) -> "TokensBuilder":
        """Add inbounds full scope.

        Returns:
            Self for method chaining
        """
        return self.add_scope("inbounds_full")

    def recipients_scopes(self) -> "TokensBuilder":
        """Add recipients-related scopes.

        Returns:
            Self for method chaining
        """
        recipients_scopes = ["recipients_read", "recipients_full"]
        for scope in recipients_scopes:
            self.add_scope(scope)
        return self

    def sender_identity_scopes(self) -> "TokensBuilder":
        """Add sender identity-related scopes.

        Returns:
            Self for method chaining
        """
        identity_scopes = ["sender_identity_read", "sender_identity_full"]
        for scope in identity_scopes:
            self.add_scope(scope)
        return self

    def users_scopes(self) -> "TokensBuilder":
        """Add users-related scopes.

        Returns:
            Self for method chaining
        """
        users_scopes = ["users_read", "users_full"]
        for scope in users_scopes:
            self.add_scope(scope)
        return self

    def smtp_users_scopes(self) -> "TokensBuilder":
        """Add SMTP users-related scopes.

        Returns:
            Self for method chaining
        """
        smtp_scopes = ["smtp_users_read", "smtp_users_full"]
        for scope in smtp_scopes:
            self.add_scope(scope)
        return self

    def all_read_scopes(self) -> "TokensBuilder":
        """Add all read-only scopes.

        Returns:
            Self for method chaining
        """
        read_scopes = [
            "domains_read",
            "activity_read",
            "analytics_read",
            "suppressions_read",
            "sms_read",
            "email_verification_read",
            "recipients_read",
            "sender_identity_read",
            "users_read",
            "smtp_users_read",
        ]
        for scope in read_scopes:
            self.add_scope(scope)
        return self

    def all_scopes(self) -> "TokensBuilder":
        """Add all available scopes.

        Returns:
            Self for method chaining
        """
        for scope in TOKEN_SCOPES:
            self.add_scope(scope)
        return self

    def reset(self) -> "TokensBuilder":
        """Reset the builder state.

        Returns:
            Self for method chaining
        """
        self._page = None
        self._limit = None
        self._token_id = None
        self._name = None
        self._domain_id = None
        self._scopes = []
        self._status = None
        return self

    def copy(self) -> "TokensBuilder":
        """Create a copy of the current builder state.

        Returns:
            New TokensBuilder instance with copied state
        """
        new_builder = TokensBuilder()
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._token_id = self._token_id
        new_builder._name = self._name
        new_builder._domain_id = self._domain_id
        new_builder._scopes = self._scopes[:]
        new_builder._status = self._status
        return new_builder

    # Build methods for each API operation
    def build_tokens_list(self) -> TokensListRequest:
        """Build a request for listing tokens.

        Returns:
            TokensListRequest object
        """
        from ..models.tokens import TokensListQueryParams

        # Build query params with defaults
        query_params_kwargs = {}
        if self._page is not None:
            query_params_kwargs["page"] = self._page
        if self._limit is not None:
            query_params_kwargs["limit"] = self._limit

        query_params = TokensListQueryParams(**query_params_kwargs)

        return TokensListRequest(query_params=query_params)

    def build_token_get(self) -> TokenGetRequest:
        """Build a request for getting a single token.

        Returns:
            TokenGetRequest object

        Raises:
            ValueError: If token_id is not set
        """
        if not self._token_id:
            raise ValueError("token_id is required for getting a token")

        return TokenGetRequest(token_id=self._token_id)

    def build_token_create(self) -> TokenCreateRequest:
        """Build a request for creating a token.

        Returns:
            TokenCreateRequest object

        Raises:
            ValueError: If required fields are missing
        """
        if not self._name:
            raise ValueError("name is required for creating a token")
        if not self._domain_id:
            raise ValueError("domain_id is required for creating a token")
        if not self._scopes:
            raise ValueError("scopes are required for creating a token")

        return TokenCreateRequest(
            name=self._name, domain_id=self._domain_id, scopes=self._scopes
        )

    def build_token_update(self) -> TokenUpdateRequest:
        """Build a request for updating a token status.

        Returns:
            TokenUpdateRequest object

        Raises:
            ValueError: If required fields are missing
        """
        if not self._token_id:
            raise ValueError("token_id is required for updating a token")
        if not self._status:
            raise ValueError("status is required for updating a token")

        return TokenUpdateRequest(token_id=self._token_id, status=self._status)

    def build_token_update_name(self) -> TokenUpdateNameRequest:
        """Build a request for updating a token name.

        Returns:
            TokenUpdateNameRequest object

        Raises:
            ValueError: If required fields are missing
        """
        if not self._token_id:
            raise ValueError("token_id is required for updating a token name")
        if not self._name:
            raise ValueError("name is required for updating a token name")

        return TokenUpdateNameRequest(token_id=self._token_id, name=self._name)

    def build_token_delete(self) -> TokenDeleteRequest:
        """Build a request for deleting a token.

        Returns:
            TokenDeleteRequest object

        Raises:
            ValueError: If token_id is not set
        """
        if not self._token_id:
            raise ValueError("token_id is required for deleting a token")

        return TokenDeleteRequest(token_id=self._token_id)
