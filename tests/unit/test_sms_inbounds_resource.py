"""Tests for SmsInbounds resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.sms_inbounds import SmsInbounds
from mailersend.models.base import APIResponse
from mailersend.models.sms_inbounds import (
    SmsInboundsListRequest,
    SmsInboundsListQueryParams,
    SmsInboundGetRequest,
    SmsInboundCreateRequest,
    SmsInboundUpdateRequest,
    SmsInboundDeleteRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestSmsInbounds:
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
        self.resource = SmsInbounds(self.mock_client)

    async def test_list_sms_inbounds_returns_api_response(self):
        result = await resolve(self.resource.list_sms_inbounds(SmsInboundsListRequest()))
        assert isinstance(result, APIResponse)

    async def test_list_sms_inbounds_calls_correct_endpoint(self):
        await resolve(self.resource.list_sms_inbounds(SmsInboundsListRequest()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-inbounds"

    async def test_get_sms_inbound_returns_api_response(self):
        result = await resolve(self.resource.get_sms_inbound(
            SmsInboundGetRequest(sms_inbound_id="inb123"))
        )
        assert isinstance(result, APIResponse)

    async def test_get_sms_inbound_calls_correct_endpoint(self):
        await resolve(self.resource.get_sms_inbound(
            SmsInboundGetRequest(sms_inbound_id="inb123"))
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
        result = await resolve(self.resource.create_sms_inbound(request))
        assert isinstance(result, APIResponse)

    async def test_create_sms_inbound_calls_correct_endpoint(self):
        request = SmsInboundCreateRequest(
            sms_number_id="num123",
            name="My Inbound",
            forward_url="https://example.com/webhook",
        )
        await resolve(self.resource.create_sms_inbound(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "sms-inbounds"

    async def test_update_sms_inbound_returns_api_response(self):
        request = SmsInboundUpdateRequest(sms_inbound_id="inb123", name="Updated")
        result = await resolve(self.resource.update_sms_inbound(request))
        assert isinstance(result, APIResponse)

    async def test_update_sms_inbound_calls_correct_endpoint(self):
        request = SmsInboundUpdateRequest(sms_inbound_id="inb123", name="Updated")
        await resolve(self.resource.update_sms_inbound(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "sms-inbounds/inb123"

    async def test_delete_sms_inbound_returns_api_response(self):
        result = await resolve(self.resource.delete_sms_inbound(
            SmsInboundDeleteRequest(sms_inbound_id="inb123"))
        )
        assert isinstance(result, APIResponse)

    async def test_delete_sms_inbound_calls_correct_endpoint(self):
        await resolve(self.resource.delete_sms_inbound(
            SmsInboundDeleteRequest(sms_inbound_id="inb123"))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "sms-inbounds/inb123"
