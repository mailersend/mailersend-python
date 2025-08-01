import pytest
from pydantic import ValidationError

from mailersend.models.identities import (
    IdentityListRequest,
    IdentityListQueryParams,
    IdentityCreateRequest,
    IdentityGetRequest,
    IdentityGetByEmailRequest,
    IdentityUpdateRequest,
    IdentityUpdateByEmailRequest,
    IdentityDeleteRequest,
    IdentityDeleteByEmailRequest,
)


class TestIdentityListQueryParams:
    """Test IdentityListQueryParams model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        query_params = IdentityListQueryParams()
        assert query_params.page == 1
        assert query_params.limit == 25
        assert query_params.domain_id is None

    def test_with_all_parameters(self):
        """Test with all parameters provided."""
        query_params = IdentityListQueryParams(page=2, limit=50, domain_id="domain123")
        assert query_params.page == 2
        assert query_params.limit == 50
        assert query_params.domain_id == "domain123"

    def test_page_validation_valid(self):
        """Test page validation with valid values."""
        query_params = IdentityListQueryParams(page=1)
        assert query_params.page == 1

        query_params = IdentityListQueryParams(page=100)
        assert query_params.page == 100

    def test_page_validation_invalid(self):
        """Test page validation with invalid values."""
        with pytest.raises(ValidationError):
            IdentityListQueryParams(page=0)

        with pytest.raises(ValidationError):
            IdentityListQueryParams(page=-1)

    def test_limit_validation_valid_range(self):
        """Test limit validation with valid values."""
        query_params = IdentityListQueryParams(limit=10)
        assert query_params.limit == 10

        query_params = IdentityListQueryParams(limit=100)
        assert query_params.limit == 100

        query_params = IdentityListQueryParams(limit=50)
        assert query_params.limit == 50

    def test_limit_validation_invalid_range(self):
        """Test limit validation with invalid values."""
        with pytest.raises(ValidationError):
            IdentityListQueryParams(limit=9)

        with pytest.raises(ValidationError):
            IdentityListQueryParams(limit=101)

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default values."""
        query_params = IdentityListQueryParams()
        result = query_params.to_query_params()
        expected = {"page": 1, "limit": 25}
        assert result == expected

    def test_to_query_params_with_all_values(self):
        """Test to_query_params with all values set."""
        query_params = IdentityListQueryParams(page=3, limit=75, domain_id="domain456")
        result = query_params.to_query_params()
        expected = {"page": 3, "limit": 75, "domain_id": "domain456"}
        assert result == expected

    def test_to_query_params_excludes_none_values(self):
        """Test to_query_params excludes None values."""
        query_params = IdentityListQueryParams(page=2, limit=30, domain_id=None)
        result = query_params.to_query_params()
        expected = {"page": 2, "limit": 30}
        assert result == expected


class TestIdentityListRequest:
    """Test IdentityListRequest model."""

    def test_with_query_params(self):
        """Test with query params object."""
        query_params = IdentityListQueryParams(page=2, limit=50, domain_id="domain123")
        request = IdentityListRequest(query_params=query_params)
        assert request.query_params == query_params

    def test_to_query_params_delegation(self):
        """Test to_query_params delegates to query_params object."""
        query_params = IdentityListQueryParams(page=3, limit=75, domain_id="domain456")
        request = IdentityListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = query_params.to_query_params()
        assert result == expected

    def test_to_query_params_with_defaults(self):
        """Test to_query_params with default query params."""
        query_params = IdentityListQueryParams()
        request = IdentityListRequest(query_params=query_params)
        result = request.to_query_params()
        expected = {"page": 1, "limit": 25}
        assert result == expected

    def test_serialization(self):
        """Test model serialization."""
        query_params = IdentityListQueryParams(page=2, limit=50, domain_id="domain123")
        request = IdentityListRequest(query_params=query_params)
        data = request.model_dump()
        assert data == {
            "query_params": {"page": 2, "limit": 50, "domain_id": "domain123"}
        }


