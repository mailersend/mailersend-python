"""Tests for AsyncMailerSendClient initialization and behaviour."""

import os
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from mailersend.async_client import AsyncMailerSendClient
from mailersend.exceptions import (
    AuthenticationError,
    BadRequestError,
    MailerSendError,
    RateLimitExceeded,
    ResourceNotFoundError,
    ServerError,
)


class TestAsyncMailerSendClientInit:
    def test_init_with_explicit_api_key(self):
        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key")
            assert client.api_key == "test-key"

    def test_init_reads_env_var(self):
        with patch.dict(os.environ, {"MAILERSEND_API_KEY": "env-key"}), patch(
            "mailersend.async_client.httpx.AsyncClient"
        ):
            client = AsyncMailerSendClient()
            assert client.api_key == "env-key"

    def test_init_explicit_key_overrides_env(self):
        with patch.dict(os.environ, {"MAILERSEND_API_KEY": "env-key"}), patch(
            "mailersend.async_client.httpx.AsyncClient"
        ):
            client = AsyncMailerSendClient(api_key="param-key")
            assert client.api_key == "param-key"

    def test_init_raises_without_api_key(self):
        with patch.dict(os.environ, {}, clear=True), patch(
            "mailersend.async_client.httpx.AsyncClient"
        ):
            with pytest.raises(ValueError, match="API key is required"):
                AsyncMailerSendClient()

    def test_init_sets_all_properties(self):
        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(
                api_key="test-key",
                base_url="https://custom.api.com/v1/",
                timeout=60,
                max_retries=5,
                debug=True,
            )
            assert client.base_url == "https://custom.api.com/v1/"
            assert client.timeout == 60
            assert client.max_retries == 5
            assert client.debug is True

    def test_init_exposes_all_resources(self):
        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key")
            assert hasattr(client, "emails")
            assert hasattr(client, "domains")
            assert hasattr(client, "activities")
            assert hasattr(client, "analytics")
            assert hasattr(client, "webhooks")
            assert hasattr(client, "templates")
            assert hasattr(client, "recipients")
            assert hasattr(client, "sms_sending")
            assert hasattr(client, "dmarc_monitoring")


