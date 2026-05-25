"""Tests for AsyncDmarcMonitoring resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.dmarc_monitoring import AsyncDmarcMonitoring
from mailersend.models.base import APIResponse
from mailersend.models.dmarc_monitoring import (
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


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestAsyncDmarcMonitoring:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncDmarcMonitoring(self.mock_client)

    async def test_list_monitors_returns_api_response(self):
        result = await self.resource.list_monitors()
        assert isinstance(result, APIResponse)

    async def test_list_monitors_calls_correct_endpoint(self):
        await self.resource.list_monitors()
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "dmarc-monitoring"

    async def test_list_monitors_with_request(self):
        request = DmarcMonitoringListRequest(
            query_params=DmarcMonitoringListQueryParams(page=2, limit=10)
        )
        await self.resource.list_monitors(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2

    async def test_create_monitor_returns_api_response(self):
        request = DmarcMonitoringCreateRequest(domain_id="dom123")
        result = await self.resource.create_monitor(request)
        assert isinstance(result, APIResponse)

    async def test_create_monitor_calls_correct_endpoint(self):
        request = DmarcMonitoringCreateRequest(domain_id="dom123")
        await self.resource.create_monitor(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "dmarc-monitoring"

    async def test_update_monitor_returns_api_response(self):
        request = DmarcMonitoringUpdateRequest(
            monitor_id="mon123", wanted_dmarc_record="v=DMARC1; p=none;"
        )
        result = await self.resource.update_monitor(request)
        assert isinstance(result, APIResponse)

    async def test_update_monitor_calls_correct_endpoint(self):
        request = DmarcMonitoringUpdateRequest(
            monitor_id="mon123", wanted_dmarc_record="v=DMARC1; p=none;"
        )
        await self.resource.update_monitor(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123"

    async def test_delete_monitor_returns_api_response(self):
        request = DmarcMonitoringDeleteRequest(monitor_id="mon123")
        result = await self.resource.delete_monitor(request)
        assert isinstance(result, APIResponse)

    async def test_delete_monitor_calls_correct_endpoint(self):
        await self.resource.delete_monitor(
            DmarcMonitoringDeleteRequest(monitor_id="mon123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123"

    async def test_get_aggregated_report_returns_api_response(self):
        request = DmarcMonitoringReportRequest(monitor_id="mon123")
        result = await self.resource.get_aggregated_report(request)
        assert isinstance(result, APIResponse)

    async def test_get_aggregated_report_calls_correct_endpoint(self):
        request = DmarcMonitoringReportRequest(monitor_id="mon123")
        await self.resource.get_aggregated_report(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/report"

    async def test_get_ip_report_returns_api_response(self):
        request = DmarcMonitoringIpReportRequest(monitor_id="mon123", ip="1.2.3.4")
        result = await self.resource.get_ip_report(request)
        assert isinstance(result, APIResponse)

    async def test_get_ip_report_calls_correct_endpoint(self):
        request = DmarcMonitoringIpReportRequest(monitor_id="mon123", ip="1.2.3.4")
        await self.resource.get_ip_report(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/report/1.2.3.4"

    async def test_get_report_sources_returns_api_response(self):
        request = DmarcMonitoringReportSourcesRequest(monitor_id="mon123")
        result = await self.resource.get_report_sources(request)
        assert isinstance(result, APIResponse)

    async def test_get_report_sources_calls_correct_endpoint(self):
        request = DmarcMonitoringReportSourcesRequest(monitor_id="mon123")
        await self.resource.get_report_sources(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/report-sources"

    async def test_mark_ip_favorite_returns_api_response(self):
        request = DmarcMonitoringFavoriteRequest(monitor_id="mon123", ip="1.2.3.4")
        result = await self.resource.mark_ip_favorite(request)
        assert isinstance(result, APIResponse)

    async def test_mark_ip_favorite_calls_correct_endpoint(self):
        request = DmarcMonitoringFavoriteRequest(monitor_id="mon123", ip="1.2.3.4")
        await self.resource.mark_ip_favorite(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/favorite/1.2.3.4"

    async def test_remove_ip_favorite_returns_api_response(self):
        request = DmarcMonitoringFavoriteRequest(monitor_id="mon123", ip="1.2.3.4")
        result = await self.resource.remove_ip_favorite(request)
        assert isinstance(result, APIResponse)

    async def test_remove_ip_favorite_calls_correct_endpoint(self):
        request = DmarcMonitoringFavoriteRequest(monitor_id="mon123", ip="1.2.3.4")
        await self.resource.remove_ip_favorite(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/favorite/1.2.3.4"
