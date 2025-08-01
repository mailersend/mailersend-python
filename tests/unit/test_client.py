"""Tests for MailerSendClient initialization and authentication."""

import os
import pytest
from unittest.mock import patch

from mailersend.client import MailerSendClient


class TestMailerSendClientInitialization:
    """Test client initialization with different authentication methods."""

    def test_client_initialization_with_explicit_api_key(self):
        """Test that client initializes correctly with explicit API key."""
        with patch('mailersend.client.get_logger'), \
             patch('mailersend.client.RequestLogger'), \
             patch('mailersend.client.requests.Session'):
            
            client = MailerSendClient(api_key="test-api-key")
            assert client.api_key == "test-api-key"

    def test_client_initialization_with_env_var(self):
        """Test that client reads API key from environment variable."""
        with patch.dict(os.environ, {'MAILERSEND_API_KEY': 'env-api-key'}), \
             patch('mailersend.client.get_logger'), \
             patch('mailersend.client.RequestLogger'), \
             patch('mailersend.client.requests.Session'):
            
            client = MailerSendClient()
            assert client.api_key == "env-api-key"

    def test_client_initialization_parameter_overrides_env(self):
        """Test that explicit API key parameter overrides environment variable."""
        with patch.dict(os.environ, {'MAILERSEND_API_KEY': 'env-api-key'}), \
             patch('mailersend.client.get_logger'), \
             patch('mailersend.client.RequestLogger'), \
             patch('mailersend.client.requests.Session'):
            
            client = MailerSendClient(api_key="param-api-key")
            assert client.api_key == "param-api-key"

    def test_client_initialization_fails_without_api_key(self):
        """Test that client initialization fails when no API key is provided."""
        with patch.dict(os.environ, {}, clear=True), \
             patch('mailersend.client.get_logger'), \
             patch('mailersend.client.RequestLogger'), \
             patch('mailersend.client.requests.Session'):
            
            with pytest.raises(ValueError) as exc_info:
                MailerSendClient()
            
            assert "API key is required" in str(exc_info.value)

    def test_client_initialization_fails_with_none_api_key_and_no_env(self):
        """Test that client initialization fails with None API key and no env var."""
        with patch.dict(os.environ, {}, clear=True), \
             patch('mailersend.client.get_logger'), \
             patch('mailersend.client.RequestLogger'), \
             patch('mailersend.client.requests.Session'):
            
            with pytest.raises(ValueError) as exc_info:
                MailerSendClient(api_key=None)
            
            assert "API key is required" in str(exc_info.value)

    def test_client_initialization_with_empty_env_var(self):
        """Test that client handles empty environment variable correctly."""
        with patch.dict(os.environ, {'MAILERSEND_API_KEY': ''}), \
             patch('mailersend.client.get_logger'), \
             patch('mailersend.client.RequestLogger'), \
             patch('mailersend.client.requests.Session'):
            
            with pytest.raises(ValueError) as exc_info:
                MailerSendClient()
            
            assert "API key is required" in str(exc_info.value)

    def test_client_initialization_sets_other_properties(self):
        """Test that client initializes other properties correctly."""
        with patch('mailersend.client.get_logger'), \
             patch('mailersend.client.RequestLogger'), \
             patch('mailersend.client.requests.Session'):
            
            client = MailerSendClient(
                api_key="test-key",
                base_url="https://custom.api.com",
                timeout=30,
                max_retries=5,
                debug=True
            )
            
            assert client.api_key == "test-key"
            assert client.base_url == "https://custom.api.com"
            assert client.timeout == 30
            assert client.debug is True