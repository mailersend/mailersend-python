"""
Unit tests for Domains models.

Tests model validation, field aliases, edge cases, and complex scenarios.
"""

import pytest
from pydantic import ValidationError

from mailersend.models.domains import (
    DomainListRequest,
    DomainListQueryParams,
    DomainCreateRequest,
    DomainDeleteRequest,
    DomainUpdateSettingsRequest,
    DomainSettings,
    Domain,
    DomainRecipient,
    DomainRecipientsRequest,
    DomainRecipientsQueryParams,
    DomainDnsRecord,
    DomainDnsRecords,
    DomainVerificationData,
    DomainGetRequest,
    DomainDnsRecordsRequest,
    DomainVerificationRequest
)


class TestDomainListQueryParams:
    """Test DomainListQueryParams model."""
    
    def test_default_query_params(self):
        """Test default query parameters."""
        params = DomainListQueryParams()
        assert params.page == 1  # Default value
        assert params.limit == 25  # Default value
        assert params.verified is None
    
    def test_query_params_with_all_fields(self):
        """Test query parameters with all fields."""
        params = DomainListQueryParams(
            page=2,
            limit=50,
            verified=True
        )
        assert params.page == 2
        assert params.limit == 50
        assert params.verified is True
    
    def test_limit_validation(self):
        """Test limit validation."""
        # Valid limits
        DomainListQueryParams(limit=10)  # Min
        DomainListQueryParams(limit=100)  # Max
        DomainListQueryParams(limit=25)  # Middle
        
        # Invalid limits
        with pytest.raises(ValidationError):
            DomainListQueryParams(limit=5)
        
        with pytest.raises(ValidationError):
            DomainListQueryParams(limit=150)
    
    def test_page_validation(self):
        """Test page validation."""
        # Valid pages
        DomainListQueryParams(page=1)
        DomainListQueryParams(page=100)
        
        # Invalid pages
        with pytest.raises(ValidationError):
            DomainListQueryParams(page=0)
        
        with pytest.raises(ValidationError):
            DomainListQueryParams(page=-1)
    
    def test_to_query_params(self):
        """Test query parameter conversion."""
        params = DomainListQueryParams(page=2, limit=10, verified=True)
        query_params = params.to_query_params()
        
        assert query_params == {
            "page": 2,
            "limit": 10,
            "verified": True
        }
    
    def test_to_query_params_exclude_none(self):
        """Test query parameter conversion excluding None values."""
        params = DomainListQueryParams(page=1, limit=15)  # verified is None
        query_params = params.to_query_params()
        
        assert query_params == {
            "page": 1,
            "limit": 15
        }
        assert "verified" not in query_params


class TestDomainListRequest:
    """Test DomainListRequest model."""
    
    def test_basic_domain_list_request(self):
        """Test basic domain list request creation."""
        query_params = DomainListQueryParams()
        request = DomainListRequest(query_params=query_params)
        
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.query_params.verified is None
    
    def test_domain_list_request_with_all_fields(self):
        """Test domain list request with all fields."""
        query_params = DomainListQueryParams(
            page=2,
            limit=50,
            verified=True
        )
        request = DomainListRequest(query_params=query_params)
        
        assert request.query_params.page == 2
        assert request.query_params.limit == 50
        assert request.query_params.verified is True
    
    def test_to_query_params_delegation(self):
        """Test that request delegates to_query_params to query_params object."""
        query_params = DomainListQueryParams(page=3, limit=20, verified=False)
        request = DomainListRequest(query_params=query_params)
        
        result = request.to_query_params()
        expected = query_params.to_query_params()
        
        assert result == expected
        assert result == {
            "page": 3,
            "limit": 20,
            "verified": False
        }


