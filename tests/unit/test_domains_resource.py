"""
Unit tests for Domains resource.

Tests basic functionality, validation, and error handling.
"""

import pytest
from unittest.mock import Mock

from mailersend.resources.domains import Domains
from mailersend.models.domains import (
    DomainListRequest,
    DomainCreateRequest, 
    DomainUpdateSettingsRequest,
    DomainRecipientsRequest
)
from mailersend.exceptions import ValidationError


class TestDomainsResourceInitialization:
    """Test Domains resource initialization."""
    
    def test_domains_resource_initialization(self):
        """Test Domains resource initializes correctly."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert domains.client is mock_client
        assert domains.logger is not None


class TestDomainsResourceValidation:
    """Test resource validation."""
    
    def test_empty_domain_id_validation_get(self):
        """Test that empty domain IDs raise errors for get_domain."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain("")
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain("   ")
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain(None)
    
    def test_empty_domain_id_validation_delete(self):
        """Test that empty domain IDs raise errors for delete_domain.""" 
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.delete_domain("")
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.delete_domain("   ")
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.delete_domain(None)
    
    def test_empty_domain_id_validation_recipients(self):
        """Test that empty domain IDs raise errors for get_domain_recipients."""
        mock_client = Mock()
        domains = Domains(mock_client)
        request = DomainRecipientsRequest()
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_recipients("", request)
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_recipients("   ", request)
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_recipients(None, request)
    
    def test_empty_domain_id_validation_settings(self):
        """Test that empty domain IDs raise errors for update_domain_settings."""
        mock_client = Mock()
        domains = Domains(mock_client)
        request = DomainUpdateSettingsRequest()
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.update_domain_settings("", request)
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.update_domain_settings("   ", request)
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.update_domain_settings(None, request)
    
    def test_empty_domain_id_validation_dns(self):
        """Test that empty domain IDs raise errors for get_domain_dns_records."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_dns_records("")
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_dns_records("   ")
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_dns_records(None)
    
    def test_empty_domain_id_validation_verification(self):
        """Test that empty domain IDs raise errors for get_domain_verification_status."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_verification_status("")
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_verification_status("   ")
        
        with pytest.raises(ValidationError, match="Domain ID must be provided"):
            domains.get_domain_verification_status(None)
    
    def test_missing_create_request_validation(self):
        """Test that missing create request raises error."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainCreateRequest must be provided"):
            domains.create_domain(None)
    
    def test_missing_settings_request_validation(self):
        """Test that missing settings request raises error."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainUpdateSettingsRequest must be provided"):
            domains.update_domain_settings("domain123", None)


class TestDomainsResourceParameterBuilding:
    """Test parameter building logic."""
    
    def test_build_query_params_with_request(self):
        """Test building query parameters from request object."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        request = DomainListRequest(page=1, limit=10, verified=True)
        params = domains._build_query_params(request)
        
        assert params == {"page": 1, "limit": 10, "verified": True}
    
    def test_build_query_params_excludes_none(self):
        """Test that None values are excluded from query parameters."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        request = DomainListRequest(page=1, verified=None)
        params = domains._build_query_params(request)
        
        assert "page" in params
        assert "verified" not in params
        assert params["page"] == 1
    
    def test_build_request_body_with_request(self):
        """Test building request body from request object."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        request = DomainCreateRequest(
            name="test.com",
            return_path_subdomain="mail"
        )
        body = domains._build_request_body(request)
        
        assert body == {"name": "test.com", "return_path_subdomain": "mail"}
    
    def test_build_request_body_excludes_none(self):
        """Test that None values are excluded from request body."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        request = DomainCreateRequest(
            name="test.com",
            return_path_subdomain="mail",
            custom_tracking_subdomain=None
        )
        body = domains._build_request_body(request)
        
        assert "name" in body
        assert "return_path_subdomain" in body
        assert "custom_tracking_subdomain" not in body
        assert body["name"] == "test.com"
        assert body["return_path_subdomain"] == "mail"


class TestDomainsResourceMethodSignatures:
    """Test that all 8 methods exist with correct signatures."""
    
    def test_list_domains_method_exists(self):
        """Test list_domains method exists."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert hasattr(domains, 'list_domains')
        assert callable(getattr(domains, 'list_domains'))
    
    def test_get_domain_method_exists(self):
        """Test get_domain method exists."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert hasattr(domains, 'get_domain')
        assert callable(getattr(domains, 'get_domain'))
    
    def test_create_domain_method_exists(self):
        """Test create_domain method exists."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert hasattr(domains, 'create_domain')
        assert callable(getattr(domains, 'create_domain'))
    
    def test_delete_domain_method_exists(self):
        """Test delete_domain method exists."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert hasattr(domains, 'delete_domain')
        assert callable(getattr(domains, 'delete_domain'))
    
    def test_get_domain_recipients_method_exists(self):
        """Test get_domain_recipients method exists."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert hasattr(domains, 'get_domain_recipients')
        assert callable(getattr(domains, 'get_domain_recipients'))
    
    def test_update_domain_settings_method_exists(self):
        """Test update_domain_settings method exists."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert hasattr(domains, 'update_domain_settings')
        assert callable(getattr(domains, 'update_domain_settings'))
    
    def test_get_domain_dns_records_method_exists(self):
        """Test get_domain_dns_records method exists."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert hasattr(domains, 'get_domain_dns_records')
        assert callable(getattr(domains, 'get_domain_dns_records'))
    
    def test_get_domain_verification_status_method_exists(self):
        """Test get_domain_verification_status method exists."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        assert hasattr(domains, 'get_domain_verification_status')
        assert callable(getattr(domains, 'get_domain_verification_status')) 