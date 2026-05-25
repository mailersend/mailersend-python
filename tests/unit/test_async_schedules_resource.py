"""Tests for AsyncSchedules resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.schedules import AsyncSchedules
from mailersend.models.base import APIResponse
from mailersend.models.schedules import (
    SchedulesListRequest,
    SchedulesListQueryParams,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestAsyncSchedules:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncSchedules(self.mock_client)

    async def test_list_schedules_returns_api_response(self):
        request = SchedulesListRequest(query_params=SchedulesListQueryParams())
        result = await self.resource.list_schedules(request)
        assert isinstance(result, APIResponse)

    async def test_list_schedules_calls_correct_endpoint(self):
        request = SchedulesListRequest(query_params=SchedulesListQueryParams())
        await self.resource.list_schedules(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "message-schedules"

    async def test_get_schedule_returns_api_response(self):
        result = await self.resource.get_schedule(
            ScheduleGetRequest(message_id="msg123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_schedule_calls_correct_endpoint(self):
        await self.resource.get_schedule(ScheduleGetRequest(message_id="msg123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "message-schedules/msg123"

    async def test_delete_schedule_returns_api_response(self):
        result = await self.resource.delete_schedule(
            ScheduleDeleteRequest(message_id="msg123")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_schedule_calls_correct_endpoint(self):
        await self.resource.delete_schedule(ScheduleDeleteRequest(message_id="msg123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "message-schedules/msg123"