class TestIdentityCreateRequest:
    """Test IdentityCreateRequest model."""

    def test_required_fields(self):
        """Test with all required fields."""
        request = IdentityCreateRequest(
            domain_id="domain123", name="John Doe", email="john@example.com"
        )
        assert request.domain_id == "domain123"
        assert request.name == "John Doe"
        assert request.email == "john@example.com"
        assert request.reply_to_email is None
        assert request.reply_to_name is None
        assert request.add_note is None
        assert request.personal_note is None

    def test_with_all_fields(self):
        """Test with all fields provided."""
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            reply_to_email="reply@example.com",
            reply_to_name="Reply Name",
            add_note=True,
            personal_note="Personal note content",
        )
        assert request.domain_id == "domain123"
        assert request.name == "John Doe"
        assert request.email == "john@example.com"
        assert request.reply_to_email == "reply@example.com"
        assert request.reply_to_name == "Reply Name"
        assert request.add_note is True
        assert request.personal_note == "Personal note content"

    def test_domain_id_validation(self):
        """Test domain ID validation."""
        # Valid domain ID
        request = IdentityCreateRequest(
            domain_id="domain123", name="John Doe", email="john@example.com"
        )
        assert request.domain_id == "domain123"

        # Empty domain ID
        with pytest.raises(ValidationError, match="Domain ID is required"):
            IdentityCreateRequest(
                domain_id="", name="John Doe", email="john@example.com"
            )

        # Whitespace domain ID
        with pytest.raises(ValidationError, match="Domain ID is required"):
            IdentityCreateRequest(
                domain_id="   ", name="John Doe", email="john@example.com"
            )

    def test_domain_id_trimming(self):
        """Test domain ID is trimmed."""
        request = IdentityCreateRequest(
            domain_id="  domain123  ", name="John Doe", email="john@example.com"
        )
        assert request.domain_id == "domain123"

    def test_name_validation(self):
        """Test name validation."""
        # Valid name
        request = IdentityCreateRequest(
            domain_id="domain123", name="John Doe", email="john@example.com"
        )
        assert request.name == "John Doe"

        # Empty name
        with pytest.raises(ValidationError, match="Name is required"):
            IdentityCreateRequest(
                domain_id="domain123", name="", email="john@example.com"
            )

        # Whitespace name
        with pytest.raises(ValidationError, match="Name is required"):
            IdentityCreateRequest(
                domain_id="domain123", name="   ", email="john@example.com"
            )

        # Name too long
        long_name = "a" * 192
        with pytest.raises(
            ValidationError, match="Name must be 191 characters or less"
        ):
            IdentityCreateRequest(
                domain_id="domain123", name=long_name, email="john@example.com"
            )

    def test_name_trimming(self):
        """Test name is trimmed."""
        request = IdentityCreateRequest(
            domain_id="domain123", name="  John Doe  ", email="john@example.com"
        )
        assert request.name == "John Doe"

    def test_email_validation(self):
        """Test email validation."""
        # Valid email
        request = IdentityCreateRequest(
            domain_id="domain123", name="John Doe", email="john@example.com"
        )
        assert request.email == "john@example.com"

        # Empty email
        with pytest.raises(ValidationError, match="Email is required"):
            IdentityCreateRequest(domain_id="domain123", name="John Doe", email="")

        # Whitespace email
        with pytest.raises(ValidationError, match="Email is required"):
            IdentityCreateRequest(domain_id="domain123", name="John Doe", email="   ")

        # Invalid email format
        with pytest.raises(ValidationError, match="Invalid email format"):
            IdentityCreateRequest(
                domain_id="domain123", name="John Doe", email="invalid-email"
            )

        # Email too long
        long_email = "a" * 180 + "@example.com"  # Total > 191 chars
        with pytest.raises(
            ValidationError, match="Email must be 191 characters or less"
        ):
            IdentityCreateRequest(
                domain_id="domain123", name="John Doe", email=long_email
            )

    def test_email_trimming(self):
        """Test email is trimmed."""
        request = IdentityCreateRequest(
            domain_id="domain123", name="John Doe", email="  john@example.com  "
        )
        assert request.email == "john@example.com"

    def test_reply_to_email_validation(self):
        """Test reply-to email validation."""
        # Valid reply-to email
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            reply_to_email="reply@example.com",
        )
        assert request.reply_to_email == "reply@example.com"

        # Invalid reply-to email format
        with pytest.raises(ValidationError, match="Invalid reply-to email format"):
            IdentityCreateRequest(
                domain_id="domain123",
                name="John Doe",
                email="john@example.com",
                reply_to_email="invalid-email",
            )

        # Reply-to email too long
        long_email = "a" * 180 + "@example.com"  # Total > 191 chars
        with pytest.raises(
            ValidationError, match="Reply-to email must be 191 characters or less"
        ):
            IdentityCreateRequest(
                domain_id="domain123",
                name="John Doe",
                email="john@example.com",
                reply_to_email=long_email,
            )

    def test_reply_to_email_trimming(self):
        """Test reply-to email is trimmed."""
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            reply_to_email="  reply@example.com  ",
        )
        assert request.reply_to_email == "reply@example.com"

    def test_personal_note_validation(self):
        """Test personal note validation."""
        # Valid personal note
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            personal_note="This is a personal note",
        )
        assert request.personal_note == "This is a personal note"

        # Personal note too long
        long_note = "a" * 251
        with pytest.raises(
            ValidationError, match="Personal note must be 250 characters or less"
        ):
            IdentityCreateRequest(
                domain_id="domain123",
                name="John Doe",
                email="john@example.com",
                personal_note=long_note,
            )

    def test_serialization(self):
        """Test model serialization."""
        request = IdentityCreateRequest(
            domain_id="domain123",
            name="John Doe",
            email="john@example.com",
            reply_to_email="reply@example.com",
            reply_to_name="Reply Name",
            add_note=True,
            personal_note="Personal note",
        )
        data = request.model_dump()
        assert data == {
            "domain_id": "domain123",
            "name": "John Doe",
            "email": "john@example.com",
            "reply_to_email": "reply@example.com",
            "reply_to_name": "Reply Name",
            "add_note": True,
            "personal_note": "Personal note",
        }


