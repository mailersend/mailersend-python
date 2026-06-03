"""Tests for Tokens resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.tokens import Tokens
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



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestTokens:
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
        self.resource = Tokens(self.mock_client)

    async def test_list_tokens_returns_api_response(self):
        result = await resolve(self.resource.list_tokens(TokensListRequest()))
        assert isinstance(result, APIResponse)

    async def test_list_tokens_calls_correct_endpoint(self):
        await resolve(self.resource.list_tokens(TokensListRequest()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "token"

    async def test_get_token_returns_api_response(self):
        result = await resolve(self.resource.get_token(TokenGetRequest(token_id="tok123")))
        assert isinstance(result, APIResponse)

    async def test_get_token_calls_correct_endpoint(self):
        await resolve(self.resource.get_token(TokenGetRequest(token_id="tok123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "token/tok123"

    async def test_create_token_returns_api_response(self):
        request = TokenCreateRequest(
            name="My Token",
            domain_id="dom123",
            scopes=["email_full"],
        )
        result = await resolve(self.resource.create_token(request))
        assert isinstance(result, APIResponse)

    async def test_create_token_calls_correct_endpoint(self):
        request = TokenCreateRequest(
            name="My Token",
            domain_id="dom123",
            scopes=["email_full"],
        )
        await resolve(self.resource.create_token(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "token"

    async def test_update_token_returns_api_response(self):
        request = TokenUpdateRequest(token_id="tok123", status="pause")
        result = await resolve(self.resource.update_token(request))
        assert isinstance(result, APIResponse)

    async def test_update_token_calls_correct_endpoint(self):
        request = TokenUpdateRequest(token_id="tok123", status="pause")
        await resolve(self.resource.update_token(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "token/tok123/settings"

    async def test_update_token_name_returns_api_response(self):
        request = TokenUpdateNameRequest(token_id="tok123", name="New Name")
        result = await resolve(self.resource.update_token_name(request))
        assert isinstance(result, APIResponse)

    async def test_update_token_name_calls_correct_endpoint(self):
        request = TokenUpdateNameRequest(token_id="tok123", name="New Name")
        await resolve(self.resource.update_token_name(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "token/tok123"

    async def test_delete_token_returns_api_response(self):
        result = await resolve(self.resource.delete_token(TokenDeleteRequest(token_id="tok123")))
        assert isinstance(result, APIResponse)

    async def test_delete_token_calls_correct_endpoint(self):
        await resolve(self.resource.delete_token(TokenDeleteRequest(token_id="tok123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "token/tok123"
