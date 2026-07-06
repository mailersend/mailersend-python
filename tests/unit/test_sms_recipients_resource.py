"""Tests for SmsRecipients resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.sms_recipients import SmsRecipients
from mailersend.models.base import APIResponse
from mailersend.models.sms_recipients import (
    SmsRecipientsListRequest,
    SmsRecipientsListQueryParams,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsRecipientStatus,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestSmsRecipients:
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
        self.resource = SmsRecipients(self.mock_client)

    async def test_list_sms_recipients_returns_api_response(self):
        result = await resolve(self.resource.list_sms_recipients(SmsRecipientsListRequest()))
        assert isinstance(result, APIResponse)

    async def test_list_sms_recipients_calls_correct_endpoint(self):
        await resolve(self.resource.list_sms_recipients(SmsRecipientsListRequest()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-recipients"

    async def test_list_sms_recipients_with_custom_params(self):
        request = SmsRecipientsListRequest(
            query_params=SmsRecipientsListQueryParams(page=2)
        )
        await resolve(self.resource.list_sms_recipients(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2

    async def test_get_sms_recipient_returns_api_response(self):
        result = await resolve(self.resource.get_sms_recipient(
            SmsRecipientGetRequest(sms_recipient_id="rec123"))
        )
        assert isinstance(result, APIResponse)

    async def test_get_sms_recipient_calls_correct_endpoint(self):
        await resolve(self.resource.get_sms_recipient(
            SmsRecipientGetRequest(sms_recipient_id="rec123"))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-recipients/rec123"

    async def test_update_sms_recipient_returns_api_response(self):
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="rec123", status=SmsRecipientStatus.ACTIVE
        )
        result = await resolve(self.resource.update_sms_recipient(request))
        assert isinstance(result, APIResponse)

    async def test_update_sms_recipient_calls_correct_endpoint(self):
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="rec123", status=SmsRecipientStatus.ACTIVE
        )
        await resolve(self.resource.update_sms_recipient(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "sms-recipients/rec123"
