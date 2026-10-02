"""Tests for WhatsAppMessages resource."""

import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.whatsapp_messages import WhatsAppMessages
from mailersend.models.base import APIResponse
from mailersend.models.whatsapp_messages import (
    WhatsAppMessagesListRequest,
    WhatsAppMessagesListQueryParams,
    WhatsAppMessageGetRequest,
)


async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestWhatsAppMessages:
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
        self.resource = WhatsAppMessages(self.mock_client)

    async def test_list_whatsapp_messages_returns_api_response(self):
        result = await resolve(
            self.resource.list_whatsapp_messages(WhatsAppMessagesListRequest())
        )
        assert isinstance(result, APIResponse)

    async def test_list_whatsapp_messages_calls_correct_endpoint(self):
        await resolve(
            self.resource.list_whatsapp_messages(WhatsAppMessagesListRequest())
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/messages"
        assert call.kwargs["params"] == {}

    async def test_list_whatsapp_messages_with_query_params(self):
        request = WhatsAppMessagesListRequest(
            query_params=WhatsAppMessagesListQueryParams(page=2)
        )
        await resolve(self.resource.list_whatsapp_messages(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"] == {"page": 2}

    async def test_get_whatsapp_message_returns_api_response(self):
        result = await resolve(
            self.resource.get_whatsapp_message(
                WhatsAppMessageGetRequest(whatsapp_message_id="abc123")
            )
        )
        assert isinstance(result, APIResponse)

    async def test_get_whatsapp_message_calls_correct_endpoint(self):
        await resolve(
            self.resource.get_whatsapp_message(
                WhatsAppMessageGetRequest(whatsapp_message_id="abc123")
            )
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/messages/abc123"
