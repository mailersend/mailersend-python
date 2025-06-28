"""Tests for Webhooks resource."""

from unittest.mock import Mock, patch

import pytest

from mailersend.models.base import APIResponse
from mailersend.models.webhooks import (
    WebhooksListQueryParams,
    WebhooksListRequest,
    WebhookGetRequest,
    WebhookCreateRequest,
    WebhookUpdateRequest,
    WebhookDeleteRequest,
    WebhooksListResponse,
    WebhookResponse,
)
from mailersend.resources.webhooks import Webhooks
from mailersend.exceptions import ValidationError


class TestWebhooks:
    """Test Webhooks resource class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
    
    def _create_mock_response(self, json_data, status_code=200, headers=None):
        """Helper to create mock response objects."""
        mock_response = Mock()
        mock_response.json.return_value = json_data
        mock_response.status_code = status_code
        mock_response.headers = headers or {}
        mock_response.request = Mock()
        mock_response.request.url = "https://api.mailersend.com/v1/webhooks"
        mock_response.request.method = "GET"
        return mock_response


class TestWebhooksListWebhooks:
    """Test list_webhooks method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
    
    def _create_mock_response(self, json_data, status_code=200, headers=None):
        """Helper to create mock response objects."""
        mock_response = Mock()
        mock_response.json.return_value = json_data
        mock_response.status_code = status_code
        mock_response.headers = headers or {}
        mock_response.request = Mock()
        mock_response.request.url = "https://api.mailersend.com/v1/webhooks"
        mock_response.request.method = "GET"
        return mock_response
    
    def test_list_webhooks_success(self):
        """Test successful webhook listing."""
        # Setup
        json_data = {
            "data": [
                {
                    "id": "webhook_123",
                    "url": "https://example.com/webhook",
                    "name": "Test Webhook",
                    "events": ["activity.sent"],
                    "enabled": True,
                    "domain_id": "domain_123",
                    "created_at": "2023-01-01T12:00:00Z",
                    "updated_at": "2023-01-02T12:00:00Z"
                }
            ]
        }
        mock_response = self._create_mock_response(json_data)
        self.client.request.return_value = mock_response
        
        query_params = WebhooksListQueryParams(domain_id="test_domain")
        request = WebhooksListRequest(query_params=query_params)
        
        # Test
        result = self.webhooks.list_webhooks(request)
        
        # Assertions
        self.client.request.assert_called_once_with(
            "GET",
            "webhooks",
            params={"domain_id": "test_domain"}
        )
        assert isinstance(result, APIResponse)
        assert isinstance(result.data, WebhooksListResponse)
        assert len(result.data.data) == 1
        assert result.data.data[0].id == "webhook_123"
    
    def test_list_webhooks_requires_request(self):
        """Test that list_webhooks requires a request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.list_webhooks(None)
        
        assert "WebhooksListRequest must be provided" in str(exc_info.value)
        self.client.request.assert_not_called()
    
    def test_list_webhooks_validates_request_type(self):
        """Test that list_webhooks validates request type."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.list_webhooks("invalid-request")
        
        assert "request must be a WebhooksListRequest instance" in str(exc_info.value)
        self.client.request.assert_not_called()