class TestDomainRecipientsQueryParams:
    """Test DomainRecipientsQueryParams model."""
    
    def test_default_query_params(self):
        """Test default query parameters."""
        params = DomainRecipientsQueryParams()
        assert params.page == 1  # Default value
        assert params.limit == 25  # Default value
    
    def test_query_params_with_all_fields(self):
        """Test query parameters with all fields."""
        params = DomainRecipientsQueryParams(page=3, limit=50)
        assert params.page == 3
        assert params.limit == 50
    
    def test_limit_validation(self):
        """Test limit validation."""
        # Valid limits
        DomainRecipientsQueryParams(limit=10)  # Min
        DomainRecipientsQueryParams(limit=100)  # Max
        DomainRecipientsQueryParams(limit=25)  # Middle
        
        # Invalid limits
        with pytest.raises(ValidationError):
            DomainRecipientsQueryParams(limit=5)
        
        with pytest.raises(ValidationError):
            DomainRecipientsQueryParams(limit=150)
    
    def test_page_validation(self):
        """Test page validation."""
        # Valid pages
        DomainRecipientsQueryParams(page=1)
        DomainRecipientsQueryParams(page=100)
        
        # Invalid pages
        with pytest.raises(ValidationError):
            DomainRecipientsQueryParams(page=0)
        
        with pytest.raises(ValidationError):
            DomainRecipientsQueryParams(page=-1)
    
    def test_to_query_params(self):
        """Test query parameter conversion."""
        params = DomainRecipientsQueryParams(page=2, limit=10)
        query_params = params.to_query_params()
        
        assert query_params == {
            "page": 2,
            "limit": 10
        }


class TestDomainRecipientsRequest:
    """Test DomainRecipientsRequest model."""
    
    def test_basic_recipients_request(self):
        """Test basic recipients request."""
        query_params = DomainRecipientsQueryParams()
        request = DomainRecipientsRequest(
            domain_id="test-domain-id",
            query_params=query_params
        )
        
        assert request.domain_id == "test-domain-id"
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_recipients_request_with_custom_params(self):
        """Test recipients request with custom parameters."""
        query_params = DomainRecipientsQueryParams(page=2, limit=50)
        request = DomainRecipientsRequest(
            domain_id="test-domain-id",
            query_params=query_params
        )
        
        assert request.domain_id == "test-domain-id"
        assert request.query_params.page == 2
        assert request.query_params.limit == 50
    
    def test_domain_id_validation(self):
        """Test domain ID validation."""
        query_params = DomainRecipientsQueryParams()
        
        # Valid domain ID
        DomainRecipientsRequest(domain_id="valid-domain-id", query_params=query_params)
        
        # Empty domain ID
        with pytest.raises(ValidationError):
            DomainRecipientsRequest(domain_id="", query_params=query_params)
        
        # Whitespace only domain ID
        with pytest.raises(ValidationError):
            DomainRecipientsRequest(domain_id="   ", query_params=query_params)
    
    def test_to_query_params_delegation(self):
        """Test that request delegates to_query_params to query_params object."""
        query_params = DomainRecipientsQueryParams(page=3, limit=20)
        request = DomainRecipientsRequest(
            domain_id="test-domain-id",
            query_params=query_params
        )
        
        result = request.to_query_params()
        expected = query_params.to_query_params()
        
        assert result == expected
        assert result == {
            "page": 3,
            "limit": 20
        }


