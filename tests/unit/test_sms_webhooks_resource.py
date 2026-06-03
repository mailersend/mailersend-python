"""Tests for SmsWebhooks resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.sms_webhooks import SmsWebhooks
from mailersend.models.base import APIResponse
from mailersend.models.sms_webhooks import (
    SmsWebhooksListRequest,
    SmsWebhooksListQueryParams,
    SmsWebhookGetRequest,
    SmsWebhookCreateRequest,
    SmsWebhookUpdateRequest,
    SmsWebhookDeleteRequest,
    SmsWebhookEvent,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestSmsWebhooks:
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
        self.resource = SmsWebhooks(self.mock_client)

    async def test_list_sms_webhooks_returns_api_response(self):
        request = SmsWebhooksListRequest(
            query_params=SmsWebhooksListQueryParams(sms_number_id="num123")
        )
        result = await resolve(self.resource.list_sms_webhooks(request))
        assert isinstance(result, APIResponse)

    async def test_list_sms_webhooks_calls_correct_endpoint(self):
        request = SmsWebhooksListRequest(
            query_params=SmsWebhooksListQueryParams(sms_number_id="num123")
        )
        await resolve(self.resource.list_sms_webhooks(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-webhooks"

    async def test_get_sms_webhook_returns_api_response(self):
        result = await resolve(self.resource.get_sms_webhook(
            SmsWebhookGetRequest(sms_webhook_id="wh123"))
        )
        assert isinstance(result, APIResponse)

    async def test_get_sms_webhook_calls_correct_endpoint(self):
        await resolve(self.resource.get_sms_webhook(
            SmsWebhookGetRequest(sms_webhook_id="wh123"))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-webhooks/wh123"

    async def test_create_sms_webhook_returns_api_response(self):
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="My Webhook",
            events=[SmsWebhookEvent.SMS_SENT],
            sms_number_id="num123",
        )
        result = await resolve(self.resource.create_sms_webhook(request))
        assert isinstance(result, APIResponse)

    async def test_create_sms_webhook_calls_correct_endpoint(self):
        request = SmsWebhookCreateRequest(
            url="https://example.com/webhook",
            name="My Webhook",
            events=[SmsWebhookEvent.SMS_SENT],
            sms_number_id="num123",
        )
        await resolve(self.resource.create_sms_webhook(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "sms-webhooks"

    async def test_update_sms_webhook_returns_api_response(self):
        request = SmsWebhookUpdateRequest(sms_webhook_id="wh123", name="Updated")
        result = await resolve(self.resource.update_sms_webhook(request))
        assert isinstance(result, APIResponse)

    async def test_update_sms_webhook_calls_correct_endpoint(self):
        request = SmsWebhookUpdateRequest(sms_webhook_id="wh123", name="Updated")
        await resolve(self.resource.update_sms_webhook(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "sms-webhooks/wh123"

    async def test_delete_sms_webhook_returns_api_response(self):
        result = await resolve(self.resource.delete_sms_webhook(
            SmsWebhookDeleteRequest(sms_webhook_id="wh123"))
        )
        assert isinstance(result, APIResponse)

    async def test_delete_sms_webhook_calls_correct_endpoint(self):
        await resolve(self.resource.delete_sms_webhook(
            SmsWebhookDeleteRequest(sms_webhook_id="wh123"))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "sms-webhooks/wh123"
