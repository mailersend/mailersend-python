"""DMARC Monitoring resource."""

from typing import Optional

from .base import BaseResource
from ..models.base import APIResponse
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


class DmarcMonitoring(BaseResource):
    """Client for interacting with the MailerSend DMARC Monitoring API."""

    def list_monitors(
        self, request: Optional[DmarcMonitoringListRequest] = None
    ) -> APIResponse:
        """
        Retrieve a list of DMARC monitors.

        Args:
            request: Optional DmarcMonitoringListRequest with pagination options

        Returns:
            APIResponse with list of monitors
        """
        if request is None:
            query_params = DmarcMonitoringListQueryParams()
            request = DmarcMonitoringListRequest(query_params=query_params)

        params = request.to_query_params()
        self.logger.debug("Listing DMARC monitors with params: %s", params)

        response = self.client.request(
            method="GET", path="dmarc-monitoring", params=params
        )
        return self._create_response(response)

    def create_monitor(self, request: DmarcMonitoringCreateRequest) -> APIResponse:
        """
        Create a new DMARC monitor.

        Args:
            request: DmarcMonitoringCreateRequest with domain_id

        Returns:
            APIResponse with created monitor information
        """
        body = request.model_dump(by_alias=True, exclude_none=True)
        self.logger.debug("Creating DMARC monitor with body: %s", body)

        response = self.client.request(
            method="POST", path="dmarc-monitoring", body=body
        )
        return self._create_response(response)

    def update_monitor(self, request: DmarcMonitoringUpdateRequest) -> APIResponse:
        """
        Update a DMARC monitor.

        Args:
            request: DmarcMonitoringUpdateRequest with monitor_id and wanted_dmarc_record

        Returns:
            APIResponse with updated monitor information
        """
        body = request.model_dump(
            by_alias=True, exclude_none=True, exclude={"monitor_id"}
        )
        self.logger.debug("Updating DMARC monitor %s with body: %s", request.monitor_id, body)

        response = self.client.request(
            method="PUT", path=f"dmarc-monitoring/{request.monitor_id}", body=body
        )
        return self._create_response(response)

    def delete_monitor(self, request: DmarcMonitoringDeleteRequest) -> APIResponse:
        """
        Delete a DMARC monitor.

        Args:
            request: DmarcMonitoringDeleteRequest with monitor_id

        Returns:
            APIResponse
        """
        self.logger.debug("Deleting DMARC monitor: %s", request.monitor_id)

        response = self.client.request(
            method="DELETE", path=f"dmarc-monitoring/{request.monitor_id}"
        )
        return self._create_response(response)

    def get_aggregated_report(
        self, request: DmarcMonitoringReportRequest
    ) -> APIResponse:
        """
        Get aggregated DMARC reports for a monitor.

        Args:
            request: DmarcMonitoringReportRequest with monitor_id and pagination options

        Returns:
            APIResponse with aggregated report data
        """
        params = request.to_query_params()
        self.logger.debug(
            "Getting aggregated report for monitor %s with params: %s",
            request.monitor_id,
            params,
        )

        response = self.client.request(
            method="GET",
            path=f"dmarc-monitoring/{request.monitor_id}/report",
            params=params,
        )
        return self._create_response(response)

    def get_ip_report(self, request: DmarcMonitoringIpReportRequest) -> APIResponse:
        """
        Get IP-specific DMARC reports for a monitor.

        Args:
            request: DmarcMonitoringIpReportRequest with monitor_id, ip, and pagination options

        Returns:
            APIResponse with IP-specific report data
        """
        params = request.to_query_params()
        self.logger.debug(
            "Getting IP report for monitor %s, IP %s with params: %s",
            request.monitor_id,
            request.ip,
            params,
        )

        response = self.client.request(
            method="GET",
            path=f"dmarc-monitoring/{request.monitor_id}/report/{request.ip}",
            params=params,
        )
        return self._create_response(response)

    def get_report_sources(
        self, request: DmarcMonitoringReportSourcesRequest
    ) -> APIResponse:
        """
        Get report sources for a DMARC monitor.

        Args:
            request: DmarcMonitoringReportSourcesRequest with monitor_id

        Returns:
            APIResponse with report sources data
        """
        self.logger.debug("Getting report sources for monitor: %s", request.monitor_id)

        response = self.client.request(
            method="GET",
            path=f"dmarc-monitoring/{request.monitor_id}/report-sources",
        )
        return self._create_response(response)

    def mark_ip_favorite(self, request: DmarcMonitoringFavoriteRequest) -> APIResponse:
        """
        Mark an IP address as favorite for a DMARC monitor.

        Args:
            request: DmarcMonitoringFavoriteRequest with monitor_id and ip

        Returns:
            APIResponse
        """
        self.logger.debug(
            "Marking IP %s as favorite for monitor: %s", request.ip, request.monitor_id
        )

        response = self.client.request(
            method="PUT",
            path=f"dmarc-monitoring/{request.monitor_id}/favorite/{request.ip}",
        )
        return self._create_response(response)

    def remove_ip_favorite(
        self, request: DmarcMonitoringFavoriteRequest
    ) -> APIResponse:
        """
        Remove an IP address from favorites for a DMARC monitor.

        Args:
            request: DmarcMonitoringFavoriteRequest with monitor_id and ip

        Returns:
            APIResponse
        """
        self.logger.debug(
            "Removing IP %s from favorites for monitor: %s",
            request.ip,
            request.monitor_id,
        )

        response = self.client.request(
            method="DELETE",
            path=f"dmarc-monitoring/{request.monitor_id}/favorite/{request.ip}",
        )
        return self._create_response(response)
