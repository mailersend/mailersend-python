from typing import List, Dict, Any, Optional
from ..models.sms_sending import SmsSendRequest, SmsPersonalization


class SmsSendingBuilder:
    """
    Builder for creating SMS sending requests using a fluent interface.
    """

    def __init__(self):
        """Initialize builder with empty values."""
        self._from_number: Optional[str] = None
        self._to: List[str] = []
        self._text: Optional[str] = None
        self._personalization: List[SmsPersonalization] = []

    def from_number(self, phone_number: str) -> "SmsSendingBuilder":
        """
        Set the from phone number.
        
        Args:
            phone_number: Phone number in E164 format (e.g., +1234567890)
            
        Returns:
            Self for method chaining
        """
        self._from_number = phone_number
        return self

    def to(self, phone_numbers: List[str]) -> "SmsSendingBuilder":
        """
        Set the recipient phone numbers.
        
        Args:
            phone_numbers: List of phone numbers in E164 format
            
        Returns:
            Self for method chaining
        """
        self._to = phone_numbers
        return self

    def add_recipient(self, phone_number: str) -> "SmsSendingBuilder":
        """
        Add a single recipient phone number.
        
        Args:
            phone_number: Phone number in E164 format
            
        Returns:
            Self for method chaining
        """
        if phone_number not in self._to:
            self._to.append(phone_number)
        return self

    def text(self, message: str) -> "SmsSendingBuilder":
        """
        Set the SMS text message.
        
        Args:
            message: Text message content (max 2048 characters)
            
        Returns:
            Self for method chaining
        """
        self._text = message
        return self

    def personalization(self, personalizations: List[SmsPersonalization]) -> "SmsSendingBuilder":
        """
        Set personalization data for recipients.
        
        Args:
            personalizations: List of personalization objects
            
        Returns:
            Self for method chaining
        """
        self._personalization = personalizations
        return self

    def add_personalization(self, phone_number: str, data: Dict[str, Any]) -> "SmsSendingBuilder":
        """
        Add personalization data for a specific recipient.
        
        Args:
            phone_number: Phone number in E164 format
            data: Dictionary of personalization key-value pairs
            
        Returns:
            Self for method chaining
        """
        personalization = SmsPersonalization(phone_number=phone_number, data=data)
        self._personalization.append(personalization)
        return self

    def build(self) -> SmsSendRequest:
        """
        Build the SmsSendRequest object.
        
        Returns:
            SmsSendRequest object ready for API call
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_number:
            raise ValueError("From number is required")
        
        if not self._to:
            raise ValueError("At least one recipient is required")
        
        if not self._text:
            raise ValueError("Text message is required")
        
        return SmsSendRequest(
            from_number=self._from_number,
            to=self._to,
            text=self._text,
            personalization=self._personalization if self._personalization else None
        )

    def clear(self) -> "SmsSendingBuilder":
        """
        Clear all builder values.
        
        Returns:
            Self for method chaining
        """
        self._from_number = None
        self._to = []
        self._text = None
        self._personalization = []
        return self