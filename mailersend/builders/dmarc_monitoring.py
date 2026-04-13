"""Builder for DMARC Monitoring requests."""

from typing import Optional

from ..exceptions import ValidationError
from ..models.dmarc_monitoring import (
    DmarcMonitoringListRequest,
    DmarcMonitoringListQueryParams,
    DmarcMonitoringCreateRequest,
    DmarcMonitoringUpdateRequest,
    DmarcMonitoringDeleteRequest,
    DmarcMonitoringReportRequest,
    DmarcMonitoringReportQueryParams,
    DmarcMonitoringIpReportRequest,
    DmarcMonitoringReportSourcesRequest,
    DmarcMonitoringFavoriteRequest,
)


class DmarcMonitoringBuilder:
    """Builder for creating DMARC Monitoring requests using a fluent interface."""

    def __init__(self):
        """Initialize a new DmarcMonitoringBuilder."""
        self._reset()

    def _reset(self):
        """Reset all builder state."""
        self._monitor_id: Optional[str] = None
        self._ip: Optional[str] = None
        self._domain_id: Optional[str] = None
        self._wanted_dmarc_record: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None

    def monitor_id(self, monitor_id: str) -> "DmarcMonitoringBuilder":
        """Set the monitor ID."""
        self._monitor_id = monitor_id
        return self

    def ip(self, ip: str) -> "DmarcMonitoringBuilder":
        """Set the IP address."""
        self._ip = ip
        return self

    def domain_id(self, domain_id: str) -> "DmarcMonitoringBuilder":
        """Set the domain ID for creating a monitor."""
        self._domain_id = domain_id
        return self

    def wanted_dmarc_record(self, record: str) -> "DmarcMonitoringBuilder":
        """Set the wanted DMARC record for updating a monitor."""
        self._wanted_dmarc_record = record
        return self

    def page(self, page: int) -> "DmarcMonitoringBuilder":
        """Set the page number for pagination."""
        if page < 1:
            raise ValidationError("Page must be greater than 0")
        self._page = page
        return self

    def limit(self, limit: int) -> "DmarcMonitoringBuilder":
        """Set the number of items per page."""
        if limit < 10 or limit > 100:
            raise ValidationError("Limit must be between 10 and 100")
        self._limit = limit
        return self

    def build_list_request(self) -> DmarcMonitoringListRequest:
        """Build a DmarcMonitoringListRequest."""
        query_params = DmarcMonitoringListQueryParams(
            page=self._page if self._page is not None else 1,
            limit=self._limit if self._limit is not None else 25,
        )
        return DmarcMonitoringListRequest(query_params=query_params)

    def build_create_request(self) -> DmarcMonitoringCreateRequest:
        """Build a DmarcMonitoringCreateRequest."""
        return DmarcMonitoringCreateRequest(domain_id=self._domain_id)

    def build_update_request(self) -> DmarcMonitoringUpdateRequest:
        """Build a DmarcMonitoringUpdateRequest."""
        return DmarcMonitoringUpdateRequest(
            monitor_id=self._monitor_id,
            wanted_dmarc_record=self._wanted_dmarc_record,
        )

    def build_delete_request(self) -> DmarcMonitoringDeleteRequest:
        """Build a DmarcMonitoringDeleteRequest."""
        return DmarcMonitoringDeleteRequest(monitor_id=self._monitor_id)

    def build_report_request(self) -> DmarcMonitoringReportRequest:
        """Build a DmarcMonitoringReportRequest for aggregated reports."""
        query_params = DmarcMonitoringReportQueryParams(
            page=self._page if self._page is not None else 1,
            limit=self._limit if self._limit is not None else 25,
        )
        return DmarcMonitoringReportRequest(
            monitor_id=self._monitor_id,
            query_params=query_params,
        )

    def build_ip_report_request(self) -> DmarcMonitoringIpReportRequest:
        """Build a DmarcMonitoringIpReportRequest for IP-specific reports."""
        query_params = DmarcMonitoringReportQueryParams(
            page=self._page if self._page is not None else 1,
            limit=self._limit if self._limit is not None else 25,
        )
        return DmarcMonitoringIpReportRequest(
            monitor_id=self._monitor_id,
            ip=self._ip,
            query_params=query_params,
        )

    def build_report_sources_request(self) -> DmarcMonitoringReportSourcesRequest:
        """Build a DmarcMonitoringReportSourcesRequest."""
        return DmarcMonitoringReportSourcesRequest(monitor_id=self._monitor_id)

    def build_mark_favorite_request(self) -> DmarcMonitoringFavoriteRequest:
        """Build a DmarcMonitoringFavoriteRequest for marking an IP as favorite."""
        return DmarcMonitoringFavoriteRequest(
            monitor_id=self._monitor_id,
            ip=self._ip,
        )

    def build_remove_favorite_request(self) -> DmarcMonitoringFavoriteRequest:
        """Build a DmarcMonitoringFavoriteRequest for removing an IP from favorites."""
        return DmarcMonitoringFavoriteRequest(
            monitor_id=self._monitor_id,
            ip=self._ip,
        )
