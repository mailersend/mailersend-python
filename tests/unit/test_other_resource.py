"""Tests for Other resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.other import Other
from mailersend.models.base import APIResponse



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestOther:
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
        self.resource = Other(self.mock_client)

    async def test_get_quota_returns_api_response(self):
        result = await resolve(self.resource.get_quota())
        assert isinstance(result, APIResponse)

    async def test_get_quota_calls_correct_endpoint(self):
        await resolve(self.resource.get_quota())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "api-quota"
