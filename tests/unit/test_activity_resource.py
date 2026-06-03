"""Tests for Activity resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.activity import Activity
from mailersend.models.activity import (
    ActivityRequest,
    ActivityQueryParams,
    SingleActivityRequest,
)
from mailersend.models.base import APIResponse



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestActivity:
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
        self.resource = Activity(self.mock_client)

    async def test_get_returns_api_response(self):
        request = ActivityRequest(
            domain_id="domain123",
            query_params=ActivityQueryParams(date_from=1443651141, date_to=1443661141),
        )
        result = await resolve(self.resource.get(request))
        assert isinstance(result, APIResponse)

    async def test_get_calls_correct_endpoint(self):
        request = ActivityRequest(
            domain_id="domain123",
            query_params=ActivityQueryParams(date_from=1443651141, date_to=1443661141),
        )
        await resolve(self.resource.get(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert "activity/domain123" in call.kwargs["path"]

    async def test_get_passes_query_params(self):
        request = ActivityRequest(
            domain_id="domain123",
            query_params=ActivityQueryParams(date_from=1443651141, date_to=1443661141),
        )
        await resolve(self.resource.get(request))
        call = self.mock_client.request.call_args
        assert "params" in call.kwargs
        assert call.kwargs["params"] is not None

    async def test_get_single_returns_api_response(self):
        request = SingleActivityRequest(activity_id="activity123")
        result = await resolve(self.resource.get_single(request))
        assert isinstance(result, APIResponse)

    async def test_get_single_calls_correct_endpoint(self):
        request = SingleActivityRequest(activity_id="activity123")
        await resolve(self.resource.get_single(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "activities/activity123"
