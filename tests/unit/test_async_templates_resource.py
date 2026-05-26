"""Tests for Templates resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.templates import Templates
from mailersend.models.base import APIResponse
from mailersend.models.templates import (
    TemplatesListRequest,
    TemplatesListQueryParams,
    TemplateGetRequest,
    TemplateDeleteRequest,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestTemplates:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = Templates(self.mock_client)

    async def test_list_templates_returns_api_response(self):
        result = await self.resource.list_templates()
        assert isinstance(result, APIResponse)

    async def test_list_templates_calls_correct_endpoint(self):
        await self.resource.list_templates()
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "templates"

    async def test_list_templates_with_request(self):
        request = TemplatesListRequest(
            query_params=TemplatesListQueryParams(page=2, limit=10)
        )
        await self.resource.list_templates(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2

    async def test_get_template_returns_api_response(self):
        result = await self.resource.get_template(
            TemplateGetRequest(template_id="tmpl123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_template_calls_correct_endpoint(self):
        await self.resource.get_template(TemplateGetRequest(template_id="tmpl123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "templates/tmpl123"

    async def test_delete_template_returns_api_response(self):
        result = await self.resource.delete_template(
            TemplateDeleteRequest(template_id="tmpl123")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_template_calls_correct_endpoint(self):
        await self.resource.delete_template(
            TemplateDeleteRequest(template_id="tmpl123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "templates/tmpl123"
