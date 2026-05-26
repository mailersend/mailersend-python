"""Tests for Recipients resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.recipients import Recipients
from mailersend.models.base import APIResponse
from mailersend.models.recipients import (
    RecipientsListRequest,
    RecipientsListQueryParams,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionListQueryParams,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestRecipients:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = Recipients(self.mock_client)

    async def test_list_recipients_returns_api_response(self):
        result = await self.resource.list_recipients()
        assert isinstance(result, APIResponse)

    async def test_list_recipients_calls_correct_endpoint(self):
        await self.resource.list_recipients()
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "recipients"

    async def test_list_recipients_with_request(self):
        request = RecipientsListRequest(
            query_params=RecipientsListQueryParams(page=2, limit=10)
        )
        await self.resource.list_recipients(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2

    async def test_get_recipient_returns_api_response(self):
        result = await self.resource.get_recipient(
            RecipientGetRequest(recipient_id="rec123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_recipient_calls_correct_endpoint(self):
        await self.resource.get_recipient(RecipientGetRequest(recipient_id="rec123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "recipients/rec123"

    async def test_delete_recipient_returns_api_response(self):
        result = await self.resource.delete_recipient(
            RecipientDeleteRequest(recipient_id="rec123")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_recipient_calls_correct_endpoint(self):
        await self.resource.delete_recipient(
            RecipientDeleteRequest(recipient_id="rec123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "recipients/rec123"

    async def test_list_blocklist_returns_api_response(self):
        result = await self.resource.list_blocklist()
        assert isinstance(result, APIResponse)

    async def test_list_blocklist_calls_correct_endpoint(self):
        await self.resource.list_blocklist()
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "suppressions/blocklist"

    async def test_list_hard_bounces_returns_api_response(self):
        result = await self.resource.list_hard_bounces()
        assert isinstance(result, APIResponse)

    async def test_list_hard_bounces_calls_correct_endpoint(self):
        await self.resource.list_hard_bounces()
        call = self.mock_client.request.call_args
        assert call.kwargs["path"] == "suppressions/hard-bounces"

    async def test_list_spam_complaints_returns_api_response(self):
        result = await self.resource.list_spam_complaints()
        assert isinstance(result, APIResponse)

    async def test_list_spam_complaints_calls_correct_endpoint(self):
        await self.resource.list_spam_complaints()
        call = self.mock_client.request.call_args
        assert call.kwargs["path"] == "suppressions/spam-complaints"

    async def test_list_unsubscribes_returns_api_response(self):
        result = await self.resource.list_unsubscribes()
        assert isinstance(result, APIResponse)

    async def test_list_unsubscribes_calls_correct_endpoint(self):
        await self.resource.list_unsubscribes()
        call = self.mock_client.request.call_args
        assert call.kwargs["path"] == "suppressions/unsubscribes"

    async def test_list_on_hold_returns_api_response(self):
        result = await self.resource.list_on_hold()
        assert isinstance(result, APIResponse)

    async def test_list_on_hold_calls_correct_endpoint(self):
        await self.resource.list_on_hold()
        call = self.mock_client.request.call_args
        assert call.kwargs["path"] == "suppressions/on-hold-list"

    async def test_add_to_blocklist_returns_api_response(self):
        request = SuppressionAddRequest(
            domain_id="dom123", recipients=["a@example.com"]
        )
        result = await self.resource.add_to_blocklist(request)
        assert isinstance(result, APIResponse)

    async def test_add_to_blocklist_calls_correct_endpoint(self):
        request = SuppressionAddRequest(
            domain_id="dom123", recipients=["a@example.com"]
        )
        await self.resource.add_to_blocklist(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "suppressions/blocklist"

    async def test_add_hard_bounces_returns_api_response(self):
        request = SuppressionAddRequest(
            domain_id="dom123", recipients=["a@example.com"]
        )
        result = await self.resource.add_hard_bounces(request)
        assert isinstance(result, APIResponse)

    async def test_add_hard_bounces_calls_correct_endpoint(self):
        request = SuppressionAddRequest(
            domain_id="dom123", recipients=["a@example.com"]
        )
        await self.resource.add_hard_bounces(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "suppressions/hard-bounces"

    async def test_add_spam_complaints_returns_api_response(self):
        request = SuppressionAddRequest(
            domain_id="dom123", recipients=["a@example.com"]
        )
        result = await self.resource.add_spam_complaints(request)
        assert isinstance(result, APIResponse)

    async def test_add_spam_complaints_calls_correct_endpoint(self):
        request = SuppressionAddRequest(
            domain_id="dom123", recipients=["a@example.com"]
        )
        await self.resource.add_spam_complaints(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "suppressions/spam-complaints"

    async def test_add_unsubscribes_returns_api_response(self):
        request = SuppressionAddRequest(
            domain_id="dom123", recipients=["a@example.com"]
        )
        result = await self.resource.add_unsubscribes(request)
        assert isinstance(result, APIResponse)

    async def test_add_unsubscribes_calls_correct_endpoint(self):
        request = SuppressionAddRequest(
            domain_id="dom123", recipients=["a@example.com"]
        )
        await self.resource.add_unsubscribes(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "suppressions/unsubscribes"

    async def test_delete_from_blocklist_returns_api_response(self):
        request = SuppressionDeleteRequest(ids=["id1"])
        result = await self.resource.delete_from_blocklist(request)
        assert isinstance(result, APIResponse)

    async def test_delete_from_blocklist_calls_correct_endpoint(self):
        request = SuppressionDeleteRequest(ids=["id1"])
        await self.resource.delete_from_blocklist(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "suppressions/blocklist"

    async def test_delete_hard_bounces_returns_api_response(self):
        result = await self.resource.delete_hard_bounces(
            SuppressionDeleteRequest(ids=["id1"])
        )
        assert isinstance(result, APIResponse)

    async def test_delete_hard_bounces_calls_correct_endpoint(self):
        await self.resource.delete_hard_bounces(SuppressionDeleteRequest(ids=["id1"]))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "suppressions/hard-bounces"

    async def test_delete_spam_complaints_returns_api_response(self):
        result = await self.resource.delete_spam_complaints(
            SuppressionDeleteRequest(ids=["id1"])
        )
        assert isinstance(result, APIResponse)

    async def test_delete_spam_complaints_calls_correct_endpoint(self):
        await self.resource.delete_spam_complaints(
            SuppressionDeleteRequest(ids=["id1"])
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "suppressions/spam-complaints"

    async def test_delete_unsubscribes_returns_api_response(self):
        result = await self.resource.delete_unsubscribes(
            SuppressionDeleteRequest(ids=["id1"])
        )
        assert isinstance(result, APIResponse)

    async def test_delete_unsubscribes_calls_correct_endpoint(self):
        await self.resource.delete_unsubscribes(SuppressionDeleteRequest(ids=["id1"]))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "suppressions/unsubscribes"

    async def test_delete_from_on_hold_returns_api_response(self):
        result = await self.resource.delete_from_on_hold(
            SuppressionDeleteRequest(ids=["id1"])
        )
        assert isinstance(result, APIResponse)

    async def test_delete_from_on_hold_calls_correct_endpoint(self):
        await self.resource.delete_from_on_hold(SuppressionDeleteRequest(ids=["id1"]))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "suppressions/on-hold-list"

    async def test_delete_hard_bounces_excludes_domain_id_from_body(self):
        request = SuppressionDeleteRequest(domain_id="dom123", ids=["id1"])
        await self.resource.delete_hard_bounces(request)
        body = self.mock_client.request.call_args.kwargs.get("body") or {}
        assert "domain_id" not in body
        assert body.get("ids") == ["id1"]

    async def test_delete_spam_complaints_excludes_domain_id_from_body(self):
        request = SuppressionDeleteRequest(domain_id="dom123", ids=["id1"])
        await self.resource.delete_spam_complaints(request)
        body = self.mock_client.request.call_args.kwargs.get("body") or {}
        assert "domain_id" not in body
        assert body.get("ids") == ["id1"]

    async def test_delete_unsubscribes_excludes_domain_id_from_body(self):
        request = SuppressionDeleteRequest(domain_id="dom123", ids=["id1"])
        await self.resource.delete_unsubscribes(request)
        body = self.mock_client.request.call_args.kwargs.get("body") or {}
        assert "domain_id" not in body
        assert body.get("ids") == ["id1"]

    async def test_delete_from_on_hold_excludes_domain_id_from_body(self):
        request = SuppressionDeleteRequest(domain_id="dom123", ids=["id1"])
        await self.resource.delete_from_on_hold(request)
        body = self.mock_client.request.call_args.kwargs.get("body") or {}
        assert "domain_id" not in body
        assert body.get("ids") == ["id1"]

    async def test_delete_from_blocklist_includes_domain_id_in_body(self):
        request = SuppressionDeleteRequest(domain_id="dom123", ids=["id1"])
        await self.resource.delete_from_blocklist(request)
        body = self.mock_client.request.call_args.kwargs.get("body") or {}
        assert body.get("domain_id") == "dom123"
