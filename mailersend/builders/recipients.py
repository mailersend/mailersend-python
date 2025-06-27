"""Recipients API builder for MailerSend SDK."""
from typing import Optional, List, TYPE_CHECKING

from mailersend.models.recipients import (
    RecipientsListRequest,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
)

if TYPE_CHECKING:
    from mailersend.builders.recipients import RecipientsBuilder


class RecipientsBuilder:
    """Builder for Recipients API requests."""

    def __init__(self) -> None:
        """Initialize the RecipientsBuilder."""
        self._domain_id: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = 25
        self._recipient_id: Optional[str] = None
        self._recipients: Optional[List[str]] = None
        self._patterns: Optional[List[str]] = None
        self._ids: Optional[List[str]] = None
        self._all: Optional[bool] = None

    def domain_id(self, domain_id: str) -> "RecipientsBuilder":
        """Set the domain ID for filtering.
        
        Args:
            domain_id: The domain ID to filter by
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        self._domain_id = domain_id
        return self

    def page(self, page: int) -> "RecipientsBuilder":
        """Set the page number for pagination.
        
        Args:
            page: The page number (must be >= 1)
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
            
        Raises:
            ValueError: If page is less than 1
        """
        if page < 1:
            raise ValueError("Page must be >= 1")
        self._page = page
        return self

    def limit(self, limit: int) -> "RecipientsBuilder":
        """Set the limit for pagination.
        
        Args:
            limit: The number of items per page (10-100)
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
            
        Raises:
            ValueError: If limit is not between 10 and 100
        """
        if not 10 <= limit <= 100:
            raise ValueError("Limit must be between 10 and 100")
        self._limit = limit
        return self

    def recipient_id(self, recipient_id: str) -> "RecipientsBuilder":
        """Set the recipient ID for single recipient operations.
        
        Args:
            recipient_id: The recipient ID
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        self._recipient_id = recipient_id
        return self

    def recipients(self, recipients: List[str]) -> "RecipientsBuilder":
        """Set the list of recipient emails for suppression operations.
        
        Args:
            recipients: List of recipient email addresses
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        self._recipients = recipients
        return self

    def add_recipient(self, recipient: str) -> "RecipientsBuilder":
        """Add a single recipient email to the list.
        
        Args:
            recipient: The recipient email address
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        if self._recipients is None:
            self._recipients = []
        self._recipients.append(recipient)
        return self

    def patterns(self, patterns: List[str]) -> "RecipientsBuilder":
        """Set the list of patterns for blocklist operations.
        
        Args:
            patterns: List of email patterns
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        self._patterns = patterns
        return self

    def add_pattern(self, pattern: str) -> "RecipientsBuilder":
        """Add a single pattern to the list.
        
        Args:
            pattern: The email pattern
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        if self._patterns is None:
            self._patterns = []
        self._patterns.append(pattern)
        return self

    def ids(self, ids: List[str]) -> "RecipientsBuilder":
        """Set the list of IDs for deletion operations.
        
        Args:
            ids: List of suppression entry IDs
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        self._ids = ids
        return self

    def add_id(self, id_val: str) -> "RecipientsBuilder":
        """Add a single ID to the list.
        
        Args:
            id_val: The suppression entry ID
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        if self._ids is None:
            self._ids = []
        self._ids.append(id_val)
        return self

    def all(self, all_entries: bool = True) -> "RecipientsBuilder":
        """Set flag to operate on all entries.
        
        Args:
            all_entries: Whether to operate on all entries
            
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        self._all = all_entries
        return self

    def build_recipients_list_request(self) -> RecipientsListRequest:
        """Build a request for listing recipients.
        
        Returns:
            RecipientsListRequest: The built request object
        """
        return RecipientsListRequest(
            domain_id=self._domain_id,
            page=self._page,
            limit=self._limit,
        )

    def build_recipient_get_request(self) -> RecipientGetRequest:
        """Build a request for getting a single recipient.
        
        Returns:
            RecipientGetRequest: The built request object
            
        Raises:
            ValueError: If recipient_id is not set
        """
        if not self._recipient_id:
            raise ValueError("recipient_id must be set for get request")
        
        return RecipientGetRequest(recipient_id=self._recipient_id)

    def build_recipient_delete_request(self) -> RecipientDeleteRequest:
        """Build a request for deleting a recipient.
        
        Returns:
            RecipientDeleteRequest: The built request object
            
        Raises:
            ValueError: If recipient_id is not set
        """
        if not self._recipient_id:
            raise ValueError("recipient_id must be set for delete request")
        
        return RecipientDeleteRequest(recipient_id=self._recipient_id)

    def build_suppression_list_request(self) -> SuppressionListRequest:
        """Build a request for listing suppression entries.
        
        Returns:
            SuppressionListRequest: The built request object
        """
        return SuppressionListRequest(
            domain_id=self._domain_id,
            page=self._page,
            limit=self._limit,
        )

    def build_suppression_add_request(self) -> SuppressionAddRequest:
        """Build a request for adding to suppression lists.
        
        Returns:
            SuppressionAddRequest: The built request object
            
        Raises:
            ValueError: If domain_id is not set or both recipients and patterns are None
        """
        if not self._domain_id:
            raise ValueError("domain_id must be set for suppression add request")
        
        if self._recipients is None and self._patterns is None:
            raise ValueError("Either recipients or patterns must be provided")
        
        return SuppressionAddRequest(
            domain_id=self._domain_id,
            recipients=self._recipients,
            patterns=self._patterns,
        )

    def build_suppression_delete_request(self) -> SuppressionDeleteRequest:
        """Build a request for deleting from suppression lists.
        
        Returns:
            SuppressionDeleteRequest: The built request object
            
        Raises:
            ValueError: If both ids and all are None
        """
        if self._ids is None and self._all is None:
            raise ValueError("Either ids or all flag must be provided")
        
        return SuppressionDeleteRequest(
            domain_id=self._domain_id,
            ids=self._ids,
            all=self._all,
        )

    def reset(self) -> "RecipientsBuilder":
        """Reset the builder to its initial state.
        
        Returns:
            RecipientsBuilder: The builder instance for method chaining
        """
        self._domain_id = None
        self._page = None
        self._limit = 25
        self._recipient_id = None
        self._recipients = None
        self._patterns = None
        self._ids = None
        self._all = None
        return self

    def copy(self) -> "RecipientsBuilder":
        """Create a copy of the current builder state.
        
        Returns:
            RecipientsBuilder: A new builder instance with the same state
        """
        new_builder = RecipientsBuilder()
        new_builder._domain_id = self._domain_id
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._recipient_id = self._recipient_id
        new_builder._recipients = self._recipients.copy() if self._recipients else None
        new_builder._patterns = self._patterns.copy() if self._patterns else None
        new_builder._ids = self._ids.copy() if self._ids else None
        new_builder._all = self._all
        return new_builder 