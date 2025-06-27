from typing import Optional
from copy import deepcopy

from ..models.messages import MessagesListRequest, MessageGetRequest
from ..exceptions import ValidationError


class MessagesBuilder:
    """
    Builder for creating message-related requests using a fluent interface.
    
    Supports building requests for:
    - Listing messages
    - Getting single message
    """
    
    def __init__(self):
        """Initialize a new MessagesBuilder."""
        self._reset()
    
    def _reset(self):
        """Reset all builder state."""
        # List messages parameters
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        
        # Get message parameters
        self._message_id: Optional[str] = None
    
    # Pagination methods (used by list)
    def page(self, page: int) -> 'MessagesBuilder':
        """
        Set the page number for pagination.
        
        Args:
            page: Page number (must be > 0)
            
        Returns:
            Self for method chaining
            
        Raises:
            ValidationError: If page is invalid
        """
        if page < 1:
            raise ValidationError("Page must be greater than 0")
        self._page = page
        return self
    
    def limit(self, limit: int) -> 'MessagesBuilder':
        """
        Set the number of items per page.
        
        Args:
            limit: Items per page (10-100)
            
        Returns:
            Self for method chaining
            
        Raises:
            ValidationError: If limit is invalid
        """
        if limit < 10 or limit > 100:
            raise ValidationError("Limit must be between 10 and 100")
        self._limit = limit
        return self
    
    # Message identification methods
    def message_id(self, message_id: str) -> 'MessagesBuilder':
        """
        Set the message ID for getting a single message.
        
        Args:
            message_id: Message ID to retrieve
            
        Returns:
            Self for method chaining
            
        Raises:
            ValidationError: If message_id is empty
        """
        if not message_id or not message_id.strip():
            raise ValidationError("Message ID cannot be empty")
        self._message_id = message_id.strip()
        return self
    
    def build_list_request(self) -> MessagesListRequest:
        """
        Build a MessagesListRequest with the configured parameters.
        
        Returns:
            MessagesListRequest object ready for API call
        """
        return MessagesListRequest(
            page=self._page,
            limit=self._limit if self._limit is not None else 25
        )
    
    def build_get_request(self) -> MessageGetRequest:
        """
        Build a MessageGetRequest with the configured parameters.
        
        Returns:
            MessageGetRequest object ready for API call
            
        Raises:
            ValidationError: If message_id is not set
        """
        if not self._message_id:
            raise ValidationError("Message ID must be set to build get request")
        
        return MessageGetRequest(message_id=self._message_id)
    
    def reset(self) -> 'MessagesBuilder':
        """
        Reset the builder to its initial state.
        
        Returns:
            Self for method chaining
        """
        self._reset()
        return self
    
    def copy(self) -> 'MessagesBuilder':
        """
        Create a deep copy of this builder.
        
        Returns:
            New MessagesBuilder instance with same configuration
        """
        new_builder = MessagesBuilder()
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._message_id = self._message_id
        return new_builder 