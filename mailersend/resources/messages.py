from typing import Union

from .base import BaseResource
from ..models.messages import (
    MessagesListRequest,
    MessageGetRequest,
    MessagesListResponse,
    MessageResponse,
)
from ..models.base import APIResponse
from ..exceptions import ValidationError as MailerSendValidationError


class Messages(BaseResource):
    """
    Client for interacting with the MailerSend Messages API.

    Provides methods for retrieving message information.
    """

    def list_messages(self, request: MessagesListRequest) -> APIResponse:
        """
        Retrieve a list of messages.

        Args:
            request: MessagesListRequest with pagination options

        Returns:
            APIResponse containing the messages list response

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, MessagesListRequest):
            raise MailerSendValidationError(
                "Request must be an instance of MessagesListRequest"
            )

        self.logger.debug("Preparing to list messages with query parameters")

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(f"Making API request to list messages with params: {params}")

        # Make API request
        response = self.client.request(
            method="GET", endpoint="messages", params=params if params else None
        )

        return self._create_response(response, MessagesListResponse)

    def get_message(self, request: MessageGetRequest) -> APIResponse:
        """
        Retrieve information about a single message.

        Args:
            request: MessageGetRequest with message ID

        Returns:
            APIResponse containing the message response

        Raises:
            MailerSendValidationError: If the request is invalid or has wrong type
        """
        # Validation
        if not isinstance(request, MessageGetRequest):
            raise MailerSendValidationError(
                "Request must be an instance of MessageGetRequest"
            )

        self.logger.debug(f"Preparing to get message with ID: {request.message_id}")

        # Make API request
        response = self.client.request(
            method="GET", endpoint=f"messages/{request.message_id}"
        )

        return self._create_response(response, MessageResponse)
