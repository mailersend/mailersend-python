"""Tests for Users resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.users import Users
from mailersend.models.base import APIResponse
from mailersend.models.users import (
    UsersListRequest,
    UsersListQueryParams,
    UserGetRequest,
    UserInviteRequest,
    UserUpdateRequest,
    UserDeleteRequest,
    InvitesListRequest,
    InvitesListQueryParams,
    InviteGetRequest,
    InviteResendRequest,
    InviteCancelRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestUsers:
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
        self.resource = Users(self.mock_client)

    async def test_list_users_returns_api_response(self):
        result = await resolve(self.resource.list_users(UsersListRequest()))
        assert isinstance(result, APIResponse)

    async def test_list_users_calls_correct_endpoint(self):
        await resolve(self.resource.list_users(UsersListRequest()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "users"

    async def test_get_user_returns_api_response(self):
        result = await resolve(self.resource.get_user(UserGetRequest(user_id="usr123")))
        assert isinstance(result, APIResponse)

    async def test_get_user_calls_correct_endpoint(self):
        await resolve(self.resource.get_user(UserGetRequest(user_id="usr123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "users/usr123"

    async def test_invite_user_returns_api_response(self):
        request = UserInviteRequest(email="newuser@example.com", role="admin")
        result = await resolve(self.resource.invite_user(request))
        assert isinstance(result, APIResponse)

    async def test_invite_user_calls_correct_endpoint(self):
        request = UserInviteRequest(email="newuser@example.com", role="admin")
        await resolve(self.resource.invite_user(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "users"

    async def test_update_user_returns_api_response(self):
        request = UserUpdateRequest(user_id="usr123", role="viewer")
        result = await resolve(self.resource.update_user(request))
        assert isinstance(result, APIResponse)

    async def test_update_user_calls_correct_endpoint(self):
        request = UserUpdateRequest(user_id="usr123", role="viewer")
        await resolve(self.resource.update_user(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "users/usr123"

    async def test_delete_user_returns_api_response(self):
        result = await resolve(self.resource.delete_user(UserDeleteRequest(user_id="usr123")))
        assert isinstance(result, APIResponse)

    async def test_delete_user_calls_correct_endpoint(self):
        await resolve(self.resource.delete_user(UserDeleteRequest(user_id="usr123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "users/usr123"

    async def test_list_invites_returns_api_response(self):
        result = await resolve(self.resource.list_invites(InvitesListRequest()))
        assert isinstance(result, APIResponse)

    async def test_list_invites_calls_correct_endpoint(self):
        await resolve(self.resource.list_invites(InvitesListRequest()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "invites"

    async def test_get_invite_returns_api_response(self):
        result = await resolve(self.resource.get_invite(InviteGetRequest(invite_id="inv123")))
        assert isinstance(result, APIResponse)

    async def test_get_invite_calls_correct_endpoint(self):
        await resolve(self.resource.get_invite(InviteGetRequest(invite_id="inv123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "invites/inv123"

    async def test_resend_invite_returns_api_response(self):
        result = await resolve(self.resource.resend_invite(
            InviteResendRequest(invite_id="inv123"))
        )
        assert isinstance(result, APIResponse)

    async def test_resend_invite_calls_correct_endpoint(self):
        await resolve(self.resource.resend_invite(InviteResendRequest(invite_id="inv123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "invites/inv123/resend"

    async def test_cancel_invite_returns_api_response(self):
        result = await resolve(self.resource.cancel_invite(
            InviteCancelRequest(invite_id="inv123"))
        )
        assert isinstance(result, APIResponse)

    async def test_cancel_invite_calls_correct_endpoint(self):
        await resolve(self.resource.cancel_invite(InviteCancelRequest(invite_id="inv123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "invites/inv123"
