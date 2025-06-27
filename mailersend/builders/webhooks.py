"""Webhooks API builder for MailerSend SDK."""

from typing import List, Optional

from ..models.webhooks import (
    WebhookCreateRequest,
    WebhookDeleteRequest,
    WebhookGetRequest,
    WebhookUpdateRequest,
    WebhooksListRequest,
)


class WebhooksBuilder:
    """Builder class for constructing webhook requests using fluent interface."""
    
    def __init__(self) -> None:
        """Initialize the webhooks builder."""
        self._domain_id: Optional[str] = None
        self._webhook_id: Optional[str] = None
        self._url: Optional[str] = None
        self._name: Optional[str] = None
        self._events: Optional[List[str]] = None
        self._enabled: Optional[bool] = None
    
    def domain_id(self, domain_id: str) -> "WebhooksBuilder":
        """Set the domain ID.
        
        Args:
            domain_id: Domain ID to set
            
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        self._domain_id = domain_id
        return self
    
    def webhook_id(self, webhook_id: str) -> "WebhooksBuilder":
        """Set the webhook ID.
        
        Args:
            webhook_id: Webhook ID to set
            
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        self._webhook_id = webhook_id
        return self
    
    def url(self, url: str) -> "WebhooksBuilder":
        """Set the webhook URL.
        
        Args:
            url: Webhook URL to set
            
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        self._url = url
        return self
    
    def name(self, name: str) -> "WebhooksBuilder":
        """Set the webhook name.
        
        Args:
            name: Webhook name to set
            
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        self._name = name
        return self
    
    def events(self, events: List[str]) -> "WebhooksBuilder":
        """Set the webhook events.
        
        Args:
            events: List of events to subscribe to
            
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        self._events = events
        return self
    
    def add_event(self, event: str) -> "WebhooksBuilder":
        """Add a single event to the events list.
        
        Args:
            event: Event to add
            
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        if self._events is None:
            self._events = []
        if event not in self._events:
            self._events.append(event)
        return self
    
    def enabled(self, enabled: bool) -> "WebhooksBuilder":
        """Set whether the webhook is enabled.
        
        Args:
            enabled: Whether webhook should be enabled
            
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        self._enabled = enabled
        return self
    
    def activity_events(self) -> "WebhooksBuilder":
        """Add all activity events to the webhook.
        
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        activity_events = [
            "activity.sent",
            "activity.delivered",
            "activity.soft_bounced",
            "activity.hard_bounced",
            "activity.opened",
            "activity.opened_unique",
            "activity.clicked",
            "activity.clicked_unique",
            "activity.unsubscribed",
            "activity.spam_complaint",
            "activity.survey_opened",
            "activity.survey_submitted",
        ]
        for event in activity_events:
            self.add_event(event)
        return self
    
    def system_events(self) -> "WebhooksBuilder":
        """Add all system events to the webhook.
        
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        system_events = [
            "sender_identity.verified",
            "maintenance.start",
            "maintenance.end",
            "inbound_forward.failed",
            "email_single.verified",
            "email_list.verified",
            "bulk_email.completed",
        ]
        for event in system_events:
            self.add_event(event)
        return self
    
    def all_events(self) -> "WebhooksBuilder":
        """Add all available events to the webhook.
        
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        self.activity_events()
        self.system_events()
        return self
    
    def build_webhooks_list_request(self) -> WebhooksListRequest:
        """Build WebhooksListRequest from current builder state.
        
        Returns:
            WebhooksListRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._domain_id:
            raise ValueError("domain_id is required for webhooks list request")
        
        return WebhooksListRequest(domain_id=self._domain_id)
    
    def build_webhook_get_request(self) -> WebhookGetRequest:
        """Build WebhookGetRequest from current builder state.
        
        Returns:
            WebhookGetRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._webhook_id:
            raise ValueError("webhook_id is required for webhook get request")
        
        return WebhookGetRequest(webhook_id=self._webhook_id)
    
    def build_webhook_create_request(self) -> WebhookCreateRequest:
        """Build WebhookCreateRequest from current builder state.
        
        Returns:
            WebhookCreateRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._url:
            raise ValueError("url is required for webhook create request")
        if not self._name:
            raise ValueError("name is required for webhook create request")
        if not self._events:
            raise ValueError("events are required for webhook create request")
        if not self._domain_id:
            raise ValueError("domain_id is required for webhook create request")
        
        return WebhookCreateRequest(
            url=self._url,
            name=self._name,
            events=self._events,
            domain_id=self._domain_id,
            enabled=self._enabled,
        )
    
    def build_webhook_update_request(self) -> WebhookUpdateRequest:
        """Build WebhookUpdateRequest from current builder state.
        
        Returns:
            WebhookUpdateRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._webhook_id:
            raise ValueError("webhook_id is required for webhook update request")
        
        return WebhookUpdateRequest(
            webhook_id=self._webhook_id,
            url=self._url,
            name=self._name,
            events=self._events,
            enabled=self._enabled,
        )
    
    def build_webhook_delete_request(self) -> WebhookDeleteRequest:
        """Build WebhookDeleteRequest from current builder state.
        
        Returns:
            WebhookDeleteRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._webhook_id:
            raise ValueError("webhook_id is required for webhook delete request")
        
        return WebhookDeleteRequest(webhook_id=self._webhook_id)
    
    def reset(self) -> "WebhooksBuilder":
        """Reset all builder parameters to None.
        
        Returns:
            WebhooksBuilder: Self for method chaining
        """
        self._domain_id = None
        self._webhook_id = None
        self._url = None
        self._name = None
        self._events = None
        self._enabled = None
        return self
    
    def copy(self) -> "WebhooksBuilder":
        """Create a copy of the current builder with the same state.
        
        Returns:
            WebhooksBuilder: New builder instance with copied state
        """
        new_builder = WebhooksBuilder()
        new_builder._domain_id = self._domain_id
        new_builder._webhook_id = self._webhook_id
        new_builder._url = self._url
        new_builder._name = self._name
        new_builder._events = self._events.copy() if self._events else None
        new_builder._enabled = self._enabled
        return new_builder 