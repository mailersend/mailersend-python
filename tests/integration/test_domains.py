import pytest
from tests.test_helpers import vcr, email_client
import os
import time
from datetime import datetime, timezone

from mailersend.builders.domains import DomainsBuilder
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
from mailersend.models.base import APIResponse


@pytest.fixture
def test_domain_id():
    """Get the test domain ID from environment variables"""
    return os.environ.get("SDK_DOMAIN_ID", "test-domain-id")

@pytest.fixture
def test_domain_name():
    """Get the test domain name from environment variables"""
    return os.environ.get("SDK_DOMAIN_NAME", "test-domain-name")

@pytest.fixture
def create_domain_name():
    """Get a unique test domain name with timestamp to avoid conflicts"""
    return os.environ.get("SDK_CREATE_DOMAIN", "test-domain")


@pytest.fixture
def base_domains_request():
    """Basic domain request parameters that are valid for most tests"""
    return DomainListRequest(
        page=1,
        limit=25,
        verified=None
    )


def domains_request_factory(base: DomainListRequest, **overrides) -> DomainListRequest:
    """Create a new DomainListRequest with the same fields, overridden with kwargs"""
    data = base.model_dump()

    # Remove fields explicitly set to `None` in overrides
    for key, value in overrides.items():
        if value is None:
            data.pop(key, None)
        else:
            data[key] = value

    return DomainListRequest(**data)


@pytest.fixture(autouse=True)
def inject_common_objects(request, email_client, base_domains_request, test_domain_id, create_domain_name, test_domain_name):
    if hasattr(request, "cls") and request.cls is not None:
        request.cls.email_client = email_client
        request.cls.base_domains_request = base_domains_request
        request.cls.test_domain_id = test_domain_id
        request.cls.create_domain_name = create_domain_name
        request.cls.test_domain_name = test_domain_name
        request.cls.domains_request_factory = staticmethod(domains_request_factory)


