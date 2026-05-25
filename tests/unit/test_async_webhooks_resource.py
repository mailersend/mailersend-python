"""Tests for AsyncWebhooks resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.webhooks import AsyncWebhooks
from mailersend.models.base import APIResponse
from mailersend.models.webhooks import (
    WebhooksListRequest,
    WebhooksListQueryParams,
    WebhookGetRequest,
    WebhookCreateRequest,
    WebhookUpdateRequest,
    WebhookDeleteRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestAsyncWebhooks:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncWebhooks(self.mock_client)

    async def test_list_webhooks_returns_api_response(self):
        request = WebhooksListRequest(
            query_params=WebhooksListQueryParams(domain_id="dom123")
        )
        result = await self.resource.list_webhooks(request)
        assert isinstance(result, APIResponse)

    async def test_list_webhooks_calls_correct_endpoint(self):
        request = WebhooksListRequest(
            query_params=WebhooksListQueryParams(domain_id="dom123")
        )
        await self.resource.list_webhooks(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "webhooks"

    async def test_get_webhook_returns_api_response(self):
        result = await self.resource.get_webhook(WebhookGetRequest(webhook_id="wh123"))
        assert isinstance(result, APIResponse)

    async def test_get_webhook_calls_correct_endpoint(self):
        await self.resource.get_webhook(WebhookGetRequest(webhook_id="wh123"))
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
        result = await self.resource.create_webhook(request)
        assert isinstance(result, APIResponse)

    async def test_create_webhook_calls_correct_endpoint(self):
        request = WebhookCreateRequest(
            url="https://example.com/hook",
            name="My Webhook",
            events=["activity.sent"],
            domain_id="dom123",
        )
        await self.resource.create_webhook(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "webhooks"

    async def test_update_webhook_returns_api_response(self):
        request = WebhookUpdateRequest(webhook_id="wh123", name="Updated")
        result = await self.resource.update_webhook(request)
        assert isinstance(result, APIResponse)

    async def test_update_webhook_excludes_id_from_body(self):
        request = WebhookUpdateRequest(webhook_id="wh123", name="Updated")
        await self.resource.update_webhook(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "webhooks/wh123"
        assert "webhook_id" not in (call.kwargs.get("body") or {})

    async def test_delete_webhook_returns_api_response(self):
        result = await self.resource.delete_webhook(
            WebhookDeleteRequest(webhook_id="wh123")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_webhook_calls_correct_endpoint(self):
        await self.resource.delete_webhook(WebhookDeleteRequest(webhook_id="wh123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "webhooks/wh123"
