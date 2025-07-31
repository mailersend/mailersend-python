from typing import List, Optional, Union
from datetime import datetime

from ..models.activity import (
    ActivityRequest,
    ActivityQueryParams,
    SingleActivityRequest,
)


class ActivityBuilder:
    """Builder for constructing activity requests."""

    def __init__(self):
        self._domain_id: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._date_from: Optional[Union[datetime, int]] = None
        self._date_to: Optional[Union[datetime, int]] = None
        self._event: List[str] = []

    def domain_id(self, domain_id: str) -> "ActivityBuilder":
        """Set the domain ID."""
        self._domain_id = domain_id
        return self

    def page(self, page: int) -> "ActivityBuilder":
        """Set the page number."""
        self._page = page
        return self

    def limit(self, limit: int) -> "ActivityBuilder":
        """Set the limit per page."""
        self._limit = limit
        return self

    def date_from(self, date_from: Union[datetime, int]) -> "ActivityBuilder":
        """Set the start date."""
        self._date_from = date_from
        return self

    def date_to(self, date_to: Union[datetime, int]) -> "ActivityBuilder":
        """Set the end date."""
        self._date_to = date_to
        return self

    def event(self, event: str) -> "ActivityBuilder":
        """Add an event type to filter by."""
        if event not in self._event:
            self._event.append(event)
        return self

    def events(self, events: List[str]) -> "ActivityBuilder":
        """Set multiple event types to filter by."""
        self._event = list(events)
        return self

    def copy(self) -> "ActivityBuilder":
        """Create a copy of this builder."""
        builder = ActivityBuilder()
        builder._domain_id = self._domain_id
        builder._page = self._page
        builder._limit = self._limit
        builder._date_from = self._date_from
        builder._date_to = self._date_to
        builder._event = self._event.copy()
        return builder

    def reset(self) -> "ActivityBuilder":
        """Reset all parameters."""
        self._domain_id = None
        self._page = None
        self._limit = None
        self._date_from = None
        self._date_to = None
        self._event = []
        return self

    def _convert_to_timestamp(self, value: Union[datetime, int]) -> int:
        """Convert datetime to timestamp if needed."""
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value

    def build_list_request(self) -> ActivityRequest:
        """Build the ActivityRequest object for listing activities."""
        return self.build()
    
    def build(self) -> ActivityRequest:
        """Build the ActivityRequest object."""
        # Convert dates to timestamps if needed
        date_from = None
        if self._date_from is not None:
            date_from = self._convert_to_timestamp(self._date_from)

        date_to = None
        if self._date_to is not None:
            date_to = self._convert_to_timestamp(self._date_to)

        # Build the query parameters
        query_params = ActivityQueryParams(
            page=self._page,
            limit=self._limit,
            date_from=date_from,
            date_to=date_to,
            event=self._event if self._event else None,
        )

        # Build the complete request
        return ActivityRequest(domain_id=self._domain_id, query_params=query_params)


class SingleActivityBuilder:
    """
    Builder for constructing SingleActivityRequest objects.

    Provides a fluent interface for building requests to get a single activity.
    """

    def __init__(self):
        """Initialize the builder with default values."""
        self._activity_id: Optional[str] = None

    def activity_id(self, activity_id: str) -> "SingleActivityBuilder":
        """
        Set the activity ID.

        Args:
            activity_id: The unique identifier of the activity

        Returns:
            Self for method chaining
        """
        self._activity_id = activity_id
        return self

    def copy(self) -> "SingleActivityBuilder":
        """
        Create a copy of this builder.

        Returns:
            A new SingleActivityBuilder instance with the same configuration
        """
        new_builder = SingleActivityBuilder()
        new_builder._activity_id = self._activity_id
        return new_builder

    def reset(self) -> "SingleActivityBuilder":
        """
        Reset the builder to its initial state.

        Returns:
            Self for method chaining
        """
        self._activity_id = None
        return self

    def build_get_request(self) -> SingleActivityRequest:
        """Build the SingleActivityRequest object for getting a single activity."""
        return self.build()
    
    def build(self) -> SingleActivityRequest:
        """
        Build the SingleActivityRequest object.

        Returns:
            A configured SingleActivityRequest instance

        Raises:
            ValueError: If required fields are missing
        """
        if not self._activity_id:
            raise ValueError("activity_id is required")

        return SingleActivityRequest(activity_id=self._activity_id)
