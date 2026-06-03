"""Tests for SmtpUsers resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

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



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestSmtpUsers:
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
        self.resource = SmtpUsers(self.mock_client)

    async def test_list_smtp_users_returns_api_response(self):
        request = SmtpUsersListRequest(domain_id="dom123")
        result = await resolve(self.resource.list_smtp_users(request))
        assert isinstance(result, APIResponse)

    async def test_list_smtp_users_calls_correct_endpoint(self):
        request = SmtpUsersListRequest(domain_id="dom123")
        await resolve(self.resource.list_smtp_users(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains/dom123/smtp-users"

    async def test_get_smtp_user_returns_api_response(self):
        request = SmtpUserGetRequest(domain_id="dom123", smtp_user_id="user456")
        result = await resolve(self.resource.get_smtp_user(request))
        assert isinstance(result, APIResponse)

    async def test_get_smtp_user_calls_correct_endpoint(self):
        request = SmtpUserGetRequest(domain_id="dom123", smtp_user_id="user456")
        await resolve(self.resource.get_smtp_user(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains/dom123/smtp-users/user456"

    async def test_create_smtp_user_returns_api_response(self):
        request = SmtpUserCreateRequest(domain_id="dom123", name="My SMTP User")
        result = await resolve(self.resource.create_smtp_user(request))
        assert isinstance(result, APIResponse)

    async def test_create_smtp_user_calls_correct_endpoint(self):
        request = SmtpUserCreateRequest(domain_id="dom123", name="My SMTP User")
        await resolve(self.resource.create_smtp_user(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "domains/dom123/smtp-users"

    async def test_update_smtp_user_returns_api_response(self):
        request = SmtpUserUpdateRequest(
            domain_id="dom123", smtp_user_id="user456", name="Updated"
        )
        result = await resolve(self.resource.update_smtp_user(request))
        assert isinstance(result, APIResponse)

    async def test_update_smtp_user_calls_correct_endpoint(self):
        request = SmtpUserUpdateRequest(
            domain_id="dom123", smtp_user_id="user456", name="Updated"
        )
        await resolve(self.resource.update_smtp_user(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "domains/dom123/smtp-users/user456"

    async def test_delete_smtp_user_returns_api_response(self):
        request = SmtpUserDeleteRequest(domain_id="dom123", smtp_user_id="user456")
        result = await resolve(self.resource.delete_smtp_user(request))
        assert isinstance(result, APIResponse)

    async def test_delete_smtp_user_calls_correct_endpoint(self):
        request = SmtpUserDeleteRequest(domain_id="dom123", smtp_user_id="user456")
        await resolve(self.resource.delete_smtp_user(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "domains/dom123/smtp-users/user456"
