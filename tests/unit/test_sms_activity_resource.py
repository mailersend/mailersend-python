"""Tests for SmsActivity resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.sms_activity import SmsActivity
from mailersend.models.base import APIResponse
from mailersend.models.sms_activity import (
    SmsActivityListRequest,
    SmsMessageGetRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestSmsActivity:
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
        self.resource = SmsActivity(self.mock_client)

    async def test_list_returns_api_response(self):
        result = await resolve(self.resource.list(SmsActivityListRequest()))
        assert isinstance(result, APIResponse)

    async def test_list_calls_correct_endpoint(self):
        await resolve(self.resource.list(SmsActivityListRequest()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-activity"

    async def test_get_returns_api_response(self):
        result = await resolve(self.resource.get(SmsMessageGetRequest(sms_message_id="msg123")))
        assert isinstance(result, APIResponse)

    async def test_get_calls_correct_endpoint(self):
        await resolve(self.resource.get(SmsMessageGetRequest(sms_message_id="msg123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-messages/msg123"
