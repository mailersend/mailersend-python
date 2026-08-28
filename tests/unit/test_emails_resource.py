"""Tests for the emails list and get requests on the Email resource."""

import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.email import Email
from mailersend.builders.email import EmailsBuilder
from mailersend.models.email import (
    EmailsListRequest,
    EmailsListQueryParams,
    EmailGetRequest,
)
from mailersend.models.base import APIResponse


async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


# Measured response for a populated page of GET /v1/emails
EMAILS_LIST_RESPONSE = {
    "data": [
        {
            "id": "6a8fa9b1902fab56e0ce50dd",
            "from": "sender@example.com",
            "to": "rcpt@example.org",
            "subject": "Welcome",
            "text": None,
            "html": None,
            "template_id": "7nxe3yjmeq28vp0k",
            "domain_id": "7nxe3yjmeq28vp0k",
            "message_id": "6a8fa9b1902fab56e0ce50aa",
            "status": "sent",
            "tags": ["newsletter"],
            "interaction": ["opened"],
            "suppression_reason": None,
            "created_at": "2026-08-27T16:48:42.000000Z",
            "updated_at": "2026-08-27T16:48:42.000000Z",
            "headers": [{"name": "X-Custom", "value": "foo"}],
        }
    ],
    "links": {
        "first": "https://api.mailersend.com/v1/emails?page=1",
        "last": None,
        "prev": None,
        "next": None,
    },
    "meta": {
        "current_page": 1,
        "current_page_url": "https://api.mailersend.com/v1/emails?page=1",
        "from": 1,
        "path": "https://api.mailersend.com/v1/emails",
        "per_page": 10,
        "to": 3,
    },
}

# Measured response for an empty page of GET /v1/emails
EMAILS_LIST_EMPTY_RESPONSE = {
    "data": [],
    "links": {
        "first": "https://api.mailersend.com/v1/emails?page=1",
        "last": None,
        "prev": "https://api.mailersend.com/v1/emails?page=1",
        "next": None,
    },
    "meta": {
        "current_page": 2,
        "current_page_url": "https://api.mailersend.com/v1/emails?page=2",
        "from": None,
        "path": "https://api.mailersend.com/v1/emails",
        "per_page": 10,
        "to": None,
    },
}


def _make_mock_response(json_data=None):
    response = MagicMock()
    response.status_code = 200
    response.headers = {"x-request-id": "test-req-id"}
    response.json.return_value = json_data if json_data is not None else {}
    response.content = b"{}"
    return response


def _list_request(**overrides):
    params = {
        "domain_id": "7nxe3yjmeq28vp0k",
        "date_from": 1672574400,
        "date_to": 1672660800,
    }
    params.update(overrides)
    return EmailsListRequest(query_params=EmailsListQueryParams(**params))