class TestDomainCreateRequest:
    """Test DomainCreateRequest model."""
    
    def test_basic_domain_create_request(self):
        """Test basic domain creation request."""
        request = DomainCreateRequest(name="example.com")
        assert request.name == "example.com"
        assert request.return_path_subdomain is None
        assert request.custom_tracking_subdomain is None
        assert request.inbound_routing_subdomain is None
    
    def test_domain_create_request_with_all_fields(self):
        """Test domain creation with all optional fields."""
        request = DomainCreateRequest(
            name="mydomain.com",
            return_path_subdomain="mail",
            custom_tracking_subdomain="track",
            inbound_routing_subdomain="inbox"
        )
        assert request.name == "mydomain.com"
        assert request.return_path_subdomain == "mail"
        assert request.custom_tracking_subdomain == "track"
        assert request.inbound_routing_subdomain == "inbox"
    
    def test_domain_name_validation(self):
        """Test domain name validation."""
        # Valid domain names
        DomainCreateRequest(name="example.com")
        DomainCreateRequest(name="sub.example.com")
        DomainCreateRequest(name="test-domain.org")
        
        # Invalid: empty name
        with pytest.raises(ValidationError, match="Domain name is required"):
            DomainCreateRequest(name="")
        
        with pytest.raises(ValidationError, match="Domain name is required"):
            DomainCreateRequest(name="   ")
        
        # Invalid: uppercase
        with pytest.raises(ValidationError, match="Domain name must be lowercase"):
            DomainCreateRequest(name="EXAMPLE.COM")
        
        with pytest.raises(ValidationError, match="Domain name must be lowercase"):
            DomainCreateRequest(name="Example.Com")
        
        # Invalid: no dot
        with pytest.raises(ValidationError, match="Invalid domain name format"):
            DomainCreateRequest(name="nodot")
        
        # Invalid: spaces
        with pytest.raises(ValidationError, match="Invalid domain name format"):
            DomainCreateRequest(name="invalid domain.com")
    
    def test_subdomain_validation(self):
        """Test subdomain validation."""
        # Valid alphanumeric subdomains
        DomainCreateRequest(
            name="test.com",
            return_path_subdomain="mail",
            custom_tracking_subdomain="track123",
            inbound_routing_subdomain="inbox"
        )
        
        # Invalid: non-alphanumeric characters
        with pytest.raises(ValidationError, match="Subdomain must be alphanumeric"):
            DomainCreateRequest(name="test.com", return_path_subdomain="mail-invalid")
        
        with pytest.raises(ValidationError, match="Subdomain must be alphanumeric"):
            DomainCreateRequest(name="test.com", custom_tracking_subdomain="track.invalid")
        
        with pytest.raises(ValidationError, match="Subdomain must be alphanumeric"):
            DomainCreateRequest(name="test.com", inbound_routing_subdomain="inbox_invalid")
    
    def test_name_no_spaces_allowed(self):
        """Test that domain names with spaces are rejected."""
        # The validation checks for spaces before trimming
        with pytest.raises(ValidationError, match="Invalid domain name format"):
            DomainCreateRequest(name="example.com ")
        
        with pytest.raises(ValidationError, match="Invalid domain name format"):
            DomainCreateRequest(name=" example.com")
        
        with pytest.raises(ValidationError, match="Invalid domain name format"):
            DomainCreateRequest(name="example .com")


class TestDomainDeleteRequest:
    """Test DomainDeleteRequest model."""
    
    def test_basic_domain_delete_request(self):
        """Test basic domain delete request."""
        request = DomainDeleteRequest(domain_id="test-domain-id")
        
        assert request.domain_id == "test-domain-id"
    
    def test_domain_id_validation(self):
        """Test domain ID validation."""
        # Valid domain ID
        DomainDeleteRequest(domain_id="valid-domain-id")
        
        # Empty domain ID
        with pytest.raises(ValidationError):
            DomainDeleteRequest(domain_id="")
        
        # Whitespace only domain ID
        with pytest.raises(ValidationError):
            DomainDeleteRequest(domain_id="   ")
    
    def test_domain_id_trimming(self):
        """Test that domain ID is trimmed."""
        request = DomainDeleteRequest(domain_id="  test-domain-id  ")
        assert request.domain_id == "test-domain-id"
    
    def test_model_dump(self):
        """Test model serialization."""
        request = DomainDeleteRequest(domain_id="test-domain-id")
        data = request.model_dump()
        
        assert data == {"domain_id": "test-domain-id"}


