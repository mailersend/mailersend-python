"""Unit tests for Recipients models."""
import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.recipients import (
    # Query Parameters Models
    RecipientsListQueryParams,
    SuppressionListQueryParams,
    # Request Models
    RecipientsListRequest,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
    # Response Models
    RecipientDomain,
    Recipient,
    BlocklistEntry,
    HardBounce,
    SpamComplaint,
    Unsubscribe,
    OnHoldEntry,
    RecipientsListResponse,
    RecipientResponse,
    BlocklistResponse,
    HardBouncesResponse,
    SpamComplaintsResponse,
    UnsubscribesResponse,
    OnHoldResponse,
    SuppressionAddResponse,
)


class TestRecipientsListQueryParams:
    """Test RecipientsListQueryParams model."""
    
    def test_create_with_defaults(self):
        """Test creating query params with default values."""
        params = RecipientsListQueryParams()
        
        assert params.domain_id is None
        assert params.page == 1
        assert params.limit == 25
    
    def test_create_with_all_params(self):
        """Test creating query params with all parameters."""
        params = RecipientsListQueryParams(
            domain_id="domain123",
            page=2,
            limit=50,
        )
        
        assert params.domain_id == "domain123"
        assert params.page == 2
        assert params.limit == 50
    
    def test_domain_id_validation(self):
        """Test domain_id validation and cleaning."""
        params = RecipientsListQueryParams(domain_id="  domain123  ")
        assert params.domain_id == "domain123"
        
        params = RecipientsListQueryParams(domain_id=None)
        assert params.domain_id is None
    
    def test_page_validation(self):
        """Test page validation."""
        # Valid page
        params = RecipientsListQueryParams(page=1)
        assert params.page == 1
        
        # Invalid page
        with pytest.raises(ValidationError) as exc_info:
            RecipientsListQueryParams(page=0)
        assert "greater than or equal to 1" in str(exc_info.value)
    
    def test_limit_validation(self):
        """Test limit validation."""
        # Valid limits
        params = RecipientsListQueryParams(limit=10)
        assert params.limit == 10
        
        params = RecipientsListQueryParams(limit=100)
        assert params.limit == 100
        
        # Invalid limits
        with pytest.raises(ValidationError) as exc_info:
            RecipientsListQueryParams(limit=9)
        assert "greater than or equal to 10" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            RecipientsListQueryParams(limit=101)
        assert "less than or equal to 100" in str(exc_info.value)
    
    def test_to_query_params(self):
        """Test converting to query parameters."""
        # With all params
        params = RecipientsListQueryParams(
            domain_id="domain123",
            page=2,
            limit=50,
        )
        result = params.to_query_params()
        
        expected = {
            "domain_id": "domain123",
            "page": 2,
            "limit": 50,
        }
        assert result == expected
        
        # With defaults (no domain_id)
        params = RecipientsListQueryParams()
        result = params.to_query_params()
        
        expected = {
            "page": 1,
            "limit": 25,
        }
        assert result == expected


class TestSuppressionListQueryParams:
    """Test SuppressionListQueryParams model."""
    
    def test_create_with_defaults(self):
        """Test creating query params with default values."""
        params = SuppressionListQueryParams()
        
        assert params.domain_id is None
        assert params.page == 1
        assert params.limit == 25
    
    def test_create_with_all_params(self):
        """Test creating query params with all parameters."""
        params = SuppressionListQueryParams(
            domain_id="domain123",
            page=3,
            limit=75,
        )
        
        assert params.domain_id == "domain123"
        assert params.page == 3
        assert params.limit == 75
    
    def test_to_query_params(self):
        """Test converting to query parameters."""
        # With all params
        params = SuppressionListQueryParams(
            domain_id="domain123",
            page=3,
            limit=75,
        )
        result = params.to_query_params()
        
        expected = {
            "domain_id": "domain123",
            "page": 3,
            "limit": 75,
        }
        assert result == expected


