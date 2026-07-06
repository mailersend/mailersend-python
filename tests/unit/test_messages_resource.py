"""Tests for Messages resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.messages import Messages
from mailersend.models.base import APIResponse
from mailersend.models.messages import (
    MessagesListRequest,
    MessagesListQueryParams,
    MessageGetRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestMessages:
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
        self.resource = Messages(self.mock_client)

    async def test_list_messages_returns_api_response(self):
        request = MessagesListRequest(query_params=MessagesListQueryParams())
        result = await resolve(self.resource.list_messages(request))
        assert isinstance(result, APIResponse)

    async def test_list_messages_calls_correct_endpoint(self):
        request = MessagesListRequest(query_params=MessagesListQueryParams())
        await resolve(self.resource.list_messages(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "messages"

    async def test_list_messages_passes_query_params(self):
        request = MessagesListRequest(
            query_params=MessagesListQueryParams(page=2, limit=10)
        )
        await resolve(self.resource.list_messages(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2
        assert call.kwargs["params"]["limit"] == 10

    async def test_get_message_returns_api_response(self):
        result = await resolve(self.resource.get_message(MessageGetRequest(message_id="msg123")))
        assert isinstance(result, APIResponse)

    async def test_get_message_calls_correct_endpoint(self):
        await resolve(self.resource.get_message(MessageGetRequest(message_id="msg123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "messages/msg123"
