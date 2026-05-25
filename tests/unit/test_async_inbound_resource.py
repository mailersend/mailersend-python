"""Tests for AsyncInboundResource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.inbound import AsyncInboundResource
from mailersend.models.base import APIResponse
from mailersend.models.inbound import (
    InboundListRequest,
    InboundListQueryParams,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
    InboundFilterGroup,
    InboundForward,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


def _make_filter_group():
    return InboundFilterGroup(type="catch_all")


def _make_forward():
    return InboundForward(type="email", value="forward@example.com")


class TestAsyncInboundResource:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncInboundResource(self.mock_client)

    async def test_list_returns_api_response(self):
        request = InboundListRequest(query_params=InboundListQueryParams())
        result = await self.resource.list(request)
        assert isinstance(result, APIResponse)

    async def test_list_calls_correct_endpoint(self):
        request = InboundListRequest(query_params=InboundListQueryParams())
        await self.resource.list(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "inbound"

    async def test_get_returns_api_response(self):
        result = await self.resource.get(InboundGetRequest(inbound_id="inb123"))
        assert isinstance(result, APIResponse)

    async def test_get_calls_correct_endpoint(self):
        await self.resource.get(InboundGetRequest(inbound_id="inb123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "inbound/inb123"

    async def test_create_returns_api_response(self):
        request = InboundCreateRequest(
            domain_id="dom123",
            name="Test Route",
            domain_enabled=False,
            catch_filter=_make_filter_group(),
            match_filter=_make_filter_group(),
            forwards=[_make_forward()],
        )
        result = await self.resource.create(request)
        assert isinstance(result, APIResponse)

    async def test_create_calls_correct_endpoint(self):
        request = InboundCreateRequest(
            domain_id="dom123",
            name="Test Route",
            domain_enabled=False,
            catch_filter=_make_filter_group(),
            match_filter=_make_filter_group(),
            forwards=[_make_forward()],
        )
        await self.resource.create(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "inbound"

    async def test_update_returns_api_response(self):
        request = InboundUpdateRequest(
            inbound_id="inb123",
            name="Updated Route",
            domain_enabled=False,
            catch_filter=_make_filter_group(),
            match_filter=_make_filter_group(),
            forwards=[_make_forward()],
        )
        result = await self.resource.update(request)
        assert isinstance(result, APIResponse)

    async def test_update_calls_correct_endpoint(self):
        request = InboundUpdateRequest(
            inbound_id="inb123",
            name="Updated Route",
            domain_enabled=False,
            catch_filter=_make_filter_group(),
            match_filter=_make_filter_group(),
            forwards=[_make_forward()],
        )
        await self.resource.update(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "inbound/inb123"

    async def test_delete_returns_api_response(self):
        result = await self.resource.delete(InboundDeleteRequest(inbound_id="inb123"))
        assert isinstance(result, APIResponse)

    async def test_delete_calls_correct_endpoint(self):
        await self.resource.delete(InboundDeleteRequest(inbound_id="inb123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "inbound/inb123"
