"""Tests for Analytics resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.analytics import Analytics
from mailersend.models.analytics import AnalyticsRequest
from mailersend.models.base import APIResponse



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


def _make_request():
    return AnalyticsRequest(
        date_from=1443651141,
        date_to=1443661141,
        tags=["newsletter"],
        event=["sent", "delivered"],
    )

class TestAnalytics:
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
        self.resource = Analytics(self.mock_client)

    async def test_get_activity_by_date_returns_api_response(self):
        result = await resolve(self.resource.get_activity_by_date(_make_request()))
        assert isinstance(result, APIResponse)

    async def test_get_activity_by_date_calls_correct_endpoint(self):
        await resolve(self.resource.get_activity_by_date(_make_request()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "analytics/date"

    async def test_get_activity_by_date_passes_params(self):
        await resolve(self.resource.get_activity_by_date(_make_request()))
        call = self.mock_client.request.call_args
        params = call.kwargs["params"]
        assert "date_from" in params
        assert "date_to" in params

    async def test_get_opens_by_country_returns_api_response(self):
        result = await resolve(self.resource.get_opens_by_country(_make_request()))
        assert isinstance(result, APIResponse)

    async def test_get_opens_by_country_calls_correct_endpoint(self):
        await resolve(self.resource.get_opens_by_country(_make_request()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "analytics/country"

    async def test_get_opens_by_country_excludes_event_and_group_by(self):
        await resolve(self.resource.get_opens_by_country(_make_request()))
        call = self.mock_client.request.call_args
        params = call.kwargs["params"]
        assert "event" not in params
        assert "event[]" not in params
        assert "group_by" not in params

    async def test_get_opens_by_user_agent_returns_api_response(self):
        result = await resolve(self.resource.get_opens_by_user_agent(_make_request()))
        assert isinstance(result, APIResponse)

    async def test_get_opens_by_user_agent_calls_correct_endpoint(self):
        await resolve(self.resource.get_opens_by_user_agent(_make_request()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "analytics/ua-name"

    async def test_get_opens_by_reading_environment_returns_api_response(self):
        result = await resolve(self.resource.get_opens_by_reading_environment(_make_request()))
        assert isinstance(result, APIResponse)

    async def test_get_opens_by_reading_environment_calls_correct_endpoint(self):
        await resolve(self.resource.get_opens_by_reading_environment(_make_request()))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "analytics/ua-type"
