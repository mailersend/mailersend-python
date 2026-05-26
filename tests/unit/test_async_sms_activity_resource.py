"""Tests for SmsActivity resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.sms_activity import SmsActivity
from mailersend.models.base import APIResponse
from mailersend.models.sms_activity import (
    SmsActivityListRequest,
    SmsMessageGetRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestSmsActivity:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = SmsActivity(self.mock_client)

    async def test_list_returns_api_response(self):
        result = await self.resource.list(SmsActivityListRequest())
        assert isinstance(result, APIResponse)

    async def test_list_calls_correct_endpoint(self):
        await self.resource.list(SmsActivityListRequest())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-activity"

    async def test_get_returns_api_response(self):
        result = await self.resource.get(SmsMessageGetRequest(sms_message_id="msg123"))
        assert isinstance(result, APIResponse)

    async def test_get_calls_correct_endpoint(self):
        await self.resource.get(SmsMessageGetRequest(sms_message_id="msg123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-messages/msg123"