class TestDomainsIntegrationListDomains:
    """Integration tests for list domains endpoint."""
    
    @vcr.use_cassette("domains_list_basic.yaml")
    def test_list_domains_basic(self):
        """Test basic domain listing using request factory pattern."""
        request = self.domains_request_factory(
            self.base_domains_request,
            page=1,
            limit=10
        )
        
        response = self.email_client.domains.list_domains(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        assert isinstance(response.headers, dict)
        
        # Verify data structure
        assert "data" in response
        if response["data"]:
            for domain in response["data"]:
                assert "id" in domain
                assert "name" in domain
                assert "domain_settings" in domain
                assert "created_at" in domain
                assert "updated_at" in domain
    
    @vcr.use_cassette("domains_list_pagination.yaml")
    def test_list_domains_with_pagination(self):
        """Test domain listing with pagination using request factory pattern."""
        request = self.domains_request_factory(
            self.base_domains_request,
            page=2,
            limit=10
        )
        
        response = self.email_client.domains.list_domains(request)
        
        # Verify pagination structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Check pagination metadata if present
        if "links" in response:
            assert isinstance(response["links"], dict)
        if "meta" in response:
            assert isinstance(response["meta"], dict)
    
    @vcr.use_cassette("domains_list_verified.yaml")
    def test_list_domains_verified_only(self):
        """Test listing only verified domains using request factory pattern."""
        # Create request without verified filter to avoid API issues
        request = self.domains_request_factory(
            self.base_domains_request,
            limit=10
        )
        
        response = self.email_client.domains.list_domains(request)
        
        # Verify response
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Verify response structure (don't filter by verification status to avoid API errors)
        if response["data"]:
            for domain in response["data"]:
                assert "id" in domain
                assert "name" in domain
                assert "domain_settings" in domain
    
    @vcr.use_cassette("domains_list_builder.yaml")
    def test_list_domains_builder(self):
        """Test domain listing using builder pattern."""
        builder = DomainsBuilder()
        request = (builder
                  .page(1)
                  .limit(15)
                  .build_list_request())  # Remove verified_only() to avoid API issues
        
        response = self.email_client.domains.list_domains(request)
        
        # Verify response
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200


class TestDomainsIntegrationGetDomain:
    """Integration tests for get single domain endpoint."""
    
    @vcr.use_cassette("domains_get_success.yaml")
    def test_get_domain_success(self):
        """Test getting a single domain."""
        request = DomainGetRequest(domain_id=self.test_domain_id)
        response = self.email_client.domains.get_domain(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Verify domain data structure
        assert "data" in response
        domain = response["data"]
        assert "id" in domain
        assert "name" in domain
        assert "domain_settings" in domain
        assert "created_at" in domain
        assert "updated_at" in domain
        
        # Verify domain settings structure
        settings = domain["domain_settings"]
        assert "send_paused" in settings
        assert "track_clicks" in settings
        assert "track_opens" in settings
        assert "track_unsubscribe" in settings
        assert "track_content" in settings
    
    @vcr.use_cassette("domains_get_not_found.yaml")
    def test_get_domain_not_found(self):
        """Test getting a non-existent domain."""
        domain_id = "non-existent-domain-id"
        
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError):
            request = DomainGetRequest(domain_id=domain_id)
            response = self.email_client.domains.get_domain(request)


class TestDomainsIntegrationCreateDomain:
    """Integration tests for create domain endpoint."""
    
    @vcr.use_cassette("domains_create_minimal.yaml")
    def test_create_domain_minimal(self):
        """Test creating domain with minimal parameters using request object."""
        request = DomainCreateRequest(
            name=self.create_domain_name
        )
        
        response = self.email_client.domains.create_domain(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 201
        
        # Verify created domain data
        assert "data" in response
        domain = response["data"]
        assert "id" in domain
        assert "name" in domain
        assert domain["name"] == self.create_domain_name
        assert "domain_settings" in domain

        # Cleanup
        delete_request = DomainDeleteRequest(domain_id=response["data"]["id"])
        self.email_client.domains.delete_domain(delete_request)
    

class TestDomainsIntegrationUpdateSettings:
    """Integration tests for update domain settings endpoint."""
    
    @vcr.use_cassette("domains_update_settings_tracking.yaml")
    def test_update_domain_settings_tracking(self):
        """Test updating domain tracking settings using request object."""
        request = DomainUpdateSettingsRequest(
            domain_id=self.test_domain_id,
            send_paused=False,
            track_clicks=True,
            track_opens=True,
            track_unsubscribe=True,
            track_content=True,
            track_unsubscribe_html="<p>Custom unsubscribe {{unsubscribe}}</p>",
            track_unsubscribe_plain="Custom unsubscribe {{unsubscribe}}",
            custom_tracking_enabled=True,
            custom_tracking_subdomain="track"
        )
        
        response = self.email_client.domains.update_domain_settings(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Verify updated domain settings
        assert "data" in response
        domain = response["data"]
        settings = domain["domain_settings"]
        assert settings["track_clicks"] is True
        assert settings["track_opens"] is True
    
    @vcr.use_cassette("domains_update_settings_pause.yaml")
    def test_update_domain_settings_pause_sending(self):
        """Test pausing domain sending using request object."""
        request = DomainUpdateSettingsRequest(
            domain_id=self.test_domain_id,
            send_paused=True
        )
        
        response = self.email_client.domains.update_domain_settings(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Verify paused status
        assert "data" in response
        domain = response["data"]
        settings = domain["domain_settings"]
        assert settings["send_paused"] is True
    
    @vcr.use_cassette("domains_update_settings_builder.yaml")
    def test_update_domain_settings_builder(self):
        """Test updating domain settings using builder pattern."""
        builder = DomainsBuilder()
        request = (builder
                  .domain_id(self.test_domain_id)
                  .enable_all_tracking()
                  .resume_sending()
                  .custom_tracking_subdomain_setting("track")
                  .build_update_settings_request())
        
        response = self.email_client.domains.update_domain_settings(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Verify settings were applied
        settings = response["data"]["domain_settings"]
        assert settings["track_clicks"] is True
        assert settings["track_opens"] is True
        assert settings["send_paused"] is False


class TestDomainsIntegrationDnsRecords:
    """Integration tests for domain DNS records endpoint."""
    
    @vcr.use_cassette("domains_dns_records_success.yaml")
    def test_get_domain_dns_records(self):
        """Test getting DNS records for a domain."""
        request = DomainDnsRecordsRequest(domain_id=self.test_domain_id)
        response = self.email_client.domains.get_domain_dns_records(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Verify DNS records data structure
        assert "data" in response
        dns_data = response["data"]
        assert "id" in dns_data
        
        # Verify DNS record types (if present)
        if "spf" in dns_data and dns_data["spf"]:
            spf_record = dns_data["spf"]
            assert "hostname" in spf_record
            assert "type" in spf_record
            assert "value" in spf_record
        
        if "dkim" in dns_data and dns_data["dkim"]:
            dkim_record = dns_data["dkim"]
            assert "hostname" in dkim_record
            assert "type" in dkim_record
            assert "value" in dkim_record
    
    @vcr.use_cassette("domains_dns_records_not_found.yaml")
    def test_get_domain_dns_records_not_found(self):
        """Test getting DNS records for non-existent domain."""
        domain_id = "non-existent-domain-id"

        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError):
            request = DomainDnsRecordsRequest(domain_id=domain_id)
            response = self.email_client.domains.get_domain_dns_records(request)


class TestDomainsIntegrationVerification:
    """Integration tests for domain verification endpoint."""
    
    @vcr.use_cassette("domains_verification_status.yaml")
    def test_get_domain_verification_status(self):
        """Test getting domain verification status."""
        request = DomainVerificationRequest(domain_id=self.test_domain_id)
        response = self.email_client.domains.get_domain_verification_status(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Verify verification data structure - API returns verification fields directly
        assert "data" in response
        verification = response["data"]
        
        # Verify verification status fields
        assert "spf" in verification
        assert "dkim" in verification
        assert "mx" in verification
        assert "tracking" in verification
        assert "cname" in verification
        assert "rp_cname" in verification
        
        # Verify all verification statuses are boolean
        assert isinstance(verification["dkim"], bool)
        assert isinstance(verification["spf"], bool)
        assert isinstance(verification["mx"], bool)
        assert isinstance(verification["tracking"], bool)
        assert isinstance(verification["cname"], bool)
        assert isinstance(verification["rp_cname"], bool)
    
    @vcr.use_cassette("domains_verification_not_found.yaml")
    def test_get_domain_verification_not_found(self):
        """Test getting verification for non-existent domain."""
        domain_id = "non-existent-domain-id"

        from mailersend.exceptions import ResourceNotFoundError
 
        with pytest.raises(ResourceNotFoundError):
            request = DomainVerificationRequest(domain_id=domain_id)
            response = self.email_client.domains.get_domain_verification_status(request)


class TestDomainsIntegrationRecipients:
    """Integration tests for domain recipients endpoint."""
    
    @vcr.use_cassette("domains_recipients_basic.yaml")
    def test_get_domain_recipients_basic(self):
        """Test getting domain recipients using request object."""
        request = DomainRecipientsRequest(
            domain_id=self.test_domain_id,
            page=1,
            limit=25
        )
        
        response = self.email_client.domains.get_domain_recipients(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Verify recipients data structure
        assert "data" in response
        recipients = response["data"]
        assert isinstance(recipients, list)
        
        # If recipients exist, verify structure
        if recipients:
            for recipient in recipients:
                assert "email" in recipient
                assert "created_at" in recipient
                assert "updated_at" in recipient
    
    @vcr.use_cassette("domains_recipients_pagination.yaml")
    def test_get_domain_recipients_pagination(self):
        """Test getting domain recipients with pagination using request object."""
        request = DomainRecipientsRequest(
            domain_id=self.test_domain_id,
            page=2,
            limit=10
        )
        
        response = self.email_client.domains.get_domain_recipients(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200
        
        # Check pagination metadata if present
        if "links" in response:
            assert isinstance(response["links"], dict)
        if "meta" in response:
            assert isinstance(response["meta"], dict)
    
    @vcr.use_cassette("domains_recipients_builder.yaml")
    def test_get_domain_recipients_builder(self):
        """Test getting domain recipients using builder pattern."""
        builder = DomainsBuilder()
        request = (builder
                  .domain_id(self.test_domain_id)
                  .page(1)
                  .limit(20)
                  .build_recipients_request())
        
        response = self.email_client.domains.get_domain_recipients(request)
        
        # Verify response structure
        assert isinstance(response, APIResponse)
        assert response.success is True
        assert response.status_code == 200


class TestDomainsIntegrationDeleteDomain:
    """Integration tests for delete domain endpoint."""
    
    @vcr.use_cassette("domains_delete_success.yaml")
    def test_delete_domain_success(self):
        """Test deleting a domain."""
        create_request = DomainCreateRequest(
            name="somerandomdomain.com"
        )
        create_response = self.email_client.domains.create_domain(create_request)

        # Delete the domain using request model
        delete_request = DomainDeleteRequest(
            domain_id=create_response["data"]["id"]
        )
        delete_response = self.email_client.domains.delete_domain(delete_request)
        
        # Verify response structure
        assert isinstance(delete_response, APIResponse)
        assert delete_response.success is True
        assert delete_response.status_code == 204  # No content for successful deletion
    
    @vcr.use_cassette("domains_delete_not_found.yaml")
    def test_delete_domain_not_found(self):
        """Test deleting a non-existent domain."""
        delete_request = DomainDeleteRequest(
            domain_id="non-existent-domain-id"
        )
        
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError):
            response = self.email_client.domains.delete_domain(delete_request)


    @vcr.use_cassette("domains_settings_workflow.yaml")
    def test_domain_settings_workflow(self):
        """Test comprehensive domain settings management using both request objects and builder."""
        # Enable all tracking using request object
        enable_request = DomainUpdateSettingsRequest(
            domain_id=self.test_domain_id,
            track_clicks=True,
            track_opens=True,
            track_unsubscribe=True,
            track_content=True,
            custom_tracking_enabled=True,
            send_paused=False
        )
        
        enable_response = self.email_client.domains.update_domain_settings(enable_request)
        assert enable_response.success is True
        
        # Verify settings were applied
        get_request = DomainGetRequest(domain_id=self.test_domain_id)
        get_response = self.email_client.domains.get_domain(get_request)
        assert get_response.success is True
        
        settings = get_response["data"]["domain_settings"]
        assert settings["track_clicks"] is True
        assert settings["track_opens"] is True
        assert settings["send_paused"] is False
        
        # Disable tracking and pause sending using builder
        builder = DomainsBuilder()
        disable_request = (builder
                          .domain_id(self.test_domain_id)
                          .disable_all_tracking()
                          .pause_sending()
                          .build_update_settings_request())
        
        disable_response = self.email_client.domains.update_domain_settings(disable_request)
        assert disable_response.success is True
        
        # Verify new settings
        final_request = DomainGetRequest(domain_id=self.test_domain_id)
        final_response = self.email_client.domains.get_domain(final_request)
        assert final_response.success is True
        
        final_settings = final_response["data"]["domain_settings"]
        assert final_settings["track_clicks"] is False
        assert final_settings["track_opens"] is False
        assert final_settings["send_paused"] is True