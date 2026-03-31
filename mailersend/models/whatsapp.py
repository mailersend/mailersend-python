"""WhatsApp models."""

from typing import List, Optional, Dict, Any
from pydantic import Field, field_validator, model_validator

from .base import BaseModel


class WhatsAppPersonalizationData(BaseModel):
    """Model for WhatsApp personalization data for each template section."""

    header: Optional[List[str]] = None
    body: Optional[List[str]] = None
    buttons: Optional[List[str]] = None

    model_config = {"validate_by_name": True}


class WhatsAppPersonalization(BaseModel):
    """Model for WhatsApp per-recipient personalization."""

    to: str
    data: WhatsAppPersonalizationData

    model_config = {"validate_by_name": True}


class WhatsAppSendRequest(BaseModel):
    """
    Request model for sending WhatsApp messages.
    """

    from_number: str = Field(alias="from")
    to: List[str] = Field(min_length=1, max_length=10)
    template_id: str
    personalization: Optional[List[WhatsAppPersonalization]] = None

    model_config = {"validate_by_name": True}

    @field_validator("from_number")
    @classmethod
    def validate_from_number(cls, v):
        """Validate from number is non-empty."""
        if not v or not v.strip():
            raise ValueError("From number is required")
        return v

    @field_validator("to")
    @classmethod
    def validate_to_numbers(cls, v):
        """Validate all to numbers are non-empty."""
        for number in v:
            if not number or not number.strip():
                raise ValueError("All recipient phone numbers must be non-empty")
        return v

    @field_validator("template_id")
    @classmethod
    def validate_template_id(cls, v):
        """Validate template ID is non-empty."""
        if not v or not v.strip():
            raise ValueError("Template ID is required")
        return v

    @model_validator(mode="after")
    def validate_personalization(self):
        """Validate personalization data matches recipient numbers."""
        if self.personalization:
            personalization_numbers = {p.to for p in self.personalization}
            to_numbers = set(self.to)

            invalid_numbers = personalization_numbers - to_numbers
            if invalid_numbers:
                raise ValueError(
                    f"Personalization phone numbers not in recipient list: {invalid_numbers}"
                )

        return self

    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON format for API request."""
        data: Dict[str, Any] = {
            "from": self.from_number,
            "to": self.to,
            "template_id": self.template_id,
        }

        if self.personalization:
            data["personalization"] = [
                {
                    "to": p.to,
                    "data": {
                        k: v
                        for k, v in {
                            "header": p.data.header,
                            "body": p.data.body,
                            "buttons": p.data.buttons,
                        }.items()
                        if v is not None
                    },
                }
                for p in self.personalization
            ]

        return data
