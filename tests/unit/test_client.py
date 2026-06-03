"""Tests for MailerSendClient initialization and authentication."""

import logging
import os
import pytest
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from mailersend.base_client import _BaseMailerSendClient
from mailersend.client import MailerSendClient
from mailersend.exceptions import (
    AuthenticationError,
    BadRequestError,
    MailerSendError,
    RateLimitExceeded,
    ResourceNotFoundError,
    ServerError,
)


class TestMailerSendClientInitialization:
    """Test client initialization with different authentication methods."""

    def test_client_initialization_with_explicit_api_key(self):
        """Test that client initializes correctly with explicit API key."""
        with patch("mailersend.base_client.get_logger"), patch(
            "mailersend.base_client.RequestLogger"
        ), patch("mailersend.client.requests.Session"):

            client = MailerSendClient(api_key="test-api-key")
            assert client.api_key == "test-api-key"

    def test_client_initialization_with_env_var(self):
        """Test that client reads API key from environment variable."""
        with patch.dict(os.environ, {"MAILERSEND_API_KEY": "env-api-key"}), patch(
            "mailersend.base_client.get_logger"
        ), patch("mailersend.base_client.RequestLogger"), patch(
            "mailersend.client.requests.Session"
        ):

            client = MailerSendClient()
            assert client.api_key == "env-api-key"

    def test_client_initialization_parameter_overrides_env(self):
        """Test that explicit API key parameter overrides environment variable."""
        with patch.dict(os.environ, {"MAILERSEND_API_KEY": "env-api-key"}), patch(
            "mailersend.base_client.get_logger"
        ), patch("mailersend.base_client.RequestLogger"), patch(
            "mailersend.client.requests.Session"
        ):

            client = MailerSendClient(api_key="param-api-key")
            assert client.api_key == "param-api-key"

    def test_client_initialization_fails_without_api_key(self):
        """Test that client initialization fails when no API key is provided."""
        with patch.dict(os.environ, {}, clear=True), patch(
            "mailersend.base_client.get_logger"
        ), patch("mailersend.base_client.RequestLogger"), patch(
            "mailersend.client.requests.Session"
        ):

            with pytest.raises(ValueError) as exc_info:
                MailerSendClient()

            assert "API key is required" in str(exc_info.value)

    def test_client_initialization_fails_with_none_api_key_and_no_env(self):
        """Test that client initialization fails with None API key and no env var."""
        with patch.dict(os.environ, {}, clear=True), patch(
            "mailersend.base_client.get_logger"
        ), patch("mailersend.base_client.RequestLogger"), patch(
            "mailersend.client.requests.Session"
        ):

            with pytest.raises(ValueError) as exc_info:
                MailerSendClient(api_key=None)

            assert "API key is required" in str(exc_info.value)

    def test_client_initialization_with_empty_env_var(self):
        """Test that client handles empty environment variable correctly."""
        with patch.dict(os.environ, {"MAILERSEND_API_KEY": ""}), patch(
            "mailersend.base_client.get_logger"
        ), patch("mailersend.base_client.RequestLogger"), patch(
            "mailersend.client.requests.Session"
        ):

            with pytest.raises(ValueError) as exc_info:
                MailerSendClient()

            assert "API key is required" in str(exc_info.value)

    def test_client_initialization_sets_other_properties(self):
        """Test that client initializes other properties correctly."""
        with patch("mailersend.base_client.get_logger"), patch(
            "mailersend.base_client.RequestLogger"
        ), patch("mailersend.client.requests.Session"):

            client = MailerSendClient(
                api_key="test-key",
                base_url="https://custom.api.com",
                timeout=30,
                max_retries=5,
                debug=True,
            )

            assert client.api_key == "test-key"
            assert client.base_url == "https://custom.api.com/"
            assert client.timeout == 30
            assert client.max_retries == 5
            assert client.debug is True

    def test_base_url_gets_trailing_slash_normalized(self):
        with patch("mailersend.base_client.get_logger"), patch(
            "mailersend.base_client.RequestLogger"
        ), patch("mailersend.client.requests.Session"):
            client = MailerSendClient(api_key="k", base_url="https://api.example.com/v1")
            assert client.base_url == "https://api.example.com/v1/"

    def test_base_url_preserves_existing_trailing_slash(self):
        with patch("mailersend.base_client.get_logger"), patch(
            "mailersend.base_client.RequestLogger"
        ), patch("mailersend.client.requests.Session"):
            client = MailerSendClient(api_key="k", base_url="https://api.example.com/v1/")
            assert client.base_url == "https://api.example.com/v1/"

    def test_is_base_client_subclass(self):
        with patch("mailersend.base_client.get_logger"), patch(
            "mailersend.base_client.RequestLogger"
        ), patch("mailersend.client.requests.Session"):
            client = MailerSendClient(api_key="test-key")
            assert isinstance(client, _BaseMailerSendClient)

    def test_exposes_all_resources(self):
        with patch("mailersend.base_client.get_logger"), patch(
            "mailersend.base_client.RequestLogger"
        ), patch("mailersend.client.requests.Session"):
            client = MailerSendClient(api_key="test-key")
            for attr in [
                "emails", "activities", "analytics", "domains", "identities",
                "inbound", "templates", "tokens", "webhooks", "email_verification",
                "users", "messages", "recipients", "schedules", "sms_messages",
                "smtp_users", "sms_sending", "sms_numbers", "sms_activity",
                "sms_inbounds", "sms_recipients", "sms_webhooks", "api_quota",
                "dmarc_monitoring",
            ]:
                assert hasattr(client, attr), f"missing resource: {attr}"


