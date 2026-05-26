"""Tests for Other resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.other import Other
from mailersend.models.base import APIResponse


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestOther:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = Other(self.mock_client)

    async def test_get_quota_returns_api_response(self):
        result = await self.resource.get_quota()
        assert isinstance(result, APIResponse)

    async def test_get_quota_calls_correct_endpoint(self):
        await self.resource.get_quota()
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "api-quota"