class TestDomainGetRequest:
    """Test DomainGetRequest model."""
    
    def test_basic_domain_get_request(self):
        """Test basic domain get request."""
        request = DomainGetRequest(domain_id="test-domain-id")
        
        assert request.domain_id == "test-domain-id"
    
    def test_domain_id_validation(self):
        """Test domain ID validation."""
        # Valid domain ID
        DomainGetRequest(domain_id="valid-domain-id")
        
        # Empty domain ID
        with pytest.raises(ValidationError):
            DomainGetRequest(domain_id="")
        
        # Whitespace only domain ID
        with pytest.raises(ValidationError):
            DomainGetRequest(domain_id="   ")
    
    def test_domain_id_trimming(self):
        """Test that domain ID is trimmed."""
        request = DomainGetRequest(domain_id="  test-domain-id  ")
        assert request.domain_id == "test-domain-id"
    
    def test_model_dump(self):
        """Test model serialization."""
        request = DomainGetRequest(domain_id="test-domain-id")
        data = request.model_dump()
        
        assert data == {"domain_id": "test-domain-id"}


class TestDomainDnsRecordsRequest:
    """Test DomainDnsRecordsRequest model."""
    
    def test_basic_dns_records_request(self):
        """Test basic DNS records request."""
        request = DomainDnsRecordsRequest(domain_id="test-domain-id")
        
        assert request.domain_id == "test-domain-id"
    
    def test_domain_id_validation(self):
        """Test domain ID validation."""
        # Valid domain ID
        DomainDnsRecordsRequest(domain_id="valid-domain-id")
        
        # Empty domain ID
        with pytest.raises(ValidationError):
            DomainDnsRecordsRequest(domain_id="")
        
        # Whitespace only domain ID
        with pytest.raises(ValidationError):
            DomainDnsRecordsRequest(domain_id="   ")
    
    def test_domain_id_trimming(self):
        """Test that domain ID is trimmed."""
        request = DomainDnsRecordsRequest(domain_id="  test-domain-id  ")
        assert request.domain_id == "test-domain-id"
    
    def test_model_dump(self):
        """Test model serialization."""
        request = DomainDnsRecordsRequest(domain_id="test-domain-id")
        data = request.model_dump()
        
        assert data == {"domain_id": "test-domain-id"}


class TestDomainVerificationRequest:
    """Test DomainVerificationRequest model."""
    
    def test_basic_verification_request(self):
        """Test basic verification request."""
        request = DomainVerificationRequest(domain_id="test-domain-id")
        
        assert request.domain_id == "test-domain-id"
    
    def test_domain_id_validation(self):
        """Test domain ID validation."""
        # Valid domain ID
        DomainVerificationRequest(domain_id="valid-domain-id")
        
        # Empty domain ID
        with pytest.raises(ValidationError):
            DomainVerificationRequest(domain_id="")
        
        # Whitespace only domain ID
        with pytest.raises(ValidationError):
            DomainVerificationRequest(domain_id="   ")
    
    def test_domain_id_trimming(self):
        """Test that domain ID is trimmed."""
        request = DomainVerificationRequest(domain_id="  test-domain-id  ")
        assert request.domain_id == "test-domain-id"
    
    def test_model_dump(self):
        """Test model serialization."""
        request = DomainVerificationRequest(domain_id="test-domain-id")
        data = request.model_dump()
        
        assert data == {"domain_id": "test-domain-id"}


