"""Tests for IdentitiesResource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.identities import IdentitiesResource
from mailersend.models.base import APIResponse
from mailersend.models.identities import (
    IdentityListRequest,
    IdentityListQueryParams,
    IdentityCreateRequest,
    IdentityGetRequest,
    IdentityGetByEmailRequest,
    IdentityUpdateRequest,
    IdentityUpdateByEmailRequest,
    IdentityDeleteRequest,
    IdentityDeleteByEmailRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestIdentitiesResource:
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
        self.resource = IdentitiesResource(self.mock_client)

    async def test_list_identities_returns_api_response(self):
        request = IdentityListRequest(query_params=IdentityListQueryParams())
        result = await resolve(self.resource.list_identities(request))
        assert isinstance(result, APIResponse)

    async def test_list_identities_calls_correct_endpoint(self):
        request = IdentityListRequest(query_params=IdentityListQueryParams())
        await resolve(self.resource.list_identities(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "identities"
        assert call.kwargs["params"] == {"page": 1, "limit": 25}

    async def test_create_identity_returns_api_response(self):
        request = IdentityCreateRequest(
            domain_id="dom123", name="John", email="john@example.com"
        )
        result = await resolve(self.resource.create_identity(request))
        assert isinstance(result, APIResponse)

    async def test_create_identity_calls_correct_endpoint(self):
        request = IdentityCreateRequest(
            domain_id="dom123", name="John", email="john@example.com"
        )
        await resolve(self.resource.create_identity(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "identities"
        assert call.kwargs["body"]["email"] == "john@example.com"

    async def test_get_identity_returns_api_response(self):
        result = await resolve(self.resource.get_identity(
            IdentityGetRequest(identity_id="id123"))
        )
        assert isinstance(result, APIResponse)

    async def test_get_identity_calls_correct_endpoint(self):
        await resolve(self.resource.get_identity(IdentityGetRequest(identity_id="id123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "identities/id123"

    async def test_get_identity_by_email_returns_api_response(self):
        result = await resolve(self.resource.get_identity_by_email(
            IdentityGetByEmailRequest(email="john@example.com"))
        )
        assert isinstance(result, APIResponse)

    async def test_get_identity_by_email_calls_correct_endpoint(self):
        await resolve(self.resource.get_identity_by_email(
            IdentityGetByEmailRequest(email="john@example.com"))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "identities/email/john@example.com"

    async def test_update_identity_returns_api_response(self):
        request = IdentityUpdateRequest(identity_id="id123", name="Updated")
        result = await resolve(self.resource.update_identity(request))
        assert isinstance(result, APIResponse)

    async def test_update_identity_excludes_id_from_body(self):
        request = IdentityUpdateRequest(identity_id="id123", name="Updated")
        await resolve(self.resource.update_identity(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "identities/id123"
        assert "identity_id" not in (call.kwargs.get("body") or {})

    async def test_update_identity_by_email_returns_api_response(self):
        request = IdentityUpdateByEmailRequest(email="john@example.com", name="Updated")
        result = await resolve(self.resource.update_identity_by_email(request))
        assert isinstance(result, APIResponse)

    async def test_update_identity_by_email_excludes_email_from_body(self):
        request = IdentityUpdateByEmailRequest(email="john@example.com", name="Updated")
        await resolve(self.resource.update_identity_by_email(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "identities/email/john@example.com"
        assert "email" not in (call.kwargs.get("body") or {})

    async def test_delete_identity_returns_api_response(self):
        result = await resolve(self.resource.delete_identity(
            IdentityDeleteRequest(identity_id="id123"))
        )
        assert isinstance(result, APIResponse)

    async def test_delete_identity_calls_correct_endpoint(self):
        await resolve(self.resource.delete_identity(IdentityDeleteRequest(identity_id="id123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "identities/id123"

    async def test_delete_identity_by_email_returns_api_response(self):
        result = await resolve(self.resource.delete_identity_by_email(
            IdentityDeleteByEmailRequest(email="john@example.com"))
        )
        assert isinstance(result, APIResponse)

    async def test_delete_identity_by_email_calls_correct_endpoint(self):
        await resolve(self.resource.delete_identity_by_email(
            IdentityDeleteByEmailRequest(email="john@example.com"))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "identities/email/john@example.com"
