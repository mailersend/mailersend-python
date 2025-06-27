from typing import Optional, Union
from copy import deepcopy

from ..models.domains import (
    DomainListRequest, DomainCreateRequest, DomainUpdateSettingsRequest,
    DomainRecipientsRequest
)
from ..exceptions import ValidationError


class DomainsBuilder:
    """
    Builder for creating domain-related requests using a fluent interface.
    
    Supports building requests for:
    - Listing domains
    - Creating domains
    - Updating domain settings
    - Getting domain recipients
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
    def page(self, page: int) -> 'DomainsBuilder':
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
    
    def limit(self, limit: int) -> 'DomainsBuilder':
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
    def verified(self, verified: bool) -> 'DomainsBuilder':
        """
        Filter domains by verification status.
        
        Args:
            verified: True for verified domains only, False for unverified
            
        Returns:
            Self for method chaining
        """
        self._verified = verified
        return self
    
    def verified_only(self) -> 'DomainsBuilder':
        """
        Show only verified domains.
        
        Returns:
            Self for method chaining
        """
        return self.verified(True)
    
    def unverified_only(self) -> 'DomainsBuilder':
        """
        Show only unverified domains.
        
        Returns:
            Self for method chaining
        """
        return self.verified(False)
    
    # Domain creation methods
    def domain_name(self, name: str) -> 'DomainsBuilder':
        """
        Set the domain name for creation.
        
        Args:
            name: Domain name (must be lowercase and valid format)
            
        Returns:
            Self for method chaining
        """
        self._name = name
        return self
    
    def return_path_subdomain(self, subdomain: str) -> 'DomainsBuilder':
        """
        Set the return path subdomain.
        
        Args:
            subdomain: Return path subdomain (must be alphanumeric)
            
        Returns:
            Self for method chaining
        """
        self._return_path_subdomain = subdomain
        return self
    
    def custom_tracking_subdomain(self, subdomain: str) -> 'DomainsBuilder':
        """
        Set the custom tracking subdomain.
        
        Args:
            subdomain: Custom tracking subdomain (must be alphanumeric)
            
        Returns:
            Self for method chaining
        """
        self._custom_tracking_subdomain = subdomain
        return self
    
    def inbound_routing_subdomain(self, subdomain: str) -> 'DomainsBuilder':
        """
        Set the inbound routing subdomain.
        
        Args:
            subdomain: Inbound routing subdomain (must be alphanumeric)
            
        Returns:
            Self for method chaining
        """
        self._inbound_routing_subdomain = subdomain
        return self
    
    # Domain settings update methods
    def send_paused(self, paused: bool) -> 'DomainsBuilder':
        """
        Set the send paused status.
        
        Args:
            paused: True to pause sending, False to resume
            
        Returns:
            Self for method chaining
        """
        self._send_paused = paused
        return self
    
    def pause_sending(self) -> 'DomainsBuilder':
        """
        Pause sending for this domain.
        
        Returns:
            Self for method chaining
        """
        return self.send_paused(True)
    
    def resume_sending(self) -> 'DomainsBuilder':
        """
        Resume sending for this domain.
        
        Returns:
            Self for method chaining
        """
        return self.send_paused(False)
    
    def track_clicks(self, enabled: bool) -> 'DomainsBuilder':
        """
        Enable or disable click tracking.
        
        Args:
            enabled: True to enable click tracking
            
        Returns:
            Self for method chaining
        """
        self._track_clicks = enabled
        return self
    
    def track_opens(self, enabled: bool) -> 'DomainsBuilder':
        """
        Enable or disable open tracking.
        
        Args:
            enabled: True to enable open tracking
            
        Returns:
            Self for method chaining
        """
        self._track_opens = enabled
        return self
    
    def track_unsubscribe(self, enabled: bool) -> 'DomainsBuilder':
        """
        Enable or disable unsubscribe tracking.
        
        Args:
            enabled: True to enable unsubscribe tracking
            
        Returns:
            Self for method chaining
        """
        self._track_unsubscribe = enabled
        return self
    
    def track_content(self, enabled: bool) -> 'DomainsBuilder':
        """
        Enable or disable content tracking.
        
        Args:
            enabled: True to enable content tracking
            
        Returns:
            Self for method chaining
        """
        self._track_content = enabled
        return self
    
    def track_unsubscribe_html(self, html: str) -> 'DomainsBuilder':
        """
        Set the HTML unsubscribe template.
        
        Args:
            html: HTML template for unsubscribe link
            
        Returns:
            Self for method chaining
        """
        self._track_unsubscribe_html = html
        return self
    
    def track_unsubscribe_plain(self, text: str) -> 'DomainsBuilder':
        """
        Set the plain text unsubscribe template.
        
        Args:
            text: Plain text template for unsubscribe link
            
        Returns:
            Self for method chaining
        """
        self._track_unsubscribe_plain = text
        return self
    
    def custom_tracking_enabled(self, enabled: bool) -> 'DomainsBuilder':
        """
        Enable or disable custom tracking.
        
        Args:
            enabled: True to enable custom tracking
            
        Returns:
            Self for method chaining
        """
        self._custom_tracking_enabled = enabled
        return self
    
    def custom_tracking_subdomain_setting(self, subdomain: str) -> 'DomainsBuilder':
        """
        Set the custom tracking subdomain in settings.
        
        Args:
            subdomain: Custom tracking subdomain
            
        Returns:
            Self for method chaining
        """
        self._custom_tracking_subdomain_setting = subdomain
        return self
    
    def precedence_bulk(self, enabled: bool) -> 'DomainsBuilder':
        """
        Enable or disable bulk precedence.
        
        Args:
            enabled: True to enable bulk precedence
            
        Returns:
            Self for method chaining
        """
        self._precedence_bulk = enabled
        return self
    
    def ignore_duplicated_recipients(self, enabled: bool) -> 'DomainsBuilder':
        """
        Enable or disable ignoring duplicated recipients.
        
        Args:
            enabled: True to ignore duplicated recipients
            
        Returns:
            Self for method chaining
        """
        self._ignore_duplicated_recipients = enabled
        return self
    
    def enable_all_tracking(self) -> 'DomainsBuilder':
        """
        Enable all tracking features.
        
        Returns:
            Self for method chaining
        """
        return (self
            .track_clicks(True)
            .track_opens(True)
            .track_unsubscribe(True)
            .track_content(True))
    
    def disable_all_tracking(self) -> 'DomainsBuilder':
        """
        Disable all tracking features.
        
        Returns:
            Self for method chaining
        """
        return (self
            .track_clicks(False)
            .track_opens(False)
            .track_unsubscribe(False)
            .track_content(False))
    
    # Build methods for different request types
    def build_list_request(self) -> DomainListRequest:
        """
        Build a domain list request.
        
        Returns:
            DomainListRequest object
        """
        return DomainListRequest(
            page=self._page,
            limit=self._limit,
            verified=self._verified
        )
    
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
            inbound_routing_subdomain=self._inbound_routing_subdomain
        )
    
    def build_update_settings_request(self) -> DomainUpdateSettingsRequest:
        """
        Build a domain settings update request.
        
        Returns:
            DomainUpdateSettingsRequest object
        """
        return DomainUpdateSettingsRequest(
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
            ignore_duplicated_recipients=self._ignore_duplicated_recipients
        )
    
    def build_recipients_request(self) -> DomainRecipientsRequest:
        """
        Build a domain recipients request.
        
        Returns:
            DomainRecipientsRequest object
        """
        return DomainRecipientsRequest(
            page=self._page,
            limit=self._limit
        )
    
    # State management methods
    def reset(self) -> 'DomainsBuilder':
        """
        Reset the builder to its initial state.
        
        Returns:
            Self for method chaining
        """
        self._reset()
        return self
    
    def copy(self) -> 'DomainsBuilder':
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
        new_builder._send_paused = self._send_paused
        new_builder._track_clicks = self._track_clicks
        new_builder._track_opens = self._track_opens
        new_builder._track_unsubscribe = self._track_unsubscribe
        new_builder._track_content = self._track_content
        new_builder._track_unsubscribe_html = self._track_unsubscribe_html
        new_builder._track_unsubscribe_plain = self._track_unsubscribe_plain
        new_builder._custom_tracking_enabled = self._custom_tracking_enabled
        new_builder._custom_tracking_subdomain_setting = self._custom_tracking_subdomain_setting
        new_builder._precedence_bulk = self._precedence_bulk
        new_builder._ignore_duplicated_recipients = self._ignore_duplicated_recipients
        return new_builder 