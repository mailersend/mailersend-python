"""Recipients API resource for MailerSend SDK."""
import logging
from typing import Optional, Dict, Any, Union

from mailersend.exceptions import ValidationError
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

    def list_recipients(
        self,
        request: Optional[RecipientsListRequest] = None,
    ) -> RecipientsListResponse:
        """List recipients with optional filtering and pagination.
        
        Args:
            request: Optional request parameters for filtering and pagination
            
        Returns:
            RecipientsListResponse: The response containing recipients list
            
        Raises:
            ValidationError: If the request is invalid
        """
        logger.debug("Starting list_recipients")
        
        if request is None:
            request = RecipientsListRequest()
        
        # Build query parameters
        params: Dict[str, Any] = {}
        
        if request.domain_id:
            params["domain_id"] = request.domain_id
            logger.debug(f"Added domain_id filter: {request.domain_id}")
        
        if request.page is not None:
            params["page"] = request.page
            logger.debug(f"Added page parameter: {request.page}")
        
        if request.limit is not None:
            params["limit"] = request.limit
            logger.debug(f"Added limit parameter: {request.limit}")
        
        logger.info(f"Fetching recipients list with params: {params}")
        
        response = self.client.get("/v1/recipients", params=params)
        return RecipientsListResponse(**response.json())

    def get_recipient(
        self,
        request: RecipientGetRequest,
    ) -> RecipientResponse:
        """Get a single recipient by ID.
        
        Args:
            request: Request parameters containing recipient ID
            
        Returns:
            RecipientResponse: The response containing recipient data
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for get_recipient")
        
        logger.debug(f"Starting get_recipient for ID: {request.recipient_id}")
        
        url = f"/v1/recipients/{request.recipient_id}"
        logger.info(f"Fetching recipient: {url}")
        
        response = self.client.get(url)
        return RecipientResponse(**response.json())

    def delete_recipient(
        self,
        request: RecipientDeleteRequest,
    ) -> None:
        """Delete a recipient by ID.
        
        Args:
            request: Request parameters containing recipient ID
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for delete_recipient")
        
        logger.debug(f"Starting delete_recipient for ID: {request.recipient_id}")
        
        url = f"/v1/recipients/{request.recipient_id}"
        logger.info(f"Deleting recipient: {url}")
        
        self.client.delete(url)

    def list_blocklist(
        self,
        request: Optional[SuppressionListRequest] = None,
    ) -> BlocklistResponse:
        """List blocklist entries with optional filtering and pagination.
        
        Args:
            request: Optional request parameters for filtering and pagination
            
        Returns:
            BlocklistResponse: The response containing blocklist entries
        """
        logger.debug("Starting list_blocklist")
        
        if request is None:
            request = SuppressionListRequest()
        
        # Build query parameters
        params: Dict[str, Any] = {}
        
        if request.domain_id:
            params["domain_id"] = request.domain_id
            logger.debug(f"Added domain_id filter: {request.domain_id}")
        
        if request.page is not None:
            params["page"] = request.page
            logger.debug(f"Added page parameter: {request.page}")
        
        if request.limit is not None:
            params["limit"] = request.limit
            logger.debug(f"Added limit parameter: {request.limit}")
        
        logger.info(f"Fetching blocklist with params: {params}")
        
        response = self.client.get("/v1/suppressions/blocklist", params=params)
        return BlocklistResponse(**response.json())

    def list_hard_bounces(
        self,
        request: Optional[SuppressionListRequest] = None,
    ) -> HardBouncesResponse:
        """List hard bounces with optional filtering and pagination.
        
        Args:
            request: Optional request parameters for filtering and pagination
            
        Returns:
            HardBouncesResponse: The response containing hard bounces
        """
        logger.debug("Starting list_hard_bounces")
        
        if request is None:
            request = SuppressionListRequest()
        
        # Build query parameters
        params: Dict[str, Any] = {}
        
        if request.domain_id:
            params["domain_id"] = request.domain_id
            logger.debug(f"Added domain_id filter: {request.domain_id}")
        
        if request.page is not None:
            params["page"] = request.page
            logger.debug(f"Added page parameter: {request.page}")
        
        if request.limit is not None:
            params["limit"] = request.limit
            logger.debug(f"Added limit parameter: {request.limit}")
        
        logger.info(f"Fetching hard bounces with params: {params}")
        
        response = self.client.get("/v1/suppressions/hard-bounces", params=params)
        return HardBouncesResponse(**response.json())

    def list_spam_complaints(
        self,
        request: Optional[SuppressionListRequest] = None,
    ) -> SpamComplaintsResponse:
        """List spam complaints with optional filtering and pagination.
        
        Args:
            request: Optional request parameters for filtering and pagination
            
        Returns:
            SpamComplaintsResponse: The response containing spam complaints
        """
        logger.debug("Starting list_spam_complaints")
        
        if request is None:
            request = SuppressionListRequest()
        
        # Build query parameters
        params: Dict[str, Any] = {}
        
        if request.domain_id:
            params["domain_id"] = request.domain_id
            logger.debug(f"Added domain_id filter: {request.domain_id}")
        
        if request.page is not None:
            params["page"] = request.page
            logger.debug(f"Added page parameter: {request.page}")
        
        if request.limit is not None:
            params["limit"] = request.limit
            logger.debug(f"Added limit parameter: {request.limit}")
        
        logger.info(f"Fetching spam complaints with params: {params}")
        
        response = self.client.get("/v1/suppressions/spam-complaints", params=params)
        return SpamComplaintsResponse(**response.json())

    def list_unsubscribes(
        self,
        request: Optional[SuppressionListRequest] = None,
    ) -> UnsubscribesResponse:
        """List unsubscribes with optional filtering and pagination.
        
        Args:
            request: Optional request parameters for filtering and pagination
            
        Returns:
            UnsubscribesResponse: The response containing unsubscribes
        """
        logger.debug("Starting list_unsubscribes")
        
        if request is None:
            request = SuppressionListRequest()
        
        # Build query parameters
        params: Dict[str, Any] = {}
        
        if request.domain_id:
            params["domain_id"] = request.domain_id
            logger.debug(f"Added domain_id filter: {request.domain_id}")
        
        if request.page is not None:
            params["page"] = request.page
            logger.debug(f"Added page parameter: {request.page}")
        
        if request.limit is not None:
            params["limit"] = request.limit
            logger.debug(f"Added limit parameter: {request.limit}")
        
        logger.info(f"Fetching unsubscribes with params: {params}")
        
        response = self.client.get("/v1/suppressions/unsubscribes", params=params)
        return UnsubscribesResponse(**response.json())

    def list_on_hold(
        self,
        request: Optional[SuppressionListRequest] = None,
    ) -> OnHoldResponse:
        """List on-hold entries with optional filtering and pagination.
        
        Args:
            request: Optional request parameters for filtering and pagination
            
        Returns:
            OnHoldResponse: The response containing on-hold entries
        """
        logger.debug("Starting list_on_hold")
        
        if request is None:
            request = SuppressionListRequest()
        
        # Build query parameters
        params: Dict[str, Any] = {}
        
        if request.domain_id:
            params["domain_id"] = request.domain_id
            logger.debug(f"Added domain_id filter: {request.domain_id}")
        
        if request.page is not None:
            params["page"] = request.page
            logger.debug(f"Added page parameter: {request.page}")
        
        if request.limit is not None:
            params["limit"] = request.limit
            logger.debug(f"Added limit parameter: {request.limit}")
        
        logger.info(f"Fetching on-hold list with params: {params}")
        
        response = self.client.get("/v1/suppressions/on-hold-list", params=params)
        return OnHoldResponse(**response.json())

    def add_to_blocklist(
        self,
        request: SuppressionAddRequest,
    ) -> SuppressionAddResponse:
        """Add recipients or patterns to blocklist.
        
        Args:
            request: Request parameters containing domain_id and recipients/patterns
            
        Returns:
            SuppressionAddResponse: The response containing created entries
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for add_to_blocklist")
        
        logger.debug(f"Starting add_to_blocklist for domain: {request.domain_id}")
        
        # Build request body
        body: Dict[str, Any] = {
            "domain_id": request.domain_id,
        }
        
        if request.recipients:
            body["recipients"] = request.recipients
            logger.debug(f"Adding {len(request.recipients)} recipients to blocklist")
        
        if request.patterns:
            body["patterns"] = request.patterns
            logger.debug(f"Adding {len(request.patterns)} patterns to blocklist")
        
        logger.info(f"Adding to blocklist with body: {body}")
        
        response = self.client.post("/v1/suppressions/blocklist", json=body)
        return SuppressionAddResponse(**response.json())

    def add_hard_bounces(
        self,
        request: SuppressionAddRequest,
    ) -> SuppressionAddResponse:
        """Add recipients to hard bounces list.
        
        Args:
            request: Request parameters containing domain_id and recipients
            
        Returns:
            SuppressionAddResponse: The response containing created entries
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for add_hard_bounces")
        
        if not request.recipients:
            raise ValidationError("Recipients are required for add_hard_bounces")
        
        logger.debug(f"Starting add_hard_bounces for domain: {request.domain_id}")
        
        # Build request body
        body: Dict[str, Any] = {
            "domain_id": request.domain_id,
            "recipients": request.recipients,
        }
        
        logger.info(f"Adding {len(request.recipients)} hard bounces")
        
        response = self.client.post("/v1/suppressions/hard-bounces", json=body)
        return SuppressionAddResponse(**response.json())

    def add_spam_complaints(
        self,
        request: SuppressionAddRequest,
    ) -> SuppressionAddResponse:
        """Add recipients to spam complaints list.
        
        Args:
            request: Request parameters containing domain_id and recipients
            
        Returns:
            SuppressionAddResponse: The response containing created entries
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for add_spam_complaints")
        
        if not request.recipients:
            raise ValidationError("Recipients are required for add_spam_complaints")
        
        logger.debug(f"Starting add_spam_complaints for domain: {request.domain_id}")
        
        # Build request body
        body: Dict[str, Any] = {
            "domain_id": request.domain_id,
            "recipients": request.recipients,
        }
        
        logger.info(f"Adding {len(request.recipients)} spam complaints")
        
        response = self.client.post("/v1/suppressions/spam-complaints", json=body)
        return SuppressionAddResponse(**response.json())

    def add_unsubscribes(
        self,
        request: SuppressionAddRequest,
    ) -> SuppressionAddResponse:
        """Add recipients to unsubscribes list.
        
        Args:
            request: Request parameters containing domain_id and recipients
            
        Returns:
            SuppressionAddResponse: The response containing created entries
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for add_unsubscribes")
        
        if not request.recipients:
            raise ValidationError("Recipients are required for add_unsubscribes")
        
        logger.debug(f"Starting add_unsubscribes for domain: {request.domain_id}")
        
        # Build request body
        body: Dict[str, Any] = {
            "domain_id": request.domain_id,
            "recipients": request.recipients,
        }
        
        logger.info(f"Adding {len(request.recipients)} unsubscribes")
        
        response = self.client.post("/v1/suppressions/unsubscribes", json=body)
        return SuppressionAddResponse(**response.json())

    def delete_from_blocklist(
        self,
        request: SuppressionDeleteRequest,
    ) -> None:
        """Delete entries from blocklist.
        
        Args:
            request: Request parameters for deletion
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for delete_from_blocklist")
        
        logger.debug("Starting delete_from_blocklist")
        
        # Build request body
        body: Dict[str, Any] = {}
        
        if request.domain_id:
            body["domain_id"] = request.domain_id
        
        if request.ids:
            body["ids"] = request.ids
            logger.debug(f"Deleting {len(request.ids)} specific entries from blocklist")
        
        if request.all:
            body["all"] = request.all
            logger.debug("Deleting all entries from blocklist")
        
        logger.info(f"Deleting from blocklist with body: {body}")
        
        self.client.delete("/v1/suppressions/blocklist", json=body)

    def delete_hard_bounces(
        self,
        request: SuppressionDeleteRequest,
    ) -> None:
        """Delete entries from hard bounces list.
        
        Args:
            request: Request parameters for deletion
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for delete_hard_bounces")
        
        logger.debug("Starting delete_hard_bounces")
        
        # Build request body
        body: Dict[str, Any] = {}
        
        if request.domain_id:
            body["domain_id"] = request.domain_id
        
        if request.ids:
            body["ids"] = request.ids
            logger.debug(f"Deleting {len(request.ids)} specific hard bounces")
        
        if request.all:
            body["all"] = request.all
            logger.debug("Deleting all hard bounces")
        
        logger.info(f"Deleting hard bounces with body: {body}")
        
        self.client.delete("/v1/suppressions/hard-bounces", json=body)

    def delete_spam_complaints(
        self,
        request: SuppressionDeleteRequest,
    ) -> None:
        """Delete entries from spam complaints list.
        
        Args:
            request: Request parameters for deletion
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for delete_spam_complaints")
        
        logger.debug("Starting delete_spam_complaints")
        
        # Build request body
        body: Dict[str, Any] = {}
        
        if request.domain_id:
            body["domain_id"] = request.domain_id
        
        if request.ids:
            body["ids"] = request.ids
            logger.debug(f"Deleting {len(request.ids)} specific spam complaints")
        
        if request.all:
            body["all"] = request.all
            logger.debug("Deleting all spam complaints")
        
        logger.info(f"Deleting spam complaints with body: {body}")
        
        self.client.delete("/v1/suppressions/spam-complaints", json=body)

    def delete_unsubscribes(
        self,
        request: SuppressionDeleteRequest,
    ) -> None:
        """Delete entries from unsubscribes list.
        
        Args:
            request: Request parameters for deletion
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for delete_unsubscribes")
        
        logger.debug("Starting delete_unsubscribes")
        
        # Build request body
        body: Dict[str, Any] = {}
        
        if request.domain_id:
            body["domain_id"] = request.domain_id
        
        if request.ids:
            body["ids"] = request.ids
            logger.debug(f"Deleting {len(request.ids)} specific unsubscribes")
        
        if request.all:
            body["all"] = request.all
            logger.debug("Deleting all unsubscribes")
        
        logger.info(f"Deleting unsubscribes with body: {body}")
        
        self.client.delete("/v1/suppressions/unsubscribes", json=body)

    def delete_from_on_hold(
        self,
        request: SuppressionDeleteRequest,
    ) -> None:
        """Delete entries from on-hold list.
        
        Args:
            request: Request parameters for deletion
            
        Raises:
            ValidationError: If the request is invalid
        """
        if not request:
            raise ValidationError("Request is required for delete_from_on_hold")
        
        logger.debug("Starting delete_from_on_hold")
        
        # Build request body
        body: Dict[str, Any] = {}
        
        if request.ids:
            body["ids"] = request.ids
            logger.debug(f"Deleting {len(request.ids)} specific on-hold entries")
        
        if request.all:
            body["all"] = request.all
            logger.debug("Deleting all on-hold entries")
        
        logger.info(f"Deleting from on-hold list with body: {body}")
        
        self.client.delete("/v1/suppressions/on-hold-list", json=body) 