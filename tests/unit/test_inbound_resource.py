"""Tests for InboundResource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.inbound import InboundResource
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



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


def _make_filter_group():
    return InboundFilterGroup(type="catch_all")


def _make_forward():
    return InboundForward(type="email", value="forward@example.com")

class TestInboundResource:
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
        self.resource = InboundResource(self.mock_client)

    async def test_list_returns_api_response(self):
        request = InboundListRequest(query_params=InboundListQueryParams())
        result = await resolve(self.resource.list(request))
        assert isinstance(result, APIResponse)

    async def test_list_calls_correct_endpoint(self):
        request = InboundListRequest(query_params=InboundListQueryParams())
        await resolve(self.resource.list(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "inbound"

    async def test_get_returns_api_response(self):
        result = await resolve(self.resource.get(InboundGetRequest(inbound_id="inb123")))
        assert isinstance(result, APIResponse)

    async def test_get_calls_correct_endpoint(self):
        await resolve(self.resource.get(InboundGetRequest(inbound_id="inb123")))
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
        result = await resolve(self.resource.create(request))
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
        await resolve(self.resource.create(request))
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
        result = await resolve(self.resource.update(request))
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
        await resolve(self.resource.update(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "inbound/inb123"

    async def test_delete_returns_api_response(self):
        result = await resolve(self.resource.delete(InboundDeleteRequest(inbound_id="inb123")))
        assert isinstance(result, APIResponse)

    async def test_delete_calls_correct_endpoint(self):
        await resolve(self.resource.delete(InboundDeleteRequest(inbound_id="inb123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "inbound/inb123"
