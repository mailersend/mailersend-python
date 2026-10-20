"""Tests for WhatsAppItems resource."""

import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.whatsapp_items import WhatsAppItems
from mailersend.models.base import APIResponse
from mailersend.models.whatsapp_items import (
    WhatsAppItemsListRequest,
    WhatsAppItemsListQueryParams,
    WhatsAppItemGetRequest,
)


async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestWhatsAppItems:
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
        self.resource = WhatsAppItems(self.mock_client)

    async def test_list_whatsapp_items_returns_api_response(self):
        result = await resolve(
            self.resource.list_whatsapp_items(WhatsAppItemsListRequest())
        )
        assert isinstance(result, APIResponse)

    async def test_list_whatsapp_items_calls_correct_endpoint(self):
        await resolve(self.resource.list_whatsapp_items(WhatsAppItemsListRequest()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/items"
        assert call.kwargs["params"] == {}

    async def test_list_whatsapp_items_with_query_params(self):
        request = WhatsAppItemsListRequest(
            query_params=WhatsAppItemsListQueryParams(
                recipient="48600000002",
                status=["failed"],
                from_="48600000001",
                date_from="2026-10-14T00:00:00Z",
                limit=10,
            )
        )
        await resolve(self.resource.list_whatsapp_items(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"] == {
            "recipient": "48600000002",
            "status[]": ["failed"],
            "from": "48600000001",
            "date_from": "2026-10-14T00:00:00Z",
            "limit": 10,
        }

    async def test_get_whatsapp_item_returns_api_response(self):
        result = await resolve(
            self.resource.get_whatsapp_item(
                WhatsAppItemGetRequest(whatsapp_item_id="abc123")
            )
        )
        assert isinstance(result, APIResponse)

    async def test_get_whatsapp_item_calls_correct_endpoint(self):
        await resolve(
            self.resource.get_whatsapp_item(
                WhatsAppItemGetRequest(whatsapp_item_id="abc123")
            )
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/items/abc123"