class TestEmailsListAndGet:
    @pytest.fixture(autouse=True, params=["sync", "async"])
    def setup(self, request):
        if request.param == "async":
            self.mock_client = MagicMock()
            self.mock_client.request = AsyncMock(return_value=_make_mock_response())
        else:
            self.mock_client = MagicMock()
            self.mock_client.request = Mock(return_value=_make_mock_response())
        self.resource = Email(self.mock_client)

    async def test_list_returns_api_response(self):
        result = await resolve(self.resource.list(_list_request()))
        assert isinstance(result, APIResponse)

    async def test_list_calls_correct_endpoint(self):
        await resolve(self.resource.list(_list_request()))

        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "emails"

    async def test_list_passes_query_params(self):
        await resolve(self.resource.list(_list_request(page=2, limit=50)))

        call = self.mock_client.request.call_args
        assert call.kwargs["params"] == {
            "domain_id": "7nxe3yjmeq28vp0k",
            "date_from": 1672574400,
            "date_to": 1672660800,
            "page": 2,
            "limit": 50,
        }

    async def test_list_sends_status_as_indexed_array_params(self):
        """The API rejects a scalar `status` with a 422, so the resource must
        send status[0], status[1], ... instead of a comma-joined value."""
        request = _list_request(status=["sent", "delivered"], interaction=["opened"])

        await resolve(self.resource.list(request))

        params = self.mock_client.request.call_args.kwargs["params"]
        assert params["status[0]"] == "sent"
        assert params["status[1]"] == "delivered"
        assert params["interaction[0]"] == "opened"
        assert "status" not in params
        assert "interaction" not in params

    async def test_list_sends_builder_query_params(self):
        request = (
            EmailsBuilder()
            .domain_id("7nxe3yjmeq28vp0k")
            .date_from(1672574400)
            .date_to(1672660800)
            .status("sent")
            .add_status("delivered")
            .interaction("opened")
            .build_list_request()
        )

        await resolve(self.resource.list(request))

        params = self.mock_client.request.call_args.kwargs["params"]
        assert params == {
            "domain_id": "7nxe3yjmeq28vp0k",
            "date_from": 1672574400,
            "date_to": 1672660800,
            "status[0]": "sent",
            "status[1]": "delivered",
            "interaction[0]": "opened",
        }

    async def test_list_surfaces_measured_page(self):
        self.mock_client.request.return_value = _make_mock_response(
            EMAILS_LIST_RESPONSE
        )

        result = await resolve(self.resource.list(_list_request()))

        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "6a8fa9b1902fab56e0ce50dd"
        assert result["data"][0]["from"] == "sender@example.com"
        assert result["links"]["next"] is None
        assert result["meta"]["current_page"] == 1
        assert result["meta"]["per_page"] == 10

    async def test_list_surfaces_measured_empty_page(self):
        self.mock_client.request.return_value = _make_mock_response(
            EMAILS_LIST_EMPTY_RESPONSE
        )

        result = await resolve(self.resource.list(_list_request(page=2)))

        assert result["data"] == []
        assert result["links"]["prev"] is not None
        assert result["links"]["next"] is None
        assert result["meta"]["from"] is None
        assert result["meta"]["to"] is None

    async def test_get_returns_api_response(self):
        result = await resolve(self.resource.get(EmailGetRequest(email_id="email123")))
        assert isinstance(result, APIResponse)

    async def test_get_calls_singular_email_endpoint(self):
        await resolve(self.resource.get(EmailGetRequest(email_id="email123")))

        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "email/email123"

    async def test_get_accepts_a_bare_id_string(self):
        result = await resolve(self.resource.get("email123"))

        assert isinstance(result, APIResponse)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "email/email123"

    async def test_get_strips_whitespace_from_a_bare_id_string(self):
        await resolve(self.resource.get("  email123  "))

        call = self.mock_client.request.call_args
        assert call.kwargs["path"] == "email/email123"

    async def test_get_accepts_a_built_request(self):
        request = EmailsBuilder().email_id("email123").build_get_request()

        await resolve(self.resource.get(request))

        call = self.mock_client.request.call_args
        assert call.kwargs["path"] == "email/email123"

    async def test_get_sends_no_query_params(self):
        await resolve(self.resource.get("email123"))

        assert "params" not in self.mock_client.request.call_args.kwargs

    async def test_get_surfaces_activity_events(self):
        payload = {
            "data": {
                **EMAILS_LIST_RESPONSE["data"][0],
                "recipient": {
                    "id": "6a8fa9b1902fab56e0ce50cc",
                    "email": "rcpt@example.org",
                    "created_at": "2026-08-27T16:48:42.000000Z",
                    "updated_at": "2026-08-27T16:48:42.000000Z",
                },
                "activity": [
                    {
                        "id": "6a8fa9b1902fab56e0ce50e1",
                        "type": "queued",
                        "created_at": "2026-08-27T16:48:42.000000Z",
                    },
                    {
                        "id": "6a8fa9b1902fab56e0ce50e2",
                        "type": "sent",
                        "created_at": "2026-08-27T16:48:43.000000Z",
                    },
                ],
            }
        }
        self.mock_client.request.return_value = _make_mock_response(payload)

        result = await resolve(self.resource.get("email123"))

        assert result["data"]["recipient"]["email"] == "rcpt@example.org"
        assert [event["type"] for event in result["data"]["activity"]] == [
            "queued",
            "sent",
        ]