class TestAsyncMailerSendClientRequest:
    def _make_mock_response(self, status_code=200, json_data=None, headers=None):
        response = MagicMock()
        response.status_code = status_code
        response.headers = headers or {"x-request-id": "req-123"}
        response.json.return_value = json_data or {}
        response.text = ""
        response.content = b"{}"
        return response

    async def test_successful_get_request(self):
        mock_response = self._make_mock_response(200, {"data": "value"})

        with patch("mailersend.async_client.httpx.AsyncClient") as MockClient:
            mock_http = AsyncMock()
            mock_http.request = AsyncMock(return_value=mock_response)
            MockClient.return_value = mock_http

            client = AsyncMailerSendClient(api_key="test-key")
            client._client = mock_http

            result = await client.request("GET", "some-endpoint")
            assert result.status_code == 200

    async def test_raises_authentication_error_on_401(self):
        mock_response = self._make_mock_response(401, {"message": "Unauthorized"})

        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key")
            client._client = AsyncMock()
            client._client.request = AsyncMock(return_value=mock_response)

            with pytest.raises(AuthenticationError):
                await client.request("GET", "some-endpoint")

    async def test_raises_not_found_on_404(self):
        mock_response = self._make_mock_response(404, {"message": "Not found"})

        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key")
            client._client = AsyncMock()
            client._client.request = AsyncMock(return_value=mock_response)

            with pytest.raises(ResourceNotFoundError):
                await client.request("GET", "some-endpoint")

    async def test_raises_rate_limit_on_429(self):
        mock_response = self._make_mock_response(429, {"message": "Too many requests"})
        mock_response.headers = {"retry-after": "60", "x-apiquota-remaining": "0"}

        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key", max_retries=0)
            client._client = AsyncMock()
            client._client.request = AsyncMock(return_value=mock_response)

            with pytest.raises(RateLimitExceeded):
                await client.request("GET", "some-endpoint")

    async def test_raises_bad_request_on_400(self):
        mock_response = self._make_mock_response(400, {"message": "Bad request"})

        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key")
            client._client = AsyncMock()
            client._client.request = AsyncMock(return_value=mock_response)

            with pytest.raises(BadRequestError):
                await client.request("GET", "some-endpoint")

    async def test_raises_server_error_on_500(self):
        mock_response = self._make_mock_response(500, {"message": "Server error"})

        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key", max_retries=0)
            client._client = AsyncMock()
            client._client.request = AsyncMock(return_value=mock_response)

            with pytest.raises(ServerError):
                await client.request("GET", "some-endpoint")

    async def test_retries_on_500_then_succeeds(self):
        error_response = self._make_mock_response(500, {"message": "Server error"})
        ok_response = self._make_mock_response(200, {"data": "ok"})

        with patch("mailersend.async_client.httpx.AsyncClient"), patch(
            "mailersend.async_client.asyncio.sleep", new_callable=AsyncMock
        ):
            client = AsyncMailerSendClient(api_key="test-key", max_retries=2)
            client._client = AsyncMock()
            client._client.request = AsyncMock(
                side_effect=[error_response, ok_response]
            )

            result = await client.request("GET", "some-endpoint")
            assert result.status_code == 200
            assert client._client.request.call_count == 2

    async def test_exhausting_retries_raises_server_error(self):
        error_response = self._make_mock_response(500, {"message": "Server error"})

        with patch("mailersend.async_client.httpx.AsyncClient"), patch(
            "mailersend.async_client.asyncio.sleep", new_callable=AsyncMock
        ):
            client = AsyncMailerSendClient(api_key="test-key", max_retries=2)
            client._client = AsyncMock()
            client._client.request = AsyncMock(return_value=error_response)

            with pytest.raises(ServerError):
                await client.request("GET", "some-endpoint")

            assert client._client.request.call_count == 3  # initial + 2 retries

    async def test_retry_uses_backoff_delay(self):
        error_response = self._make_mock_response(500, {"message": "Server error"})
        ok_response = self._make_mock_response(200, {})

        with patch("mailersend.async_client.httpx.AsyncClient"), patch(
            "mailersend.async_client.asyncio.sleep", new_callable=AsyncMock
        ) as mock_sleep:
            client = AsyncMailerSendClient(api_key="test-key", max_retries=2)
            client._client = AsyncMock()
            client._client.request = AsyncMock(
                side_effect=[error_response, error_response, ok_response]
            )

            await client.request("GET", "some-endpoint")

            assert mock_sleep.call_count == 2
            assert mock_sleep.call_args_list[0].args[0] == pytest.approx(
                0.3
            )  # 0.3 * 2^0
            assert mock_sleep.call_args_list[1].args[0] == pytest.approx(
                0.6
            )  # 0.3 * 2^1

    async def test_429_retry_uses_retry_after_header(self):
        rate_limit_response = self._make_mock_response(
            429, {"message": "Too many requests"}
        )
        rate_limit_response.headers = {"retry-after": "30", "x-apiquota-remaining": "0"}
        ok_response = self._make_mock_response(200, {})

        with patch("mailersend.async_client.httpx.AsyncClient"), patch(
            "mailersend.async_client.asyncio.sleep", new_callable=AsyncMock
        ) as mock_sleep:
            client = AsyncMailerSendClient(api_key="test-key", max_retries=1)
            client._client = AsyncMock()
            client._client.request = AsyncMock(
                side_effect=[rate_limit_response, ok_response]
            )

            await client.request("GET", "some-endpoint")

            mock_sleep.assert_called_once_with(30.0)

    async def test_429_retry_falls_back_to_backoff_without_retry_after(self):
        rate_limit_response = self._make_mock_response(
            429, {"message": "Too many requests"}
        )
        rate_limit_response.headers = {}
        ok_response = self._make_mock_response(200, {})

        with patch("mailersend.async_client.httpx.AsyncClient"), patch(
            "mailersend.async_client.asyncio.sleep", new_callable=AsyncMock
        ) as mock_sleep:
            client = AsyncMailerSendClient(api_key="test-key", max_retries=1)
            client._client = AsyncMock()
            client._client.request = AsyncMock(
                side_effect=[rate_limit_response, ok_response]
            )

            await client.request("GET", "some-endpoint")

            mock_sleep.assert_called_once_with(pytest.approx(0.3))

    async def test_raises_mailer_send_error_on_unexpected_status(self):
        mock_response = self._make_mock_response(418, {"message": "I'm a teapot"})

        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key")
            client._client = AsyncMock()
            client._client.request = AsyncMock(return_value=mock_response)

            with pytest.raises(MailerSendError):
                await client.request("GET", "some-endpoint")

    async def test_retries_on_network_error_then_succeeds(self):
        ok_response = self._make_mock_response(200, {"data": "ok"})

        with patch("mailersend.async_client.httpx.AsyncClient"), patch(
            "mailersend.async_client.asyncio.sleep", new_callable=AsyncMock
        ):
            client = AsyncMailerSendClient(api_key="test-key", max_retries=2)
            client._client = AsyncMock()
            client._client.request = AsyncMock(
                side_effect=[httpx.ConnectError("Connection refused"), ok_response]
            )

            result = await client.request("GET", "some-endpoint")
            assert result.status_code == 200
            assert client._client.request.call_count == 2

    async def test_exhausting_retries_on_network_error_raises(self):
        with patch("mailersend.async_client.httpx.AsyncClient"), patch(
            "mailersend.async_client.asyncio.sleep", new_callable=AsyncMock
        ):
            client = AsyncMailerSendClient(api_key="test-key", max_retries=2)
            client._client = AsyncMock()
            client._client.request = AsyncMock(
                side_effect=httpx.ConnectError("Connection refused")
            )

            with pytest.raises(MailerSendError, match="Request failed"):
                await client.request("GET", "some-endpoint")

            assert client._client.request.call_count == 3


class TestAsyncMailerSendClientContextManager:
    async def test_context_manager_calls_close(self):
        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key")
            client._client = AsyncMock()
            client._client.aclose = AsyncMock()

            async with client as c:
                assert c is client

            client._client.aclose.assert_called_once()

    async def test_close_method(self):
        with patch("mailersend.async_client.httpx.AsyncClient"):
            client = AsyncMailerSendClient(api_key="test-key")
            client._client = AsyncMock()
            client._client.aclose = AsyncMock()

            await client.close()
            client._client.aclose.assert_called_once()
