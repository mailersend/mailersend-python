import pytest
from pydantic import ValidationError

from mailersend.models.inbound import (
    InboundListRequest,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
    InboundListResponse,
    InboundResponse,
    InboundRoute,
    InboundFilter,
    InboundFilterGroup,
    InboundForward,
    InboundMxValues
)


class TestInboundFilter:
    """Test InboundFilter model."""

    def test_create_valid_filter(self):
        """Test creating a valid inbound filter."""
        filter_obj = InboundFilter(
            type="catch_all",
            key=None,
            comparer=None,
            value=None
        )
        assert filter_obj.type == "catch_all"
        assert filter_obj.key is None
        assert filter_obj.comparer is None
        assert filter_obj.value is None

    def test_create_filter_with_all_fields(self):
        """Test creating a filter with all fields."""
        filter_obj = InboundFilter(
            type="match_header",
            key="X-Custom-Header",
            comparer="equal",
            value="test-value"
        )
        assert filter_obj.type == "match_header"
        assert filter_obj.key == "X-Custom-Header"
        assert filter_obj.comparer == "equal"
        assert filter_obj.value == "test-value"

    def test_invalid_filter_type(self):
        """Test validation of invalid filter type."""
        with pytest.raises(ValidationError) as exc_info:
            InboundFilter(type="invalid_type")
        assert "Type must be one of" in str(exc_info.value)

    def test_invalid_comparer(self):
        """Test validation of invalid comparer."""
        with pytest.raises(ValidationError) as exc_info:
            InboundFilter(type="catch_recipient", comparer="invalid_comparer")
        assert "Comparer must be one of" in str(exc_info.value)

    def test_valid_comparers(self):
        """Test all valid comparers."""
        valid_comparers = [
            'equal', 'not-equal', 'contains', 'not-contains',
            'starts-with', 'ends-with', 'not-starts-with', 'not-ends-with'
        ]
        for comparer in valid_comparers:
            filter_obj = InboundFilter(type="catch_recipient", comparer=comparer, value="test")
            assert filter_obj.comparer == comparer

    def test_value_length_limit(self):
        """Test value length validation."""
        long_value = "x" * 192  # Exceeds 191 character limit
        with pytest.raises(ValidationError) as exc_info:
            InboundFilter(type="catch_recipient", value=long_value)
        assert "Value cannot exceed 191 characters" in str(exc_info.value)

    def test_key_length_limit(self):
        """Test key length validation."""
        long_key = "x" * 192  # Exceeds 191 character limit
        with pytest.raises(ValidationError) as exc_info:
            InboundFilter(type="match_header", key=long_key)
        assert "Key cannot exceed 191 characters" in str(exc_info.value)

    def test_value_trimming(self):
        """Test that values are trimmed."""
        filter_obj = InboundFilter(type="catch_recipient", value="  test  ")
        assert filter_obj.value == "test"

    def test_key_trimming(self):
        """Test that keys are trimmed."""
        filter_obj = InboundFilter(type="match_header", key="  header  ")
        assert filter_obj.key == "header"


class TestInboundFilterGroup:
    """Test InboundFilterGroup model."""

    def test_create_valid_filter_group(self):
        """Test creating a valid filter group."""
        group = InboundFilterGroup(type="catch_all")
        assert group.type == "catch_all"
        assert group.filters is None

    def test_create_filter_group_with_filters(self):
        """Test creating a filter group with filters."""
        filters = [{"comparer": "equal", "value": "test"}]
        group = InboundFilterGroup(type="catch_recipient", filters=filters)
        assert group.type == "catch_recipient"
        assert group.filters == filters

    def test_invalid_filter_group_type(self):
        """Test validation of invalid filter group type."""
        with pytest.raises(ValidationError) as exc_info:
            InboundFilterGroup(type="invalid_type")
        assert "Type must be one of" in str(exc_info.value)

    def test_filters_limit(self):
        """Test filters count limit."""
        filters = [{"comparer": "equal", "value": f"test{i}"} for i in range(6)]  # 6 filters, exceeds limit
        with pytest.raises(ValidationError) as exc_info:
            InboundFilterGroup(type="catch_recipient", filters=filters)
        assert "Maximum 5 filters allowed" in str(exc_info.value)


