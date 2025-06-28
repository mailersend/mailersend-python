"""Tests for Templates resource."""
import pytest
from unittest.mock import Mock, MagicMock
import requests

from mailersend.resources.templates import Templates
from mailersend.models.base import APIResponse
from mailersend.models.templates import (
    TemplatesListQueryParams, TemplatesListRequest,
    TemplateGetRequest, TemplateDeleteRequest,
    TemplatesListResponse, TemplateResponse, Template
)
from mailersend.exceptions import ValidationError


class TestTemplatesResource:
    """Test Templates resource functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.templates = Templates(self.mock_client)
    
    def _create_mock_response(self, json_data, status_code=200, headers=None):
        """Helper to create mock response objects."""
        mock_response = Mock()
        mock_response.json.return_value = json_data
        mock_response.status_code = status_code
        mock_response.headers = headers or {}
        mock_response.request = Mock()
        mock_response.request.url = "https://api.mailersend.com/v1/templates"
        mock_response.request.method = "GET"
        return mock_response
    
    def test_list_templates_minimal(self):
        """Test listing templates with minimal parameters."""
        # Mock response
        json_data = {
            "data": [
                {
                    "id": "template-123",
                    "name": "Welcome Email",
                    "type": "html",
                    "created_at": "2024-01-15T10:30:00Z"
                }
            ],
            "links": {"first": "page1", "last": "page1", "prev": None, "next": None},
            "meta": {"current_page": 1, "total": 1}
        }
        mock_response = self._create_mock_response(json_data)
        self.mock_client.request.return_value = mock_response
        
        # Call method
        response = self.templates.list_templates()
        
        # Verify request - should use defaults
        self.mock_client.request.assert_called_once_with(
            "GET",
            "templates",
            params={"page": 1, "limit": 25}
        )
        
        # Verify response
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, TemplatesListResponse)
        assert len(response.data.data) == 1
        assert response.data.data[0].name == "Welcome Email"
    
    def test_list_templates_with_request(self):
        """Test listing templates with request parameters."""
        # Mock response
        json_data = {
            "data": [],
            "links": {"first": "page1", "last": "page2", "prev": None, "next": "page2"},
            "meta": {"current_page": 1, "total": 0}
        }
        mock_response = self._create_mock_response(json_data)
        self.mock_client.request.return_value = mock_response
        
        # Create request
        query_params = TemplatesListQueryParams(
            domain_id="domain-123",
            page=2,
            limit=50
        )
        request = TemplatesListRequest(query_params=query_params)
        
        # Call method
        response = self.templates.list_templates(request)
        
        # Verify request
        self.mock_client.request.assert_called_once_with(
            "GET",
            "templates",
            params={
                "domain_id": "domain-123",
                "page": 2,
                "limit": 50
            }
        )
        
        # Verify response
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, TemplatesListResponse)
        assert len(response.data.data) == 0
    
    def test_list_templates_with_partial_request(self):
        """Test listing templates with partial request parameters."""
        # Mock response
        json_data = {
            "data": [],
            "links": {},
            "meta": {}
        }
        mock_response = self._create_mock_response(json_data)
        self.mock_client.request.return_value = mock_response
        
        # Create request with only domain_id
        query_params = TemplatesListQueryParams(domain_id="domain-123")
        request = TemplatesListRequest(query_params=query_params)
        
        # Call method
        response = self.templates.list_templates(request)
        
        # Verify request - should include domain_id and defaults
        self.mock_client.request.assert_called_once_with(
            "GET",
            "templates",
            params={
                "domain_id": "domain-123",
                "page": 1,
                "limit": 25
            }
        )
        
        # Verify response
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, TemplatesListResponse)
    
    def test_list_templates_excludes_none_domain_id(self):
        """Test listing templates excludes None domain_id from params."""
        # Mock response
        json_data = {
            "data": [],
            "links": {},
            "meta": {}
        }
        mock_response = self._create_mock_response(json_data)
        self.mock_client.request.return_value = mock_response
        
        # Create request with None domain_id
        query_params = TemplatesListQueryParams(domain_id=None, page=2, limit=50)
        request = TemplatesListRequest(query_params=query_params)
        
        # Call method
        response = self.templates.list_templates(request)
        
        # Verify request - should exclude domain_id
        self.mock_client.request.assert_called_once_with(
            "GET",
            "templates",
            params={
                "page": 2,
                "limit": 50
            }
        )
        
        # Verify response
        assert isinstance(response, APIResponse)
    
    def test_get_template_success(self):
        """Test getting a single template successfully."""
        # Mock response
        json_data = {
            "data": {
                "id": "template-123",
                "name": "Welcome Email",
                "type": "html",
                "image_path": "https://example.com/image.jpg",
                "created_at": "2024-01-15T10:30:00Z",
                "category": {
                    "id": "cat-1",
                    "name": "Marketing"
                },
                "domain": {
                    "id": "domain-1",
                    "name": "example.com"
                },
                "template_stats": {
                    "total": 100,
                    "sent": 95,
                    "delivered": 90,
                    "queued": 0,
                    "rejected": 5,
                    "last_email_sent_at": "2024-01-14T15:30:00Z"
                }
            }
        }
        mock_response = self._create_mock_response(json_data)
        self.mock_client.request.return_value = mock_response
        
        # Create request
        request = TemplateGetRequest(template_id="template-123")
        
        # Call method
        response = self.templates.get_template(request)
        
        # Verify request
        self.mock_client.request.assert_called_once_with("GET", "templates/template-123")
        
        # Verify response
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, TemplateResponse)
        assert response.data.data.id == "template-123"
        assert response.data.data.name == "Welcome Email"
        assert response.data.data.category.name == "Marketing"
        assert response.data.data.template_stats.total == 100
    
    def test_get_template_requires_request(self):
        """Test get_template requires a request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.templates.get_template(None)
        
        assert "TemplateGetRequest must be provided" in str(exc_info.value)
        
        # Verify no API call was made
        self.mock_client.request.assert_not_called()
    
    def test_get_template_validates_request_type(self):
        """Test get_template validates request type."""
        with pytest.raises(ValidationError) as exc_info:
            self.templates.get_template("invalid-request")
        
        assert "request must be a TemplateGetRequest instance" in str(exc_info.value)
        
        # Verify no API call was made
        self.mock_client.request.assert_not_called()
    
    def test_delete_template_success(self):
        """Test deleting a template successfully."""
        # Mock response (delete returns empty response)
        mock_response = self._create_mock_response({}, status_code=204)
        self.mock_client.request.return_value = mock_response
        
        # Create request
        request = TemplateDeleteRequest(template_id="template-123")
        
        # Call method
        response = self.templates.delete_template(request)
        
        # Verify request
        self.mock_client.request.assert_called_once_with("DELETE", "templates/template-123")
        
        # Verify response
        assert isinstance(response, APIResponse)
        assert response.status_code == 204
    
    def test_delete_template_requires_request(self):
        """Test delete_template requires a request object."""
        with pytest.raises(ValidationError) as exc_info:
            self.templates.delete_template(None)
        
        assert "TemplateDeleteRequest must be provided" in str(exc_info.value)
        
        # Verify no API call was made
        self.mock_client.request.assert_not_called()
    
    def test_delete_template_validates_request_type(self):
        """Test delete_template validates request type."""
        with pytest.raises(ValidationError) as exc_info:
            self.templates.delete_template("invalid-request")
        
        assert "request must be a TemplateDeleteRequest instance" in str(exc_info.value)
        
        # Verify no API call was made
        self.mock_client.request.assert_not_called()
    
    def test_list_templates_api_error(self):
        """Test list_templates handles API errors."""
        # Mock error response
        self.mock_client.request.side_effect = Exception("API Error")
        
        # Verify exception is raised
        with pytest.raises(Exception) as exc_info:
            self.templates.list_templates()
        
        assert "API Error" in str(exc_info.value)
    
    def test_get_template_api_error(self):
        """Test get_template handles API errors."""
        # Mock error response
        self.mock_client.request.side_effect = Exception("API Error")
        
        # Create request
        request = TemplateGetRequest(template_id="template-123")
        
        # Verify exception is raised
        with pytest.raises(Exception) as exc_info:
            self.templates.get_template(request)
        
        assert "API Error" in str(exc_info.value)
    
    def test_delete_template_api_error(self):
        """Test delete_template handles API errors."""
        # Mock error response
        self.mock_client.request.side_effect = Exception("API Error")
        
        # Create request
        request = TemplateDeleteRequest(template_id="template-123")
        
        # Verify exception is raised
        with pytest.raises(Exception) as exc_info:
            self.templates.delete_template(request)
        
        assert "API Error" in str(exc_info.value)
    
    def test_list_templates_response_parsing(self):
        """Test list_templates properly parses response data."""
        # Mock response with multiple templates
        json_data = {
            "data": [
                {
                    "id": "template-1",
                    "name": "Template 1",
                    "type": "html",
                    "created_at": "2024-01-15T10:30:00Z"
                },
                {
                    "id": "template-2",
                    "name": "Template 2", 
                    "type": "text",
                    "created_at": "2024-01-16T11:30:00Z"
                }
            ],
            "links": {
                "first": "https://api.mailersend.com/v1/templates?page=1",
                "last": "https://api.mailersend.com/v1/templates?page=5",
                "prev": None,
                "next": "https://api.mailersend.com/v1/templates?page=2"
            },
            "meta": {
                "current_page": 1,
                "from": 1,
                "last_page": 5,
                "path": "https://api.mailersend.com/v1/templates",
                "per_page": 25,
                "to": 25,
                "total": 125
            }
        }
        mock_response = self._create_mock_response(json_data)
        self.mock_client.request.return_value = mock_response
        
        # Call method
        response = self.templates.list_templates()
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, TemplatesListResponse)
        assert len(response.data.data) == 2
        assert response.data.data[0].id == "template-1"
        assert response.data.data[1].id == "template-2"
        assert response.data.meta["total"] == 125
        assert response.data.links["next"] == "https://api.mailersend.com/v1/templates?page=2" 