"""Tests for AsyncAnalytics resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.analytics import AsyncAnalytics
from mailersend.models.analytics import AnalyticsRequest
from mailersend.models.base import APIResponse


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


def _make_request():
    return AnalyticsRequest(
        date_from=1443651141,
        date_to=1443661141,
        tags=["newsletter"],
        event=["sent", "delivered"],
    )


class TestAsyncAnalytics:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = AsyncAnalytics(self.mock_client)

    async def test_get_activity_by_date_returns_api_response(self):
        result = await self.resource.get_activity_by_date(_make_request())
        assert isinstance(result, APIResponse)

    async def test_get_activity_by_date_calls_correct_endpoint(self):
        await self.resource.get_activity_by_date(_make_request())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "analytics/date"

    async def test_get_activity_by_date_passes_params(self):
        await self.resource.get_activity_by_date(_make_request())
        call = self.mock_client.request.call_args
        params = call.kwargs["params"]
        assert "date_from" in params
        assert "date_to" in params

    async def test_get_opens_by_country_returns_api_response(self):
        result = await self.resource.get_opens_by_country(_make_request())
        assert isinstance(result, APIResponse)

    async def test_get_opens_by_country_calls_correct_endpoint(self):
        await self.resource.get_opens_by_country(_make_request())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "analytics/country"

    async def test_get_opens_by_country_excludes_event_and_group_by(self):
        await self.resource.get_opens_by_country(_make_request())
        call = self.mock_client.request.call_args
        params = call.kwargs["params"]
        assert "event" not in params
        assert "event[]" not in params
        assert "group_by" not in params

    async def test_get_opens_by_user_agent_returns_api_response(self):
        result = await self.resource.get_opens_by_user_agent(_make_request())
        assert isinstance(result, APIResponse)

    async def test_get_opens_by_user_agent_calls_correct_endpoint(self):
        await self.resource.get_opens_by_user_agent(_make_request())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "analytics/ua-name"

    async def test_get_opens_by_reading_environment_returns_api_response(self):
        result = await self.resource.get_opens_by_reading_environment(_make_request())
        assert isinstance(result, APIResponse)

    async def test_get_opens_by_reading_environment_calls_correct_endpoint(self):
        await self.resource.get_opens_by_reading_environment(_make_request())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "analytics/ua-type"
