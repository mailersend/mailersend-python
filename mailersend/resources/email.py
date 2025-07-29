"""Email resource"""

from typing import List

from .base import BaseResource
from ..models.email import EmailRequest
from ..models.base import APIResponse


class Email(BaseResource):
    """
    Client for interacting with the MailerSend Email API.
    """

    def send(self, email: EmailRequest) -> APIResponse:
        """
        Send a single email.

        Args:
            email: A fully-validated EmailRequest object

        Returns:
            APIResponse with email ID and metadata

        """
        self.logger.debug("Preparing to send email")

        payload = email.model_dump(by_alias=True, exclude_none=True)

        self.logger.debug("Sending email request to MailerSend API")
        self.logger.debug("Payload: %s", payload)

        response = self.client.request(method="POST", endpoint="email", body=payload)

        # Create custom data with email ID from headers
        email_data = {"id": response.headers.get("x-message-id")}

        return self._create_response(response, email_data)

    def send_bulk(self, emails: List[EmailRequest]) -> APIResponse:
        """
        Send multiple emails in one request.

        Args:
            emails: List of EmailRequest objects to send

        Returns:
            APIResponse with bulk email information and metadata
        """
        self.logger.debug("Preparing to send emails in bulk")

        payload = []
        for email in emails:
            # Prepare payload for each email
            email_payload = email.model_dump(by_alias=True, exclude_none=True)
            payload.append(email_payload)

        self.logger.debug("Sending bulk email request to MailerSend API")
        self.logger.debug("Payload: %s", payload)

        response = self.client.request(
            method="POST", endpoint="bulk-email", body=payload
        )

        return self._create_response(response)

    def get_bulk_status(self, bulk_email_id: str) -> APIResponse:
        """
        Get the status of a bulk email send request.

        Args:
            bulk_email_id: The ID of the bulk email request

        Returns:
            APIResponse with bulk email status and metadata
        """
        self.logger.debug("Getting bulk email status")

        response = self.client.request(
            method="GET", endpoint=f"bulk-email/{bulk_email_id}"
        )

        return self._create_response(response)
