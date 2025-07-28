"""SMS Inbounds models."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, HttpUrl
from enum import Enum

from .base import BaseModel as BaseMailerSendModel


class FilterComparer(str, Enum):
    """SMS inbound filter comparers."""
    EQUAL = "equal"
    NOT_EQUAL = "not-equal"
    CONTAINS = "contains"
    NOT_CONTAINS = "not-contains"
    STARTS_WITH = "starts-with"
    ENDS_WITH = "ends-with"
    NOT_STARTS_WITH = "not-starts-with"
    NOT_ENDS_WITH = "not-ends-with"


class SmsInboundFilter(BaseMailerSendModel):
    """SMS inbound filter model."""
    comparer: FilterComparer = Field(..., description="Filter comparer")
    value: str = Field(..., min_length=1, max_length=255, description="Filter value")
    
    @field_validator("value")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip whitespace from filter value."""
        return v.strip()


# Query Parameters
class SmsInboundsListQueryParams(BaseMailerSendModel):
    """Query parameters for listing SMS inbounds."""
    sms_number_id: Optional[str] = Field(default=None, min_length=1, description="SMS number ID")
    enabled: Optional[bool] = Field(default=None, description="Whether inbound route is enabled")
    page: Optional[int] = Field(default=None, ge=1, description="Page number")
    limit: Optional[int] = Field(default=None, ge=10, le=100, description="Items per page")
    
    @field_validator("sms_number_id")
    @classmethod
    def strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from SMS number ID."""
        return v.strip() if v else v
    
    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        params = {}
        if self.sms_number_id is not None:
            params["sms_number_id"] = self.sms_number_id
        if self.enabled is not None:
            params["enabled"] = self.enabled
        if self.page is not None:
            params["page"] = self.page
        if self.limit is not None:
            params["limit"] = self.limit
        return params


# Request Models
class SmsInboundsListRequest(BaseMailerSendModel):
    """Request model for listing SMS inbounds."""
    query_params: SmsInboundsListQueryParams = Field(default_factory=SmsInboundsListQueryParams)
    
    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class SmsInboundGetRequest(BaseMailerSendModel):
    """Request model for getting a single SMS inbound."""
    sms_inbound_id: str = Field(..., min_length=1, description="SMS inbound ID")
    
    @field_validator("sms_inbound_id")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip whitespace from SMS inbound ID."""
        return v.strip()


class SmsInboundCreateRequest(BaseMailerSendModel):
    """Request model for creating an SMS inbound."""
    sms_number_id: str = Field(..., min_length=1, description="SMS number ID")
    name: str = Field(..., min_length=1, max_length=191, description="Inbound route name")
    forward_url: str = Field(..., min_length=1, max_length=255, description="Forward URL")
    filter: Optional[SmsInboundFilter] = Field(default=None, description="Filter settings")
    enabled: Optional[bool] = Field(default=True, description="Whether route is enabled")
    
    @field_validator("sms_number_id", "name", "forward_url")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip whitespace from string fields."""
        return v.strip()
    
    def to_request_body(self) -> Dict[str, Any]:
        """Convert to request body dictionary."""
        body = {
            "sms_number_id": self.sms_number_id,
            "name": self.name,
            "forward_url": self.forward_url,
            "enabled": self.enabled
        }
        if self.filter is not None:
            body["filter"] = {
                "comparer": self.filter.comparer.value,
                "value": self.filter.value
            }
        return body


class SmsInboundUpdateRequest(BaseMailerSendModel):
    """Request model for updating an SMS inbound."""
    sms_inbound_id: str = Field(..., min_length=1, description="SMS inbound ID")
    sms_number_id: Optional[str] = Field(default=None, min_length=1, description="SMS number ID")
    name: Optional[str] = Field(default=None, min_length=1, max_length=191, description="Inbound route name")
    forward_url: Optional[str] = Field(default=None, min_length=1, max_length=255, description="Forward URL")
    filter: Optional[SmsInboundFilter] = Field(default=None, description="Filter settings")
    enabled: Optional[bool] = Field(default=None, description="Whether route is enabled")
    
    @field_validator("sms_inbound_id")
    @classmethod
    def strip_inbound_id_whitespace(cls, v: str) -> str:
        """Strip whitespace from SMS inbound ID."""
        return v.strip()
    
    @field_validator("sms_number_id", "name", "forward_url")
    @classmethod
    def strip_optional_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from optional string fields."""
        return v.strip() if v else v
    
    def to_request_body(self) -> Dict[str, Any]:
        """Convert to request body dictionary."""
        body = {}
        if self.sms_number_id is not None:
            body["sms_number_id"] = self.sms_number_id
        if self.name is not None:
            body["name"] = self.name
        if self.forward_url is not None:
            body["forward_url"] = self.forward_url
        if self.filter is not None:
            body["filter"] = {
                "comparer": self.filter.comparer.value,
                "value": self.filter.value
            }
        if self.enabled is not None:
            body["enabled"] = self.enabled
        return body


class SmsInboundDeleteRequest(BaseMailerSendModel):
    """Request model for deleting an SMS inbound."""
    sms_inbound_id: str = Field(..., min_length=1, description="SMS inbound ID")
    
    @field_validator("sms_inbound_id")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip whitespace from SMS inbound ID."""
        return v.strip()


# Response Models
class SmsNumber(BaseMailerSendModel):
    """SMS number model."""
    id: str = Field(..., description="SMS number ID")
    telephone_number: str = Field(..., description="Telephone number")
    paused: bool = Field(..., description="Whether SMS number is paused")
    created_at: datetime = Field(..., description="Creation timestamp")


class SmsInbound(BaseMailerSendModel):
    """SMS inbound route model."""
    id: str = Field(..., description="Inbound route ID")
    name: str = Field(..., description="Inbound route name")
    filter: Optional[Dict[str, str]] = Field(default=None, description="Filter settings")
    forward_url: str = Field(..., description="Forward URL")
    enabled: bool = Field(..., description="Whether route is enabled")
    secret: Optional[str] = Field(default=None, description="Secret key for webhook verification")
    created_at: datetime = Field(..., description="Creation timestamp")
    sms_number: Optional[SmsNumber] = Field(default=None, description="Associated SMS number")


class SmsInboundsListResponse(BaseMailerSendModel):
    """Response model for SMS inbounds list."""
    data: List[SmsInbound] = Field(..., description="List of SMS inbound routes")


class SmsInboundGetResponse(BaseMailerSendModel):
    """Response model for SMS inbound get."""
    data: SmsInbound = Field(..., description="SMS inbound route details")


class SmsInboundCreateResponse(BaseMailerSendModel):
    """Response model for SMS inbound create."""
    data: SmsInbound = Field(..., description="Created SMS inbound route")


class SmsInboundUpdateResponse(BaseMailerSendModel):
    """Response model for SMS inbound update."""
    data: SmsInbound = Field(..., description="Updated SMS inbound route")


class SmsInboundDeleteResponse(BaseMailerSendModel):
    """Response model for SMS inbound delete."""
    message: str = Field(..., description="Delete confirmation message") 