class TestInboundForward:
    """Test InboundForward model."""

    def test_create_email_forward(self):
        """Test creating an email forward."""
        forward = InboundForward(type="email", value="test@example.com")
        assert forward.type == "email"
        assert forward.value == "test@example.com"
        assert forward.id is None
        assert forward.secret is None

    def test_create_webhook_forward(self):
        """Test creating a webhook forward."""
        forward = InboundForward(
            type="webhook",
            value="https://example.com/webhook",
            secret="secret123"
        )
        assert forward.type == "webhook"
        assert forward.value == "https://example.com/webhook"
        assert forward.secret == "secret123"

    def test_invalid_forward_type(self):
        """Test validation of invalid forward type."""
        with pytest.raises(ValidationError) as exc_info:
            InboundForward(type="invalid", value="test")
        assert "Type must be either 'email' or 'webhook'" in str(exc_info.value)

    def test_empty_value(self):
        """Test validation of empty value."""
        with pytest.raises(ValidationError) as exc_info:
            InboundForward(type="email", value="")
        assert "Value is required" in str(exc_info.value)

    def test_value_length_limit(self):
        """Test value length validation."""
        long_value = "x" * 192  # Exceeds 191 character limit
        with pytest.raises(ValidationError) as exc_info:
            InboundForward(type="email", value=long_value)
        assert "Value cannot exceed 191 characters" in str(exc_info.value)

    def test_value_trimming(self):
        """Test that values are trimmed."""
        forward = InboundForward(type="email", value="  test@example.com  ")
        assert forward.value == "test@example.com"


class TestInboundMxValues:
    """Test InboundMxValues model."""

    def test_create_mx_values(self):
        """Test creating MX values."""
        mx = InboundMxValues(priority=10, target="inbound.mailersend.net")
        assert mx.priority == 10
        assert mx.target == "inbound.mailersend.net"