class TestMailerSendClientRequest:
    def _make_client(self):
        with patch("mailersend.base_client.get_logger"), patch(
            "mailersend.base_client.RequestLogger"
        ), patch("mailersend.client.requests.Session"):
            client = MailerSendClient(api_key="test-key", max_retries=0)
        client.session = MagicMock()
        client.request_logger = MagicMock()
        return client

    def _make_response(self, status_code, json_data=None, headers=None):
        r = MagicMock()
        r.status_code = status_code
        r.headers = headers or {"x-request-id": "req-1"}
        r.json.return_value = json_data or {}
        r.text = ""
        r.content = b"{}"
        return r

    def test_raises_authentication_error_on_401(self):
        client = self._make_client()
        client.session.request.return_value = self._make_response(401, {"message": "Unauthorized"})
        with pytest.raises(AuthenticationError):
            client.request("GET", "some-endpoint")

    def test_raises_not_found_on_404(self):
        client = self._make_client()
        client.session.request.return_value = self._make_response(404, {"message": "Not found"})
        with pytest.raises(ResourceNotFoundError):
            client.request("GET", "some-endpoint")

    def test_raises_rate_limit_on_429(self):
        client = self._make_client()
        r = self._make_response(429, {"message": "Too many requests"})
        r.headers = {"retry-after": "60", "x-apiquota-remaining": "0"}
        client.session.request.return_value = r
        with pytest.raises(RateLimitExceeded):
            client.request("GET", "some-endpoint")

    def test_raises_bad_request_on_400(self):
        client = self._make_client()
        client.session.request.return_value = self._make_response(400, {"message": "Bad request"})
        with pytest.raises(BadRequestError):
            client.request("GET", "some-endpoint")

    def test_raises_server_error_on_500(self):
        client = self._make_client()
        client.session.request.return_value = self._make_response(500, {"message": "Server error"})
        with pytest.raises(ServerError):
            client.request("GET", "some-endpoint")

    def test_raises_mailer_send_error_on_unexpected_status(self):
        client = self._make_client()
        client.session.request.return_value = self._make_response(418, {"message": "Teapot"})
        with pytest.raises(MailerSendError):
            client.request("GET", "some-endpoint")

    def test_successful_request_returns_response(self):
        client = self._make_client()
        client.session.request.return_value = self._make_response(200, {"id": "abc"})
        result = client.request("GET", "some-endpoint")
        assert result.status_code == 200

    def test_network_error_raises_mailer_send_error(self):
        import requests as req_lib
        client = self._make_client()
        client.session.request.side_effect = req_lib.RequestException("timeout")
        with pytest.raises(MailerSendError, match="Request failed"):
            client.request("GET", "some-endpoint")


class TestMailerSendClientDebug:
    def _make_client(self):
        with patch("mailersend.client.requests.Session"):
            return MailerSendClient(api_key="test-key", max_retries=2)

    def test_enable_debug_sets_flag_and_log_level(self):
        client = self._make_client()
        client.disable_debug()
        client.enable_debug()
        assert client.debug is True
        assert client.logger.level == logging.DEBUG

    def test_disable_debug_clears_flag_and_log_level(self):
        client = self._make_client()
        client.enable_debug()
        client.disable_debug()
        assert client.debug is False
        assert client.logger.level == logging.WARNING

    def test_get_debug_info_contains_base_keys(self):
        client = self._make_client()
        info = client.get_debug_info()
        assert info["max_retries"] == 2
        assert "base_url" in info
        assert "timeout" in info
        assert "user_agent" in info
        assert "logger_level" in info

    def test_get_debug_info_contains_session_adapters(self):
        client = self._make_client()
        info = client.get_debug_info()
        assert "session_adapters" in info
        assert isinstance(info["session_adapters"], list)


class TestMailerSendClientContextManager:
    def test_context_manager_closes_session(self):
        with patch("mailersend.base_client.get_logger"), patch(
            "mailersend.base_client.RequestLogger"
        ), patch("mailersend.client.requests.Session"):
            client = MailerSendClient(api_key="test-key")
            client.session = MagicMock()

            with client as c:
                assert c is client

            client.session.close.assert_called_once()
