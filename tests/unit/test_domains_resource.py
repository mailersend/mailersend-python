"""
Unit tests for Domains resource.

Tests basic functionality, validation, and error handling.
"""

import pytest
from unittest.mock import Mock
from pydantic import ValidationError as PydanticValidationError

from mailersend.resources.domains import Domains
from mailersend.models.domains import (
    DomainListRequest,
    DomainCreateRequest,
    DomainDeleteRequest,
    DomainGetRequest,
    DomainUpdateSettingsRequest,
    DomainRecipientsRequest,
    DomainDnsRecordsRequest,
    DomainVerificationRequest
)
from mailersend.exceptions import ValidationError
from mailersend.models.base import APIResponse


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
        
        with pytest.raises(ValidationError, match="DomainGetRequest must be provided"):
            domains.get_domain(None)
    
    def test_empty_domain_id_validation_delete(self):
        """Test that empty domain IDs raise errors for delete_domain."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainDeleteRequest must be provided"):
            domains.delete_domain(None)
    
    def test_empty_domain_id_validation_recipients(self):
        """Test that empty domain IDs raise errors for get_domain_recipients."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainRecipientsRequest must be provided"):
            domains.get_domain_recipients(None)
    
    def test_empty_domain_id_validation_settings(self):
        """Test that empty domain IDs raise errors for update_domain_settings."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainUpdateSettingsRequest must be provided"):
            domains.update_domain_settings(None)
    
    def test_empty_domain_id_validation_dns(self):
        """Test that empty domain IDs raise errors for get_domain_dns_records."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainDnsRecordsRequest must be provided"):
            domains.get_domain_dns_records(None)
    
    def test_empty_domain_id_validation_verification(self):
        """Test that empty domain IDs raise errors for get_domain_verification_status."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainVerificationRequest must be provided"):
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
            domains.update_domain_settings(None)
    
    def test_missing_delete_request_validation(self):
        """Test that missing delete request raises error."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainDeleteRequest must be provided"):
            domains.delete_domain(None)


class TestDomainsResourceParameterBuilding:
    """Test parameter building logic."""
    
    def test_build_query_params_with_request(self):
        """Test building query parameters from request object."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        request = DomainRecipientsRequest(domain_id="test-domain", page=2, limit=50)
        params = domains._build_query_params(request)
        
        # domain_id should not be in query params (it's in the URL path)
        assert "domain_id" not in params
        assert params["page"] == 2
        assert params["limit"] == 50

    def test_build_query_params_excludes_none(self):
        """Test that None values are excluded from query parameters."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        request = DomainRecipientsRequest(domain_id="test-domain", page=None, limit=25)
        params = domains._build_query_params(request)
        
        assert "domain_id" not in params
        assert "page" not in params
        assert params["limit"] == 25

    def test_build_request_body_with_request(self):
        """Test building request body from request object."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        request = DomainUpdateSettingsRequest(
            domain_id="test-domain",
            track_opens=True,
            send_paused=False
        )
        body = domains._build_request_body(request)
        
        # domain_id should not be in request body (it's in the URL path)
        assert "domain_id" not in body
        assert body["track_opens"] is True
        assert body["send_paused"] is False

    def test_build_request_body_excludes_none(self):
        """Test that None values are excluded from request body."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        request = DomainUpdateSettingsRequest(
            domain_id="test-domain",
            track_opens=None,
            send_paused=False
        )
        body = domains._build_request_body(request)
        
        assert "domain_id" not in body
        assert "track_opens" not in body
        assert body["send_paused"] is False


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