class TestIdentityGetRequest:
    """Test IdentityGetRequest model."""

    def test_valid_identity_id(self):
        """Test with valid identity ID."""
        request = IdentityGetRequest(identity_id="identity123")
        assert request.identity_id == "identity123"

    def test_identity_id_validation(self):
        """Test identity ID validation."""
        # Empty identity ID
        with pytest.raises(ValidationError, match="Identity ID is required"):
            IdentityGetRequest(identity_id="")

        # Whitespace identity ID
        with pytest.raises(ValidationError, match="Identity ID is required"):
            IdentityGetRequest(identity_id="   ")

    def test_identity_id_trimming(self):
        """Test identity ID is trimmed."""
        request = IdentityGetRequest(identity_id="  identity123  ")
        assert request.identity_id == "identity123"

    def test_serialization(self):
        """Test model serialization."""
        request = IdentityGetRequest(identity_id="identity123")
        data = request.model_dump()
        assert data == {"identity_id": "identity123"}


class TestIdentityGetByEmailRequest:
    """Test IdentityGetByEmailRequest model."""

    def test_valid_email(self):
        """Test with valid email."""
        request = IdentityGetByEmailRequest(email="john@example.com")
        assert request.email == "john@example.com"

    def test_email_validation(self):
        """Test email validation."""
        # Empty email
        with pytest.raises(ValidationError, match="Email is required"):
            IdentityGetByEmailRequest(email="")

        # Whitespace email
        with pytest.raises(ValidationError, match="Email is required"):
            IdentityGetByEmailRequest(email="   ")

        # Invalid email format
        with pytest.raises(ValidationError, match="Invalid email format"):
            IdentityGetByEmailRequest(email="invalid-email")

    def test_email_trimming(self):
        """Test email is trimmed."""
        request = IdentityGetByEmailRequest(email="  john@example.com  ")
        assert request.email == "john@example.com"

    def test_serialization(self):
        """Test model serialization."""
        request = IdentityGetByEmailRequest(email="john@example.com")
        data = request.model_dump()
        assert data == {"email": "john@example.com"}


