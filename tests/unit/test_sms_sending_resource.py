"""Tests for SmsSending resource."""

import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.sms_sending import SmsSending
from mailersend.models.base import APIResponse
from mailersend.models.sms_sending import SmsSendRequest


async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestSmsSending:
    @pytest.fixture(autouse=True, params=["sync", "async"])
    def setup(self, request):
        if request.param == "async":
            self.mock_client = MagicMock()
            self.mock_client.request = AsyncMock(
                return_value=MagicMock(
                    status_code=200,
                    headers={"x-request-id": "test-req-id"},
                    json=MagicMock(return_value={}),
                    content=b"{}",
                )
            )
        else:
            self.mock_client = MagicMock()
            self.mock_client.request = Mock(
                return_value=MagicMock(
                    status_code=200,
                    headers={"x-request-id": "test-req-id"},
                    json=MagicMock(return_value={}),
                    content=b"{}",
                )
            )
        self.resource = SmsSending(self.mock_client)

    async def test_send_returns_api_response(self):
        request = SmsSendRequest(
            from_number="+15551234567",
            to=["+15559876543"],
            text="Hello from tests",
        )
        result = await resolve(self.resource.send(request))
        assert isinstance(result, APIResponse)

    async def test_send_calls_correct_endpoint(self):
        request = SmsSendRequest(
            from_number="+15551234567",
            to=["+15559876543"],
            text="Hello from tests",
        )
        await resolve(self.resource.send(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "sms"