class TestDomainUpdateSettingsRequest:
    """Test DomainUpdateSettingsRequest model."""
    
    def test_empty_settings_request(self):
        """Test settings request with no fields set."""
        request = DomainUpdateSettingsRequest(domain_id="test-domain-id")
        
        # All optional fields should be None
        assert request.domain_id == "test-domain-id"
        assert request.send_paused is None
        assert request.track_clicks is None
        assert request.track_opens is None
        assert request.track_unsubscribe is None
        assert request.track_content is None
        assert request.track_unsubscribe_html is None
        assert request.track_unsubscribe_plain is None
        assert request.custom_tracking_enabled is None
        assert request.custom_tracking_subdomain is None
        assert request.precedence_bulk is None
        assert request.ignore_duplicated_recipients is None
    
    def test_partial_settings_request(self):
        """Test settings request with some fields set."""
        request = DomainUpdateSettingsRequest(
            domain_id="test-domain-id",
            send_paused=True,
            track_opens=False,
            custom_tracking_enabled=True
        )
        
        assert request.domain_id == "test-domain-id"
        assert request.send_paused is True
        assert request.track_opens is False
        assert request.custom_tracking_enabled is True
        # Other fields should be None
        assert request.track_clicks is None
        assert request.track_unsubscribe is None
    
    def test_all_settings_fields(self):
        """Test settings request with all fields."""
        request = DomainUpdateSettingsRequest(
            domain_id="test-domain-id",
            send_paused=False,
            track_clicks=True,
            track_opens=True,
            track_unsubscribe=True,
            track_content=False,
            track_unsubscribe_html="<p>Unsubscribe</p>",
            track_unsubscribe_plain="Unsubscribe here",
            custom_tracking_enabled=True,
            custom_tracking_subdomain="links",
            precedence_bulk=False,
            ignore_duplicated_recipients=True
        )
        
        assert request.domain_id == "test-domain-id"
        assert request.send_paused is False
        assert request.track_clicks is True
        assert request.track_opens is True
        assert request.track_unsubscribe is True
        assert request.track_content is False
        assert request.track_unsubscribe_html == "<p>Unsubscribe</p>"
        assert request.track_unsubscribe_plain == "Unsubscribe here"
        assert request.custom_tracking_enabled is True
        assert request.custom_tracking_subdomain == "links"
        assert request.precedence_bulk is False
        assert request.ignore_duplicated_recipients is True
    
    def test_custom_tracking_subdomain_validation(self):
        """Test custom tracking subdomain validation."""
        # Valid alphanumeric subdomain
        DomainUpdateSettingsRequest(domain_id="test-domain-id", custom_tracking_subdomain="links123")
        
        # Invalid subdomain with special characters
        with pytest.raises(ValidationError):
            DomainUpdateSettingsRequest(domain_id="test-domain-id", custom_tracking_subdomain="links-123")


class TestDomainSettings:
    """Test DomainSettings model."""
    
    def test_default_domain_settings(self):
        """Test domain settings with default values."""
        settings = DomainSettings()
        
        # Check default values match API documentation
        assert settings.send_paused is False
        assert settings.track_clicks is True
        assert settings.track_opens is True
        assert settings.track_unsubscribe is True
        assert settings.track_content is True
        assert settings.custom_tracking_enabled is False
        assert settings.custom_tracking_subdomain == "email"
        assert settings.return_path_subdomain == "mta"
        assert settings.inbound_routing_enabled is False
        assert settings.inbound_routing_subdomain == "inbound"
        assert settings.precedence_bulk is False
        assert settings.ignore_duplicated_recipients is False
    
    def test_custom_domain_settings(self):
        """Test domain settings with custom values."""
        settings = DomainSettings(
            send_paused=True,
            track_clicks=False,
            custom_tracking_subdomain="links",
            precedence_bulk=True
        )
        
        assert settings.send_paused is True
        assert settings.track_clicks is False
        assert settings.custom_tracking_subdomain == "links"
        assert settings.precedence_bulk is True
        # Other fields should have defaults
        assert settings.track_opens is True
        assert settings.custom_tracking_enabled is False


