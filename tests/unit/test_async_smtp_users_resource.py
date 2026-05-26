"""Tests for SmtpUsers resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.smtp_users import SmtpUsers
from mailersend.models.base import APIResponse
from mailersend.models.smtp_users import (
    SmtpUsersListRequest,
    SmtpUsersListQueryParams,
    SmtpUserGetRequest,
    SmtpUserCreateRequest,
    SmtpUserUpdateRequest,
    SmtpUserDeleteRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestSmtpUsers:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = SmtpUsers(self.mock_client)

    async def test_list_smtp_users_returns_api_response(self):
        request = SmtpUsersListRequest(domain_id="dom123")
        result = await self.resource.list_smtp_users(request)
        assert isinstance(result, APIResponse)

    async def test_list_smtp_users_calls_correct_endpoint(self):
        request = SmtpUsersListRequest(domain_id="dom123")
        await self.resource.list_smtp_users(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains/dom123/smtp-users"

    async def test_get_smtp_user_returns_api_response(self):
        request = SmtpUserGetRequest(domain_id="dom123", smtp_user_id="user456")
        result = await self.resource.get_smtp_user(request)
        assert isinstance(result, APIResponse)

    async def test_get_smtp_user_calls_correct_endpoint(self):
        request = SmtpUserGetRequest(domain_id="dom123", smtp_user_id="user456")
        await self.resource.get_smtp_user(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains/dom123/smtp-users/user456"

    async def test_create_smtp_user_returns_api_response(self):
        request = SmtpUserCreateRequest(domain_id="dom123", name="My SMTP User")
        result = await self.resource.create_smtp_user(request)
        assert isinstance(result, APIResponse)

    async def test_create_smtp_user_calls_correct_endpoint(self):
        request = SmtpUserCreateRequest(domain_id="dom123", name="My SMTP User")
        await self.resource.create_smtp_user(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "domains/dom123/smtp-users"

    async def test_update_smtp_user_returns_api_response(self):
        request = SmtpUserUpdateRequest(
            domain_id="dom123", smtp_user_id="user456", name="Updated"
        )
        result = await self.resource.update_smtp_user(request)
        assert isinstance(result, APIResponse)

    async def test_update_smtp_user_calls_correct_endpoint(self):
        request = SmtpUserUpdateRequest(
            domain_id="dom123", smtp_user_id="user456", name="Updated"
        )
        await self.resource.update_smtp_user(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "domains/dom123/smtp-users/user456"

    async def test_delete_smtp_user_returns_api_response(self):
        request = SmtpUserDeleteRequest(domain_id="dom123", smtp_user_id="user456")
        result = await self.resource.delete_smtp_user(request)
        assert isinstance(result, APIResponse)

    async def test_delete_smtp_user_calls_correct_endpoint(self):
        request = SmtpUserDeleteRequest(domain_id="dom123", smtp_user_id="user456")
        await self.resource.delete_smtp_user(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "domains/dom123/smtp-users/user456"
