"""Tests for WhatsAppActivities resource."""

import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.whatsapp_activities import WhatsAppActivities
from mailersend.models.base import APIResponse
from mailersend.models.whatsapp_activities import (
    WhatsAppActivitiesListRequest,
    WhatsAppActivitiesListQueryParams,
)


async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestWhatsAppActivities:
    @pytest.fixture(autouse=True, params=["sync", "async"])
    def setup(self, request):
        response = MagicMock(
            status_code=200,
            headers={"x-request-id": "test-req-id"},
            json=MagicMock(return_value={}),
            content=b"{}",
        )
        self.mock_client = MagicMock()
        if request.param == "async":
            self.mock_client.request = AsyncMock(return_value=response)
        else:
            self.mock_client.request = Mock(return_value=response)
        self.resource = WhatsAppActivities(self.mock_client)

    async def test_list_whatsapp_activities_returns_api_response(self):
        result = await resolve(
            self.resource.list_whatsapp_activities(WhatsAppActivitiesListRequest())
        )
        assert isinstance(result, APIResponse)

    async def test_list_whatsapp_activities_calls_correct_endpoint(self):
        await resolve(
            self.resource.list_whatsapp_activities(WhatsAppActivitiesListRequest())
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "whatsapp/activities"
        assert call.kwargs["params"] == {}

    async def test_list_whatsapp_activities_with_query_params(self):
        request = WhatsAppActivitiesListRequest(
            query_params=WhatsAppActivitiesListQueryParams(
                whatsapp_item_id="item-id", type=["delivered", "read"], page=2
            )
        )
        await resolve(self.resource.list_whatsapp_activities(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"] == {
            "whatsapp_item_id": "item-id",
            "type[]": ["delivered", "read"],
            "page": 2,
        }