class TestWebhooksGetWebhook:
    """Test get_webhook method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
    
    def _create_mock_response(self, json_data, status_code=200, headers=None):
        """Helper to create mock response objects."""
        mock_response = Mock()
        mock_response.json.return_value = json_data
        mock_response.status_code = status_code
        mock_response.headers = headers or {}
        mock_response.request = Mock()
        mock_response.request.url = "https://api.mailersend.com/v1/webhooks/webhook_123"
        mock_response.request.method = "GET"
        return mock_response
    
    def test_get_webhook_success(self):
        """Test successful webhook retrieval."""
        # Setup
        json_data = {
            "data": {
                "id": "webhook_123",
                "url": "https://example.com/webhook",
                "name": "Test Webhook",
                "events": ["activity.sent"],
                "enabled": True,
                "domain_id": "domain_123",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
        mock_response = self._create_mock_response(json_data)
        self.client.request.return_value = mock_response
        
        request = WebhookGetRequest(webhook_id="webhook_123")
        
        # Test
        result = self.webhooks.get_webhook(request)
        
        # Assertions
        self.client.request.assert_called_once_with("GET", "webhooks/webhook_123")
        assert isinstance(result, APIResponse)
        assert isinstance(result.data, WebhookResponse)
        assert result.data.data.id == "webhook_123"
        assert result.data.data.name == "Test Webhook"
    
    def test_get_webhook_requires_request(self):
        """Test that get_webhook requires a request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.get_webhook(None)
        
        assert "WebhookGetRequest must be provided" in str(exc_info.value)
        self.client.request.assert_not_called()
    
    def test_get_webhook_validates_request_type(self):
        """Test that get_webhook validates request type."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.get_webhook("invalid-request")
        
        assert "request must be a WebhookGetRequest instance" in str(exc_info.value)
        self.client.request.assert_not_called()


class TestWebhooksCreateWebhook:
    """Test create_webhook method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
    
    def _create_mock_response(self, json_data, status_code=201, headers=None):
        """Helper to create mock response objects."""
        mock_response = Mock()
        mock_response.json.return_value = json_data
        mock_response.status_code = status_code
        mock_response.headers = headers or {}
        mock_response.request = Mock()
        mock_response.request.url = "https://api.mailersend.com/v1/webhooks"
        mock_response.request.method = "POST"
        return mock_response
    
    def test_create_webhook_success(self):
        """Test successful webhook creation."""
        # Setup
        json_data = {
            "data": {
                "id": "webhook_123",
                "url": "https://example.com/webhook",
                "name": "Test Webhook",
                "events": ["activity.sent", "activity.delivered"],
                "enabled": True,
                "domain_id": "test_domain",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        }
        mock_response = self._create_mock_response(json_data)
        self.client.request.return_value = mock_response
        
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent", "activity.delivered"],
            domain_id="test_domain",
            enabled=True
        )
        
        # Test
        result = self.webhooks.create_webhook(request)
        
        # Assertions
        expected_data = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["activity.sent", "activity.delivered"],
            "domain_id": "test_domain",
            "enabled": True
        }
        self.client.request.assert_called_once_with("POST", "webhooks", json=expected_data)
        assert isinstance(result, APIResponse)
        assert isinstance(result.data, WebhookResponse)
        assert result.data.data.id == "webhook_123"
        assert result.data.data.name == "Test Webhook"
    
    def test_create_webhook_without_enabled(self):
        """Test webhook creation without enabled field."""
        # Setup
        json_data = {
            "data": {
                "id": "webhook_123",
                "url": "https://example.com/webhook",
                "name": "Test Webhook",
                "events": ["activity.sent"],
                "enabled": False,
                "domain_id": "test_domain",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        }
        mock_response = self._create_mock_response(json_data)
        self.client.request.return_value = mock_response
        
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="test_domain"
        )
        
        # Test
        result = self.webhooks.create_webhook(request)
        
        # Assertions
        expected_data = {
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "events": ["activity.sent"],
            "domain_id": "test_domain"
        }
        self.client.request.assert_called_once_with("POST", "webhooks", json=expected_data)
        assert isinstance(result, APIResponse)
        assert isinstance(result.data, WebhookResponse)
    
    def test_create_webhook_requires_request(self):
        """Test that create_webhook requires a request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.create_webhook(None)
        
        assert "WebhookCreateRequest must be provided" in str(exc_info.value)
        self.client.request.assert_not_called()
    
    def test_create_webhook_validates_request_type(self):
        """Test that create_webhook validates request type."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.create_webhook("invalid-request")
        
        assert "request must be a WebhookCreateRequest instance" in str(exc_info.value)
        self.client.request.assert_not_called()