class TestDomain:
    """Test Domain model."""
    
    def test_basic_domain_creation(self):
        """Test basic domain model creation."""
        domain_settings = DomainSettings()
        
        domain = Domain(
            id="test123",
            name="example.com",
            domain_settings=domain_settings,
            created_at="2023-01-01 00:00:00",
            updated_at="2023-01-01 00:00:00"
        )
        
        assert domain.id == "test123"
        assert domain.name == "example.com"
        assert domain.is_verified is False  # Default
        assert domain.is_dns_active is False  # Default
        assert isinstance(domain.domain_settings, DomainSettings)
    
    def test_domain_with_all_fields(self):
        """Test domain with all optional fields."""
        domain_settings = DomainSettings()
        
        domain = Domain(
            id="test123",
            name="example.com",
            dkim=True,
            spf=True,
            mx=False,
            tracking=True,
            is_verified=True,
            is_cname_verified=True,
            is_dns_active=True,
            is_cname_active=True,
            is_tracking_allowed=True,
            has_not_queued_messages=False,
            not_queued_messages_count=0,
            domain_settings=domain_settings,
            can={"manage": True},
            totals=[],
            created_at="2023-01-01 00:00:00",
            updated_at="2023-01-01 00:00:00"
        )
        
        assert domain.dkim is True
        assert domain.spf is True
        assert domain.mx is False
        assert domain.tracking is True
        assert domain.is_verified is True
        assert domain.is_cname_verified is True
        assert domain.is_dns_active is True


class TestDomainRecipient:
    """Test DomainRecipient model."""
    
    def test_domain_recipient_creation(self):
        """Test domain recipient creation."""
        recipient = DomainRecipient(
            id="recipient123",
            email="test@example.com",
            created_at="2023-01-01 00:00:00",
            updated_at="2023-01-01 00:00:00"
        )
        
        assert recipient.id == "recipient123"
        assert recipient.email == "test@example.com"
        assert recipient.deleted_at is None  # Default
    
    def test_domain_recipient_with_deleted_at(self):
        """Test domain recipient with deletion date."""
        recipient = DomainRecipient(
            id="recipient123",
            email="test@example.com",
            created_at="2023-01-01 00:00:00",
            updated_at="2023-01-01 00:00:00",
            deleted_at="2023-01-02 00:00:00"
        )
        
        assert recipient.deleted_at == "2023-01-02 00:00:00"


class TestDomainDnsRecord:
    """Test DomainDnsRecord model."""
    
    def test_basic_dns_record(self):
        """Test basic DNS record creation."""
        record = DomainDnsRecord(
            hostname="example.com",
            type="TXT",
            value="v=spf1 include:mailersend.net -all"
        )
        
        assert record.hostname == "example.com"
        assert record.type == "TXT"
        assert record.value == "v=spf1 include:mailersend.net -all"
        assert record.priority is None
    
    def test_dns_record_with_priority(self):
        """Test DNS record with priority (for MX records)."""
        record = DomainDnsRecord(
            hostname="example.com",
            type="MX",
            value="mailersend.net",
            priority="10"
        )
        
        assert record.priority == "10"


class TestDomainDnsRecords:
    """Test DomainDnsRecords model."""
    
    def test_empty_dns_records(self):
        """Test DNS records collection with only ID."""
        records = DomainDnsRecords(id="domain123")
        
        assert records.id == "domain123"
        assert records.spf is None
        assert records.dkim is None
        assert records.return_path is None
        assert records.custom_tracking is None
        assert records.inbound_routing is None
    
    def test_complete_dns_records(self):
        """Test DNS records with all record types."""
        spf_record = DomainDnsRecord(hostname="example.com", type="TXT", value="spf-value")
        dkim_record = DomainDnsRecord(hostname="dkim.example.com", type="TXT", value="dkim-value")
        return_path_record = DomainDnsRecord(hostname="rp.example.com", type="CNAME", value="mailersend.net")
        tracking_record = DomainDnsRecord(hostname="track.example.com", type="CNAME", value="links.mailersend.net")
        inbound_record = DomainDnsRecord(hostname="inbound.example.com", type="MX", value="inbound.mailersend.net", priority="10")
        
        records = DomainDnsRecords(
            id="domain123",
            spf=spf_record,
            dkim=dkim_record,
            return_path=return_path_record,
            custom_tracking=tracking_record,
            inbound_routing=inbound_record
        )
        
        assert records.spf == spf_record
        assert records.dkim == dkim_record
        assert records.return_path == return_path_record
        assert records.custom_tracking == tracking_record
        assert records.inbound_routing == inbound_record


