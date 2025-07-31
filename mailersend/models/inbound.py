"""
Inbound models
"""

from typing import List, Optional
from pydantic import Field, field_validator, model_validator
from mailersend.models.base import BaseModel


# Data Models
class InboundFilter(BaseModel):
    """Represents an inbound filter (catch or match filter)."""

    type: str = Field(..., description="Filter type")
    key: Optional[str] = Field(
        None, description="Filter key (required for match_header)"
    )
    comparer: Optional[str] = Field(None, description="Filter comparer")
    value: Optional[str] = Field(None, description="Filter value")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        """Validate filter type."""
        if v is None:
            return v
        valid_types = [
            "catch_all",
            "catch_recipient",
            "match_all",
            "match_sender",
            "match_domain",
            "match_header",
        ]
        if v not in valid_types:
            raise ValueError(f"Type must be one of: {', '.join(valid_types)}")
        return v

    @field_validator("comparer")
    @classmethod
    def validate_comparer(cls, v):
        """Validate comparer."""
        if v is None:
            return v
        valid_comparers = [
            "equal",
            "not-equal",
            "contains",
            "not-contains",
            "starts-with",
            "ends-with",
            "not-starts-with",
            "not-ends-with",
        ]
        if v not in valid_comparers:
            raise ValueError(f"Comparer must be one of: {', '.join(valid_comparers)}")
        return v

    @field_validator("value")
    @classmethod
    def validate_value(cls, v):
        """Validate value."""
        if v is not None and len(v) > 191:
            raise ValueError("Value cannot exceed 191 characters")
        return v.strip() if v else v

    @field_validator("key")
    @classmethod
    def validate_key(cls, v):
        """Validate key."""
        if v is not None and len(v) > 191:
            raise ValueError("Key cannot exceed 191 characters")
        return v.strip() if v else v


class InboundFilterGroup(BaseModel):
    """Represents a group of inbound filters with type and filters."""

    type: str = Field(..., description="Filter group type")
    filters: Optional[List[dict]] = Field(None, description="List of filter conditions")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        """Validate filter type."""
        valid_types = [
            "catch_all",
            "catch_recipient",
            "match_all",
            "match_sender",
            "match_domain",
            "match_header",
        ]
        if v not in valid_types:
            raise ValueError(f"Type must be one of: {', '.join(valid_types)}")
        return v

    @field_validator("filters")
    @classmethod
    def validate_filters(cls, v):
        """Validate filters."""
        if v is not None and len(v) > 5:
            raise ValueError("Maximum 5 filters allowed")
        return v


class InboundForward(BaseModel):
    """Represents an inbound forward configuration."""

    id: Optional[str] = Field(None, description="Forward ID")
    type: str = Field(..., description="Forward type (email or webhook)")
    value: str = Field(..., description="Forward destination")
    secret: Optional[str] = Field(None, description="Webhook secret")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        """Validate forward type."""
        if v not in ["email", "webhook"]:
            raise ValueError("Type must be either 'email' or 'webhook'")
        return v

    @field_validator("value")
    @classmethod
    def validate_value(cls, v):
        """Validate forward value."""

        if not v or not v.strip():
            raise ValueError("Value is required")
        if len(v) > 191:
            raise ValueError("Value cannot exceed 191 characters")
        return v.strip()


# Request Models
class InboundListQueryParams(BaseModel):
    """Model for inbound list query parameters with validation."""

    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)
    domain_id: Optional[str] = None

    def to_query_params(self) -> dict:
        """Convert to query parameters for API request."""
        params = {"page": self.page, "limit": self.limit, "domain_id": self.domain_id}

        return {k: v for k, v in params.items() if v is not None}


class InboundListRequest(BaseModel):
    """Request model for listing inbound routes."""

    query_params: InboundListQueryParams

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class InboundGetRequest(BaseModel):
    """Request model for getting a single inbound route."""

    inbound_id: str = Field(..., description="Inbound route ID")

    @field_validator("inbound_id")
    @classmethod
    def validate_inbound_id(cls, v):
        """Validate inbound ID."""
        if not v or not v.strip():
            raise ValueError("Inbound ID is required")
        return v.strip()


