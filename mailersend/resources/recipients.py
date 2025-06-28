"""Recipients API resource for MailerSend SDK."""
import logging
from typing import Optional, Dict, Any, Union

from mailersend.exceptions import ValidationError
from mailersend.models.base import APIResponse
from mailersend.models.recipients import (
    RecipientsListRequest,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
    RecipientsListResponse,
    RecipientResponse,
    BlocklistResponse,
    HardBouncesResponse,
    SpamComplaintsResponse,
    UnsubscribesResponse,
    OnHoldResponse,
    SuppressionAddResponse,
)
from mailersend.resources.base import BaseResource

logger = logging.getLogger(__name__)


class Recipients(BaseResource):
    """Recipients API resource for managing recipients and suppression lists."""

    def list_recipients(self, request: Optional[RecipientsListRequest] = None) -> APIResponse:
        """
        List recipients with optional filtering.

        Args:
            request: Request parameters for listing recipients (optional)

        Returns:
            APIResponse containing RecipientsListResponse data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request type if provided
        if request is not None and not isinstance(request, RecipientsListRequest):
            raise ValidationError("Request must be an instance of RecipientsListRequest or None")

        # Use default request if none provided
        if request is None:
            from mailersend.models.recipients import RecipientsListQueryParams
            query_params = RecipientsListQueryParams()
            request = RecipientsListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        logger.debug(f"Listing recipients with params: {params}")

        # Make API call
        response = self.client.get("/v1/recipients", params=params)
        
        # Create response model instance
        response_data = response.json()
        recipients_response = RecipientsListResponse(**response_data)

        logger.info(f"Listed recipients successfully")

        return self._create_response(response, recipients_response)

    def get_recipient(self, request: RecipientGetRequest) -> APIResponse:
        """
        Get a single recipient by ID.

        Args:
            request: Request parameters for getting recipient

        Returns:
            APIResponse containing RecipientResponse data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, RecipientGetRequest):
            raise ValidationError("Request is required for get_recipient")

        logger.debug(f"Getting recipient: {request.recipient_id}")

        # Make API call
        response = self.client.get(f"/v1/recipients/{request.recipient_id}")
        
        # Create response model instance
        response_data = response.json()
        recipient_response = RecipientResponse(**response_data)

        logger.info(f"Retrieved recipient {request.recipient_id} successfully")

        return self._create_response(response, recipient_response)

    def delete_recipient(self, request: RecipientDeleteRequest) -> APIResponse:
        """
        Delete a recipient.

        Args:
            request: Request parameters for deleting recipient

        Returns:
            APIResponse with empty data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, RecipientDeleteRequest):
            raise ValidationError("Request is required for delete_recipient")

        logger.debug(f"Deleting recipient: {request.recipient_id}")

        # Make API call
        response = self.client.delete(f"/v1/recipients/{request.recipient_id}")

        logger.info(f"Deleted recipient {request.recipient_id} successfully")

        return self._create_response(response)

    def list_blocklist(self, request: Optional[SuppressionListRequest] = None) -> APIResponse:
        """
        List blocklist entries.

        Args:
            request: Request parameters for listing blocklist entries (optional)

        Returns:
            APIResponse containing BlocklistResponse data
        """
        # Use default request if none provided
        if request is None:
            from mailersend.models.recipients import SuppressionListQueryParams
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        logger.debug(f"Listing blocklist with params: {params}")

        # Make API call
        response = self.client.get("/v1/suppressions/blocklist", params=params)
        
        # Create response model instance
        response_data = response.json()
        blocklist_response = BlocklistResponse(**response_data)

        logger.info("Listed blocklist successfully")

        return self._create_response(response, blocklist_response)

    def list_hard_bounces(self, request: Optional[SuppressionListRequest] = None) -> APIResponse:
        """
        List hard bounces.

        Args:
            request: Request parameters for listing hard bounces (optional)

        Returns:
            APIResponse containing HardBouncesResponse data
        """
        # Use default request if none provided
        if request is None:
            from mailersend.models.recipients import SuppressionListQueryParams
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        logger.debug(f"Listing hard bounces with params: {params}")

        # Make API call
        response = self.client.get("/v1/suppressions/hard-bounces", params=params)
        
        # Create response model instance
        response_data = response.json()
        hard_bounces_response = HardBouncesResponse(**response_data)

        logger.info("Listed hard bounces successfully")

        return self._create_response(response, hard_bounces_response)

    def list_spam_complaints(self, request: Optional[SuppressionListRequest] = None) -> APIResponse:
        """
        List spam complaints.

        Args:
            request: Request parameters for listing spam complaints (optional)

        Returns:
            APIResponse containing SpamComplaintsResponse data
        """
        # Use default request if none provided
        if request is None:
            from mailersend.models.recipients import SuppressionListQueryParams
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        logger.debug(f"Listing spam complaints with params: {params}")

        # Make API call
        response = self.client.get("/v1/suppressions/spam-complaints", params=params)
        
        # Create response model instance
        response_data = response.json()
        spam_complaints_response = SpamComplaintsResponse(**response_data)

        logger.info("Listed spam complaints successfully")

        return self._create_response(response, spam_complaints_response)

    def list_unsubscribes(self, request: Optional[SuppressionListRequest] = None) -> APIResponse:
        """
        List unsubscribes.

        Args:
            request: Request parameters for listing unsubscribes (optional)

        Returns:
            APIResponse containing UnsubscribesResponse data
        """
        # Use default request if none provided
        if request is None:
            from mailersend.models.recipients import SuppressionListQueryParams
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        logger.debug(f"Listing unsubscribes with params: {params}")

        # Make API call
        response = self.client.get("/v1/suppressions/unsubscribes", params=params)
        
        # Create response model instance
        response_data = response.json()
        unsubscribes_response = UnsubscribesResponse(**response_data)

        logger.info("Listed unsubscribes successfully")

        return self._create_response(response, unsubscribes_response)

    def list_on_hold(self, request: Optional[SuppressionListRequest] = None) -> APIResponse:
        """
        List on-hold entries.

        Args:
            request: Request parameters for listing on-hold entries (optional)

        Returns:
            APIResponse containing OnHoldResponse data
        """
        # Use default request if none provided
        if request is None:
            from mailersend.models.recipients import SuppressionListQueryParams
            query_params = SuppressionListQueryParams()
            request = SuppressionListRequest(query_params=query_params)

        # Extract query parameters
        params = request.to_query_params()

        logger.debug(f"Listing on-hold entries with params: {params}")

        # Make API call
        response = self.client.get("/v1/suppressions/on-hold-list", params=params)
        
        # Create response model instance
        response_data = response.json()
        on_hold_response = OnHoldResponse(**response_data)

        logger.info("Listed on-hold entries successfully")

        return self._create_response(response, on_hold_response)

    def add_to_blocklist(self, request: SuppressionAddRequest) -> APIResponse:
        """
        Add entries to blocklist.

        Args:
            request: Request parameters for adding to blocklist

        Returns:
            APIResponse containing SuppressionAddResponse data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionAddRequest):
            raise ValidationError("Request is required for add_to_blocklist")

        # Build request body
        body = self._build_suppression_add_body(request)

        logger.debug(f"Adding to blocklist with body: {body}")

        # Make API call
        response = self.client.post("/v1/suppressions/blocklist", json=body)
        
        # Create response model instance
        response_data = response.json()
        suppression_response = SuppressionAddResponse(**response_data)

        logger.info("Added to blocklist successfully")

        return self._create_response(response, suppression_response)

    def add_hard_bounces(self, request: SuppressionAddRequest) -> APIResponse:
        """
        Add hard bounces.

        Args:
            request: Request parameters for adding hard bounces

        Returns:
            APIResponse containing SuppressionAddResponse data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionAddRequest):
            raise ValidationError("Request is required for add_hard_bounces")

        # Validate recipients are provided
        if not request.recipients:
            raise ValidationError("Recipients are required for add_hard_bounces")

        # Build request body
        body = self._build_suppression_add_body(request)

        logger.debug(f"Adding hard bounces with body: {body}")

        # Make API call
        response = self.client.post("/v1/suppressions/hard-bounces", json=body)
        
        # Create response model instance
        response_data = response.json()
        suppression_response = SuppressionAddResponse(**response_data)

        logger.info("Added hard bounces successfully")

        return self._create_response(response, suppression_response)

    def add_spam_complaints(self, request: SuppressionAddRequest) -> APIResponse:
        """
        Add spam complaints.

        Args:
            request: Request parameters for adding spam complaints

        Returns:
            APIResponse containing SuppressionAddResponse data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionAddRequest):
            raise ValidationError("Request is required for add_spam_complaints")

        # Build request body
        body = self._build_suppression_add_body(request)

        logger.debug(f"Adding spam complaints with body: {body}")

        # Make API call
        response = self.client.post("/v1/suppressions/spam-complaints", json=body)
        
        # Create response model instance
        response_data = response.json()
        suppression_response = SuppressionAddResponse(**response_data)

        logger.info("Added spam complaints successfully")

        return self._create_response(response, suppression_response)

    def add_unsubscribes(self, request: SuppressionAddRequest) -> APIResponse:
        """
        Add unsubscribes.

        Args:
            request: Request parameters for adding unsubscribes

        Returns:
            APIResponse containing SuppressionAddResponse data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionAddRequest):
            raise ValidationError("Request is required for add_unsubscribes")

        # Build request body
        body = self._build_suppression_add_body(request)

        logger.debug(f"Adding unsubscribes with body: {body}")

        # Make API call
        response = self.client.post("/v1/suppressions/unsubscribes", json=body)
        
        # Create response model instance
        response_data = response.json()
        suppression_response = SuppressionAddResponse(**response_data)

        logger.info("Added unsubscribes successfully")

        return self._create_response(response, suppression_response)

    def delete_from_blocklist(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete entries from blocklist.

        Args:
            request: Request parameters for deleting from blocklist

        Returns:
            APIResponse with empty data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionDeleteRequest):
            raise ValidationError("Request is required for delete_from_blocklist")

        # Build request body
        body = self._build_suppression_delete_body(request)

        logger.debug(f"Deleting from blocklist with body: {body}")

        # Make API call
        response = self.client.delete("/v1/suppressions/blocklist", json=body)

        logger.info("Deleted from blocklist successfully")

        return self._create_response(response)

    def delete_hard_bounces(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete hard bounces.

        Args:
            request: Request parameters for deleting hard bounces

        Returns:
            APIResponse with empty data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionDeleteRequest):
            raise ValidationError("Request is required for delete_hard_bounces")

        # Build request body (without domain_id for hard bounces)
        body = {}
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all

        logger.debug(f"Deleting hard bounces with body: {body}")

        # Make API call
        response = self.client.delete("/v1/suppressions/hard-bounces", json=body)

        logger.info("Deleted hard bounces successfully")

        return self._create_response(response)

    def delete_spam_complaints(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete spam complaints.

        Args:
            request: Request parameters for deleting spam complaints

        Returns:
            APIResponse with empty data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionDeleteRequest):
            raise ValidationError("Request is required for delete_spam_complaints")

        # Build request body (without domain_id for spam complaints)
        body = {}
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all

        logger.debug(f"Deleting spam complaints with body: {body}")

        # Make API call
        response = self.client.delete("/v1/suppressions/spam-complaints", json=body)

        logger.info("Deleted spam complaints successfully")

        return self._create_response(response)

    def delete_unsubscribes(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete unsubscribes.

        Args:
            request: Request parameters for deleting unsubscribes

        Returns:
            APIResponse with empty data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionDeleteRequest):
            raise ValidationError("Request is required for delete_unsubscribes")

        # Build request body (without domain_id for unsubscribes)
        body = {}
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all

        logger.debug(f"Deleting unsubscribes with body: {body}")

        # Make API call
        response = self.client.delete("/v1/suppressions/unsubscribes", json=body)

        logger.info("Deleted unsubscribes successfully")

        return self._create_response(response)

    def delete_from_on_hold(self, request: SuppressionDeleteRequest) -> APIResponse:
        """
        Delete entries from on-hold list.

        Args:
            request: Request parameters for deleting from on-hold

        Returns:
            APIResponse with empty data

        Raises:
            ValidationError: If request validation fails
        """
        # Validate request
        if not isinstance(request, SuppressionDeleteRequest):
            raise ValidationError("Request is required for delete_from_on_hold")

        # Build request body (without domain_id for on-hold)
        body = {}
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all

        logger.debug(f"Deleting from on-hold with body: {body}")

        # Make API call
        response = self.client.delete("/v1/suppressions/on-hold-list", json=body)

        logger.info("Deleted from on-hold successfully")

        return self._create_response(response)

    def _build_suppression_add_body(self, request: SuppressionAddRequest) -> Dict[str, Any]:
        """Build request body for suppression add operations."""
        body = {}
        
        if request.domain_id:
            body["domain_id"] = request.domain_id
        if request.recipients:
            body["recipients"] = request.recipients
        if request.patterns:
            body["patterns"] = request.patterns
            
        return body

    def _build_suppression_delete_body(self, request: SuppressionDeleteRequest) -> Dict[str, Any]:
        """Build request body for suppression delete operations."""
        body = {}
        
        if request.domain_id:
            body["domain_id"] = request.domain_id
        if request.ids:
            body["ids"] = request.ids
        if request.all is not None:
            body["all"] = request.all
            
        return body 