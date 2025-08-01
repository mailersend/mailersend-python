"""SMS Inbounds builder for MailerSend SDK."""

from typing import Optional

from ..models.sms_inbounds import (
    SmsInboundsListRequest,
    SmsInboundsListQueryParams,
    SmsInboundGetRequest,
    SmsInboundCreateRequest,
    SmsInboundUpdateRequest,
    SmsInboundDeleteRequest,
    SmsInboundFilter,
    FilterComparer,
)


class SmsInboundsBuilder:
    """Builder for SMS Inbounds requests."""

    def __init__(self) -> None:
        """Initialize the SMS Inbounds builder."""
        # Query parameters
        self._sms_number_id: Optional[str] = None
        self._enabled: Optional[bool] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None

        # Resource identifiers
        self._sms_inbound_id: Optional[str] = None

        # Create/Update fields
        self._name: Optional[str] = None
        self._forward_url: Optional[str] = None
        self._filter_comparer: Optional[FilterComparer] = None
        self._filter_value: Optional[str] = None

    def sms_number_id(self, sms_number_id: str) -> "SmsInboundsBuilder":
        """Set SMS number ID.

        Args:
            sms_number_id: SMS number ID

        Returns:
            SmsInboundsBuilder: Builder instance for method chaining
        """
        self._sms_number_id = sms_number_id
        return self

    def enabled(self, enabled: bool) -> "SmsInboundsBuilder":
        """Set enabled filter.

        Args:
            enabled: Whether inbound routes are enabled

        Returns:
            SmsInboundsBuilder: Builder instance for method chaining
        """
        self._enabled = enabled
        return self

    def page(self, page: int) -> "SmsInboundsBuilder":
        """Set page number.

        Args:
            page: Page number for pagination

        Returns:
            SmsInboundsBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "SmsInboundsBuilder":
        """Set page size limit.

        Args:
            limit: Number of items per page

        Returns:
            SmsInboundsBuilder: Builder instance for method chaining
        """
        self._limit = limit
        return self

    def sms_inbound_id(self, sms_inbound_id: str) -> "SmsInboundsBuilder":
        """Set SMS inbound ID.

        Args:
            sms_inbound_id: SMS inbound route ID

        Returns:
            SmsInboundsBuilder: Builder instance for method chaining
        """
        self._sms_inbound_id = sms_inbound_id
        return self

    def name(self, name: str) -> "SmsInboundsBuilder":
        """Set inbound route name.

        Args:
            name: Name of the inbound route

        Returns:
            SmsInboundsBuilder: Builder instance for method chaining
        """
        self._name = name
        return self

    def forward_url(self, forward_url: str) -> "SmsInboundsBuilder":
        """Set forward URL.

        Args:
            forward_url: URL to forward inbound messages to

        Returns:
            SmsInboundsBuilder: Builder instance for method chaining
        """
        self._forward_url = forward_url
        return self

    def filter(self, comparer: FilterComparer, value: str) -> "SmsInboundsBuilder":
        """Set filter for inbound routing.

        Args:
            comparer: Filter comparison method
            value: Value to compare against

        Returns:
            SmsInboundsBuilder: Builder instance for method chaining
        """
        self._filter_comparer = comparer
        self._filter_value = value
        return self

    def build_list_request(self) -> SmsInboundsListRequest:
        """Build a list request for SMS inbounds.

        Returns:
            SmsInboundsListRequest: Request object for listing SMS inbounds
        """
        query_params = SmsInboundsListQueryParams(
            sms_number_id=self._sms_number_id,
            enabled=self._enabled,
            page=self._page,
            limit=self._limit,
        )
        return SmsInboundsListRequest(query_params=query_params)

    def build_get_request(self) -> SmsInboundGetRequest:
        """Build a get request for a single SMS inbound.

        Returns:
            SmsInboundGetRequest: Request object for getting SMS inbound

        Raises:
            ValueError: If SMS inbound ID is not set
        """
        if self._sms_inbound_id is None:
            raise ValueError("SMS inbound ID is required for get request")
        return SmsInboundGetRequest(sms_inbound_id=self._sms_inbound_id)

    def build_create_request(self) -> SmsInboundCreateRequest:
        """Build a create request for SMS inbound.

        Returns:
            SmsInboundCreateRequest: Request object for creating SMS inbound

        Raises:
            ValueError: If required fields are not set
        """
        if self._sms_number_id is None:
            raise ValueError("SMS number ID is required for create request")
        if self._name is None:
            raise ValueError("Name is required for create request")
        if self._forward_url is None:
            raise ValueError("Forward URL is required for create request")

        # Only include filter if both comparer and value are set
        filter_obj = None
        if self._filter_comparer is not None and self._filter_value is not None:
            filter_obj = SmsInboundFilter(
                comparer=self._filter_comparer, value=self._filter_value
            )

        # Only include enabled if it's explicitly set
        kwargs = {
            "sms_number_id": self._sms_number_id,
            "name": self._name,
            "forward_url": self._forward_url,
        }
        if filter_obj is not None:
            kwargs["filter"] = filter_obj
        if self._enabled is not None:
            kwargs["enabled"] = self._enabled

        return SmsInboundCreateRequest(**kwargs)

    def build_update_request(self) -> SmsInboundUpdateRequest:
        """Build an update request for SMS inbound.

        Returns:
            SmsInboundUpdateRequest: Request object for updating SMS inbound

        Raises:
            ValueError: If SMS inbound ID is not set
        """
        if self._sms_inbound_id is None:
            raise ValueError("SMS inbound ID is required for update request")

        # Only include filter if both comparer and value are set
        filter_obj = None
        if self._filter_comparer is not None and self._filter_value is not None:
            filter_obj = SmsInboundFilter(
                comparer=self._filter_comparer, value=self._filter_value
            )

        return SmsInboundUpdateRequest(
            sms_inbound_id=self._sms_inbound_id,
            sms_number_id=self._sms_number_id,
            name=self._name,
            forward_url=self._forward_url,
            filter=filter_obj,
            enabled=self._enabled,
        )

    def build_delete_request(self) -> SmsInboundDeleteRequest:
        """Build a delete request for SMS inbound.

        Returns:
            SmsInboundDeleteRequest: Request object for deleting SMS inbound

        Raises:
            ValueError: If SMS inbound ID is not set
        """
        if self._sms_inbound_id is None:
            raise ValueError("SMS inbound ID is required for delete request")
        return SmsInboundDeleteRequest(sms_inbound_id=self._sms_inbound_id)
