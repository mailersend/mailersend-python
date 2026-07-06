"""Tests for DmarcMonitoring resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.dmarc_monitoring import DmarcMonitoring
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



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestDmarcMonitoring:
    @pytest.fixture(autouse=True, params=["sync", "async"])
    def setup(self, request):
        if request.param == "async":
            self.mock_client = MagicMock()
            self.mock_client.request = AsyncMock(
                return_value=MagicMock(
                    status_code=200, headers={"x-request-id": "test-req-id"},
                    json=MagicMock(return_value={}), content=b"{}"
                )
            )
        else:
            self.mock_client = MagicMock()
            self.mock_client.request = Mock(
                return_value=MagicMock(
                    status_code=200, headers={"x-request-id": "test-req-id"},
                    json=MagicMock(return_value={}), content=b"{}"
                )
            )
        self.resource = DmarcMonitoring(self.mock_client)

    async def test_list_monitors_returns_api_response(self):
        result = await resolve(self.resource.list_monitors())
        assert isinstance(result, APIResponse)

    async def test_list_monitors_calls_correct_endpoint(self):
        await resolve(self.resource.list_monitors())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "dmarc-monitoring"

    async def test_list_monitors_with_request(self):
        request = DmarcMonitoringListRequest(
            query_params=DmarcMonitoringListQueryParams(page=2, limit=10)
        )
        await resolve(self.resource.list_monitors(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2

    async def test_create_monitor_returns_api_response(self):
        request = DmarcMonitoringCreateRequest(domain_id="dom123")
        result = await resolve(self.resource.create_monitor(request))
        assert isinstance(result, APIResponse)

    async def test_create_monitor_calls_correct_endpoint(self):
        request = DmarcMonitoringCreateRequest(domain_id="dom123")
        await resolve(self.resource.create_monitor(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "dmarc-monitoring"

    async def test_update_monitor_returns_api_response(self):
        request = DmarcMonitoringUpdateRequest(
            monitor_id="mon123", wanted_dmarc_record="v=DMARC1; p=none;"
        )
        result = await resolve(self.resource.update_monitor(request))
        assert isinstance(result, APIResponse)

    async def test_update_monitor_calls_correct_endpoint(self):
        request = DmarcMonitoringUpdateRequest(
            monitor_id="mon123", wanted_dmarc_record="v=DMARC1; p=none;"
        )
        await resolve(self.resource.update_monitor(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123"

    async def test_delete_monitor_returns_api_response(self):
        request = DmarcMonitoringDeleteRequest(monitor_id="mon123")
        result = await resolve(self.resource.delete_monitor(request))
        assert isinstance(result, APIResponse)

    async def test_delete_monitor_calls_correct_endpoint(self):
        await resolve(self.resource.delete_monitor(
            DmarcMonitoringDeleteRequest(monitor_id="mon123"))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123"

    async def test_get_aggregated_report_returns_api_response(self):
        request = DmarcMonitoringReportRequest(monitor_id="mon123")
        result = await resolve(self.resource.get_aggregated_report(request))
        assert isinstance(result, APIResponse)

    async def test_get_aggregated_report_calls_correct_endpoint(self):
        request = DmarcMonitoringReportRequest(monitor_id="mon123")
        await resolve(self.resource.get_aggregated_report(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/report"

    async def test_get_ip_report_returns_api_response(self):
        request = DmarcMonitoringIpReportRequest(monitor_id="mon123", ip="1.2.3.4")
        result = await resolve(self.resource.get_ip_report(request))
        assert isinstance(result, APIResponse)

    async def test_get_ip_report_calls_correct_endpoint(self):
        request = DmarcMonitoringIpReportRequest(monitor_id="mon123", ip="1.2.3.4")
        await resolve(self.resource.get_ip_report(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/report/1.2.3.4"

    async def test_get_report_sources_returns_api_response(self):
        request = DmarcMonitoringReportSourcesRequest(monitor_id="mon123")
        result = await resolve(self.resource.get_report_sources(request))
        assert isinstance(result, APIResponse)

    async def test_get_report_sources_calls_correct_endpoint(self):
        request = DmarcMonitoringReportSourcesRequest(monitor_id="mon123")
        await resolve(self.resource.get_report_sources(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/report-sources"

    async def test_mark_ip_favorite_returns_api_response(self):
        request = DmarcMonitoringFavoriteRequest(monitor_id="mon123", ip="1.2.3.4")
        result = await resolve(self.resource.mark_ip_favorite(request))
        assert isinstance(result, APIResponse)

    async def test_mark_ip_favorite_calls_correct_endpoint(self):
        request = DmarcMonitoringFavoriteRequest(monitor_id="mon123", ip="1.2.3.4")
        await resolve(self.resource.mark_ip_favorite(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/favorite/1.2.3.4"

    async def test_remove_ip_favorite_returns_api_response(self):
        request = DmarcMonitoringFavoriteRequest(monitor_id="mon123", ip="1.2.3.4")
        result = await resolve(self.resource.remove_ip_favorite(request))
        assert isinstance(result, APIResponse)

    async def test_remove_ip_favorite_calls_correct_endpoint(self):
        request = DmarcMonitoringFavoriteRequest(monitor_id="mon123", ip="1.2.3.4")
        await resolve(self.resource.remove_ip_favorite(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "dmarc-monitoring/mon123/favorite/1.2.3.4"
