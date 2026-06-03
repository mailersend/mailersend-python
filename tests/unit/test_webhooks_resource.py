"""Tests for Webhooks resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.webhooks import Webhooks
from mailersend.models.base import APIResponse
from mailersend.models.webhooks import (
    WebhooksListRequest,
    WebhooksListQueryParams,
    WebhookGetRequest,
    WebhookCreateRequest,
    WebhookUpdateRequest,
    WebhookDeleteRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestWebhooks:
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
        self.resource = Webhooks(self.mock_client)

    async def test_list_webhooks_returns_api_response(self):
        request = WebhooksListRequest(
            query_params=WebhooksListQueryParams(domain_id="dom123")
        )
        result = await resolve(self.resource.list_webhooks(request))
        assert isinstance(result, APIResponse)

    async def test_list_webhooks_calls_correct_endpoint(self):
        request = WebhooksListRequest(
            query_params=WebhooksListQueryParams(domain_id="dom123")
        )
        await resolve(self.resource.list_webhooks(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "webhooks"

    async def test_get_webhook_returns_api_response(self):
        result = await resolve(self.resource.get_webhook(WebhookGetRequest(webhook_id="wh123")))
        assert isinstance(result, APIResponse)

    async def test_get_webhook_calls_correct_endpoint(self):
        await resolve(self.resource.get_webhook(WebhookGetRequest(webhook_id="wh123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "webhooks/wh123"

    async def test_create_webhook_returns_api_response(self):
        request = WebhookCreateRequest(
            url="https://example.com/hook",
            name="My Webhook",
            events=["activity.sent"],
            domain_id="dom123",
        )
        result = await resolve(self.resource.create_webhook(request))
        assert isinstance(result, APIResponse)

    async def test_create_webhook_calls_correct_endpoint(self):
        request = WebhookCreateRequest(
            url="https://example.com/hook",
            name="My Webhook",
            events=["activity.sent"],
            domain_id="dom123",
        )
        await resolve(self.resource.create_webhook(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "webhooks"

    async def test_update_webhook_returns_api_response(self):
        request = WebhookUpdateRequest(webhook_id="wh123", name="Updated")
        result = await resolve(self.resource.update_webhook(request))
        assert isinstance(result, APIResponse)

    async def test_update_webhook_excludes_id_from_body(self):
        request = WebhookUpdateRequest(webhook_id="wh123", name="Updated")
        await resolve(self.resource.update_webhook(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "webhooks/wh123"
        assert "webhook_id" not in (call.kwargs.get("body") or {})

    async def test_delete_webhook_returns_api_response(self):
        result = await resolve(self.resource.delete_webhook(
            WebhookDeleteRequest(webhook_id="wh123"))
        )
        assert isinstance(result, APIResponse)

    async def test_delete_webhook_calls_correct_endpoint(self):
        await resolve(self.resource.delete_webhook(WebhookDeleteRequest(webhook_id="wh123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "webhooks/wh123"
