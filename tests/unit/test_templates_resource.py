import pytest
from unittest.mock import Mock, MagicMock
import requests

from mailersend.resources.templates import Templates
from mailersend.models.templates import (
    TemplatesListRequest, TemplateGetRequest, TemplateDeleteRequest,
    TemplatesListResponse, TemplateResponse, Template
)
from mailersend.exceptions import ValidationError


class TestTemplatesResource:
    """Test Templates resource functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_client = Mock()
        self.templates = Templates(self.mock_client)
    
    def test_list_templates_minimal(self):
        """Test listing templates with minimal parameters"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
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
        self.mock_client.request.return_value = mock_response
        
        # Call method
        response = self.templates.list_templates()
        
        # Verify request
        self.mock_client.request.assert_called_once_with(
            "GET",
            "templates",
            params={"limit": 25}
        )
        
        # Verify response
        assert isinstance(response, TemplatesListResponse)
        assert len(response.data) == 1
        assert response.data[0].name == "Welcome Email"
    
    def test_list_templates_with_request(self):
        """Test listing templates with request parameters"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [],
            "links": {"first": "page1", "last": "page2", "prev": None, "next": "page2"},
            "meta": {"current_page": 1, "total": 0}
        }
        self.mock_client.request.return_value = mock_response
        
        # Create request
        request = TemplatesListRequest(
            domain_id="domain-123",
            page=2,
            limit=50
        )
        
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
        assert isinstance(response, TemplatesListResponse)
        assert len(response.data) == 0
    
    def test_list_templates_with_partial_request(self):
        """Test listing templates with partial request parameters"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [],
            "links": {},
            "meta": {}
        }
        self.mock_client.request.return_value = mock_response
        
        # Create request with only domain_id
        request = TemplatesListRequest(domain_id="domain-123")
        
        # Call method
        response = self.templates.list_templates(request)
        
        # Verify request - should include domain_id and default limit
        self.mock_client.request.assert_called_once_with(
            "GET",
            "templates",
            params={
                "domain_id": "domain-123",
                "limit": 25
            }
        )
        
        # Verify response
        assert isinstance(response, TemplatesListResponse)
    
    def test_list_templates_defaults_limit(self):
        """Test listing templates defaults limit to 25 when not specified"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [],
            "links": {},
            "meta": {}
        }
        self.mock_client.request.return_value = mock_response
        
        # Call method without request
        self.templates.list_templates()
        
        # Verify default limit is added
        self.mock_client.request.assert_called_once_with(
            "GET",
            "templates",
            params={"limit": 25}
        )
    
    def test_get_template_success(self):
        """Test getting a single template successfully"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
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
        self.mock_client.request.return_value = mock_response
        
        # Create request
        request = TemplateGetRequest(template_id="template-123")
        
        # Call method
        response = self.templates.get_template(request)
        
        # Verify request
        self.mock_client.request.assert_called_once_with("GET", "templates/template-123")
        
        # Verify response
        assert isinstance(response, TemplateResponse)
        assert response.data.id == "template-123"
        assert response.data.name == "Welcome Email"
        assert response.data.category.name == "Marketing"
        assert response.data.template_stats.total == 100
    
    def test_get_template_requires_request(self):
        """Test get_template requires a request object"""
        with pytest.raises(ValidationError) as exc_info:
            self.templates.get_template(None)
        
        assert "TemplateGetRequest must be provided" in str(exc_info.value)
        
        # Verify no API call was made
        self.mock_client.request.assert_not_called()
    
    def test_delete_template_success(self):
        """Test deleting a template successfully"""
        # Mock response (delete returns empty response)
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response
        
        # Create request
        request = TemplateDeleteRequest(template_id="template-123")
        
        # Call method
        result = self.templates.delete_template(request)
        
        # Verify request
        self.mock_client.request.assert_called_once_with("DELETE", "templates/template-123")
        
        # Verify response (should be None for delete)
        assert result is None
    
    def test_delete_template_requires_request(self):
        """Test delete_template requires a request object"""
        with pytest.raises(ValidationError) as exc_info:
            self.templates.delete_template(None)
        
        assert "TemplateDeleteRequest must be provided" in str(exc_info.value)
        
        # Verify no API call was made
        self.mock_client.request.assert_not_called()
    
    def test_list_templates_api_error(self):
        """Test list_templates handles API errors"""
        # Mock client to raise an exception
        self.mock_client.request.side_effect = requests.exceptions.RequestException("API Error")
        
        # Call method and expect exception to propagate
        with pytest.raises(requests.exceptions.RequestException):
            self.templates.list_templates()
    
    def test_get_template_api_error(self):
        """Test get_template handles API errors"""
        # Mock client to raise an exception
        self.mock_client.request.side_effect = requests.exceptions.RequestException("Template not found")
        
        # Create request
        request = TemplateGetRequest(template_id="template-123")
        
        # Call method and expect exception to propagate
        with pytest.raises(requests.exceptions.RequestException):
            self.templates.get_template(request)
    
    def test_delete_template_api_error(self):
        """Test delete_template handles API errors"""
        # Mock client to raise an exception
        self.mock_client.request.side_effect = requests.exceptions.RequestException("Delete failed")
        
        # Create request
        request = TemplateDeleteRequest(template_id="template-123")
        
        # Call method and expect exception to propagate
        with pytest.raises(requests.exceptions.RequestException):
            self.templates.delete_template(request)
    
    def test_list_templates_response_parsing(self):
        """Test list_templates correctly parses complex response"""
        # Mock complex response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "template-1",
                    "name": "Newsletter Template",
                    "type": "html",
                    "image_path": "https://example.com/newsletter.jpg",
                    "created_at": "2024-01-15T10:30:00Z",
                    "category": {
                        "id": "cat-1",
                        "name": "Newsletter"
                    }
                },
                {
                    "id": "template-2",
                    "name": "Welcome Email",
                    "type": "html",
                    "created_at": "2024-01-16T11:30:00Z"
                }
            ],
            "links": {
                "first": "https://api.mailersend.com/v1/templates?page=1",
                "last": "https://api.mailersend.com/v1/templates?page=3",
                "prev": None,
                "next": "https://api.mailersend.com/v1/templates?page=2"
            },
            "meta": {
                "current_page": 1,
                "from": 1,
                "last_page": 3,
                "path": "https://api.mailersend.com/v1/templates",
                "per_page": 25,
                "to": 25,
                "total": 65
            }
        }
        self.mock_client.request.return_value = mock_response
        
        # Call method
        response = self.templates.list_templates()
        
        # Verify parsing
        assert isinstance(response, TemplatesListResponse)
        assert len(response.data) == 2
        
        # Check first template
        template1 = response.data[0]
        assert template1.id == "template-1"
        assert template1.name == "Newsletter Template"
        assert template1.category.name == "Newsletter"
        
        # Check second template
        template2 = response.data[1]
        assert template2.id == "template-2"
        assert template2.name == "Welcome Email"
        assert template2.category is None
        
        # Check pagination info
        assert response.links["next"] == "https://api.mailersend.com/v1/templates?page=2"
        assert response.meta["total"] == 65
    
    def test_get_template_with_full_response(self):
        """Test get_template with full response including all optional fields"""
        # Mock full response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {
                "id": "template-123",
                "name": "Premium Template",
                "type": "html",
                "image_path": "https://example.com/premium.jpg",
                "personalization": {
                    "name": "John Doe",
                    "elements": [
                        {"name": "Product A", "price": "$99"},
                        {"name": "Product B", "price": "$149"}
                    ],
                    "license_key": "LICENSE-ABC123",
                    "account_name": "Acme Corporation",
                    "product_name": "Premium Service",
                    "renew_button": "Renew Subscription",
                    "expiration_date": "2024-12-31"
                },
                "created_at": "2024-01-15T10:30:00Z",
                "category": {
                    "id": "cat-premium",
                    "name": "Premium Templates"
                },
                "domain": {
                    "id": "domain-123",
                    "name": "premium.example.com",
                    "domain_settings": {
                        "track_opens": True,
                        "track_clicks": True
                    },
                    "totals": {
                        "sent": 1000,
                        "delivered": 950,
                        "hard_bounced": 25,
                        "soft_bounced": 25
                    }
                },
                "template_stats": {
                    "total": 500,
                    "queued": 10,
                    "sent": 480,
                    "rejected": 10,
                    "delivered": 470,
                    "last_email_sent_at": "2024-01-20T14:30:00Z"
                }
            }
        }
        self.mock_client.request.return_value = mock_response
        
        # Create request
        request = TemplateGetRequest(template_id="template-123")
        
        # Call method
        response = self.templates.get_template(request)
        
        # Verify detailed parsing
        assert isinstance(response, TemplateResponse)
        template = response.data
        
        # Basic fields
        assert template.id == "template-123"
        assert template.name == "Premium Template"
        assert template.type == "html"
        assert template.image_path == "https://example.com/premium.jpg"
        
        # Personalization
        assert template.personalization.name == "John Doe"
        assert len(template.personalization.elements) == 2
        assert template.personalization.elements[0]["name"] == "Product A"
        assert template.personalization.license_key == "LICENSE-ABC123"
        
        # Category
        assert template.category.id == "cat-premium"
        assert template.category.name == "Premium Templates"
        
        # Domain
        assert template.domain.id == "domain-123"
        assert template.domain.name == "premium.example.com"
        assert template.domain.domain_settings["track_opens"] is True
        assert template.domain.totals["sent"] == 1000
        
        # Stats
        assert template.template_stats.total == 500
        assert template.template_stats.sent == 480
        assert template.template_stats.delivered == 470
        assert template.template_stats.last_email_sent_at == "2024-01-20T14:30:00Z" 