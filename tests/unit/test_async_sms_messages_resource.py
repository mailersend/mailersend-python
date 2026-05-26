"""Tests for SmsMessages resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.sms_messages import SmsMessages
from mailersend.models.base import APIResponse
from mailersend.models.sms_messages import (
    SmsMessagesListRequest,
    SmsMessagesListQueryParams,
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


class TestSmsMessages:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = SmsMessages(self.mock_client)

    async def test_list_sms_messages_returns_api_response(self):
        result = await self.resource.list_sms_messages(SmsMessagesListRequest())
        assert isinstance(result, APIResponse)

    async def test_list_sms_messages_calls_correct_endpoint(self):
        await self.resource.list_sms_messages(SmsMessagesListRequest())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-messages"

    async def test_list_sms_messages_passes_query_params(self):
        request = SmsMessagesListRequest(
            query_params=SmsMessagesListQueryParams(page=2, limit=10)
        )
        await self.resource.list_sms_messages(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2
        assert call.kwargs["params"]["limit"] == 10

    async def test_get_sms_message_returns_api_response(self):
        result = await self.resource.get_sms_message(
            SmsMessageGetRequest(sms_message_id="msg123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_sms_message_calls_correct_endpoint(self):
        await self.resource.get_sms_message(
            SmsMessageGetRequest(sms_message_id="msg123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-messages/msg123"
