"""Tests for AsyncTokens resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.tokens import AsyncTokens
from mailersend.models.base import APIResponse
from mailersend.models.tokens import (
    TokensListRequest,
    TokensListQueryParams,
    TokenGetRequest,
    TokenCreateRequest,
    TokenUpdateRequest,
    TokenUpdateNameRequest,
    TokenDeleteRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestAsyncTokens:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncTokens(self.mock_client)

    async def test_list_tokens_returns_api_response(self):
        result = await self.resource.list_tokens(TokensListRequest())
        assert isinstance(result, APIResponse)

    async def test_list_tokens_calls_correct_endpoint(self):
        await self.resource.list_tokens(TokensListRequest())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "token"

    async def test_get_token_returns_api_response(self):
        result = await self.resource.get_token(TokenGetRequest(token_id="tok123"))
        assert isinstance(result, APIResponse)

    async def test_get_token_calls_correct_endpoint(self):
        await self.resource.get_token(TokenGetRequest(token_id="tok123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "token/tok123"

    async def test_create_token_returns_api_response(self):
        request = TokenCreateRequest(
            name="My Token",
            domain_id="dom123",
            scopes=["email_full"],
        )
        result = await self.resource.create_token(request)
        assert isinstance(result, APIResponse)

    async def test_create_token_calls_correct_endpoint(self):
        request = TokenCreateRequest(
            name="My Token",
            domain_id="dom123",
            scopes=["email_full"],
        )
        await self.resource.create_token(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "token"

    async def test_update_token_returns_api_response(self):
        request = TokenUpdateRequest(token_id="tok123", status="pause")
        result = await self.resource.update_token(request)
        assert isinstance(result, APIResponse)

    async def test_update_token_calls_correct_endpoint(self):
        request = TokenUpdateRequest(token_id="tok123", status="pause")
        await self.resource.update_token(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "token/tok123/settings"

    async def test_update_token_name_returns_api_response(self):
        request = TokenUpdateNameRequest(token_id="tok123", name="New Name")
        result = await self.resource.update_token_name(request)
        assert isinstance(result, APIResponse)

    async def test_update_token_name_calls_correct_endpoint(self):
        request = TokenUpdateNameRequest(token_id="tok123", name="New Name")
        await self.resource.update_token_name(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "token/tok123"

    async def test_delete_token_returns_api_response(self):
        result = await self.resource.delete_token(TokenDeleteRequest(token_id="tok123"))
        assert isinstance(result, APIResponse)

    async def test_delete_token_calls_correct_endpoint(self):
        await self.resource.delete_token(TokenDeleteRequest(token_id="tok123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "token/tok123"
