from typing import Dict, Any, Optional
import logging

from .base import BaseResource
from ..models.templates import (
    TemplatesListRequest, TemplateGetRequest, TemplateDeleteRequest,
    TemplatesListResponse, TemplateResponse
)
from ..exceptions import ValidationError

logger = logging.getLogger(__name__)


class Templates(BaseResource):
    """
    Client for interacting with the MailerSend Templates API.
    
    Provides methods for managing templates including listing,
    retrieving single templates, and deleting templates.
    """

    def list_templates(self, request: Optional[TemplatesListRequest] = None) -> TemplatesListResponse:
        """
        Retrieve a list of templates.
        
        Args:
            request: Optional TemplatesListRequest with filtering and pagination options
            
        Returns:
            TemplatesListResponse with list of templates
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        logger.debug("Retrieving templates list")
        
        # Convert to query parameters
        params = {}
        if request:
            if request.domain_id:
                params['domain_id'] = request.domain_id
            if request.page:
                params['page'] = request.page
            if request.limit:
                params['limit'] = request.limit
        
        # Default limit if not specified
        if 'limit' not in params:
            params['limit'] = 25
        
        logger.info(f"Fetching templates with params: {params}")
        
        response = self.client.request("GET", "templates", params=params)
        return TemplatesListResponse(**response.json())

    def get_template(self, request: TemplateGetRequest) -> TemplateResponse:
        """
        Retrieve information about a single template.
        
        Args:
            request: TemplateGetRequest with template ID
            
        Returns:
            TemplateResponse with template information
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        if not request:
            logger.error("No TemplateGetRequest object provided")
            raise ValidationError("TemplateGetRequest must be provided")
        
        url = f"templates/{request.template_id}"
        logger.info(f"Fetching template: {url}")
        
        response = self.client.request("GET", url)
        return TemplateResponse(**response.json())

    def delete_template(self, request: TemplateDeleteRequest) -> None:
        """
        Delete a template.
        
        Args:
            request: TemplateDeleteRequest with template ID to delete
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        if not request:
            logger.error("No TemplateDeleteRequest object provided")
            raise ValidationError("TemplateDeleteRequest must be provided")
        
        url = f"templates/{request.template_id}"
        logger.info(f"Deleting template: {url}")
        
        self.client.request("DELETE", url) 