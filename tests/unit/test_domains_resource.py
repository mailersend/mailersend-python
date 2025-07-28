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
    DomainListQueryParams,
    DomainCreateRequest,
    DomainDeleteRequest,
    DomainGetRequest,
    DomainUpdateSettingsRequest,
    DomainRecipientsRequest,
    DomainRecipientsQueryParams,
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
    
    def test_invalid_type_validation_get(self):
        """Test that invalid request types raise errors for get_domain."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainGetRequest must be provided"):
            domains.get_domain("not-a-request-object")
    
    def test_empty_domain_id_validation_delete(self):
        """Test that empty domain IDs raise errors for delete_domain."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainDeleteRequest must be provided"):
            domains.delete_domain(None)
    
    def test_invalid_type_validation_delete(self):
        """Test that invalid request types raise errors for delete_domain."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainDeleteRequest must be provided"):
            domains.delete_domain("not-a-request-object")
    
    def test_empty_domain_id_validation_recipients(self):
        """Test that empty domain IDs raise errors for get_domain_recipients."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainRecipientsRequest must be provided"):
            domains.get_domain_recipients(None)
    
    def test_invalid_type_validation_recipients(self):
        """Test that invalid request types raise errors for get_domain_recipients."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainRecipientsRequest must be provided"):
            domains.get_domain_recipients("not-a-request-object")
    
    def test_empty_domain_id_validation_settings(self):
        """Test that empty domain IDs raise errors for update_domain_settings."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainUpdateSettingsRequest must be provided"):
            domains.update_domain_settings(None)
    
    def test_invalid_type_validation_settings(self):
        """Test that invalid request types raise errors for update_domain_settings."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainUpdateSettingsRequest must be provided"):
            domains.update_domain_settings("not-a-request-object")
    
    def test_empty_domain_id_validation_dns(self):
        """Test that empty domain IDs raise errors for get_domain_dns_records."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainDnsRecordsRequest must be provided"):
            domains.get_domain_dns_records(None)
    
    def test_invalid_type_validation_dns(self):
        """Test that invalid request types raise errors for get_domain_dns_records."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainDnsRecordsRequest must be provided"):
            domains.get_domain_dns_records("not-a-request-object")
    
    def test_empty_domain_id_validation_verification(self):
        """Test that empty domain IDs raise errors for get_domain_verification_status."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainVerificationRequest must be provided"):
            domains.get_domain_verification_status(None)
    
    def test_invalid_type_validation_verification(self):
        """Test that invalid request types raise errors for get_domain_verification_status."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainVerificationRequest must be provided"):
            domains.get_domain_verification_status("not-a-request-object")
    
    def test_missing_create_request_validation(self):
        """Test that missing create request raises error."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainCreateRequest must be provided"):
            domains.create_domain(None)
    
    def test_invalid_type_validation_create(self):
        """Test that invalid request types raise errors for create_domain."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainCreateRequest must be provided"):
            domains.create_domain("not-a-request-object")
    
    def test_missing_list_request_validation(self):
        """Test that invalid list request types raise errors."""
        mock_client = Mock()
        domains = Domains(mock_client)
        
        with pytest.raises(ValidationError, match="DomainListRequest must be provided"):
            domains.list_domains("not-a-request-object")


class TestDomainsResourceQueryParams:
    """Test query parameter handling."""
    
    def test_list_domains_default_params(self):
        """Test list_domains with default parameters."""
        mock_client = Mock()
        mock_response = Mock()
        mock_client.request.return_value = mock_response
        
        domains = Domains(mock_client)
        domains._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        # Call without request should use defaults
        result = domains.list_domains()
        
        # Should call with default query params
        mock_client.request.assert_called_once_with("GET", "domains", params={"page": 1, "limit": 25})
        domains._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(domains._create_response.return_value))
    
    def test_list_domains_with_custom_params(self):
        """Test list_domains with custom parameters."""
        mock_client = Mock()
        mock_response = Mock()
        mock_client.request.return_value = mock_response
        
        domains = Domains(mock_client)
        domains._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = DomainListQueryParams(page=2, limit=50, verified=True)
        request = DomainListRequest(query_params=query_params)
        
        result = domains.list_domains(request)
        
        expected_params = {"page": 2, "limit": 50, "verified": True}
        mock_client.request.assert_called_once_with("GET", "domains", params=expected_params)
        domains._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(domains._create_response.return_value))
    
    def test_recipients_query_params_delegation(self):
        """Test that recipients request properly delegates query parameters."""
        mock_client = Mock()
        mock_response = Mock()
        mock_client.request.return_value = mock_response
        
        domains = Domains(mock_client)
        domains._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        query_params = DomainRecipientsQueryParams(page=3, limit=20)
        request = DomainRecipientsRequest(
            domain_id="test-domain-id",
            query_params=query_params
        )
        
        result = domains.get_domain_recipients(request)
        
        expected_params = {"page": 3, "limit": 20}
        mock_client.request.assert_called_once_with(
            "GET", 
            "domains/test-domain-id/recipients", 
            params=expected_params
        )
        domains._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(domains._create_response.return_value))


class TestDomainsResourceRequestBodyHandling:
    """Test request body handling."""
    
    def test_create_domain_body_serialization(self):
        """Test that create domain properly serializes request body."""
        mock_client = Mock()
        mock_response = Mock()
        mock_client.request.return_value = mock_response
        
        domains = Domains(mock_client)
        domains._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = DomainCreateRequest(
            name="example.com",
            return_path_subdomain="mail"
        )
        
        result = domains.create_domain(request)
        
        expected_body = {
            "name": "example.com",
            "return_path_subdomain": "mail"
        }
        mock_client.request.assert_called_once_with("POST", "domains", body=expected_body)
        domains._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(domains._create_response.return_value))
    
    def test_update_settings_body_excludes_domain_id(self):
        """Test that update settings excludes domain_id from request body."""
        mock_client = Mock()
        mock_response = Mock()
        mock_client.request.return_value = mock_response
        
        domains = Domains(mock_client)
        domains._create_response = Mock(return_value=Mock(spec=APIResponse))
        
        request = DomainUpdateSettingsRequest(
            domain_id="test-domain-id",
            track_opens=True,
            send_paused=False
        )
        
        result = domains.update_domain_settings(request)
        
        expected_body = {
            "track_opens": True,
            "send_paused": False
        }
        # domain_id should NOT be in body, only in URL
        assert "domain_id" not in expected_body
        
        mock_client.request.assert_called_once_with(
            "PUT", 
            "domains/test-domain-id/settings", 
            body=expected_body
        )
        domains._create_response.assert_called_once_with(mock_response)
        assert isinstance(result, type(domains._create_response.return_value))


class TestDomainsResourceMethodSignatures:
    """Test that all methods exist with correct signatures."""
    
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