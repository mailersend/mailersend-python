"""Tests for Domains resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.domains import Domains
from mailersend.models.domains import (
    DomainListRequest,
    DomainListQueryParams,
    DomainCreateRequest,
    DomainGetRequest,
    DomainDeleteRequest,
    DomainUpdateSettingsRequest,
    DomainRecipientsRequest,
    DomainRecipientsQueryParams,
    DomainDnsRecordsRequest,
    DomainVerificationRequest,
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


class TestDomains:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = Domains(self.mock_client)

    async def test_list_domains_returns_api_response(self):
        result = await self.resource.list_domains()
        assert isinstance(result, APIResponse)

    async def test_list_domains_uses_default_params(self):
        await self.resource.list_domains()
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains"
        assert call.kwargs["params"] == {"page": 1, "limit": 25}

    async def test_list_domains_with_custom_params(self):
        request = DomainListRequest(
            query_params=DomainListQueryParams(page=2, limit=50, verified=True)
        )
        await self.resource.list_domains(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["params"]["page"] == 2
        assert call.kwargs["params"]["limit"] == 50

    async def test_get_domain_returns_api_response(self):
        result = await self.resource.get_domain(DomainGetRequest(domain_id="dom123"))
        assert isinstance(result, APIResponse)

    async def test_get_domain_calls_correct_endpoint(self):
        await self.resource.get_domain(DomainGetRequest(domain_id="dom123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains/dom123"

    async def test_create_domain_returns_api_response(self):
        result = await self.resource.create_domain(
            DomainCreateRequest(name="example.com")
        )
        assert isinstance(result, APIResponse)

    async def test_create_domain_calls_correct_endpoint(self):
        await self.resource.create_domain(DomainCreateRequest(name="example.com"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "domains"
        assert call.kwargs["body"]["name"] == "example.com"

    async def test_delete_domain_returns_api_response(self):
        result = await self.resource.delete_domain(
            DomainDeleteRequest(domain_id="dom123")
        )
        assert isinstance(result, APIResponse)

    async def test_delete_domain_calls_correct_endpoint(self):
        await self.resource.delete_domain(DomainDeleteRequest(domain_id="dom123"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "DELETE"
        assert call.kwargs["path"] == "domains/dom123"

    async def test_get_domain_recipients_returns_api_response(self):
        request = DomainRecipientsRequest(
            domain_id="dom123",
            query_params=DomainRecipientsQueryParams(),
        )
        result = await self.resource.get_domain_recipients(request)
        assert isinstance(result, APIResponse)

    async def test_get_domain_recipients_calls_correct_endpoint(self):
        request = DomainRecipientsRequest(
            domain_id="dom123", query_params=DomainRecipientsQueryParams()
        )
        await self.resource.get_domain_recipients(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains/dom123/recipients"

    async def test_update_domain_settings_returns_api_response(self):
        request = DomainUpdateSettingsRequest(domain_id="dom123", track_opens=True)
        result = await self.resource.update_domain_settings(request)
        assert isinstance(result, APIResponse)

    async def test_update_domain_settings_excludes_domain_id_from_body(self):
        request = DomainUpdateSettingsRequest(domain_id="dom123", track_opens=True)
        await self.resource.update_domain_settings(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "PUT"
        assert call.kwargs["path"] == "domains/dom123/settings"
        assert "domain_id" not in call.kwargs["body"]
        assert call.kwargs["body"]["track_opens"] is True

    async def test_get_domain_dns_records_returns_api_response(self):
        result = await self.resource.get_domain_dns_records(
            DomainDnsRecordsRequest(domain_id="dom123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_domain_dns_records_calls_correct_endpoint(self):
        await self.resource.get_domain_dns_records(
            DomainDnsRecordsRequest(domain_id="dom123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains/dom123/dns-records"

    async def test_get_domain_verification_status_returns_api_response(self):
        result = await self.resource.get_domain_verification_status(
            DomainVerificationRequest(domain_id="dom123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_domain_verification_status_calls_correct_endpoint(self):
        await self.resource.get_domain_verification_status(
            DomainVerificationRequest(domain_id="dom123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "domains/dom123/verify"
