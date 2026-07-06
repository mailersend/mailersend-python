"""Tests for Templates resource."""
import inspect

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.resources.templates import Templates
from mailersend.models.base import APIResponse
from mailersend.models.templates import (
    TemplatesListRequest,
    TemplatesListQueryParams,
    TemplateGetRequest,
    TemplateDeleteRequest,
)



async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestTemplates:
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
        self.resource = Templates(self.mock_client)

    async def test_list_templates_returns_api_response(self):
        result = await resolve(self.resource.list_templates())
        assert isinstance(result, APIResponse)

    async def test_list_templates_calls_correct_endpoint(self):
        await resolve(self.resource.list_templates())
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "templates"

    async def test_list_templates_with_request(self):
        request = TemplatesListRequest(
            query_params=TemplatesListQueryParams(page=2, limit=10)
        )
        await resolve(self.resource.list_templates(request))
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2

    async def test_get_template_returns_api_response(self):
        result = await resolve(self.resource.get_template(
            TemplateGetRequest(template_id="tmpl123"))
        )
        assert isinstance(result, APIResponse)

    async def test_get_template_calls_correct_endpoint(self):
        await resolve(self.resource.get_template(TemplateGetRequest(template_id="tmpl123")))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "templates/tmpl123"

    async def test_delete_template_returns_api_response(self):
        result = await resolve(self.resource.delete_template(
            TemplateDeleteRequest(template_id="tmpl123"))
        )
        assert isinstance(result, APIResponse)

    async def test_delete_template_calls_correct_endpoint(self):
        await resolve(self.resource.delete_template(
            TemplateDeleteRequest(template_id="tmpl123"))
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "templates/tmpl123"