class TestRecipientsListRequest:
    """Test RecipientsListRequest model."""
    
    def test_create_with_defaults(self):
        """Test creating request with default values."""
        request = RecipientsListRequest()
        
        assert request.query_params.domain_id is None
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
    
    def test_create_with_query_params(self):
        """Test creating request with query params."""
        query_params = RecipientsListQueryParams(
            domain_id="domain123",
            page=2,
            limit=50,
        )
        request = RecipientsListRequest(query_params=query_params)
        
        assert request.query_params.domain_id == "domain123"
        assert request.query_params.page == 2
        assert request.query_params.limit == 50
    
    def test_to_query_params(self):
        """Test converting to query parameters."""
        query_params = RecipientsListQueryParams(
            domain_id="domain123",
            page=2,
            limit=50,
        )
        request = RecipientsListRequest(query_params=query_params)
        result = request.to_query_params()
        
        expected = {
            "domain_id": "domain123",
            "page": 2,
            "limit": 50,
        }
        assert result == expected


class TestRecipientGetRequest:
    """Test RecipientGetRequest model."""
    
    def test_create_valid(self):
        """Test creating valid request."""
        request = RecipientGetRequest(recipient_id="recipient123")
        assert request.recipient_id == "recipient123"
    
    def test_recipient_id_validation(self):
        """Test recipient_id validation and cleaning."""
        request = RecipientGetRequest(recipient_id="  recipient123  ")
        assert request.recipient_id == "recipient123"
        
        # Empty recipient_id
        with pytest.raises(ValidationError) as exc_info:
            RecipientGetRequest(recipient_id="")
        assert "recipient_id cannot be empty" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            RecipientGetRequest(recipient_id="   ")
        assert "recipient_id cannot be empty" in str(exc_info.value)


class TestRecipientDeleteRequest:
    """Test RecipientDeleteRequest model."""
    
    def test_create_valid(self):
        """Test creating valid request."""
        request = RecipientDeleteRequest(recipient_id="recipient123")
        assert request.recipient_id == "recipient123"
    
    def test_recipient_id_validation(self):
        """Test recipient_id validation and cleaning."""
        request = RecipientDeleteRequest(recipient_id="  recipient123  ")
        assert request.recipient_id == "recipient123"
        
        # Empty recipient_id
        with pytest.raises(ValidationError) as exc_info:
            RecipientDeleteRequest(recipient_id="")
        assert "recipient_id cannot be empty" in str(exc_info.value)


class TestSuppressionListRequest:
    """Test SuppressionListRequest model."""
    
    def test_create_with_defaults(self):
        """Test creating request with default values."""
        request = SuppressionListRequest()
        
        assert request.query_params.domain_id is None
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
    
    def test_create_with_query_params(self):
        """Test creating request with query params."""
        query_params = SuppressionListQueryParams(
            domain_id="domain123",
            page=3,
            limit=75,
        )
        request = SuppressionListRequest(query_params=query_params)
        
        assert request.query_params.domain_id == "domain123"
        assert request.query_params.page == 3
        assert request.query_params.limit == 75
    
    def test_to_query_params(self):
        """Test converting to query parameters."""
        query_params = SuppressionListQueryParams(
            domain_id="domain123",
            page=3,
            limit=75,
        )
        request = SuppressionListRequest(query_params=query_params)
        result = request.to_query_params()
        
        expected = {
            "domain_id": "domain123",
            "page": 3,
            "limit": 75,
        }
        assert result == expected


