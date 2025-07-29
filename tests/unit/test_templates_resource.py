"""Unit tests for Templates resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.templates import Templates
from mailersend.models.base import APIResponse
from mailersend.models.templates import (
    TemplatesListRequest,
    TemplatesListQueryParams,
    TemplateGetRequest,
    TemplateDeleteRequest,
)
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestTemplates:
    """Test Templates resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = Templates(self.mock_client)
        self.resource.logger = Mock()
        
        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_templates_returns_api_response(self):
        """Test list_templates method returns APIResponse."""
        query_params = TemplatesListQueryParams()
        request = TemplatesListRequest(query_params=query_params)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_templates(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_templates_with_none_request(self):
        """Test list_templates with None request uses default."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_templates(None)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_templates_uses_query_params(self):
        """Test list_templates method uses query params correctly."""
        query_params = TemplatesListQueryParams(
            domain_id="test-domain",
            page=2,
            limit=50
        )
        request = TemplatesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_templates(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='templates',
            params={'domain_id': 'test-domain', 'page': 2, 'limit': 50}
        )

        # Verify _create_response was called
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_templates_with_defaults(self):
        """Test list_templates with default query params."""
        query_params = TemplatesListQueryParams()
        request = TemplatesListRequest(query_params=query_params)
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_templates(request)

        # Verify client was called with defaults
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='templates',
            params={'page': 1, 'limit': 25}
        )

    def test_get_template_returns_api_response(self):
        """Test get_template method returns APIResponse."""
        request = TemplateGetRequest(template_id="template123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_template(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_template_endpoint_construction(self):
        """Test get_template constructs endpoint correctly."""
        request = TemplateGetRequest(template_id="template123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_template(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method='GET',
            endpoint='templates/template123'
        )

    def test_delete_template_returns_api_response(self):
        """Test delete_template method returns APIResponse."""
        request = TemplateDeleteRequest(template_id="template123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_template(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_template_endpoint_construction(self):
        """Test delete_template constructs endpoint correctly."""
        request = TemplateDeleteRequest(template_id="template123")
        
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_template(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method='DELETE',
            endpoint='templates/template123'
        )

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        query_params = TemplatesListQueryParams()
        request_list = TemplatesListRequest(query_params=query_params)
        request_get = TemplateGetRequest(template_id="template123")
        request_delete = TemplateDeleteRequest(template_id="template123")

        # Test that each method returns the expected APIResponse type
        assert isinstance(self.resource.list_templates(request_list), type(self.mock_api_response))
        assert isinstance(self.resource.get_template(request_get), type(self.mock_api_response))
        assert isinstance(self.resource.delete_template(request_delete), type(self.mock_api_response)) 