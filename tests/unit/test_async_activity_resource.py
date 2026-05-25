"""Tests for AsyncActivity resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.activity import AsyncActivity
from mailersend.models.activity import (
    ActivityRequest,
    ActivityQueryParams,
    SingleActivityRequest,
)
from mailersend.models.base import APIResponse


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestAsyncActivity:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncActivity(self.mock_client)

    async def test_get_returns_api_response(self):
        request = ActivityRequest(
            domain_id="domain123",
            query_params=ActivityQueryParams(date_from=1443651141, date_to=1443661141),
        )
        result = await self.resource.get(request)
        assert isinstance(result, APIResponse)

    async def test_get_calls_correct_endpoint(self):
        request = ActivityRequest(
            domain_id="domain123",
            query_params=ActivityQueryParams(date_from=1443651141, date_to=1443661141),
        )
        await self.resource.get(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert "activity/domain123" in call.kwargs["path"]

    async def test_get_passes_query_params(self):
        request = ActivityRequest(
            domain_id="domain123",
            query_params=ActivityQueryParams(date_from=1443651141, date_to=1443661141),
        )
        await self.resource.get(request)
        call = self.mock_client.request.call_args
        assert "params" in call.kwargs
        assert call.kwargs["params"] is not None

    async def test_get_single_returns_api_response(self):
        request = SingleActivityRequest(activity_id="activity123")
        result = await self.resource.get_single(request)
        assert isinstance(result, APIResponse)

    async def test_get_single_calls_correct_endpoint(self):
        request = SingleActivityRequest(activity_id="activity123")
        await self.resource.get_single(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "activities/activity123"
