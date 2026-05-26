"""Tests for IdentitiesResource."""

from unittest.mock import AsyncMock, MagicMock

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


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestIdentitiesResource:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = IdentitiesResource(self.mock_client)

    async def test_list_identities_returns_api_response(self):
        request = IdentityListRequest(query_params=IdentityListQueryParams())
        result = await self.resource.list_identities(request)
        assert isinstance(result, APIResponse)

    async def test_list_identities_calls_correct_endpoint(self):
        request = IdentityListRequest(query_params=IdentityListQueryParams())
        await self.resource.list_identities(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "identities"
        assert call.kwargs["params"] == {"page": 1, "limit": 25}

    async def test_create_identity_returns_api_response(self):
        request = IdentityCreateRequest(
            domain_id="dom123", name="John", email="john@example.com"
        )
        result = await self.resource.create_identity(request)
        assert isinstance(result, APIResponse)

    async def test_create_identity_calls_correct_endpoint(self):
        request = IdentityCreateRequest(
            domain_id="dom123", name="John", email="john@example.com"
        )
        await self.resource.create_identity(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "identities"
        assert call.kwargs["body"]["email"] == "john@example.com"

    async def test_get_identity_returns_api_response(self):
        result = await self.resource.get_identity(
            IdentityGetRequest(identity_id="id123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_identity_calls_correct_endpoint(self):
        await self.resource.get_identity(IdentityGetRequest(identity_id="id123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "identities/id123"

    async def test_get_identity_by_email_returns_api_response(self):
        result = await self.resource.get_identity_by_email(
            IdentityGetByEmailRequest(email="john@example.com")
        )
        assert isinstance(result, APIResponse)

    async def test_get_identity_by_email_calls_correct_endpoint(self):
        await self.resource.get_identity_by_email(
            IdentityGetByEmailRequest(email="john@example.com")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "identities/email/john@example.com"

    async def test_update_identity_returns_api_response(self):
        request = IdentityUpdateRequest(identity_id="id123", name="Updated")
        result = await self.resource.update_identity(request)
        assert isinstance(result, APIResponse)

    async def test_update_identity_excludes_id_from_body(self):
        request = IdentityUpdateRequest(identity_id="id123", name="Updated")
        await self.resource.update_identity(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "identities/id123"
        assert "identity_id" not in (call.kwargs.get("body") or {})

    async def test_update_identity_by_email_returns_api_response(self):
        request = IdentityUpdateByEmailRequest(email="john@example.com", name="Updated")
        result = await self.resource.update_identity_by_email(request)
        assert isinstance(result, APIResponse)

    async def test_update_identity_by_email_excludes_email_from_body(self):
        request = IdentityUpdateByEmailRequest(email="john@example.com", name="Updated")
        await self.resource.update_identity_by_email(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "identities/email/john@example.com"
        assert "email" not in (call.kwargs.get("body") or {})

    async def test_delete_identity_returns_api_response(self):
        result = await self.resource.delete_identity(
            IdentityDeleteRequest(identity_id="id123")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_identity_calls_correct_endpoint(self):
        await self.resource.delete_identity(IdentityDeleteRequest(identity_id="id123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "identities/id123"

    async def test_delete_identity_by_email_returns_api_response(self):
        result = await self.resource.delete_identity_by_email(
            IdentityDeleteByEmailRequest(email="john@example.com")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_identity_by_email_calls_correct_endpoint(self):
        await self.resource.delete_identity_by_email(
            IdentityDeleteByEmailRequest(email="john@example.com")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "identities/email/john@example.com"
