"""Tests for SmsRecipients resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.sms_recipients import SmsRecipients
from mailersend.models.base import APIResponse
from mailersend.models.sms_recipients import (
    SmsRecipientsListRequest,
    SmsRecipientsListQueryParams,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsRecipientStatus,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestSmsRecipients:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = SmsRecipients(self.mock_client)

    async def test_list_sms_recipients_returns_api_response(self):
        result = await self.resource.list_sms_recipients(SmsRecipientsListRequest())
        assert isinstance(result, APIResponse)

    async def test_list_sms_recipients_calls_correct_endpoint(self):
        await self.resource.list_sms_recipients(SmsRecipientsListRequest())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-recipients"

    async def test_list_sms_recipients_with_custom_params(self):
        request = SmsRecipientsListRequest(
            query_params=SmsRecipientsListQueryParams(page=2)
        )
        await self.resource.list_sms_recipients(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2

    async def test_get_sms_recipient_returns_api_response(self):
        result = await self.resource.get_sms_recipient(
            SmsRecipientGetRequest(sms_recipient_id="rec123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_sms_recipient_calls_correct_endpoint(self):
        await self.resource.get_sms_recipient(
            SmsRecipientGetRequest(sms_recipient_id="rec123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "sms-recipients/rec123"

    async def test_update_sms_recipient_returns_api_response(self):
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="rec123", status=SmsRecipientStatus.ACTIVE
        )
        result = await self.resource.update_sms_recipient(request)
        assert isinstance(result, APIResponse)

    async def test_update_sms_recipient_calls_correct_endpoint(self):
        request = SmsRecipientUpdateRequest(
            sms_recipient_id="rec123", status=SmsRecipientStatus.ACTIVE
        )
        await self.resource.update_sms_recipient(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "sms-recipients/rec123"
