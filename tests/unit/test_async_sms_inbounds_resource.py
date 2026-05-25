"""Tests for AsyncSmsInbounds resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.sms_inbounds import AsyncSmsInbounds
from mailersend.models.base import APIResponse
from mailersend.models.sms_inbounds import (
    SmsInboundsListRequest,
    SmsInboundsListQueryParams,
    SmsInboundGetRequest,
    SmsInboundCreateRequest,
    SmsInboundUpdateRequest,
    SmsInboundDeleteRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestAsyncSmsInbounds:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncSmsInbounds(self.mock_client)

    async def test_list_sms_inbounds_returns_api_response(self):
        result = await self.resource.list_sms_inbounds(SmsInboundsListRequest())
        assert isinstance(result, APIResponse)

    async def test_list_sms_inbounds_calls_correct_endpoint(self):
        await self.resource.list_sms_inbounds(SmsInboundsListRequest())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-inbounds"

    async def test_get_sms_inbound_returns_api_response(self):
        result = await self.resource.get_sms_inbound(
            SmsInboundGetRequest(sms_inbound_id="inb123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_sms_inbound_calls_correct_endpoint(self):
        await self.resource.get_sms_inbound(
            SmsInboundGetRequest(sms_inbound_id="inb123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-inbounds/inb123"

    async def test_create_sms_inbound_returns_api_response(self):
        request = SmsInboundCreateRequest(
            sms_number_id="num123",
            name="My Inbound",
            forward_url="https://example.com/webhook",
        )
        result = await self.resource.create_sms_inbound(request)
        assert isinstance(result, APIResponse)

    async def test_create_sms_inbound_calls_correct_endpoint(self):
        request = SmsInboundCreateRequest(
            sms_number_id="num123",
            name="My Inbound",
            forward_url="https://example.com/webhook",
        )
        await self.resource.create_sms_inbound(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "sms-inbounds"

    async def test_update_sms_inbound_returns_api_response(self):
        request = SmsInboundUpdateRequest(sms_inbound_id="inb123", name="Updated")
        result = await self.resource.update_sms_inbound(request)
        assert isinstance(result, APIResponse)

    async def test_update_sms_inbound_calls_correct_endpoint(self):
        request = SmsInboundUpdateRequest(sms_inbound_id="inb123", name="Updated")
        await self.resource.update_sms_inbound(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "sms-inbounds/inb123"

    async def test_delete_sms_inbound_returns_api_response(self):
        result = await self.resource.delete_sms_inbound(
            SmsInboundDeleteRequest(sms_inbound_id="inb123")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_sms_inbound_calls_correct_endpoint(self):
        await self.resource.delete_sms_inbound(
            SmsInboundDeleteRequest(sms_inbound_id="inb123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "sms-inbounds/inb123"
