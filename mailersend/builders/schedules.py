from typing import Optional, Literal
from copy import deepcopy

from ..models.schedules import SchedulesListRequest, ScheduleGetRequest, ScheduleDeleteRequest
from ..exceptions import ValidationError


class SchedulesBuilder:
    """
    Builder for creating schedule-related requests using a fluent interface.
    
    Supports building requests for:
    - Listing scheduled messages
    - Getting single scheduled message
    - Deleting scheduled message
    """
    
    def __init__(self):
        """Initialize a new SchedulesBuilder."""
        self._reset()
    
    def _reset(self):
        """Reset all builder state."""
        # List schedules parameters
        self._domain_id: Optional[str] = None
        self._status: Optional[Literal["scheduled", "sent", "error"]] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        
        # Get/Delete schedule parameters
        self._message_id: Optional[str] = None
    
    # Filtering methods
    def domain_id(self, domain_id: str) -> 'SchedulesBuilder':
        """
        Filter by domain ID.
        
        Args:
            domain_id: Domain ID to filter by
            
        Returns:
            Self for method chaining
            
        Raises:
            ValidationError: If domain_id is empty
        """
        if not domain_id or not domain_id.strip():
            raise ValidationError("Domain ID cannot be empty")
        self._domain_id = domain_id.strip()
        return self
    
    def status(self, status: Literal["scheduled", "sent", "error"]) -> 'SchedulesBuilder':
        """
        Filter by status.
        
        Args:
            status: Status to filter by (scheduled, sent, error)
            
        Returns:
            Self for method chaining
        """
        self._status = status
        return self
    
    def scheduled_only(self) -> 'SchedulesBuilder':
        """
        Show only scheduled messages.
        
        Returns:
            Self for method chaining
        """
        return self.status("scheduled")
    
    def sent_only(self) -> 'SchedulesBuilder':
        """
        Show only sent messages.
        
        Returns:
            Self for method chaining
        """
        return self.status("sent")
    
    def error_only(self) -> 'SchedulesBuilder':
        """
        Show only messages with errors.
        
        Returns:
            Self for method chaining
        """
        return self.status("error")
    
    # Pagination methods
    def page(self, page: int) -> 'SchedulesBuilder':
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
    
    def limit(self, limit: int) -> 'SchedulesBuilder':
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
    def message_id(self, message_id: str) -> 'SchedulesBuilder':
        """
        Set the message ID for getting or deleting a scheduled message.
        
        Args:
            message_id: Message ID to retrieve or delete
            
        Returns:
            Self for method chaining
            
        Raises:
            ValidationError: If message_id is empty
        """
        if not message_id or not message_id.strip():
            raise ValidationError("Message ID cannot be empty")
        self._message_id = message_id.strip()
        return self
    
    def build_list_request(self) -> SchedulesListRequest:
        """
        Build a SchedulesListRequest with the configured parameters.
        
        Returns:
            SchedulesListRequest object ready for API call
        """
        return SchedulesListRequest(
            domain_id=self._domain_id,
            status=self._status,
            page=self._page,
            limit=self._limit if self._limit is not None else 25
        )
    
    def build_get_request(self) -> ScheduleGetRequest:
        """
        Build a ScheduleGetRequest with the configured parameters.
        
        Returns:
            ScheduleGetRequest object ready for API call
            
        Raises:
            ValidationError: If message_id is not set
        """
        if not self._message_id:
            raise ValidationError("Message ID must be set to build get request")
        
        return ScheduleGetRequest(message_id=self._message_id)
    
    def build_delete_request(self) -> ScheduleDeleteRequest:
        """
        Build a ScheduleDeleteRequest with the configured parameters.
        
        Returns:
            ScheduleDeleteRequest object ready for API call
            
        Raises:
            ValidationError: If message_id is not set
        """
        if not self._message_id:
            raise ValidationError("Message ID must be set to build delete request")
        
        return ScheduleDeleteRequest(message_id=self._message_id)
    
    def reset(self) -> 'SchedulesBuilder':
        """
        Reset the builder to its initial state.
        
        Returns:
            Self for method chaining
        """
        self._reset()
        return self
    
    def copy(self) -> 'SchedulesBuilder':
        """
        Create a deep copy of this builder.
        
        Returns:
            New SchedulesBuilder instance with same configuration
        """
        new_builder = SchedulesBuilder()
        new_builder._domain_id = self._domain_id
        new_builder._status = self._status
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._message_id = self._message_id
        return new_builder 