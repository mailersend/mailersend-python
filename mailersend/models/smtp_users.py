"""SMTP Users models."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from .base import BaseModel as BaseMailerSendModel


class SmtpUsersListQueryParams(BaseModel):
    """Query parameters for listing SMTP users."""
    
    limit: int = Field(default=25, ge=10, le=100, description="Number of results per page")
    
    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict, excluding None values."""
        params = {}
        
        # Only include non-default values
        if self.limit != 25:
            params["limit"] = self.limit
            
        return params


class SmtpUsersListRequest(BaseModel):
    """Request model for listing SMTP users."""
    
    domain_id: str = Field(..., min_length=1, description="Domain ID")
    query_params: SmtpUsersListQueryParams = Field(default_factory=SmtpUsersListQueryParams)
    
    @field_validator('domain_id')
    @classmethod
    def validate_domain_id(cls, v):
        """Validate domain ID."""
        if not v or not v.strip():
            raise ValueError("Domain ID cannot be empty")
        return v.strip()
    
    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()


class SmtpUserGetRequest(BaseModel):
    """Request model for getting a single SMTP user."""
    
    domain_id: str = Field(..., min_length=1, description="Domain ID")
    smtp_user_id: str = Field(..., min_length=1, description="SMTP User ID")
    
    @field_validator('domain_id', 'smtp_user_id')
    @classmethod
    def validate_ids(cls, v):
        """Validate IDs."""
        if not v or not v.strip():
            raise ValueError("ID cannot be empty")
        return v.strip()


class SmtpUserCreateRequest(BaseModel):
    """Request model for creating an SMTP user."""
    
    domain_id: str = Field(..., min_length=1, description="Domain ID")
    name: str = Field(..., min_length=1, max_length=50, description="SMTP user name")
    enabled: Optional[bool] = Field(default=None, description="Whether the SMTP user is enabled")
    
    @field_validator('domain_id')
    @classmethod
    def validate_domain_id(cls, v):
        """Validate domain ID."""
        if not v or not v.strip():
            raise ValueError("Domain ID cannot be empty")
        return v.strip()
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate name."""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        v = v.strip()
        if len(v) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        return v
    
    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON dict for API request."""
        json_data = {
            "name": self.name
        }
        
        if self.enabled is not None:
            json_data["enabled"] = self.enabled
            
        return json_data


class SmtpUserUpdateRequest(BaseModel):
    """Request model for updating an SMTP user."""
    
    domain_id: str = Field(..., min_length=1, description="Domain ID")
    smtp_user_id: str = Field(..., min_length=1, description="SMTP User ID")
    name: str = Field(..., min_length=1, max_length=50, description="SMTP user name")
    enabled: Optional[bool] = Field(default=None, description="Whether the SMTP user is enabled")
    
    @field_validator('domain_id', 'smtp_user_id')
    @classmethod
    def validate_ids(cls, v):
        """Validate IDs."""
        if not v or not v.strip():
            raise ValueError("ID cannot be empty")
        return v.strip()
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate name."""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        v = v.strip()
        if len(v) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        return v
    
    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON dict for API request."""
        json_data = {
            "name": self.name
        }
        
        if self.enabled is not None:
            json_data["enabled"] = self.enabled
            
        return json_data


class SmtpUserDeleteRequest(BaseModel):
    """Request model for deleting an SMTP user."""
    
    domain_id: str = Field(..., min_length=1, description="Domain ID")
    smtp_user_id: str = Field(..., min_length=1, description="SMTP User ID")
    
    @field_validator('domain_id', 'smtp_user_id')
    @classmethod
    def validate_ids(cls, v):
        """Validate IDs."""
        if not v or not v.strip():
            raise ValueError("ID cannot be empty")
        return v.strip()


# Response Models
class SmtpUser(BaseMailerSendModel):
    """SMTP User model."""
    
    id: str = Field(..., description="SMTP User ID")
    name: str = Field(..., description="SMTP User name")
    username: str = Field(..., description="SMTP username")
    password: str = Field(..., description="SMTP password")
    enabled: bool = Field(..., description="Whether the SMTP user is enabled")
    accessed_at: Optional[datetime] = Field(None, description="Last access time")
    server: str = Field(..., description="SMTP server")
    port: int = Field(..., description="SMTP port")
    domain_id: str = Field(..., description="Domain ID")


class SmtpUsersListResponse(BaseMailerSendModel):
    """Response model for SMTP users list."""
    
    data: List[SmtpUser] = Field(..., description="List of SMTP users")


class SmtpUserResponse(BaseMailerSendModel):
    """Response model for single SMTP user."""
    
    data: SmtpUser = Field(..., description="SMTP user data")


class SmtpUserCreateResponse(BaseMailerSendModel):
    """Response model for SMTP user creation."""
    
    data: SmtpUser = Field(..., description="Created SMTP user data") 