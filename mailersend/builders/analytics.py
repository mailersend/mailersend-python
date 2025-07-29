"""
Analytics Builder - Fluent API for constructing analytics requests.

This module provides the AnalyticsBuilder class which offers a chainable,
developer-friendly API for building analytics requests with intelligent
defaults, date handling, and validation.
"""

from datetime import datetime, timezone, timedelta
from typing import List, Optional, Union, Literal

from ..models.analytics import AnalyticsRequest
from ..exceptions import ValidationError


class AnalyticsBuilder:
    """
    Fluent builder for constructing AnalyticsRequest objects.

    Provides a chainable API that makes it easy to build analytics requests
    for all analytics endpoints with intelligent date handling and validation.

    Examples:
        >>> # Activity data by date
        >>> request = (AnalyticsBuilder()
        ...     .date_range_days(7)  # Last 7 days
        ...     .events("sent", "delivered", "opened")
        ...     .group_by("days")
        ...     .tags("newsletter", "marketing")
        ...     .build())

        >>> # Opens by country for specific domain
        >>> request = (AnalyticsBuilder()
        ...     .domain("domain-id-123")
        ...     .date_from_timestamp(1443651141)
        ...     .date_to_timestamp(1443661141)
        ...     .tags("campaign-2024")
        ...     .build())

        >>> # Custom date range with datetime objects
        >>> request = (AnalyticsBuilder()
        ...     .date_from_datetime(datetime(2024, 1, 1))
        ...     .date_to_datetime(datetime(2024, 1, 31))
        ...     .events("opened", "clicked")
        ...     .group_by("weeks")
        ...     .build())
    """

    def __init__(self):
        """Initialize a new AnalyticsBuilder."""
        self._domain_id: Optional[str] = None
        self._recipient_id: List[str] = []
        self._date_from: Optional[int] = None
        self._date_to: Optional[int] = None
        self._tags: List[str] = []
        self._group_by: str = "days"
        self._event: List[str] = []

    def domain(self, domain_id: str) -> "AnalyticsBuilder":
        """
        Set the domain ID to filter analytics data.

        Args:
            domain_id: The domain ID to filter by

        Returns:
            AnalyticsBuilder instance for chaining
        """
        self._domain_id = domain_id
        return self

    def recipient(self, recipient_id: str) -> "AnalyticsBuilder":
        """
        Add a recipient ID to filter analytics data.

        Args:
            recipient_id: The recipient ID to add

        Returns:
            AnalyticsBuilder instance for chaining
        """
        if len(self._recipient_id) >= 50:
            raise ValidationError("Maximum 50 recipients are allowed")
        self._recipient_id.append(recipient_id)
        return self

    def recipients(self, *recipient_ids: str) -> "AnalyticsBuilder":
        """
        Add multiple recipient IDs to filter analytics data.

        Args:
            recipient_ids: The recipient IDs to add

        Returns:
            AnalyticsBuilder instance for chaining
        """
        for recipient_id in recipient_ids:
            self.recipient(recipient_id)
        return self

    def date_from_timestamp(self, timestamp: int) -> "AnalyticsBuilder":
        """
        Set the start date using a Unix timestamp.

        Args:
            timestamp: Unix timestamp (UTC)

        Returns:
            AnalyticsBuilder instance for chaining
        """
        if timestamp <= 0:
            raise ValidationError("Timestamp must be a positive integer")
        self._date_from = timestamp
        return self

    def date_to_timestamp(self, timestamp: int) -> "AnalyticsBuilder":
        """
        Set the end date using a Unix timestamp.

        Args:
            timestamp: Unix timestamp (UTC)

        Returns:
            AnalyticsBuilder instance for chaining
        """
        if timestamp <= 0:
            raise ValidationError("Timestamp must be a positive integer")
        self._date_to = timestamp
        return self

    def date_from_datetime(self, dt: datetime) -> "AnalyticsBuilder":
        """
        Set the start date using a datetime object.

        Args:
            dt: Datetime object (will be converted to UTC)

        Returns:
            AnalyticsBuilder instance for chaining
        """
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        self._date_from = int(dt.timestamp())
        return self

    def date_to_datetime(self, dt: datetime) -> "AnalyticsBuilder":
        """
        Set the end date using a datetime object.

        Args:
            dt: Datetime object (will be converted to UTC)

        Returns:
            AnalyticsBuilder instance for chaining
        """
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        self._date_to = int(dt.timestamp())
        return self

    def date_range(self, date_from: datetime, date_to: datetime) -> "AnalyticsBuilder":
        """
        Set both start and end dates using datetime objects.

        Args:
            date_from: Start datetime
            date_to: End datetime

        Returns:
            AnalyticsBuilder instance for chaining
        """
        self.date_from_datetime(date_from)
        self.date_to_datetime(date_to)
        return self

    def date_range_days(
        self, days: int, end_date: Optional[datetime] = None
    ) -> "AnalyticsBuilder":
        """
        Set date range for the last N days.

        Args:
            days: Number of days to look back
            end_date: End date (defaults to now)

        Returns:
            AnalyticsBuilder instance for chaining
        """
        if end_date is None:
            end_date = datetime.now(timezone.utc)
        elif end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=timezone.utc)

        start_date = end_date - timedelta(days=days)
        return self.date_range(start_date, end_date)

    def date_range_weeks(
        self, weeks: int, end_date: Optional[datetime] = None
    ) -> "AnalyticsBuilder":
        """
        Set date range for the last N weeks.

        Args:
            weeks: Number of weeks to look back
            end_date: End date (defaults to now)

        Returns:
            AnalyticsBuilder instance for chaining
        """
        return self.date_range_days(weeks * 7, end_date)

    def date_range_months(
        self, months: int, end_date: Optional[datetime] = None
    ) -> "AnalyticsBuilder":
        """
        Set date range for the last N months (approximate).

        Args:
            months: Number of months to look back
            end_date: End date (defaults to now)

        Returns:
            AnalyticsBuilder instance for chaining
        """
        return self.date_range_days(months * 30, end_date)

    def today(self) -> "AnalyticsBuilder":
        """
        Set date range for today (00:00 to now).

        Returns:
            AnalyticsBuilder instance for chaining
        """
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.date_range(start_of_day, now)

    def yesterday(self) -> "AnalyticsBuilder":
        """
        Set date range for yesterday (full day).

        Returns:
            AnalyticsBuilder instance for chaining
        """
        now = datetime.now(timezone.utc)
        end_of_yesterday = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_yesterday = end_of_yesterday - timedelta(days=1)
        return self.date_range(start_of_yesterday, end_of_yesterday)

    def this_week(self) -> "AnalyticsBuilder":
        """
        Set date range for this week (Monday to now).

        Returns:
            AnalyticsBuilder instance for chaining
        """
        now = datetime.now(timezone.utc)
        days_since_monday = now.weekday()
        start_of_week = now - timedelta(days=days_since_monday)
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.date_range(start_of_week, now)

    def this_month(self) -> "AnalyticsBuilder":
        """
        Set date range for this month (1st to now).

        Returns:
            AnalyticsBuilder instance for chaining
        """
        now = datetime.now(timezone.utc)
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.date_range(start_of_month, now)

    def tag(self, *tags: str) -> "AnalyticsBuilder":
        """
        Add tags to filter analytics data.

        Args:
            tags: Tag names to add

        Returns:
            AnalyticsBuilder instance for chaining
        """
        for tag in tags:
            if not tag.strip():
                raise ValidationError("Tags cannot be empty")
            if tag not in self._tags:
                self._tags.append(tag)
        return self

    def tags(self, *tags: str) -> "AnalyticsBuilder":
        """
        Alias for tag() method for better readability.

        Args:
            tags: Tag names to add

        Returns:
            AnalyticsBuilder instance for chaining
        """
        return self.tag(*tags)

    def group_by(
        self, group_by: Literal["days", "weeks", "months", "years"]
    ) -> "AnalyticsBuilder":
        """
        Set how to group date-based analytics data.

        Args:
            group_by: Grouping option (days, weeks, months, years)

        Returns:
            AnalyticsBuilder instance for chaining
        """
        if group_by not in ["days", "weeks", "months", "years"]:
            raise ValidationError("group_by must be one of: days, weeks, months, years")
        self._group_by = group_by
        return self

    def event(self, *events: str) -> "AnalyticsBuilder":
        """
        Add events to track in date-based analytics.

        Args:
            events: Event names to track

        Returns:
            AnalyticsBuilder instance for chaining
        """
        valid_events = [
            "queued",
            "sent",
            "delivered",
            "soft_bounced",
            "hard_bounced",
            "opened",
            "clicked",
            "unsubscribed",
            "spam_complaints",
            "survey_opened",
            "survey_submitted",
            "opened_unique",
            "clicked_unique",
        ]

        for event in events:
            if event not in valid_events:
                raise ValidationError(
                    f"Invalid event: {event}. Valid events: {', '.join(valid_events)}"
                )
            if event not in self._event:
                self._event.append(event)
        return self

    def events(self, *events: str) -> "AnalyticsBuilder":
        """
        Alias for event() method for better readability.

        Args:
            events: Event names to track

        Returns:
            AnalyticsBuilder instance for chaining
        """
        return self.event(*events)

    def all_events(self) -> "AnalyticsBuilder":
        """
        Track all available events.

        Returns:
            AnalyticsBuilder instance for chaining
        """
        return self.events(
            "queued",
            "sent",
            "delivered",
            "soft_bounced",
            "hard_bounced",
            "opened",
            "clicked",
            "unsubscribed",
            "spam_complaints",
            "survey_opened",
            "survey_submitted",
            "opened_unique",
            "clicked_unique",
        )

    def delivery_events(self) -> "AnalyticsBuilder":
        """
        Track delivery-related events.

        Returns:
            AnalyticsBuilder instance for chaining
        """
        return self.events(
            "queued", "sent", "delivered", "soft_bounced", "hard_bounced"
        )

    def engagement_events(self) -> "AnalyticsBuilder":
        """
        Track engagement-related events.

        Returns:
            AnalyticsBuilder instance for chaining
        """
        return self.events("opened", "clicked", "opened_unique", "clicked_unique")

    def negative_events(self) -> "AnalyticsBuilder":
        """
        Track negative feedback events.

        Returns:
            AnalyticsBuilder instance for chaining
        """
        return self.events("unsubscribed", "spam_complaints")

    def build(self) -> AnalyticsRequest:
        """
        Build the final AnalyticsRequest object.

        Returns:
            Validated AnalyticsRequest instance

        Raises:
            ValidationError: If required fields are missing or invalid
        """
        if self._date_from is None:
            raise ValidationError("date_from is required")
        if self._date_to is None:
            raise ValidationError("date_to is required")

        return AnalyticsRequest(
            domain_id=self._domain_id,
            recipient_id=self._recipient_id if self._recipient_id else None,
            date_from=self._date_from,
            date_to=self._date_to,
            tags=self._tags if self._tags else None,
            group_by=self._group_by,
            event=self._event if self._event else None,
        )

    def reset(self) -> "AnalyticsBuilder":
        """
        Reset the builder to initial state.

        Returns:
            AnalyticsBuilder instance for chaining
        """
        self._domain_id = None
        self._recipient_id = []
        self._date_from = None
        self._date_to = None
        self._tags = []
        self._group_by = "days"
        self._event = []
        return self

    def copy(self) -> "AnalyticsBuilder":
        """
        Create a copy of the current builder state.

        Returns:
            New AnalyticsBuilder instance with copied state
        """
        new_builder = AnalyticsBuilder()
        new_builder._domain_id = self._domain_id
        new_builder._recipient_id = self._recipient_id.copy()
        new_builder._date_from = self._date_from
        new_builder._date_to = self._date_to
        new_builder._tags = self._tags.copy()
        new_builder._group_by = self._group_by
        new_builder._event = self._event.copy()
        return new_builder
