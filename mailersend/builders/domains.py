from typing import Optional, Union
from copy import deepcopy

from ..models.domains import (
    DomainListRequest,
    DomainListQueryParams,
    DomainCreateRequest,
    DomainDeleteRequest,
    DomainGetRequest,
    DomainUpdateSettingsRequest,
    DomainRecipientsRequest,
    DomainRecipientsQueryParams,
    DomainDnsRecordsRequest,
    DomainVerificationRequest,
)
from ..exceptions import ValidationError


class DomainsBuilder:
    """
    Builder for creating domain-related requests using a fluent interface.

    Supports building requests for:
    - Listing domains
    - Creating domains
    - Getting single domain
    - Deleting domains
    - Updating domain settings
    - Getting domain recipients
    - Getting domain DNS records
    - Getting domain verification status
    """

    def __init__(self):
        """Initialize a new DomainsBuilder."""
        self._reset()

    def _reset(self):
        """Reset all builder state."""
        # List domains parameters
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._verified: Optional[bool] = None

        # Create domain parameters
        self._name: Optional[str] = None
        self._return_path_subdomain: Optional[str] = None
        self._custom_tracking_subdomain: Optional[str] = None
        self._inbound_routing_subdomain: Optional[str] = None

        # Delete domain parameters
        self._domain_id: Optional[str] = None

        # Update domain settings parameters
        self._send_paused: Optional[bool] = None
        self._track_clicks: Optional[bool] = None
        self._track_opens: Optional[bool] = None
        self._track_unsubscribe: Optional[bool] = None
        self._track_content: Optional[bool] = None
        self._track_unsubscribe_html: Optional[str] = None
        self._track_unsubscribe_plain: Optional[str] = None
        self._custom_tracking_enabled: Optional[bool] = None
        self._custom_tracking_subdomain_setting: Optional[str] = None
        self._precedence_bulk: Optional[bool] = None
        self._ignore_duplicated_recipients: Optional[bool] = None

    # Pagination methods (used by list and recipients)
    def page(self, page: int) -> "DomainsBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number (must be > 0)

        Returns:
            Self for method chaining
        """
        if page < 1:
            raise ValidationError("Page must be greater than 0")
        self._page = page
        return self

    def limit(self, limit: int) -> "DomainsBuilder":
        """
        Set the number of items per page.

        Args:
            limit: Items per page (10-100)

        Returns:
            Self for method chaining
        """
        if limit < 10 or limit > 100:
            raise ValidationError("Limit must be between 10 and 100")
        self._limit = limit
        return self

    # Domain list specific methods
    def verified(self, verified: bool) -> "DomainsBuilder":
        """
        Filter domains by verification status.

        Args:
            verified: True for verified domains only, False for unverified

        Returns:
            Self for method chaining
        """
        self._verified = verified
        return self

    def verified_only(self) -> "DomainsBuilder":
        """
        Show only verified domains.

        Returns:
            Self for method chaining
        """
        return self.verified(True)

    def unverified_only(self) -> "DomainsBuilder":
        """
        Show only unverified domains.

        Returns:
            Self for method chaining
        """
        return self.verified(False)

    # Domain creation methods
    def domain_name(self, name: str) -> "DomainsBuilder":
        """
        Set the domain name for creation.

        Args:
            name: Domain name (must be lowercase and valid format)

        Returns:
            Self for method chaining
        """
        self._name = name
        return self

    def return_path_subdomain(self, subdomain: str) -> "DomainsBuilder":
        """
        Set the return path subdomain.

        Args:
            subdomain: Return path subdomain (must be alphanumeric)

        Returns:
            Self for method chaining
        """
        self._return_path_subdomain = subdomain
        return self

    def custom_tracking_subdomain(self, subdomain: str) -> "DomainsBuilder":
        """
        Set the custom tracking subdomain.

        Args:
            subdomain: Custom tracking subdomain (must be alphanumeric)

        Returns:
            Self for method chaining
        """
        self._custom_tracking_subdomain = subdomain
        return self

    def inbound_routing_subdomain(self, subdomain: str) -> "DomainsBuilder":
        """
        Set the inbound routing subdomain.

        Args:
            subdomain: Inbound routing subdomain (must be alphanumeric)

        Returns:
            Self for method chaining
        """
        self._inbound_routing_subdomain = subdomain
        return self

    # Domain deletion methods
    def domain_id(self, domain_id: str) -> "DomainsBuilder":
        """
        Set the domain ID for deletion.

        Args:
            domain_id: Domain ID to delete

        Returns:
            Self for method chaining
        """
        self._domain_id = domain_id
        return self

    # Domain settings update methods
    def send_paused(self, paused: bool) -> "DomainsBuilder":
        """
        Set the send paused status.

        Args:
            paused: True to pause sending, False to resume

        Returns:
            Self for method chaining
        """
        self._send_paused = paused
        return self

    def pause_sending(self) -> "DomainsBuilder":
        """
        Pause email sending for the domain.

        Returns:
            Self for method chaining
        """
        return self.send_paused(True)

    def resume_sending(self) -> "DomainsBuilder":
        """
        Resume email sending for the domain.

        Returns:
            Self for method chaining
        """
        return self.send_paused(False)

    def track_clicks(self, enabled: bool) -> "DomainsBuilder":
        """
        Set click tracking status.

        Args:
            enabled: True to enable click tracking, False to disable

        Returns:
            Self for method chaining
        """
        self._track_clicks = enabled
        return self

    def track_opens(self, enabled: bool) -> "DomainsBuilder":
        """
        Set open tracking status.

        Args:
            enabled: True to enable open tracking, False to disable

        Returns:
            Self for method chaining
        """
        self._track_opens = enabled
        return self

    def track_unsubscribe(self, enabled: bool) -> "DomainsBuilder":
        """
        Set unsubscribe tracking status.

        Args:
            enabled: True to enable unsubscribe tracking, False to disable

        Returns:
            Self for method chaining
        """
        self._track_unsubscribe = enabled
        return self

    def track_content(self, enabled: bool) -> "DomainsBuilder":
        """
        Set content tracking status.

        Args:
            enabled: True to enable content tracking, False to disable

        Returns:
            Self for method chaining
        """
        self._track_content = enabled
        return self

    def track_unsubscribe_html(self, html: str) -> "DomainsBuilder":
        """
        Set HTML unsubscribe tracking content.

        Args:
            html: HTML content for unsubscribe tracking

        Returns:
            Self for method chaining
        """
        self._track_unsubscribe_html = html
        return self

    def track_unsubscribe_plain(self, text: str) -> "DomainsBuilder":
        """
        Set plain text unsubscribe tracking content.

        Args:
            text: Plain text content for unsubscribe tracking

        Returns:
            Self for method chaining
        """
        self._track_unsubscribe_plain = text
        return self

    def custom_tracking_enabled(self, enabled: bool) -> "DomainsBuilder":
        """
        Set custom tracking status.

        Args:
            enabled: True to enable custom tracking, False to disable

        Returns:
            Self for method chaining
        """
        self._custom_tracking_enabled = enabled
        return self

    def custom_tracking_subdomain_setting(self, subdomain: str) -> "DomainsBuilder":
        """
        Set custom tracking subdomain.

        Args:
            subdomain: Custom tracking subdomain

        Returns:
            Self for method chaining
        """
        self._custom_tracking_subdomain_setting = subdomain
        return self

    def precedence_bulk(self, enabled: bool) -> "DomainsBuilder":
        """
        Set bulk precedence status.

        Args:
            enabled: True to enable bulk precedence, False to disable

        Returns:
            Self for method chaining
        """
        self._precedence_bulk = enabled
        return self

    def ignore_duplicated_recipients(self, enabled: bool) -> "DomainsBuilder":
        """
        Set ignore duplicated recipients status.

        Args:
            enabled: True to ignore duplicated recipients, False to include

        Returns:
            Self for method chaining
        """
        self._ignore_duplicated_recipients = enabled
        return self

    def enable_all_tracking(self) -> "DomainsBuilder":
        """
        Enable all tracking features.

        Returns:
            Self for method chaining
        """
        return (
            self.track_clicks(True)
            .track_opens(True)
            .track_unsubscribe(True)
            .track_content(True)
        )

    def disable_all_tracking(self) -> "DomainsBuilder":
        """
        Disable all tracking features.

        Returns:
            Self for method chaining
        """
        return (
            self.track_clicks(False)
            .track_opens(False)
            .track_unsubscribe(False)
            .track_content(False)
        )

    # Build methods for different request types
    def build_list_request(self) -> DomainListRequest:
        """
        Build a domain list request.

        Returns:
            DomainListRequest object
        """
        # Create query params with proper defaults, using builder values only if set
        query_params_data = {}
        if self._page is not None:
            query_params_data["page"] = self._page
        if self._limit is not None:
            query_params_data["limit"] = self._limit
        if self._verified is not None:
            query_params_data["verified"] = self._verified

        query_params = DomainListQueryParams(**query_params_data)
        return DomainListRequest(query_params=query_params)

    def build_create_request(self) -> DomainCreateRequest:
        """
        Build a domain creation request.

        Returns:
            DomainCreateRequest object

        Raises:
            ValidationError: If domain name is not provided
        """
        if not self._name:
            raise ValidationError("Domain name is required for creation")

        return DomainCreateRequest(
            name=self._name,
            return_path_subdomain=self._return_path_subdomain,
            custom_tracking_subdomain=self._custom_tracking_subdomain,
            inbound_routing_subdomain=self._inbound_routing_subdomain,
        )

    def build_delete_request(self) -> DomainDeleteRequest:
        """
        Build a domain deletion request.

        Returns:
            DomainDeleteRequest object

        Raises:
            ValidationError: If domain ID is not provided
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required for deletion")

        return DomainDeleteRequest(domain_id=self._domain_id)

    def build_update_settings_request(self) -> DomainUpdateSettingsRequest:
        """
        Build a domain settings update request.

        Returns:
            DomainUpdateSettingsRequest object

        Raises:
            ValidationError: If domain ID is not provided
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required for updating settings")

        return DomainUpdateSettingsRequest(
            domain_id=self._domain_id,
            send_paused=self._send_paused,
            track_clicks=self._track_clicks,
            track_opens=self._track_opens,
            track_unsubscribe=self._track_unsubscribe,
            track_content=self._track_content,
            track_unsubscribe_html=self._track_unsubscribe_html,
            track_unsubscribe_plain=self._track_unsubscribe_plain,
            custom_tracking_enabled=self._custom_tracking_enabled,
            custom_tracking_subdomain=self._custom_tracking_subdomain_setting,
            precedence_bulk=self._precedence_bulk,
            ignore_duplicated_recipients=self._ignore_duplicated_recipients,
        )

    def build_recipients_request(self) -> DomainRecipientsRequest:
        """
        Build a domain recipients request.

        Returns:
            DomainRecipientsRequest object

        Raises:
            ValidationError: If domain ID is not provided
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required for getting recipients")

        # Create query params with proper defaults, using builder values only if set
        query_params_data = {}
        if self._page is not None:
            query_params_data["page"] = self._page
        if self._limit is not None:
            query_params_data["limit"] = self._limit

        query_params = DomainRecipientsQueryParams(**query_params_data)
        return DomainRecipientsRequest(
            domain_id=self._domain_id, query_params=query_params
        )

    def build_get_request(self) -> DomainGetRequest:
        """
        Build a domain get request.

        Returns:
            DomainGetRequest object

        Raises:
            ValidationError: If domain ID is not provided
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required for getting domain")

        return DomainGetRequest(domain_id=self._domain_id)

    def build_dns_records_request(self) -> DomainDnsRecordsRequest:
        """
        Build a domain DNS records request.

        Returns:
            DomainDnsRecordsRequest object

        Raises:
            ValidationError: If domain ID is not provided
        """
        if not self._domain_id:
            raise ValidationError("Domain ID is required for getting DNS records")

        return DomainDnsRecordsRequest(domain_id=self._domain_id)

    def build_verification_request(self) -> DomainVerificationRequest:
        """
        Build a domain verification request.

        Returns:
            DomainVerificationRequest object

        Raises:
            ValidationError: If domain ID is not provided
        """
        if not self._domain_id:
            raise ValidationError(
                "Domain ID is required for getting verification status"
            )

        return DomainVerificationRequest(domain_id=self._domain_id)

    # State management methods
    def reset(self) -> "DomainsBuilder":
        """
        Reset the builder to its initial state.

        Returns:
            Self for method chaining
        """
        self._reset()
        return self

    def copy(self) -> "DomainsBuilder":
        """
        Create a copy of this builder.

        Returns:
            New DomainsBuilder instance with the same state
        """
        new_builder = DomainsBuilder()
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._verified = self._verified
        new_builder._name = self._name
        new_builder._return_path_subdomain = self._return_path_subdomain
        new_builder._custom_tracking_subdomain = self._custom_tracking_subdomain
        new_builder._inbound_routing_subdomain = self._inbound_routing_subdomain
        new_builder._domain_id = self._domain_id
        new_builder._send_paused = self._send_paused
        new_builder._track_clicks = self._track_clicks
        new_builder._track_opens = self._track_opens
        new_builder._track_unsubscribe = self._track_unsubscribe
        new_builder._track_content = self._track_content
        new_builder._track_unsubscribe_html = self._track_unsubscribe_html
        new_builder._track_unsubscribe_plain = self._track_unsubscribe_plain
        new_builder._custom_tracking_enabled = self._custom_tracking_enabled
        new_builder._custom_tracking_subdomain_setting = (
            self._custom_tracking_subdomain_setting
        )
        new_builder._precedence_bulk = self._precedence_bulk
        new_builder._ignore_duplicated_recipients = self._ignore_duplicated_recipients
        return new_builder
