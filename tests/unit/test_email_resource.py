"""Tests for Email resource."""
import inspect

import pytest
from unittest.mock import AsyncMock, MagicMock, Mock

from mailersend.resources.email import Email
from mailersend.models.base import APIResponse
from mailersend.models.email import EmailRequest, EmailContact



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


def _make_mock_response(status_code=200, json_data=None, headers=None):
    response = MagicMock()
    response.status_code = status_code
    response.headers = headers or {"x-request-id": "req-123", "x-message-id": "msg-456"}
    response.json.return_value = json_data or {}
    response.content = b"{}"
    return response


def _make_email_request():
    return EmailRequest(
        from_email=EmailContact(email="sender@example.com", name="Sender"),
        to=[EmailContact(email="recipient@example.com", name="Recipient")],
        subject="Test Subject",
        text="Test body",
    )

class TestEmail:
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
        self.resource = Email(self.mock_client)

    async def test_send_returns_api_response(self):
        self.mock_client.request.return_value = _make_mock_response()
        email = _make_email_request()

        result = await resolve(self.resource.send(email))

        assert isinstance(result, APIResponse)

    async def test_send_calls_correct_endpoint(self):
        self.mock_client.request.return_value = _make_mock_response()
        email = _make_email_request()

        await resolve(self.resource.send(email))

        self.mock_client.request.assert_called_once()
        call_kwargs = self.mock_client.request.call_args
        assert call_kwargs.kwargs["method"] == "POST"
        assert call_kwargs.kwargs["path"] == "email"

    async def test_send_includes_message_id_in_response(self):
        mock_response = _make_mock_response(
            headers={"x-request-id": "req-123", "x-message-id": "msg-789"}
        )
        self.mock_client.request.return_value = mock_response
        email = _make_email_request()

        result = await resolve(self.resource.send(email))

        assert result.data.get("id") == "msg-789"

    async def test_send_bulk_calls_correct_endpoint(self):
        self.mock_client.request.return_value = _make_mock_response()
        emails = [_make_email_request(), _make_email_request()]

        result = await resolve(self.resource.send_bulk(emails))

        assert isinstance(result, APIResponse)
        call_kwargs = self.mock_client.request.call_args
        assert call_kwargs.kwargs["method"] == "POST"
        assert call_kwargs.kwargs["path"] == "bulk-email"
        assert isinstance(call_kwargs.kwargs["body"], list)
        assert len(call_kwargs.kwargs["body"]) == 2

    async def test_get_bulk_status_calls_correct_endpoint(self):
        self.mock_client.request.return_value = _make_mock_response()

        result = await resolve(self.resource.get_bulk_status("bulk-id-123"))

        assert isinstance(result, APIResponse)
        call_kwargs = self.mock_client.request.call_args
        assert call_kwargs.kwargs["method"] == "GET"
        assert "bulk-id-123" in call_kwargs.kwargs["path"]
