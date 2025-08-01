from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator

from .base import BaseModel as MailerSendBaseModel


class SmsPersonalization(MailerSendBaseModel):
    """Model for SMS personalization data."""

    phone_number: str
    data: Dict[str, Any]

    model_config = {"validate_by_name": True}

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        """Validate phone number format."""
        if not v.startswith("+"):
            raise ValueError("Phone number must be in E164 format (start with +)")
        return v


class SmsSendRequest(MailerSendBaseModel):
    """
    Request model for sending SMS messages.
    """

    from_number: str = Field(alias="from")
    to: List[str] = Field(min_length=1, max_length=50)
    text: str = Field(max_length=2048)
    personalization: Optional[List[SmsPersonalization]] = None

    model_config = {"validate_by_name": True}

    @field_validator("from_number")
    def validate_from_number(cls, v):
        """Validate from number is in E164 format."""
        if not v.startswith("+"):
            raise ValueError("From number must be in E164 format (start with +)")
        return v

    @field_validator("to")
    def validate_to_numbers(cls, v):
        """Validate all to numbers are in E164 format."""
        for number in v:
            if not number.startswith("+"):
                raise ValueError(
                    "All phone numbers must be in E164 format (start with +)"
                )
        return v

    @field_validator("text")
    def validate_text_length(cls, v):
        """Validate text message length."""
        if len(v) > 2048:
            raise ValueError("Text message cannot exceed 2048 characters")
        if not v.strip():
            raise ValueError("Text message cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_personalization(cls, v):
        """Validate personalization data matches recipient numbers."""
        if v.personalization:
            personalization_numbers = {p.phone_number for p in v.personalization}
            to_numbers = set(v.to)

            # Check if all personalization numbers are in the to list
            invalid_numbers = personalization_numbers - to_numbers
            if invalid_numbers:
                raise ValueError(
                    f"Personalization phone numbers not in recipient list: {invalid_numbers}"
                )

        return v

    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON format for API request."""
        data = {"from": self.from_number, "to": self.to, "text": self.text}

        if self.personalization:
            data["personalization"] = [
                {"phone_number": p.phone_number, "data": p.data}
                for p in self.personalization
            ]

        return data
