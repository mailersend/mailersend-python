"""Email resource"""

from typing import List, Union

from .base import BaseResource
from ..models.email import EmailRequest, EmailsListRequest, EmailGetRequest
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

        return self._request(
            method="POST",
            path="email",
            body=payload,
            data=lambda r: {"id": r.headers.get("x-message-id")},
        )

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

        return self._request(method="POST", path="bulk-email", body=payload)

    def get_bulk_status(self, bulk_email_id: str) -> APIResponse:
        """
        Get the status of a bulk email send request.

        Args:
            bulk_email_id: The ID of the bulk email request

        Returns:
            APIResponse with bulk email status and metadata
        """
        self.logger.debug("Getting bulk email status")

        return self._request(method="GET", path=f"bulk-email/{bulk_email_id}")

    def list(self, request: EmailsListRequest) -> APIResponse:
        """
        Get a list of emails sent from a domain.

        Paginated with ``page`` and ``limit``. ``response["meta"]`` carries
        ``current_page``, ``per_page``, ``from`` and ``to``, but no ``total``
        and no ``last_page`` — walk pages until ``links["next"]`` is ``None``.

        Args:
            request: A fully-validated EmailsListRequest object

        Returns:
            APIResponse with the emails, pagination links and metadata
        """
        self.logger.debug("Preparing to list emails")

        params = request.to_query_params()

        self.logger.debug(
            "Listing emails for domain: %s", request.query_params.domain_id
        )
        self.logger.debug("Query params: %s", params)

        return self._request(method="GET", path="emails", params=params)

    def get(self, request: Union[EmailGetRequest, str]) -> APIResponse:
        """
        Get a single email, its content and its activity events.

        Args:
            request: An EmailGetRequest object, or the email ID as a string

        Returns:
            APIResponse with the email and its activity events
        """
        if isinstance(request, str):
            request = EmailGetRequest(email_id=request)

        self.logger.debug("Getting email: %s", request.email_id)

        return self._request(method="GET", path=f"email/{request.email_id}")
