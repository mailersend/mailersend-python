"""Recipients API resource for MailerSend SDK."""

from typing import Optional

from mailersend.models.base import APIResponse
from mailersend.models.recipients import (
    RecipientsListRequest,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
    RecipientsListQueryParams,
    SuppressionListQueryParams,
)
from mailersend.resources.base import BaseResource


class Recipients(BaseResource):
    """Recipients API resource for managing recipients and suppression lists."""

    def list_recipients(
        self, request: Optional[RecipientsListRequest] = None
    ) -> APIResponse:
        """
        List recipients with optional filtering.

        Args:
            request: Request parameters for listing recipients (optional)

        Returns:
            APIResponse with recipients list
        """

        # Use default request if none provided
        if request is None:
            query_params = RecipientsListQueryParams()
            request = RecipientsListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(f"Listing recipients with params: {params}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint="/v1/recipients", params=params
        )

        return self._create_response(response)

    def get_recipient(self, request: RecipientGetRequest) -> APIResponse:
        """
        Get a single recipient by ID.

        Args:
            request: Request parameters for getting recipient
        """
        self.logger.debug(f"Getting recipient: {request.recipient_id}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint=f"/v1/recipients/{request.recipient_id}"
        )

        return self._create_response(response)

    def delete_recipient(self, request: RecipientDeleteRequest) -> APIResponse:
        """
        Delete a recipient.

        Args:
            request: Request parameters for deleting recipient

        Returns:
            APIResponse with empty data
        """
        self.logger.debug(f"Deleting recipient: {request.recipient_id}")

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint=f"/v1/recipients/{request.recipient_id}"
        )

        return self._create_response(response)

    def list_blocklist(
        self, request: Optional[SuppressionListRequest] = None
    ) -> APIResponse:
        """
        List blocklist entries.

        Args:
            request: Request parameters for listing blocklist entries (optional)

        Returns:
            APIResponse with blocklist entries
        """
        # Use default request if none provided
        if request is None:
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(f"Listing blocklist with params: {params}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint="/v1/suppressions/blocklist", params=params
        )

        return self._create_response(response)

    def list_hard_bounces(
        self, request: Optional[SuppressionListRequest] = None
    ) -> APIResponse:
        """
        List hard bounces.

        Args:
            request: Request parameters for listing hard bounces (optional)

        Returns:
            APIResponse with hard bounces
        """
        # Use default request if none provided
        if request is None:
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(f"Listing hard bounces with params: {params}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint="/v1/suppressions/hard-bounces", params=params
        )

        return self._create_response(response)

    def list_spam_complaints(
        self, request: Optional[SuppressionListRequest] = None
    ) -> APIResponse:
        """
        List spam complaints.

        Args:
            request: Request parameters for listing spam complaints (optional)

        Returns:
            APIResponse with spam complaints
        """
        # Use default request if none provided
        if request is None:
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(f"Listing spam complaints with params: {params}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint="/v1/suppressions/spam-complaints", params=params
        )

        return self._create_response(response)

    def list_unsubscribes(
        self, request: Optional[SuppressionListRequest] = None
    ) -> APIResponse:
        """
        List unsubscribes.

        Args:
            request: Request parameters for listing unsubscribes (optional)

        Returns:
            APIResponse with unsubscribes
        """
        # Use default request if none provided
        if request is None:
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(f"Listing unsubscribes with params: {params}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint="/v1/suppressions/unsubscribes", params=params
        )

        return self._create_response(response)

    def list_on_hold(
        self, request: Optional[SuppressionListRequest] = None
    ) -> APIResponse:
        """
        List on-hold entries.

        Args:
            request: Request parameters for listing on-hold entries (optional)

        Returns:
            APIResponse with on-hold entries
        """
        # Use default request if none provided
        if request is None:
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(f"Listing on-hold entries with params: {params}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint="/v1/suppressions/on-hold-list", params=params
        )

        return self._create_response(response)

    def add_to_blocklist(self, request: SuppressionAddRequest) -> APIResponse:
        """
        Add entries to blocklist.

        Args:
            request: Request parameters for adding to blocklist

        Returns:
            APIResponse with added entries
        """
        body = request.model_dump(by_alias=True, exclude_none=True)

        self.logger.debug(f"Adding to blocklist with body: {body}")

        # Make API call
        response = self.client.request(
            method="POST", endpoint="/v1/suppressions/blocklist", body=body
        )

        return self._create_response(response)

    def add_hard_bounces(self, request: SuppressionAddRequest) -> APIResponse:
        """
        Add hard bounces.

        Args:
            request: Request parameters for adding hard bounces

        Returns:
            APIResponse with added entries
        """
        # Build request body
        body = request.model_dump(by_alias=True, exclude_none=True)

        self.logger.debug(f"Adding hard bounces with body: {body}")

        # Make API call
        response = self.client.request(
            method="POST", endpoint="/v1/suppressions/hard-bounces", body=body
        )

        return self._create_response(response)

    def add_spam_complaints(self, request: SuppressionAddRequest) -> APIResponse:
        """
        Add spam complaints.

        Args:
            request: Request parameters for adding spam complaints

        Returns:
            APIResponse with added entries

        """
        # Build request body
        body = request.model_dump(by_alias=True, exclude_none=True)

        self.logger.debug(f"Adding spam complaints with body: {body}")

        # Make API call
        response = self.client.request(
            method="POST", endpoint="/v1/suppressions/spam-complaints", body=body
        )

        return self._create_response(response)

    def add_unsubscribes(self, request: SuppressionAddRequest) -> APIResponse:
        """
        Add unsubscribes.

        Args:
            request: Request parameters for adding unsubscribes

        Returns:
            APIResponse with added entries
        """
        # Build request body
        body = request.model_dump(by_alias=True, exclude_none=True)

        self.logger.debug(f"Adding unsubscribes with body: {body}")

        # Make API call
        response = self.client.request(
            method="POST", endpoint="/v1/suppressions/unsubscribes", body=body
        )

        return self._create_response(response)

    def delete_from_blocklist(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete entries from blocklist.

        Args:
            request: Request parameters for deleting from blocklist

        Returns:
            APIResponse with deleted entries            
        """
        # Build request body
        body = request.model_dump(by_alias=True, exclude_none=True)

        self.logger.debug(f"Deleting from blocklist with body: {body}")

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint="/v1/suppressions/blocklist", body=body
        )

        return self._create_response(response)

    def delete_hard_bounces(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete hard bounces.

        Args:
            request: Request parameters for deleting hard bounces

        Returns:
            APIResponse with deleted entries
        """
        # Build request body (without domain_id for hard bounces)
        body = {}
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all

        self.logger.debug(f"Deleting hard bounces with body: {body}")

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint="/v1/suppressions/hard-bounces", body=body
        )

        return self._create_response(response)

    def delete_spam_complaints(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete spam complaints.

        Args:
            request: Request parameters for deleting spam complaints

        Returns:
            APIResponse with deleted entries
        """

        # Build request body (without domain_id for spam complaints)
        body = {}
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all

        self.logger.debug(f"Deleting spam complaints with body: {body}")

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint="/v1/suppressions/spam-complaints", body=body
        )

        return self._create_response(response)

    def delete_unsubscribes(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete unsubscribes.

        Args:
            request: Request parameters for deleting unsubscribes

        Returns:
            APIResponse with deleted entries
        """
        # Build request body (without domain_id for unsubscribes)
        body = {}
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all

        self.logger.debug(f"Deleting unsubscribes with body: {body}")

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint="/v1/suppressions/unsubscribes", body=body
        )

        return self._create_response(response)

    def delete_from_on_hold(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete entries from on-hold list.

        Args:
            request: Request parameters for deleting from on-hold

        Returns:
            APIResponse with deleted entries
        """
        # Build request body (without domain_id for on-hold)
        body = {}
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all

        self.logger.debug(f"Deleting from on-hold with body: {body}")

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint="/v1/suppressions/on-hold-list", body=body
        )

        return self._create_response(response)
