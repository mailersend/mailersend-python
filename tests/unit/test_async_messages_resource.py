"""Tests for Messages resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.messages import Messages
from mailersend.models.base import APIResponse
from mailersend.models.messages import (
    MessagesListRequest,
    MessagesListQueryParams,
    MessageGetRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestMessages:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = Messages(self.mock_client)

    async def test_list_messages_returns_api_response(self):
        request = MessagesListRequest(query_params=MessagesListQueryParams())
        result = await self.resource.list_messages(request)
        assert isinstance(result, APIResponse)

    async def test_list_messages_calls_correct_endpoint(self):
        request = MessagesListRequest(query_params=MessagesListQueryParams())
        await self.resource.list_messages(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "messages"

    async def test_list_messages_passes_query_params(self):
        request = MessagesListRequest(
            query_params=MessagesListQueryParams(page=2, limit=10)
        )
        await self.resource.list_messages(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2
        assert call.kwargs["params"]["limit"] == 10

    async def test_get_message_returns_api_response(self):
        result = await self.resource.get_message(MessageGetRequest(message_id="msg123"))
        assert isinstance(result, APIResponse)

    async def test_get_message_calls_correct_endpoint(self):
        await self.resource.get_message(MessageGetRequest(message_id="msg123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "messages/msg123"