class TestIdentityUpdateRequest:
    """Test IdentityUpdateRequest model."""

    def test_required_identity_id_only(self):
        """Test with only required identity ID."""
        request = IdentityUpdateRequest(identity_id="identity123")
        assert request.identity_id == "identity123"
        assert request.name is None
        assert request.reply_to_email is None
        assert request.reply_to_name is None
        assert request.add_note is None
        assert request.personal_note is None

    def test_with_all_fields(self):
        """Test with all fields provided."""
        request = IdentityUpdateRequest(
            identity_id="identity123",
            name="Updated Name",
            reply_to_email="updated@example.com",
            reply_to_name="Updated Reply Name",
            add_note=False,
            personal_note="Updated note",
        )
        assert request.identity_id == "identity123"
        assert request.name == "Updated Name"
        assert request.reply_to_email == "updated@example.com"
        assert request.reply_to_name == "Updated Reply Name"
        assert request.add_note is False
        assert request.personal_note == "Updated note"

    def test_identity_id_validation(self):
        """Test identity ID validation."""
        # Empty identity ID
        with pytest.raises(ValidationError, match="Identity ID is required"):
            IdentityUpdateRequest(identity_id="")

        # Whitespace identity ID
        with pytest.raises(ValidationError, match="Identity ID is required"):
            IdentityUpdateRequest(identity_id="   ")

    def test_name_validation(self):
        """Test name validation."""
        # Valid name
        request = IdentityUpdateRequest(identity_id="identity123", name="Updated Name")
        assert request.name == "Updated Name"

        # Empty name after trimming
        with pytest.raises(ValidationError, match="Name cannot be empty"):
            IdentityUpdateRequest(identity_id="identity123", name="   ")

        # Name too long
        long_name = "a" * 192
        with pytest.raises(
            ValidationError, match="Name must be 191 characters or less"
        ):
            IdentityUpdateRequest(identity_id="identity123", name=long_name)

    def test_reply_to_email_validation(self):
        """Test reply-to email validation."""
        # Valid reply-to email
        request = IdentityUpdateRequest(
            identity_id="identity123", reply_to_email="reply@example.com"
        )
        assert request.reply_to_email == "reply@example.com"

        # Invalid reply-to email format
        with pytest.raises(ValidationError, match="Invalid reply-to email format"):
            IdentityUpdateRequest(
                identity_id="identity123", reply_to_email="invalid-email"
            )

    def test_personal_note_validation(self):
        """Test personal note validation."""
        # Valid personal note
        request = IdentityUpdateRequest(
            identity_id="identity123", personal_note="Updated personal note"
        )
        assert request.personal_note == "Updated personal note"

        # Personal note too long
        long_note = "a" * 251
        with pytest.raises(
            ValidationError, match="Personal note must be 250 characters or less"
        ):
            IdentityUpdateRequest(identity_id="identity123", personal_note=long_note)

    def test_serialization(self):
        """Test model serialization."""
        request = IdentityUpdateRequest(
            identity_id="identity123",
            name="Updated Name",
            reply_to_email="updated@example.com",
            add_note=True,
        )
        data = request.model_dump()
        assert data == {
            "identity_id": "identity123",
            "name": "Updated Name",
            "reply_to_email": "updated@example.com",
            "reply_to_name": None,
            "add_note": True,
            "personal_note": None,
        }