class InboundCreateRequest(BaseModel):
    """Request model for creating an inbound route."""

    domain_id: str = Field(..., description="Domain ID")
    name: str = Field(..., description="Route name")
    domain_enabled: bool = Field(..., description="Whether domain is enabled")
    inbound_domain: Optional[str] = Field(None, description="Inbound domain")
    inbound_priority: Optional[int] = Field(
        None, ge=0, le=100, description="Inbound priority"
    )
    catch_filter: InboundFilterGroup = Field(
        ..., description="Catch filter configuration"
    )
    catch_type: Optional[str] = Field(None, description="Catch type (all or one)")
    match_filter: InboundFilterGroup = Field(
        ..., description="Match filter configuration"
    )
    match_type: Optional[str] = Field(None, description="Match type (all or one)")
    forwards: List[InboundForward] = Field(..., description="Forward configurations")

    @field_validator("domain_id")
    @classmethod
    def validate_domain_id(cls, v):
        """Validate domain ID."""
        if not v or not v.strip():
            raise ValueError("Domain ID is required")
        return v.strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """Validate name."""
        if not v or not v.strip():
            raise ValueError("Name is required")
        if len(v) > 191:
            raise ValueError("Name cannot exceed 191 characters")
        return v.strip()

    @field_validator("inbound_domain")
    @classmethod
    def validate_inbound_domain(cls, v):
        """Validate inbound domain."""
        if v is not None:
            if len(v) > 191:
                raise ValueError("Inbound domain cannot exceed 191 characters")
            return v.strip()
        return v

    @field_validator("catch_type")
    @classmethod
    def validate_catch_type(cls, v):
        """Validate catch type."""
        if v is not None and v not in ["all", "one"]:
            raise ValueError("Catch type must be 'all' or 'one'")
        return v

    @field_validator("match_type")
    @classmethod
    def validate_match_type(cls, v):
        """Validate match type."""
        if v is not None and v not in ["all", "one"]:
            raise ValueError("Match type must be 'all' or 'one'")
        return v

    @field_validator("forwards")
    @classmethod
    def validate_forwards(cls, v):
        """Validate forwards."""
        if not v:
            raise ValueError("At least one forward is required")
        if len(v) > 5:
            raise ValueError("Maximum 5 forwards allowed")

        # Check for distinct values
        values = [forward.value for forward in v]
        if len(values) != len(set(values)):
            raise ValueError("Forward values must be distinct")

        return v

    @model_validator(mode="after")
    def validate_conditional_fields(self):
        """Validate conditional fields."""
        if self.domain_enabled:
            if not self.inbound_domain:
                raise ValueError("Inbound domain is required when domain is enabled")
            if self.inbound_priority is None:
                raise ValueError("Inbound priority is required when domain is enabled")

        return self

    def to_request_body(self) -> dict:
        """Convert to API request body with proper serialization."""
        data = self.model_dump(by_alias=True, exclude_none=True)

        # Exclude 'id' from forwards for creation
        if "forwards" in data and data["forwards"]:
            data["forwards"] = [
                {k: v for k, v in forward.items() if k != "id"}
                for forward in data["forwards"]
            ]

        return data


class InboundUpdateRequest(BaseModel):
    """Request model for updating an inbound route."""

    inbound_id: str = Field(..., description="Inbound route ID")
    name: str = Field(..., description="Route name")
    domain_enabled: bool = Field(..., description="Whether domain is enabled")
    inbound_domain: Optional[str] = Field(None, description="Inbound domain")
    inbound_priority: Optional[int] = Field(
        None, ge=0, le=100, description="Inbound priority"
    )
    catch_filter: InboundFilterGroup = Field(
        ..., description="Catch filter configuration"
    )
    catch_type: Optional[str] = Field(None, description="Catch type (all or one)")
    match_filter: InboundFilterGroup = Field(
        ..., description="Match filter configuration"
    )
    match_type: Optional[str] = Field(None, description="Match type (all or one)")
    forwards: List[InboundForward] = Field(..., description="Forward configurations")

    @field_validator("inbound_id")
    @classmethod
    def validate_inbound_id(cls, v):
        """Validate inbound ID."""
        if not v or not v.strip():
            raise ValueError("Inbound ID is required")
        return v.strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """Validate name."""
        if not v or not v.strip():
            raise ValueError("Name is required")
        if len(v) > 191:
            raise ValueError("Name cannot exceed 191 characters")
        return v.strip()

    @field_validator("inbound_domain")
    @classmethod
    def validate_inbound_domain(cls, v):
        """Validate inbound domain."""
        if v is not None:
            if len(v) > 191:
                raise ValueError("Inbound domain cannot exceed 191 characters")
            return v.strip()
        return v

    @field_validator("catch_type")
    @classmethod
    def validate_catch_type(cls, v):
        """Validate catch type."""
        if v is not None and v not in ["all", "one"]:
            raise ValueError("Catch type must be 'all' or 'one'")
        return v

    @field_validator("match_type")
    @classmethod
    def validate_match_type(cls, v):
        """Validate match type."""
        if v is not None and v not in ["all", "one"]:
            raise ValueError("Match type must be 'all' or 'one'")
        return v

    @field_validator("forwards")
    @classmethod
    def validate_forwards(cls, v):
        """Validate forwards."""
        if not v:
            raise ValueError("At least one forward is required")
        if len(v) > 5:
            raise ValueError("Maximum 5 forwards allowed")

        # Check for distinct values
        values = [forward.value for forward in v]
        if len(values) != len(set(values)):
            raise ValueError("Forward values must be distinct")

        return v

    @model_validator(mode="after")
    def validate_conditional_fields(self):
        """Validate conditional fields."""
        if self.domain_enabled:
            if not self.inbound_domain:
                raise ValueError("Inbound domain is required when domain is enabled")
            if self.inbound_priority is None:
                raise ValueError("Inbound priority is required when domain is enabled")

        return self

    def to_request_body(self) -> dict:
        """Convert to API request body with proper serialization."""
        data = self.model_dump(by_alias=True, exclude_none=True, exclude={"inbound_id"})

        # Exclude 'id' from forwards for update
        if "forwards" in data and data["forwards"]:
            data["forwards"] = [
                {k: v for k, v in forward.items() if k != "id"}
                for forward in data["forwards"]
            ]

        return data


class InboundDeleteRequest(BaseModel):
    """Request model for deleting an inbound route."""

    inbound_id: str = Field(..., description="Inbound route ID")

    @field_validator("inbound_id")
    @classmethod
    def validate_inbound_id(cls, v):
        """Validate inbound ID."""
        if not v or not v.strip():
            raise ValueError("Inbound ID is required")
        return v.strip()
