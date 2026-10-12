"""Tests for WhatsAppRecipients resource."""

import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.whatsapp_recipients import WhatsAppRecipients
from mailersend.models.base import APIResponse
from mailersend.models.whatsapp_recipients import (
    WhatsAppRecipientsListRequest,
    WhatsAppRecipientsListQueryParams,
    WhatsAppRecipientGetRequest,
)


async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestWhatsAppRecipients:
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
        self.resource = WhatsAppRecipients(self.mock_client)

    async def test_list_whatsapp_recipients_returns_api_response(self):
        result = await resolve(
            self.resource.list_whatsapp_recipients(WhatsAppRecipientsListRequest())
        )
        assert isinstance(result, APIResponse)

    async def test_list_whatsapp_recipients_calls_correct_endpoint(self):
        await resolve(
            self.resource.list_whatsapp_recipients(WhatsAppRecipientsListRequest())
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/recipients"
        assert call.kwargs["params"] == {}

    async def test_list_whatsapp_recipients_with_query_params(self):
        request = WhatsAppRecipientsListRequest(
            query_params=WhatsAppRecipientsListQueryParams(status="active", limit=50)
        )
        await resolve(self.resource.list_whatsapp_recipients(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"] == {"status": "active", "limit": 50}

    async def test_get_whatsapp_recipient_returns_api_response(self):
        result = await resolve(
            self.resource.get_whatsapp_recipient(
                WhatsAppRecipientGetRequest(whatsapp_recipient_id="abc123")
            )
        )
        assert isinstance(result, APIResponse)

    async def test_get_whatsapp_recipient_calls_correct_endpoint(self):
        await resolve(
            self.resource.get_whatsapp_recipient(
                WhatsAppRecipientGetRequest(whatsapp_recipient_id="abc123")
            )
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/recipients/abc123"
