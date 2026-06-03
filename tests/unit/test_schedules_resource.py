"""Tests for Schedules resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.schedules import Schedules
from mailersend.models.base import APIResponse
from mailersend.models.schedules import (
    SchedulesListRequest,
    SchedulesListQueryParams,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestSchedules:
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
        self.resource = Schedules(self.mock_client)

    async def test_list_schedules_returns_api_response(self):
        request = SchedulesListRequest(query_params=SchedulesListQueryParams())
        result = await resolve(self.resource.list_schedules(request))
        assert isinstance(result, APIResponse)

    async def test_list_schedules_calls_correct_endpoint(self):
        request = SchedulesListRequest(query_params=SchedulesListQueryParams())
        await resolve(self.resource.list_schedules(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "message-schedules"

    async def test_get_schedule_returns_api_response(self):
        result = await resolve(self.resource.get_schedule(
            ScheduleGetRequest(message_id="msg123"))
        )
        assert isinstance(result, APIResponse)

    async def test_get_schedule_calls_correct_endpoint(self):
        await resolve(self.resource.get_schedule(ScheduleGetRequest(message_id="msg123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "message-schedules/msg123"

    async def test_delete_schedule_returns_api_response(self):
        result = await resolve(self.resource.delete_schedule(
            ScheduleDeleteRequest(message_id="msg123"))
        )
        assert isinstance(result, APIResponse)

    async def test_delete_schedule_calls_correct_endpoint(self):
        await resolve(self.resource.delete_schedule(ScheduleDeleteRequest(message_id="msg123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "message-schedules/msg123"