class TestInboundRoute:
    """Test InboundRoute model."""

    def test_create_minimal_route(self):
        """Test creating a minimal inbound route."""
        route = InboundRoute(
            id="test-id",
            name="Test Route",
            address="test@inbound.mailersend.net",
            domain="example.com",
            enabled=True
        )
        assert route.id == "test-id"
        assert route.name == "Test Route"
        assert route.address == "test@inbound.mailersend.net"
        assert route.domain == "example.com"
        assert route.enabled is True
        assert route.dns_checked_at is None
        assert route.filters == []
        assert route.forwards == []
        assert route.priority is None
        assert route.mxValues is None

    def test_create_complete_route(self):
        """Test creating a complete inbound route."""
        filters = [InboundFilter(type="catch_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        mx_values = InboundMxValues(priority=10, target="inbound.mailersend.net")
        
        route = InboundRoute(
            id="test-id",
            name="Test Route",
            address="test@inbound.mailersend.net",
            domain="example.com",
            dns_checked_at="2023-01-01T00:00:00Z",
            enabled=True,
            filters=filters,
            forwards=forwards,
            priority=100,
            mxValues=mx_values
        )
        assert route.filters == filters
        assert route.forwards == forwards
        assert route.priority == 100
        assert route.mxValues == mx_values


class TestInboundListRequest:
    """Test InboundListRequest model."""

    def test_create_minimal_request(self):
        """Test creating a minimal list request."""
        request = InboundListRequest()
        assert request.domain_id is None
        assert request.page is None
        assert request.limit == 25  # Default value

    def test_create_request_with_all_params(self):
        """Test creating a request with all parameters."""
        request = InboundListRequest(
            domain_id="domain123",
            page=2,
            limit=50
        )
        assert request.domain_id == "domain123"
        assert request.page == 2
        assert request.limit == 50

    def test_page_validation(self):
        """Test page number validation."""
        with pytest.raises(ValidationError) as exc_info:
            InboundListRequest(page=0)
        assert "Input should be greater than or equal to 1" in str(exc_info.value)

    def test_limit_validation(self):
        """Test limit validation."""
        with pytest.raises(ValidationError) as exc_info:
            InboundListRequest(limit=5)  # Below minimum
        assert "Input should be greater than or equal to 10" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            InboundListRequest(limit=150)  # Above maximum
        assert "Input should be less than or equal to 100" in str(exc_info.value)


class TestInboundGetRequest:
    """Test InboundGetRequest model."""

    def test_create_valid_request(self):
        """Test creating a valid get request."""
        request = InboundGetRequest(inbound_id="test-id")
        assert request.inbound_id == "test-id"

    def test_empty_inbound_id(self):
        """Test validation of empty inbound ID."""
        with pytest.raises(ValidationError) as exc_info:
            InboundGetRequest(inbound_id="")
        assert "Inbound ID is required" in str(exc_info.value)

    def test_whitespace_inbound_id(self):
        """Test validation of whitespace-only inbound ID."""
        with pytest.raises(ValidationError) as exc_info:
            InboundGetRequest(inbound_id="   ")
        assert "Inbound ID is required" in str(exc_info.value)

    def test_inbound_id_trimming(self):
        """Test that inbound ID is trimmed."""
        request = InboundGetRequest(inbound_id="  test-id  ")
        assert request.inbound_id == "test-id"


class TestInboundCreateRequest:
    """Test InboundCreateRequest model."""

    def test_create_minimal_request(self):
        """Test creating a minimal create request."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        request = InboundCreateRequest(
            domain_id="domain123",
            name="Test Route",
            domain_enabled=False,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        assert request.domain_id == "domain123"
        assert request.name == "Test Route"
        assert request.domain_enabled is False
        assert request.inbound_domain is None
        assert request.inbound_priority is None

    def test_create_request_with_domain_enabled(self):
        """Test creating a request with domain enabled."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        request = InboundCreateRequest(
            domain_id="domain123",
            name="Test Route",
            domain_enabled=True,
            inbound_domain="inbound.example.com",
            inbound_priority=50,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        assert request.domain_enabled is True
        assert request.inbound_domain == "inbound.example.com"
        assert request.inbound_priority == 50

    def test_required_fields_validation(self):
        """Test validation of required fields."""
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest()
        error_str = str(exc_info.value)
        assert "domain_id" in error_str
        assert "name" in error_str
        assert "domain_enabled" in error_str

    def test_domain_enabled_conditional_validation(self):
        """Test conditional validation when domain is enabled."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        # Missing inbound_domain when domain_enabled=True
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=True,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Inbound domain is required when domain is enabled" in str(exc_info.value)

        # Missing inbound_priority when domain_enabled=True
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=True,
                inbound_domain="inbound.example.com",
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Inbound priority is required when domain is enabled" in str(exc_info.value)

    def test_name_validation(self):
        """Test name field validation."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        # Empty name
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="",
                domain_enabled=False,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Name is required" in str(exc_info.value)

        # Name too long
        long_name = "x" * 192
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name=long_name,
                domain_enabled=False,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Name cannot exceed 191 characters" in str(exc_info.value)

    def test_forwards_validation(self):
        """Test forwards validation."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        
        # Empty forwards
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=False,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=[]
            )
        assert "At least one forward is required" in str(exc_info.value)

        # Too many forwards
        forwards = [InboundForward(type="email", value=f"test{i}@example.com") for i in range(6)]
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=False,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Maximum 5 forwards allowed" in str(exc_info.value)

        # Duplicate forward values
        forwards = [
            InboundForward(type="email", value="test@example.com"),
            InboundForward(type="webhook", value="test@example.com")  # Same value
        ]
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=False,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Forward values must be distinct" in str(exc_info.value)

    def test_priority_validation(self):
        """Test priority validation."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        # Priority below minimum
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=True,
                inbound_domain="inbound.example.com",
                inbound_priority=-1,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Input should be greater than or equal to 0" in str(exc_info.value)

        # Priority above maximum
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=True,
                inbound_domain="inbound.example.com",
                inbound_priority=101,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Input should be less than or equal to 100" in str(exc_info.value)

    def test_catch_type_validation(self):
        """Test catch type validation."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=False,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards,
                catch_type="invalid"
            )
        assert "Catch type must be 'all' or 'one'" in str(exc_info.value)

    def test_match_type_validation(self):
        """Test match type validation."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        with pytest.raises(ValidationError) as exc_info:
            InboundCreateRequest(
                domain_id="domain123",
                name="Test Route",
                domain_enabled=False,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards,
                match_type="invalid"
            )
        assert "Match type must be 'all' or 'one'" in str(exc_info.value)


class TestInboundUpdateRequest:
    """Test InboundUpdateRequest model."""

    def test_create_valid_request(self):
        """Test creating a valid update request."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        request = InboundUpdateRequest(
            inbound_id="test-id",
            name="Updated Route",
            domain_enabled=True,
            inbound_domain="inbound.example.com",
            inbound_priority=75,
            catch_filter=catch_filter,
            match_filter=match_filter,
            forwards=forwards
        )
        assert request.inbound_id == "test-id"
        assert request.name == "Updated Route"
        assert request.domain_enabled is True
        assert request.inbound_domain == "inbound.example.com"
        assert request.inbound_priority == 75

    def test_conditional_validation_like_create(self):
        """Test that update request has same conditional validation as create."""
        catch_filter = [InboundFilterGroup(type="catch_all")]
        match_filter = [InboundFilterGroup(type="match_all")]
        forwards = [InboundForward(type="email", value="test@example.com")]
        
        # Missing inbound_domain when domain_enabled=True
        with pytest.raises(ValidationError) as exc_info:
            InboundUpdateRequest(
                inbound_id="test-id",
                name="Test Route",
                domain_enabled=True,
                catch_filter=catch_filter,
                match_filter=match_filter,
                forwards=forwards
            )
        assert "Inbound domain is required when domain is enabled" in str(exc_info.value)


class TestInboundDeleteRequest:
    """Test InboundDeleteRequest model."""

    def test_create_valid_request(self):
        """Test creating a valid delete request."""
        request = InboundDeleteRequest(inbound_id="test-id")
        assert request.inbound_id == "test-id"

    def test_empty_inbound_id(self):
        """Test validation of empty inbound ID."""
        with pytest.raises(ValidationError) as exc_info:
            InboundDeleteRequest(inbound_id="")
        assert "Inbound ID is required" in str(exc_info.value)


class TestInboundListResponse:
    """Test InboundListResponse model."""

    def test_create_empty_response(self):
        """Test creating an empty response."""
        response = InboundListResponse()
        assert response.data == []

    def test_create_response_with_data(self):
        """Test creating a response with data."""
        route = InboundRoute(
            id="test-id",
            name="Test Route",
            address="test@inbound.mailersend.net",
            domain="example.com",
            enabled=True
        )
        response = InboundListResponse(data=[route])
        assert len(response.data) == 1
        assert response.data[0] == route


class TestInboundResponse:
    """Test InboundResponse model."""

    def test_create_response(self):
        """Test creating a response."""
        route = InboundRoute(
            id="test-id",
            name="Test Route",
            address="test@inbound.mailersend.net",
            domain="example.com",
            enabled=True
        )
        response = InboundResponse(data=route)
        assert response.data == route 