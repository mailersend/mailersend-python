from typing import List, Optional

from ..models.whatsapp import WhatsAppPersonalization, WhatsAppSendRequest


class WhatsAppBuilder:
    """
    Builder for creating WhatsApp sending requests using a fluent interface.
    """

    def __init__(self):
        """Initialize builder with empty values."""
        self._from_number: Optional[str] = None
        self._to: List[str] = []
        self._template_id: Optional[str] = None
        self._personalization: List[WhatsAppPersonalization] = []

    def from_number(self, phone_number: str) -> "WhatsAppBuilder":
        """
        Set the from phone number.

        Args:
            phone_number: Phone number in international format without + (e.g., 12345678901)

        Returns:
            Self for method chaining
        """
        self._from_number = phone_number
        return self

    def to(self, phone_numbers: List[str]) -> "WhatsAppBuilder":
        """
        Set the recipient phone numbers.

        Args:
            phone_numbers: List of phone numbers in international format without +

        Returns:
            Self for method chaining
        """
        self._to = phone_numbers
        return self

    def add_recipient(self, phone_number: str) -> "WhatsAppBuilder":
        """
        Add a single recipient phone number.

        Args:
            phone_number: Phone number in international format without +

        Returns:
            Self for method chaining
        """
        if phone_number not in self._to:
            self._to.append(phone_number)
        return self

    def template_id(self, template_id: str) -> "WhatsAppBuilder":
        """
        Set the WhatsApp template ID.

        Args:
            template_id: ID of an approved WhatsApp template

        Returns:
            Self for method chaining
        """
        self._template_id = template_id
        return self

    def add_personalization(
        self, personalization: WhatsAppPersonalization
    ) -> "WhatsAppBuilder":
        """
        Add personalization data for a specific recipient.

        Args:
            personalization: WhatsAppPersonalization object for a recipient

        Returns:
            Self for method chaining
        """
        self._personalization.append(personalization)
        return self

    def build(self) -> WhatsAppSendRequest:
        """
        Build the WhatsAppSendRequest object.

        Returns:
            WhatsAppSendRequest object ready for API call

        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_number:
            raise ValueError("From number is required")

        if not self._to:
            raise ValueError("At least one recipient is required")

        if not self._template_id:
            raise ValueError("Template ID is required")

        return WhatsAppSendRequest(
            from_number=self._from_number,
            to=self._to,
            template_id=self._template_id,
            personalization=self._personalization if self._personalization else None,
        )

    def clear(self) -> "WhatsAppBuilder":
        """
        Clear all builder values.

        Returns:
            Self for method chaining
        """
        self._from_number = None
        self._to = []
        self._template_id = None
        self._personalization = []
        return self