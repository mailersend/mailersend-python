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


# Request models
class UsersListRequest(BaseModel):
    """Request model for listing users."""
    pass  # No parameters for users list


class UserGetRequest(BaseModel):
    """Request model for getting a single user."""
    user_id: str


class UserInviteRequest(BaseModel):
    """Request model for inviting a user."""
    email: str = Field(max_length=191)
    role: str
    permissions: List[str] = Field(default_factory=list)
    templates: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    requires_periodic_password_change: Optional[bool] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        if '@' not in v or len(v.strip()) == 0:
            raise ValueError('Invalid email address')
        return v.strip()

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is not empty."""
        if not v.strip():
            raise ValueError('Role cannot be empty')
        return v.strip()


class UserUpdateRequest(BaseModel):
    """Request model for updating a user."""
    user_id: str
    role: str
    permissions: List[str] = Field(default_factory=list)
    templates: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    requires_periodic_password_change: Optional[bool] = None

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is not empty."""
        if not v.strip():
            raise ValueError('Role cannot be empty')
        return v.strip()


class UserDeleteRequest(BaseModel):
    """Request model for deleting a user."""
    user_id: str


class InvitesListRequest(BaseModel):
    """Request model for listing invites."""
    pass  # No parameters for invites list


class InviteGetRequest(BaseModel):
    """Request model for getting a single invite."""
    invite_id: str


class InviteResendRequest(BaseModel):
    """Request model for resending an invite."""
    invite_id: str


class InviteCancelRequest(BaseModel):
    """Request model for canceling an invite."""
    invite_id: str


# Response models
class UsersListResponse(BaseModel):
    """Response model for users list."""
    data: List[User]


class UserResponse(BaseModel):
    """Response model for single user."""
    data: User


class UserInviteResponse(BaseModel):
    """Response model for user invite creation."""
    data: UserInvite


class UserUpdateResponse(BaseModel):
    """Response model for user update."""
    data: User


class InvitesListResponse(BaseModel):
    """Response model for invites list."""
    data: List[UserInvite]


class InviteResponse(BaseModel):
    """Response model for single invite."""
    data: UserInvite


class InviteResendResponse(BaseModel):
    """Response model for invite resend."""
    data: UserInvite 