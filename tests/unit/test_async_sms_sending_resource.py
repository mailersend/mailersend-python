"""Tests for SmsSending resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.sms_sending import SmsSending
from mailersend.models.base import APIResponse
from mailersend.models.sms_sending import SmsSendRequest


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestSmsSending:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = SmsSending(self.mock_client)

    async def test_send_returns_api_response(self):
        request = SmsSendRequest(
            from_number="+15551234567",
            to=["+15559876543"],
            text="Hello from tests",
        )
        result = await self.resource.send(request)
        assert isinstance(result, APIResponse)

    async def test_send_calls_correct_endpoint(self):
        request = SmsSendRequest(
            from_number="+15551234567",
            to=["+15559876543"],
            text="Hello from tests",
        )
        await self.resource.send(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "sms"
