"""Tests for EmailVerification resource."""

from unittest.mock import AsyncMock, MagicMock

from mailersend.resources.email_verification import EmailVerification
from mailersend.models.base import APIResponse
from mailersend.models.email_verification import (
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationAsyncStatusRequest,
    EmailVerificationListsRequest,
    EmailVerificationListsQueryParams,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
    EmailVerificationResultsQueryParams,
)


def _make_mock_client():
    client = MagicMock()
    client.request = AsyncMock(
        return_value=MagicMock(
            status_code=200, headers={}, json=MagicMock(return_value={}), content=b"{}"
        )
    )
    return client


class TestEmailVerification:
    def setup_method(self):
        self.mock_client = _make_mock_client()
        self.resource = EmailVerification(self.mock_client)

    async def test_verify_email_returns_api_response(self):
        result = await self.resource.verify_email(
            EmailVerifyRequest(email="test@example.com")
        )
        assert isinstance(result, APIResponse)

    async def test_verify_email_calls_correct_endpoint(self):
        await self.resource.verify_email(EmailVerifyRequest(email="test@example.com"))
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "email-verification/verify"
        assert call.kwargs["body"]["email"] == "test@example.com"

    async def test_verify_email_async_returns_api_response(self):
        result = await self.resource.verify_email_async(
            EmailVerifyAsyncRequest(email="test@example.com")
        )
        assert isinstance(result, APIResponse)

    async def test_verify_email_async_calls_correct_endpoint(self):
        await self.resource.verify_email_async(
            EmailVerifyAsyncRequest(email="test@example.com")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "email-verification/verify-async"

    async def test_get_async_status_returns_api_response(self):
        result = await self.resource.get_async_status(
            EmailVerificationAsyncStatusRequest(email_verification_id="abc123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_async_status_calls_correct_endpoint(self):
        await self.resource.get_async_status(
            EmailVerificationAsyncStatusRequest(email_verification_id="abc123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "email-verification/verify-async/abc123"

    async def test_list_verifications_returns_api_response(self):
        request = EmailVerificationListsRequest(
            query_params=EmailVerificationListsQueryParams()
        )
        result = await self.resource.list_verifications(request)
        assert isinstance(result, APIResponse)

    async def test_list_verifications_calls_correct_endpoint(self):
        request = EmailVerificationListsRequest(
            query_params=EmailVerificationListsQueryParams()
        )
        await self.resource.list_verifications(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "email-verification"
        assert call.kwargs["params"] == {"page": 1, "limit": 25}

    async def test_get_verification_returns_api_response(self):
        result = await self.resource.get_verification(
            EmailVerificationGetRequest(email_verification_id="abc123")
        )
        assert isinstance(result, APIResponse)

    async def test_get_verification_calls_correct_endpoint(self):
        await self.resource.get_verification(
            EmailVerificationGetRequest(email_verification_id="abc123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "email-verification/abc123"

    async def test_create_verification_returns_api_response(self):
        request = EmailVerificationCreateRequest(
            name="Test List", emails=["a@example.com", "b@example.com"]
        )
        result = await self.resource.create_verification(request)
        assert isinstance(result, APIResponse)

    async def test_create_verification_calls_correct_endpoint(self):
        request = EmailVerificationCreateRequest(
            name="Test List", emails=["a@example.com"]
        )
        await self.resource.create_verification(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "POST"
        assert call.kwargs["path"] == "email-verification"
        assert call.kwargs["body"]["name"] == "Test List"

    async def test_verify_list_returns_api_response(self):
        result = await self.resource.verify_list(
            EmailVerificationVerifyRequest(email_verification_id="abc123")
        )
        assert isinstance(result, APIResponse)

    async def test_verify_list_calls_correct_endpoint(self):
        await self.resource.verify_list(
            EmailVerificationVerifyRequest(email_verification_id="abc123")
        )
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "email-verification/abc123/verify"

    async def test_get_results_returns_api_response(self):
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123",
            query_params=EmailVerificationResultsQueryParams(),
        )
        result = await self.resource.get_results(request)
        assert isinstance(result, APIResponse)

    async def test_get_results_calls_correct_endpoint(self):
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123",
            query_params=EmailVerificationResultsQueryParams(),
        )
        await self.resource.get_results(request)
        call = self.mock_client.request.call_args
        assert call.kwargs["method"] == "GET"
        assert call.kwargs["path"] == "email-verification/abc123/results"
