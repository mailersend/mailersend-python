"""DMARC Monitoring models."""

from typing import Optional, Dict, Any

from pydantic import Field, field_validator

from .base import BaseModel


class DmarcMonitoringListQueryParams(BaseModel):
    """Query parameters for listing DMARC monitors."""

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=25, ge=10, le=100)

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary, excluding None values."""
        return {"page": self.page, "limit": self.limit}


class DmarcMonitoringListRequest(BaseModel):
    """Request model for listing DMARC monitors."""

    query_params: DmarcMonitoringListQueryParams = Field(
        default_factory=DmarcMonitoringListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class DmarcMonitoringCreateRequest(BaseModel):
    """Request model for creating a DMARC monitor."""

    domain_id: str

    @field_validator("domain_id")
    @classmethod
    def validate_domain_id(cls, v: str) -> str:
        """Validate domain_id is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("domain_id cannot be empty")
        return v.strip()


class DmarcMonitoringUpdateRequest(BaseModel):
    """Request model for updating a DMARC monitor."""

    monitor_id: str
    wanted_dmarc_record: str

    @field_validator("monitor_id")
    @classmethod
    def validate_monitor_id(cls, v: str) -> str:
        """Validate monitor_id is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("monitor_id cannot be empty")
        return v.strip()

    @field_validator("wanted_dmarc_record")
    @classmethod
    def validate_wanted_dmarc_record(cls, v: str) -> str:
        """Validate wanted_dmarc_record is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("wanted_dmarc_record cannot be empty")
        return v.strip()


class DmarcMonitoringDeleteRequest(BaseModel):
    """Request model for deleting a DMARC monitor."""

    monitor_id: str

    @field_validator("monitor_id")
    @classmethod
    def validate_monitor_id(cls, v: str) -> str:
        """Validate monitor_id is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("monitor_id cannot be empty")
        return v.strip()


class DmarcMonitoringReportQueryParams(BaseModel):
    """Query parameters for DMARC monitoring reports."""

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=25, ge=10, le=100)

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return {"page": self.page, "limit": self.limit}


class DmarcMonitoringReportRequest(BaseModel):
    """Request model for getting aggregated DMARC reports."""

    monitor_id: str
    query_params: DmarcMonitoringReportQueryParams = Field(
        default_factory=DmarcMonitoringReportQueryParams
    )

    @field_validator("monitor_id")
    @classmethod
    def validate_monitor_id(cls, v: str) -> str:
        """Validate monitor_id is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("monitor_id cannot be empty")
        return v.strip()

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class DmarcMonitoringIpReportRequest(BaseModel):
    """Request model for getting IP-specific DMARC reports."""

    monitor_id: str
    ip: str
    query_params: DmarcMonitoringReportQueryParams = Field(
        default_factory=DmarcMonitoringReportQueryParams
    )

    @field_validator("monitor_id")
    @classmethod
    def validate_monitor_id(cls, v: str) -> str:
        """Validate monitor_id is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("monitor_id cannot be empty")
        return v.strip()

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        """Validate ip is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("ip cannot be empty")
        return v.strip()

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class DmarcMonitoringReportSourcesRequest(BaseModel):
    """Request model for getting DMARC report sources."""

    monitor_id: str

    @field_validator("monitor_id")
    @classmethod
    def validate_monitor_id(cls, v: str) -> str:
        """Validate monitor_id is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("monitor_id cannot be empty")
        return v.strip()


class DmarcMonitoringFavoriteRequest(BaseModel):
    """Request model for marking or removing an IP as favorite."""

    monitor_id: str
    ip: str

    @field_validator("monitor_id")
    @classmethod
    def validate_monitor_id(cls, v: str) -> str:
        """Validate monitor_id is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("monitor_id cannot be empty")
        return v.strip()

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        """Validate ip is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("ip cannot be empty")
        return v.strip()