class TestDomainVerificationData:
    """Test DomainVerificationData model."""
    
    def test_default_verification_data(self):
        """Test verification data with defaults."""
        verification = DomainVerificationData()
        
        # All should default to False
        assert verification.dkim is False
        assert verification.spf is False
        assert verification.mx is False
        assert verification.tracking is False
        assert verification.cname is False
        assert verification.rp_cname is False
    
    def test_custom_verification_data(self):
        """Test verification data with custom values."""
        verification = DomainVerificationData(
            dkim=True,
            spf=True,
            mx=False,
            tracking=True,
            cname=True,
            rp_cname=False
        )
        
        assert verification.dkim is True
        assert verification.spf is True
        assert verification.mx is False
        assert verification.tracking is True
        assert verification.cname is True
        assert verification.rp_cname is False


class TestDomainsModelIntegration:
    """Test integration scenarios between domain models."""
    
    def test_complete_domain_creation_from_api_data(self):
        """Test creating complete domain from API-like data."""
        api_data = {
            "id": "domain123",
            "name": "example.com",
            "dkim": True,
            "spf": True,
            "is_verified": True,
            "domain_settings": {
                "send_paused": False,
                "track_clicks": True,
                "track_opens": True,
                "custom_tracking_subdomain": "links"
            },
            "created_at": "2023-01-01 00:00:00",
            "updated_at": "2023-01-01 00:00:00"
        }
        
        domain = Domain(**api_data)
        
        assert domain.id == "domain123"
        assert domain.name == "example.com"
        assert domain.dkim is True
        assert domain.spf is True
        assert domain.is_verified is True
        assert domain.domain_settings.track_clicks is True
        assert domain.domain_settings.custom_tracking_subdomain == "links"
    
    def test_model_serialization_compatibility(self):
        """Test that models serialize correctly for API requests."""
        # List request with query params
        query_params = DomainListQueryParams(page=1, limit=10, verified=True)
        list_req = DomainListRequest(query_params=query_params)
        
        # Test query params serialization
        query_data = list_req.to_query_params()
        assert query_data["page"] == 1
        assert query_data["limit"] == 10
        assert query_data["verified"] is True
        
        # Create request
        create_req = DomainCreateRequest(
            name="test.com",
            return_path_subdomain="mail"
        )
        create_data = create_req.model_dump(exclude_none=True)
        assert create_data["name"] == "test.com"
        assert create_data["return_path_subdomain"] == "mail"
        assert "custom_tracking_subdomain" not in create_data  # Should be excluded if None
        
        # Update settings request
        settings_req = DomainUpdateSettingsRequest(
            domain_id="test-domain-id",
            track_opens=True,
            send_paused=False
        )
        settings_data = settings_req.model_dump(exclude_none=True)
        assert settings_data["domain_id"] == "test-domain-id"
        assert settings_data["track_opens"] is True
        assert settings_data["send_paused"] is False
        assert "track_clicks" not in settings_data  # Should be excluded if None
        
        # Recipients request with query params
        recipients_query_params = DomainRecipientsQueryParams(page=2, limit=50)
        recipients_req = DomainRecipientsRequest(
            domain_id="test-domain-id",
            query_params=recipients_query_params
        )
        
        # Test recipients query params serialization
        recipients_query_data = recipients_req.to_query_params()
        assert recipients_query_data["page"] == 2
        assert recipients_query_data["limit"] == 50 