class TestSuppressionAddRequest:
    """Test SuppressionAddRequest model."""
    
    def test_create_with_recipients(self):
        """Test creating request with recipients."""
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com", "user@example.com"],
        )
        
        assert request.domain_id == "domain123"
        assert request.recipients == ["test@example.com", "user@example.com"]
        assert request.patterns is None
    
    def test_create_with_patterns(self):
        """Test creating request with patterns."""
        request = SuppressionAddRequest(
            domain_id="domain123",
            patterns=[".*@example.com", ".*@test.com"],
        )
        
        assert request.domain_id == "domain123"
        assert request.patterns == [".*@example.com", ".*@test.com"]
        assert request.recipients is None
    
    def test_create_with_both(self):
        """Test creating request with both recipients and patterns."""
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
            patterns=[".*@example.com"],
        )
        
        assert request.domain_id == "domain123"
        assert request.recipients == ["test@example.com"]
        assert request.patterns == [".*@example.com"]
    
    def test_domain_id_validation(self):
        """Test domain_id validation."""
        request = SuppressionAddRequest(
            domain_id="  domain123  ",
            recipients=["test@example.com"],
        )
        assert request.domain_id == "domain123"
        
        # Empty domain_id
        with pytest.raises(ValidationError) as exc_info:
            SuppressionAddRequest(
                domain_id="",
                recipients=["test@example.com"],
            )
        assert "domain_id cannot be empty" in str(exc_info.value)
    
    def test_recipients_validation(self):
        """Test recipients validation."""
        # Valid recipients
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com", "user@example.com"],
        )
        assert request.recipients == ["test@example.com", "user@example.com"]
        
        # Clean recipients
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["  test@example.com  ", "user@example.com"],
        )
        assert request.recipients == ["test@example.com", "user@example.com"]
        
        # Empty recipients list
        with pytest.raises(ValidationError) as exc_info:
            SuppressionAddRequest(
                domain_id="domain123",
                recipients=[],
            )
        assert "recipients list cannot be empty if provided" in str(exc_info.value)
        
        # Empty recipient email
        with pytest.raises(ValidationError) as exc_info:
            SuppressionAddRequest(
                domain_id="domain123",
                recipients=["test@example.com", ""],
            )
        assert "recipient email cannot be empty" in str(exc_info.value)
    
    def test_patterns_validation(self):
        """Test patterns validation."""
        # Valid patterns
        request = SuppressionAddRequest(
            domain_id="domain123",
            patterns=[".*@example.com", ".*@test.com"],
        )
        assert request.patterns == [".*@example.com", ".*@test.com"]
        
        # Clean patterns
        request = SuppressionAddRequest(
            domain_id="domain123",
            patterns=["  .*@example.com  ", ".*@test.com"],
        )
        assert request.patterns == [".*@example.com", ".*@test.com"]
        
        # Empty patterns list
        with pytest.raises(ValidationError) as exc_info:
            SuppressionAddRequest(
                domain_id="domain123",
                patterns=[],
            )
        assert "patterns list cannot be empty if provided" in str(exc_info.value)
        
        # Empty pattern
        with pytest.raises(ValidationError) as exc_info:
            SuppressionAddRequest(
                domain_id="domain123",
                patterns=[".*@example.com", ""],
            )
        assert "pattern cannot be empty" in str(exc_info.value)


class TestSuppressionDeleteRequest:
    """Test SuppressionDeleteRequest model."""
    
    def test_create_with_ids(self):
        """Test creating request with IDs."""
        request = SuppressionDeleteRequest(
            domain_id="domain123",
            ids=["id1", "id2", "id3"],
        )
        
        assert request.domain_id == "domain123"
        assert request.ids == ["id1", "id2", "id3"]
        assert request.all is None
    
    def test_create_with_all_flag(self):
        """Test creating request with all flag."""
        request = SuppressionDeleteRequest(
            domain_id="domain123",
            all=True,
        )
        
        assert request.domain_id == "domain123"
        assert request.all is True
        assert request.ids is None
    
    def test_create_without_domain_id(self):
        """Test creating request without domain_id (for on-hold)."""
        request = SuppressionDeleteRequest(
            ids=["id1", "id2"],
        )
        
        assert request.domain_id is None
        assert request.ids == ["id1", "id2"]
    
    def test_ids_validation(self):
        """Test IDs validation."""
        # Valid IDs
        request = SuppressionDeleteRequest(ids=["id1", "id2"])
        assert request.ids == ["id1", "id2"]
        
        # Clean IDs
        request = SuppressionDeleteRequest(ids=["  id1  ", "id2"])
        assert request.ids == ["id1", "id2"]
        
        # Empty IDs list
        with pytest.raises(ValidationError) as exc_info:
            SuppressionDeleteRequest(ids=[])
        assert "ids list cannot be empty if provided" in str(exc_info.value)
        
        # Empty ID
        with pytest.raises(ValidationError) as exc_info:
            SuppressionDeleteRequest(ids=["id1", ""])
        assert "id cannot be empty" in str(exc_info.value)


