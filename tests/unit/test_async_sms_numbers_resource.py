"""Tests for AsyncSmsNumbers resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.sms_numbers import AsyncSmsNumbers
from mailersend.models.base import APIResponse
from mailersend.models.sms_numbers import (
    SmsNumbersListRequest,
    SmsNumberGetRequest,
    SmsNumberUpdateRequest,
    SmsNumberDeleteRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestAsyncSmsNumbers:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncSmsNumbers(self.mock_client)

    async def test_list_returns_api_response(self):
        result = await self.resource.list(SmsNumbersListRequest())
        assert isinstance(result, APIResponse)

    async def test_list_calls_correct_endpoint(self):
        await self.resource.list(SmsNumbersListRequest())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-numbers"

    async def test_get_returns_api_response(self):
        result = await self.resource.get(SmsNumberGetRequest(sms_number_id="num123"))
        assert isinstance(result, APIResponse)

    async def test_get_calls_correct_endpoint(self):
        await self.resource.get(SmsNumberGetRequest(sms_number_id="num123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-numbers/num123"

    async def test_update_returns_api_response(self):
        result = await self.resource.update(
            SmsNumberUpdateRequest(sms_number_id="num123", paused=True)
        )
        assert isinstance(result, APIResponse)

    async def test_update_calls_correct_endpoint(self):
        await self.resource.update(
            SmsNumberUpdateRequest(sms_number_id="num123", paused=True)
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "sms-numbers/num123"

    async def test_delete_returns_api_response(self):
        result = await self.resource.delete(
            SmsNumberDeleteRequest(sms_number_id="num123")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_calls_correct_endpoint(self):
        await self.resource.delete(SmsNumberDeleteRequest(sms_number_id="num123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "sms-numbers/num123"
