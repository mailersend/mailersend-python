"""Tests for WhatsAppInboundMessages resource."""

import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.whatsapp_inbound_messages import WhatsAppInboundMessages
from mailersend.models.base import APIResponse
from mailersend.models.whatsapp_inbound_messages import (
    WhatsAppInboundMessagesListRequest,
    WhatsAppInboundMessagesListQueryParams,
    WhatsAppInboundMessageGetRequest,
)


async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestWhatsAppInboundMessages:
    @pytest.fixture(autouse=True, params=["sync", "async"])
    def setup(self, request):
        response = MagicMock(
            status_code=200,
            headers={"x-request-id": "test-req-id"},
            json=MagicMock(return_value={}),
            content=b"{}",
        )
        self.mock_client = MagicMock()
        if request.param == "async":
            self.mock_client.request = AsyncMock(return_value=response)
        else:
            self.mock_client.request = Mock(return_value=response)
        self.resource = WhatsAppInboundMessages(self.mock_client)

    async def test_list_whatsapp_inbound_messages_returns_api_response(self):
        result = await resolve(
            self.resource.list_whatsapp_inbound_messages(
                WhatsAppInboundMessagesListRequest()
            )
        )
        assert isinstance(result, APIResponse)

    async def test_list_whatsapp_inbound_messages_calls_correct_endpoint(self):
        await resolve(
            self.resource.list_whatsapp_inbound_messages(
                WhatsAppInboundMessagesListRequest()
            )
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/inbound-messages"
        assert call.kwargs["params"] == {}

    async def test_list_whatsapp_inbound_messages_with_query_params(self):
        request = WhatsAppInboundMessagesListRequest(
            query_params=WhatsAppInboundMessagesListQueryParams(
                type=["text", "image"], date_from=1790000000
            )
        )
        await resolve(self.resource.list_whatsapp_inbound_messages(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"] == {
            "type[]": ["text", "image"],
            "date_from": 1790000000,
        }

    async def test_get_whatsapp_inbound_message_returns_api_response(self):
        result = await resolve(
            self.resource.get_whatsapp_inbound_message(
                WhatsAppInboundMessageGetRequest(whatsapp_inbound_message_id="abc123")
            )
        )
        assert isinstance(result, APIResponse)

    async def test_get_whatsapp_inbound_message_calls_correct_endpoint(self):
        await resolve(
            self.resource.get_whatsapp_inbound_message(
                WhatsAppInboundMessageGetRequest(whatsapp_inbound_message_id="abc123")
            )
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/inbound-messages/abc123"
