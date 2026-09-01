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
        Set the sender to send from.

        Accepts either form of sender identifier, both found in your
        MailerSend account under WhatsApp > Phone numbers:

        - A phone number in E.164 format (e.g., 15550001234)
        - A MailerSend sender ID (e.g., 3enl6x27wmrxrl2v)

        A sender connected with a Meta virtual number has no phone number,
        so it can only be addressed by its MailerSend sender ID. The sender
        ID is also stable across disconnecting and reconnecting a sender,
        which the phone number is not.

        Args:
            phone_number: Phone number in E.164 format, or a MailerSend sender ID

        Returns:
            Self for method chaining
        """
        self._from_number = phone_number
        return self

    def to(self, phone_numbers: List[str]) -> "WhatsAppBuilder":
        """
        Set the recipients, replacing any already added.

        Each recipient is either a phone number in E.164 format
        (e.g., +48600000001) or a BSUID taken from an inbound message
        (e.g., US.13491208655302741918). Spaces, dashes, brackets, dots and
        the leading + are ignored, so "+48 600 000 001" and "48600000001"
        are the same recipient. WhatsApp usernames cannot be used.

        A message accepts at most 10 recipients, and each must be unique.

        Args:
            phone_numbers: List of phone numbers in E.164 format, or BSUIDs

        Returns:
            Self for method chaining
        """
        self._to = list(phone_numbers)
        return self

    def add_recipient(self, phone_number: str) -> "WhatsAppBuilder":
        """
        Add a single recipient, ignoring it if already added.

        The recipient is either a phone number in E.164 format
        (e.g., +48600000001) or a BSUID taken from an inbound message
        (e.g., US.13491208655302741918). WhatsApp usernames cannot be used.

        Args:
            phone_number: Phone number in E.164 format, or a BSUID

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
            template_id: ID of an approved WhatsApp template belonging to the
                sender set with from_number(), found under WhatsApp > Templates

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
