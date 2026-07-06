"""Tests for SmsNumbers resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.sms_numbers import SmsNumbers
from mailersend.models.base import APIResponse
from mailersend.models.sms_numbers import (
    SmsNumbersListRequest,
    SmsNumberGetRequest,
    SmsNumberUpdateRequest,
    SmsNumberDeleteRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestSmsNumbers:
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
        self.resource = SmsNumbers(self.mock_client)

    async def test_list_returns_api_response(self):
        result = await resolve(self.resource.list(SmsNumbersListRequest()))
        assert isinstance(result, APIResponse)

    async def test_list_calls_correct_endpoint(self):
        await resolve(self.resource.list(SmsNumbersListRequest()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-numbers"

    async def test_get_returns_api_response(self):
        result = await resolve(self.resource.get(SmsNumberGetRequest(sms_number_id="num123")))
        assert isinstance(result, APIResponse)

    async def test_get_calls_correct_endpoint(self):
        await resolve(self.resource.get(SmsNumberGetRequest(sms_number_id="num123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-numbers/num123"

    async def test_update_returns_api_response(self):
        result = await resolve(self.resource.update(
            SmsNumberUpdateRequest(sms_number_id="num123", paused=True))
        )
        assert isinstance(result, APIResponse)

    async def test_update_calls_correct_endpoint(self):
        await resolve(self.resource.update(
            SmsNumberUpdateRequest(sms_number_id="num123", paused=True))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "sms-numbers/num123"

    async def test_delete_returns_api_response(self):
        result = await resolve(self.resource.delete(
            SmsNumberDeleteRequest(sms_number_id="num123"))
        )
        assert isinstance(result, APIResponse)

    async def test_delete_calls_correct_endpoint(self):
        await resolve(self.resource.delete(SmsNumberDeleteRequest(sms_number_id="num123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "sms-numbers/num123"