class TestWebhooksUpdateWebhook:
    """Test update_webhook method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
    
    def _create_mock_response(self, json_data, status_code=200, headers=None):
        """Helper to create mock response objects."""
        mock_response = Mock()
        mock_response.json.return_value = json_data
        mock_response.status_code = status_code
        mock_response.headers = headers or {}
        mock_response.request = Mock()
        mock_response.request.url = "https://api.mailersend.com/v1/webhooks/webhook_123"
        mock_response.request.method = "PUT"
        return mock_response
    
    def test_update_webhook_success(self):
        """Test successful webhook update."""
        # Setup
        json_data = {
            "data": {
                "id": "webhook_123",
                "url": "https://example.com/webhook",
                "name": "Updated Webhook",
                "events": ["activity.sent"],
                "enabled": False,
                "domain_id": "test_domain",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
        mock_response = self._create_mock_response(json_data)
        self.client.request.return_value = mock_response
        
        request = WebhookUpdateRequest(
            webhook_id="webhook_123",
            url="https://example.com/webhook",
            name="Updated Webhook",
            events=["activity.sent"],
            enabled=False
        )
        
        # Test
        result = self.webhooks.update_webhook(request)
        
        # Assertions
        expected_data = {
            "url": "https://example.com/webhook",
            "name": "Updated Webhook",
            "events": ["activity.sent"],
            "enabled": False
        }
        self.client.request.assert_called_once_with("PUT", "webhooks/webhook_123", json=expected_data)
        assert isinstance(result, APIResponse)
        assert isinstance(result.data, WebhookResponse)
        assert result.data.data.id == "webhook_123"
        assert result.data.data.name == "Updated Webhook"
    
    def test_update_webhook_partial(self):
        """Test partial webhook update."""
        # Setup
        json_data = {
            "data": {
                "id": "webhook_123",
                "url": "https://example.com/webhook",
                "name": "Updated Name",
                "events": ["activity.sent"],
                "enabled": True,
                "domain_id": "test_domain",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
        mock_response = self._create_mock_response(json_data)
        self.client.request.return_value = mock_response
        
        request = WebhookUpdateRequest(
            webhook_id="webhook_123",
            name="Updated Name"
        )
        
        # Test
        result = self.webhooks.update_webhook(request)
        
        # Assertions
        expected_data = {"name": "Updated Name"}
        self.client.request.assert_called_once_with("PUT", "webhooks/webhook_123", json=expected_data)
        assert isinstance(result, APIResponse)
        assert isinstance(result.data, WebhookResponse)
    
    def test_update_webhook_minimal(self):
        """Test minimal webhook update (only webhook_id)."""
        # Setup
        json_data = {
            "data": {
                "id": "webhook_123",
                "url": "https://example.com/webhook",
                "name": "Test Webhook",
                "events": ["activity.sent"],
                "enabled": True,
                "domain_id": "test_domain",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
        mock_response = self._create_mock_response(json_data)
        self.client.request.return_value = mock_response
        
        request = WebhookUpdateRequest(webhook_id="webhook_123")
        
        # Test
        result = self.webhooks.update_webhook(request)
        
        # Assertions
        self.client.request.assert_called_once_with("PUT", "webhooks/webhook_123", json={})
        assert isinstance(result, APIResponse)
        assert isinstance(result.data, WebhookResponse)
    
    def test_update_webhook_requires_request(self):
        """Test that update_webhook requires a request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.update_webhook(None)
        
        assert "WebhookUpdateRequest must be provided" in str(exc_info.value)
        self.client.request.assert_not_called()
    
    def test_update_webhook_validates_request_type(self):
        """Test that update_webhook validates request type."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.update_webhook("invalid-request")
        
        assert "request must be a WebhookUpdateRequest instance" in str(exc_info.value)
        self.client.request.assert_not_called()


class TestWebhooksDeleteWebhook:
    """Test delete_webhook method."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
    
    def _create_mock_response(self, json_data, status_code=204, headers=None):
        """Helper to create mock response objects."""
        mock_response = Mock()
        mock_response.json.return_value = json_data
        mock_response.status_code = status_code
        mock_response.headers = headers or {}
        mock_response.request = Mock()
        mock_response.request.url = "https://api.mailersend.com/v1/webhooks/webhook_123"
        mock_response.request.method = "DELETE"
        return mock_response
    
    def test_delete_webhook_success(self):
        """Test successful webhook deletion."""
        # Setup
        mock_response = self._create_mock_response({})
        self.client.request.return_value = mock_response
        
        request = WebhookDeleteRequest(webhook_id="webhook_123")
        
        # Test
        result = self.webhooks.delete_webhook(request)
        
        # Assertions
        self.client.request.assert_called_once_with("DELETE", "webhooks/webhook_123")
        assert isinstance(result, APIResponse)
        assert result.status_code == 204
    
    def test_delete_webhook_requires_request(self):
        """Test that delete_webhook requires a request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.delete_webhook(None)
        
        assert "WebhookDeleteRequest must be provided" in str(exc_info.value)
        self.client.request.assert_not_called()
    
    def test_delete_webhook_validates_request_type(self):
        """Test that delete_webhook validates request type."""
        with pytest.raises(ValidationError) as exc_info:
            self.webhooks.delete_webhook("invalid-request")
        
        assert "request must be a WebhookDeleteRequest instance" in str(exc_info.value)
        self.client.request.assert_not_called()


class TestWebhooksApiErrors:
    """Test API error handling."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.webhooks = Webhooks(self.client)
    
    def test_list_webhooks_api_error(self):
        """Test list_webhooks handles API errors."""
        self.client.request.side_effect = Exception("API Error")
        
        query_params = WebhooksListQueryParams(domain_id="test_domain")
        request = WebhooksListRequest(query_params=query_params)
        
        with pytest.raises(Exception) as exc_info:
            self.webhooks.list_webhooks(request)
        
        assert "API Error" in str(exc_info.value)
    
    def test_get_webhook_api_error(self):
        """Test get_webhook handles API errors."""
        self.client.request.side_effect = Exception("API Error")
        
        request = WebhookGetRequest(webhook_id="webhook_123")
        
        with pytest.raises(Exception) as exc_info:
            self.webhooks.get_webhook(request)
        
        assert "API Error" in str(exc_info.value)
    
    def test_create_webhook_api_error(self):
        """Test create_webhook handles API errors."""
        self.client.request.side_effect = Exception("API Error")
        
        request = WebhookCreateRequest(
            url="https://example.com/webhook",
            name="Test Webhook",
            events=["activity.sent"],
            domain_id="test_domain"
        )
        
        with pytest.raises(Exception) as exc_info:
            self.webhooks.create_webhook(request)
        
        assert "API Error" in str(exc_info.value)
    
    def test_update_webhook_api_error(self):
        """Test update_webhook handles API errors."""
        self.client.request.side_effect = Exception("API Error")
        
        request = WebhookUpdateRequest(webhook_id="webhook_123", name="Updated")
        
        with pytest.raises(Exception) as exc_info:
            self.webhooks.update_webhook(request)
        
        assert "API Error" in str(exc_info.value)
    
    def test_delete_webhook_api_error(self):
        """Test delete_webhook handles API errors."""
        self.client.request.side_effect = Exception("API Error")
        
        request = WebhookDeleteRequest(webhook_id="webhook_123")
        
        with pytest.raises(Exception) as exc_info:
            self.webhooks.delete_webhook(request)
        
        assert "API Error" in str(exc_info.value) 