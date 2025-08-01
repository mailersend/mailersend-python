"""Models for Users API."""

from datetime import datetime
from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field, field_validator


# Domain and Template nested models
class UserDomain(BaseModel):
    """Domain associated with a user."""

    id: str
    name: str
    created_at: datetime
    updated_at: datetime


class UserTemplate(BaseModel):
    """Template associated with a user."""

    id: str
    name: str
    type: str
    created_at: datetime


# User models
class User(BaseModel):
    """User data model."""

    id: str
    email: str
    last_name: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    twofa: bool = Field(alias="2fa", default=False)
    created_at: datetime
    updated_at: datetime
    role: str
    permissions: List[str] = Field(default_factory=list)
    domains: List[UserDomain] = Field(default_factory=list)
    templates: List[UserTemplate] = Field(default_factory=list)


class UserInviteData(BaseModel):
    """Data associated with a user invite."""

    domains: List[str] = Field(default_factory=list)
    templates: List[str] = Field(default_factory=list)


class UserInvite(BaseModel):
    """User invite data model."""

    id: str
    email: str
    data: Optional[UserInviteData] = None
    role: str
    permissions: List[str] = Field(default_factory=list)
    requires_periodic_password_change: Optional[bool] = None
    created_at: datetime
    updated_at: datetime


# Query parameters models
class UsersListQueryParams(BaseModel):
    """Query parameters for users list request."""

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=25, ge=10, le=100)

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        params = {}
        if self.page != 1:  # Only include if not default
            params["page"] = self.page
        if self.limit != 25:  # Only include if not default
            params["limit"] = self.limit
        return params


class InvitesListQueryParams(BaseModel):
    """Query parameters for invites list request."""

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=25, ge=10, le=100)

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        params = {}
        if self.page != 1:  # Only include if not default
            params["page"] = self.page
        if self.limit != 25:  # Only include if not default
            params["limit"] = self.limit
        return params


# Request models
class UsersListRequest(BaseModel):
    """Request model for listing users."""

    query_params: UsersListQueryParams = Field(default_factory=UsersListQueryParams)

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class UserGetRequest(BaseModel):
    """Request model for getting a single user."""

    user_id: str


class UserInviteRequest(BaseModel):
    """Request model for inviting a user."""

    email: str = Field(..., max_length=191)
    role: str
    permissions: List[str] = Field(default_factory=list)
    templates: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    requires_periodic_password_change: Optional[bool] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        import re

        if not v or not v.strip():
            raise ValueError("Invalid email address")
        # Basic email validation
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v.strip()):
            raise ValueError("Invalid email address")
        return v.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        """Validate role is not empty."""
        if not v or not v.strip():
            raise ValueError("Role cannot be empty")
        return v.strip()

    def to_json(self) -> Dict[str, Any]:
        """Convert request to JSON data for API call."""
        json_data = {
            "email": self.email,
            "role": self.role,
            "permissions": self.permissions,
            "templates": self.templates,
            "domains": self.domains,
        }

        if self.requires_periodic_password_change is not None:
            json_data[
                "requires_periodic_password_change"
            ] = self.requires_periodic_password_change

        return json_data


class UserUpdateRequest(BaseModel):
    """Request model for updating a user."""

    user_id: str
    role: str
    permissions: List[str] = Field(default_factory=list)
    templates: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    requires_periodic_password_change: Optional[bool] = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        """Validate role is not empty."""
        if not v or not v.strip():
            raise ValueError("Role cannot be empty")
        return v.strip()

    def to_json(self) -> Dict[str, Any]:
        """Convert request to JSON data for API call."""
        json_data = {
            "role": self.role,
            "permissions": self.permissions,
            "templates": self.templates,
            "domains": self.domains,
        }

        if self.requires_periodic_password_change is not None:
            json_data[
                "requires_periodic_password_change"
            ] = self.requires_periodic_password_change

        return json_data


class UserDeleteRequest(BaseModel):
    """Request model for deleting a user."""

    user_id: str


class InvitesListRequest(BaseModel):
    """Request model for listing invites."""

    query_params: InvitesListQueryParams = Field(default_factory=InvitesListQueryParams)

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class InviteGetRequest(BaseModel):
    """Request model for getting a single invite."""

    invite_id: str


class InviteResendRequest(BaseModel):
    """Request model for resending an invite."""

    invite_id: str


class InviteCancelRequest(BaseModel):
    """Request model for canceling an invite."""

    invite_id: str
