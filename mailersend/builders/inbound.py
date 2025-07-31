from typing import List, Optional, Dict, Any
from pydantic import ValidationError as PydanticValidationError

from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.inbound import (
    InboundListRequest,
    InboundListQueryParams,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
    InboundFilterGroup,
    InboundForward,
)


class InboundBuilder:
    """Builder for constructing inbound route requests with a fluent API."""

    def __init__(self):
        """Initialize the builder with default values."""
        self.reset()

    def reset(self) -> "InboundBuilder":
        """Reset the builder to its initial state."""
        self._domain_id: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._inbound_id: Optional[str] = None
        self._name: Optional[str] = None
        self._domain_enabled: Optional[bool] = None
        self._inbound_domain: Optional[str] = None
        self._inbound_priority: Optional[int] = None
        self._catch_filter: List[InboundFilterGroup] = []
        self._catch_type: Optional[str] = None
        self._match_filter: List[InboundFilterGroup] = []
        self._match_type: Optional[str] = None
        self._forwards: List[InboundForward] = []
        return self

    def copy(self) -> "InboundBuilder":
        """Create a copy of the current builder state."""
        new_builder = InboundBuilder()
        new_builder._domain_id = self._domain_id
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._inbound_id = self._inbound_id
        new_builder._name = self._name
        new_builder._domain_enabled = self._domain_enabled
        new_builder._inbound_domain = self._inbound_domain
        new_builder._inbound_priority = self._inbound_priority
        new_builder._catch_filter = self._catch_filter.copy()
        new_builder._catch_type = self._catch_type
        new_builder._match_filter = self._match_filter.copy()
        new_builder._match_type = self._match_type
        new_builder._forwards = self._forwards.copy()
        return new_builder

    # Pagination methods
    def page(self, page: int) -> "InboundBuilder":
        """Set the page number for pagination."""
        self._page = page
        return self

    def limit(self, limit: int) -> "InboundBuilder":
        """Set the limit for pagination."""
        self._limit = limit
        return self

    # Filtering methods
    def domain_id(self, domain_id: str) -> "InboundBuilder":
        """Set the domain ID filter."""
        self._domain_id = domain_id
        return self

    # Identification methods
    def inbound_id(self, inbound_id: str) -> "InboundBuilder":
        """Set the inbound route ID."""
        self._inbound_id = inbound_id
        return self

    # Basic configuration methods
    def name(self, name: str) -> "InboundBuilder":
        """Set the inbound route name."""
        self._name = name
        return self

    def domain_enabled(self, enabled: bool) -> "InboundBuilder":
        """Set whether the domain is enabled."""
        self._domain_enabled = enabled
        return self

    def inbound_domain(self, domain: str) -> "InboundBuilder":
        """Set the inbound domain."""
        self._inbound_domain = domain
        return self

    def inbound_priority(self, priority: int) -> "InboundBuilder":
        """Set the inbound priority."""
        self._inbound_priority = priority
        return self

    def catch_type(self, catch_type: str) -> "InboundBuilder":
        """Set the catch type (all or one)."""
        self._catch_type = catch_type
        return self

    def match_type(self, match_type: str) -> "InboundBuilder":
        """Set the match type (all or one)."""
        self._match_type = match_type
        return self

    # Filter management methods
    def add_catch_filter(
        self, filter_type: str, filters: Optional[List[Dict[str, Any]]] = None
    ) -> "InboundBuilder":
        """Add a catch filter group."""
        filter_group = InboundFilterGroup(type=filter_type, filters=filters)
        self._catch_filter.append(filter_group)
        return self

    def add_match_filter(
        self, filter_type: str, filters: Optional[List[Dict[str, Any]]] = None
    ) -> "InboundBuilder":
        """Add a match filter group."""
        filter_group = InboundFilterGroup(type=filter_type, filters=filters)
        self._match_filter.append(filter_group)
        return self

    def clear_catch_filters(self) -> "InboundBuilder":
        """Clear all catch filters."""
        self._catch_filter = []
        return self

    def clear_match_filters(self) -> "InboundBuilder":
        """Clear all match filters."""
        self._match_filter = []
        return self

    # Forward management methods
    def add_forward(
        self,
        forward_type: str,
        value: str,
        forward_id: Optional[str] = None,
        secret: Optional[str] = None,
    ) -> "InboundBuilder":
        """Add a forward configuration."""
        forward = InboundForward(
            id=forward_id, type=forward_type, value=value, secret=secret
        )
        self._forwards.append(forward)
        return self

    def add_email_forward(self, email: str) -> "InboundBuilder":
        """Add an email forward."""
        return self.add_forward("email", email)

    def add_webhook_forward(
        self, url: str, secret: Optional[str] = None
    ) -> "InboundBuilder":
        """Add a webhook forward."""
        return self.add_forward("webhook", url, secret=secret)

    def clear_forwards(self) -> "InboundBuilder":
        """Clear all forwards."""
        self._forwards = []
        return self

    # Convenience methods for common filter configurations
    def catch_all(self) -> "InboundBuilder":
        """Add a catch-all filter."""
        return self.add_catch_filter("catch_all")

    def catch_recipient(
        self, filters: List[Dict[str, Any]], catch_type: str = "all"
    ) -> "InboundBuilder":
        """Add a catch recipient filter with conditions."""
        self.add_catch_filter("catch_recipient", filters)
        self._catch_type = catch_type
        return self

    def match_all(self) -> "InboundBuilder":
        """Add a match-all filter."""
        return self.add_match_filter("match_all")

    def match_sender(
        self, filters: List[Dict[str, Any]], match_type: str = "all"
    ) -> "InboundBuilder":
        """Add a match sender filter with conditions."""
        self.add_match_filter("match_sender", filters)
        self._match_type = match_type
        return self

    def match_domain(
        self, filters: List[Dict[str, Any]], match_type: str = "all"
    ) -> "InboundBuilder":
        """Add a match domain filter with conditions."""
        self.add_match_filter("match_domain", filters)
        self._match_type = match_type
        return self

    def match_header(
        self, filters: List[Dict[str, Any]], match_type: str = "all"
    ) -> "InboundBuilder":
        """Add a match header filter with conditions."""
        self.add_match_filter("match_header", filters)
        self._match_type = match_type
        return self

    # Convenience methods for common configurations
    def enable_domain(self, domain: str, priority: int) -> "InboundBuilder":
        """Enable domain with specified domain and priority."""
        self._domain_enabled = True
        self._inbound_domain = domain
        self._inbound_priority = priority
        return self

    def disable_domain(self) -> "InboundBuilder":
        """Disable domain configuration."""
        self._domain_enabled = False
        self._inbound_domain = None
        self._inbound_priority = None
        return self

    # Build methods
    def build_list_request(self) -> InboundListRequest:
        """Build an InboundListRequest."""
        try:
            query_params = InboundListQueryParams()

            # Only set values if they were explicitly set by the user
            if self._page is not None:
                query_params.page = self._page
            if self._limit is not None:
                query_params.limit = self._limit
            if self._domain_id is not None:
                query_params.domain_id = self._domain_id

            return InboundListRequest(query_params=query_params)
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid inbound list request: {e}")

    def build_get_request(self) -> InboundGetRequest:
        """Build an InboundGetRequest."""
        if not self._inbound_id:
            raise MailerSendValidationError("Inbound ID is required for get request")

        try:
            return InboundGetRequest(inbound_id=self._inbound_id)
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid inbound get request: {e}")

    def build_create_request(self) -> InboundCreateRequest:
        """Build an InboundCreateRequest."""
        if not self._domain_id:
            raise MailerSendValidationError("Domain ID is required for create request")
        if not self._name:
            raise MailerSendValidationError("Name is required for create request")
        if self._domain_enabled is None:
            raise MailerSendValidationError(
                "Domain enabled flag is required for create request"
            )
        if not self._catch_filter:
            raise MailerSendValidationError(
                "At least one catch filter is required for create request"
            )
        if not self._match_filter:
            raise MailerSendValidationError(
                "At least one match filter is required for create request"
            )
        if not self._forwards:
            raise MailerSendValidationError(
                "At least one forward is required for create request"
            )

        try:
            return InboundCreateRequest(
                domain_id=self._domain_id,
                name=self._name,
                domain_enabled=self._domain_enabled,
                inbound_domain=self._inbound_domain,
                inbound_priority=self._inbound_priority,
                catch_filter=self._catch_filter[0] if self._catch_filter else None,
                catch_type=self._catch_type,
                match_filter=self._match_filter[0] if self._match_filter else None,
                match_type=self._match_type,
                forwards=self._forwards,
            )
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid inbound create request: {e}")

    def build_update_request(self) -> InboundUpdateRequest:
        """Build an InboundUpdateRequest."""
        if not self._inbound_id:
            raise MailerSendValidationError("Inbound ID is required for update request")
        if not self._name:
            raise MailerSendValidationError("Name is required for update request")
        if self._domain_enabled is None:
            raise MailerSendValidationError(
                "Domain enabled flag is required for update request"
            )
        if not self._catch_filter:
            raise MailerSendValidationError(
                "At least one catch filter is required for update request"
            )
        if not self._match_filter:
            raise MailerSendValidationError(
                "At least one match filter is required for update request"
            )
        if not self._forwards:
            raise MailerSendValidationError(
                "At least one forward is required for update request"
            )

        try:
            return InboundUpdateRequest(
                inbound_id=self._inbound_id,
                name=self._name,
                domain_enabled=self._domain_enabled,
                inbound_domain=self._inbound_domain,
                inbound_priority=self._inbound_priority,
                catch_filter=self._catch_filter[0] if self._catch_filter else None,
                catch_type=self._catch_type,
                match_filter=self._match_filter[0] if self._match_filter else None,
                match_type=self._match_type,
                forwards=self._forwards,
            )
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid inbound update request: {e}")

    def build_delete_request(self) -> InboundDeleteRequest:
        """Build an InboundDeleteRequest."""
        if not self._inbound_id:
            raise MailerSendValidationError("Inbound ID is required for delete request")

        try:
            return InboundDeleteRequest(inbound_id=self._inbound_id)
        except PydanticValidationError as e:
            raise MailerSendValidationError(f"Invalid inbound delete request: {e}")