class TestResponseModels:
    """Test response models."""
    
    def test_recipient_domain(self):
        """Test RecipientDomain model."""
        domain_data = {
            "id": "domain123",
            "name": "example.com",
            "created_at": "2020-06-10T10:09:56Z",
            "updated_at": "2020-06-10T10:09:56Z",
            "dkim": True,
            "spf": True,
            "mx": False,
            "tracking": False,
            "is_verified": True,
        }
        
        domain = RecipientDomain(**domain_data)
        
        assert domain.id == "domain123"
        assert domain.name == "example.com"
        assert isinstance(domain.created_at, datetime)
        assert isinstance(domain.updated_at, datetime)
        assert domain.dkim is True
        assert domain.spf is True
        assert domain.mx is False
        assert domain.tracking is False
        assert domain.is_verified is True
    
    def test_recipient(self):
        """Test Recipient model."""
        recipient_data = {
            "id": "recipient123",
            "email": "test@example.com",
            "created_at": "2020-06-10T10:09:56Z",
            "updated_at": "2020-06-10T10:09:56Z",
            "deleted_at": "",
            "emails": [],
            "domain": {
                "id": "domain123",
                "name": "example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
            },
        }
        
        recipient = Recipient(**recipient_data)
        
        assert recipient.id == "recipient123"
        assert recipient.email == "test@example.com"
        assert isinstance(recipient.created_at, datetime)
        assert isinstance(recipient.updated_at, datetime)
        assert recipient.deleted_at == ""
        assert recipient.emails == []
        assert isinstance(recipient.domain, RecipientDomain)
        assert recipient.domain.id == "domain123"
    
    def test_blocklist_entry(self):
        """Test BlocklistEntry model."""
        entry_data = {
            "id": "entry123",
            "type": "pattern",
            "pattern": ".*@example.com",
            "created_at": "2020-06-10T10:09:56Z",
            "updated_at": "2020-06-10T10:09:56Z",
            "domain": {
                "id": "domain123",
                "name": "example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
            },
        }
        
        entry = BlocklistEntry(**entry_data)
        
        assert entry.id == "entry123"
        assert entry.type == "pattern"
        assert entry.pattern == ".*@example.com"
        assert isinstance(entry.created_at, datetime)
        assert isinstance(entry.updated_at, datetime)
        assert isinstance(entry.domain, RecipientDomain)
    
    def test_hard_bounce(self):
        """Test HardBounce model."""
        bounce_data = {
            "id": "bounce123",
            "reason": "Unknown reason",
            "created_at": "2020-06-10T10:09:56Z",
            "recipient": {
                "id": "recipient123",
                "email": "test@example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
                "deleted_at": "",
                "domain": {
                    "id": "domain123",
                    "name": "example.com",
                    "created_at": "2020-06-10T10:09:56Z",
                    "updated_at": "2020-06-10T10:09:56Z",
                },
            },
        }
        
        bounce = HardBounce(**bounce_data)
        
        assert bounce.id == "bounce123"
        assert bounce.reason == "Unknown reason"
        assert isinstance(bounce.created_at, datetime)
        assert isinstance(bounce.recipient, Recipient)
        assert bounce.recipient.id == "recipient123"
    
    def test_spam_complaint(self):
        """Test SpamComplaint model."""
        complaint_data = {
            "id": "complaint123",
            "created_at": "2020-06-10T10:09:56Z",
            "recipient": {
                "id": "recipient123",
                "email": "test@example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
                "deleted_at": "",
                "domain": {
                    "id": "domain123",
                    "name": "example.com",
                    "created_at": "2020-06-10T10:09:56Z",
                    "updated_at": "2020-06-10T10:09:56Z",
                },
            },
        }
        
        complaint = SpamComplaint(**complaint_data)
        
        assert complaint.id == "complaint123"
        assert isinstance(complaint.created_at, datetime)
        assert isinstance(complaint.recipient, Recipient)
        assert complaint.recipient.id == "recipient123"
    
    def test_unsubscribe(self):
        """Test Unsubscribe model."""
        unsubscribe_data = {
            "id": "unsubscribe123",
            "reason": "NEVER_SIGNED",
            "readable_reason": "I never signed up for this mailing list",
            "created_at": "2020-06-10T10:09:56Z",
            "recipient": {
                "id": "recipient123",
                "email": "test@example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
                "deleted_at": "",
                "domain": {
                    "id": "domain123",
                    "name": "example.com",
                    "created_at": "2020-06-10T10:09:56Z",
                    "updated_at": "2020-06-10T10:09:56Z",
                },
            },
        }
        
        unsubscribe = Unsubscribe(**unsubscribe_data)
        
        assert unsubscribe.id == "unsubscribe123"
        assert unsubscribe.reason == "NEVER_SIGNED"
        assert unsubscribe.readable_reason == "I never signed up for this mailing list"
        assert isinstance(unsubscribe.created_at, datetime)
        assert isinstance(unsubscribe.recipient, Recipient)
    
    def test_on_hold_entry(self):
        """Test OnHoldEntry model."""
        hold_data = {
            "id": "hold123",
            "created_at": "2020-06-10T10:09:56Z",
            "on_hold_until": "2020-06-13T10:09:56Z",
            "email": "test@example.com",
            "recipient": {
                "id": "recipient123",
                "email": "test@example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
                "deleted_at": "",
                "domain": {
                    "id": "domain123",
                    "name": "example.com",
                    "created_at": "2020-06-10T10:09:56Z",
                    "updated_at": "2020-06-10T10:09:56Z",
                },
            },
        }
        
        hold = OnHoldEntry(**hold_data)
        
        assert hold.id == "hold123"
        assert isinstance(hold.created_at, datetime)
        assert isinstance(hold.on_hold_until, datetime)
        assert hold.email == "test@example.com"
        assert isinstance(hold.recipient, Recipient)
    
    def test_recipients_list_response(self):
        """Test RecipientsListResponse model."""
        response_data = {
            "data": [
                {
                    "id": "recipient123",
                    "email": "test@example.com",
                    "created_at": "2020-06-10T10:09:56Z",
                    "updated_at": "2020-06-10T10:09:56Z",
                    "deleted_at": "",
                },
            ],
            "links": {
                "first": "https://api.mailersend.com/v1/recipients?page=1",
                "last": "https://api.mailersend.com/v1/recipients?page=1",
                "prev": None,
                "next": None,
            },
            "meta": {
                "current_page": 1,
                "from": 1,
                "last_page": 1,
                "per_page": 25,
                "to": 1,
                "total": 1,
            },
        }
        
        response = RecipientsListResponse(**response_data)
        
        assert len(response.data) == 1
        assert isinstance(response.data[0], Recipient)
        assert response.data[0].id == "recipient123"
        assert response.links is not None
        assert response.meta is not None
    
    def test_recipient_response(self):
        """Test RecipientResponse model."""
        response_data = {
            "data": {
                "id": "recipient123",
                "email": "test@example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
                "deleted_at": "",
            },
        }
        
        response = RecipientResponse(**response_data)
        
        assert isinstance(response.data, Recipient)
        assert response.data.id == "recipient123" 