class TestIdentityUpdateByEmailRequest:
    """Test IdentityUpdateByEmailRequest model."""

    def test_required_email_only(self):
        """Test with only required email."""
        request = IdentityUpdateByEmailRequest(email="john@example.com")
        assert request.email == "john@example.com"
        assert request.name is None
        assert request.reply_to_email is None
        assert request.reply_to_name is None
        assert request.add_note is None
        assert request.personal_note is None

    def test_with_all_fields(self):
        """Test with all fields provided."""
        request = IdentityUpdateByEmailRequest(
            email="john@example.com",
            name="Updated Name",
            reply_to_email="updated@example.com",
            reply_to_name="Updated Reply Name",
            add_note=False,
            personal_note="Updated note",
        )
        assert request.email == "john@example.com"
        assert request.name == "Updated Name"
        assert request.reply_to_email == "updated@example.com"
        assert request.reply_to_name == "Updated Reply Name"
        assert request.add_note is False
        assert request.personal_note == "Updated note"

    def test_email_validation(self):
        """Test email validation."""
        # Empty email
        with pytest.raises(ValidationError, match="Email is required"):
            IdentityUpdateByEmailRequest(email="")

        # Invalid email format
        with pytest.raises(ValidationError, match="Invalid email format"):
            IdentityUpdateByEmailRequest(email="invalid-email")

    def test_name_validation(self):
        """Test name validation."""
        # Empty name after trimming
        with pytest.raises(ValidationError, match="Name cannot be empty"):
            IdentityUpdateByEmailRequest(email="john@example.com", name="   ")

        # Name too long
        long_name = "a" * 192
        with pytest.raises(
            ValidationError, match="Name must be 191 characters or less"
        ):
            IdentityUpdateByEmailRequest(email="john@example.com", name=long_name)

    def test_serialization(self):
        """Test model serialization."""
        request = IdentityUpdateByEmailRequest(
            email="john@example.com", name="Updated Name", add_note=True
        )
        data = request.model_dump()
        assert data == {
            "email": "john@example.com",
            "name": "Updated Name",
            "reply_to_email": None,
            "reply_to_name": None,
            "add_note": True,
            "personal_note": None,
        }


class TestIdentityDeleteRequest:
    """Test IdentityDeleteRequest model."""

    def test_valid_identity_id(self):
        """Test with valid identity ID."""
        request = IdentityDeleteRequest(identity_id="identity123")
        assert request.identity_id == "identity123"

    def test_identity_id_validation(self):
        """Test identity ID validation."""
        # Empty identity ID
        with pytest.raises(ValidationError, match="Identity ID is required"):
            IdentityDeleteRequest(identity_id="")

        # Whitespace identity ID
        with pytest.raises(ValidationError, match="Identity ID is required"):
            IdentityDeleteRequest(identity_id="   ")

    def test_identity_id_trimming(self):
        """Test identity ID is trimmed."""
        request = IdentityDeleteRequest(identity_id="  identity123  ")
        assert request.identity_id == "identity123"

    def test_serialization(self):
        """Test model serialization."""
        request = IdentityDeleteRequest(identity_id="identity123")
        data = request.model_dump()
        assert data == {"identity_id": "identity123"}


class TestIdentityDeleteByEmailRequest:
    """Test IdentityDeleteByEmailRequest model."""

    def test_basic(self):
        """Test basic functionality."""
        request = IdentityDeleteByEmailRequest(email="john@example.com")
        assert request.email == "john@example.com"

    def test_empty_email(self):
        """Test empty email validation."""
        with pytest.raises(ValidationError) as exc_info:
            IdentityDeleteByEmailRequest(email="")
        assert "Email is required" in str(exc_info.value)

    def test_whitespace_email(self):
        """Test whitespace-only email validation."""
        with pytest.raises(ValidationError) as exc_info:
            IdentityDeleteByEmailRequest(email="   ")
        assert "Email is required" in str(exc_info.value)

    def test_invalid_email_format(self):
        """Test invalid email format validation."""
        with pytest.raises(ValidationError) as exc_info:
            IdentityDeleteByEmailRequest(email="invalid_email")
        assert "Invalid email format" in str(exc_info.value)

    def test_email_trimming(self):
        """Test email trimming."""
        request = IdentityDeleteByEmailRequest(email="  john@example.com  ")
        assert request.email == "john@example.com"

    def test_serialization(self):
        """Test model serialization."""
        request = IdentityDeleteByEmailRequest(email="john@example.com")
        data = request.model_dump()
        assert data == {"email": "john@example.com"}
