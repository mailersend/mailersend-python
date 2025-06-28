"""Templates resource for MailerSend SDK."""
from typing import Optional
import logging

from .base import BaseResource
from ..models.base import APIResponse
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

    def list_templates(self, request: Optional[TemplatesListRequest] = None) -> APIResponse:
        """
        Retrieve a list of templates.
        
        Args:
            request: Optional TemplatesListRequest with filtering and pagination options
            
        Returns:
            APIResponse with TemplatesListResponse data
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        logger.debug("Starting list_templates operation")
        
        # Validate and prepare request
        if request is None:
            request = TemplatesListRequest()
        
        logger.debug(f"Templates list request: {request}")
        
        # Extract query parameters
        params = request.to_query_params()
        
        logger.info(f"Fetching templates with params: {params}")
        
        # Make API call
        response = self.client.request("GET", "templates", params=params)
        
        # Create standardized response
        return self._create_response(
            response,
            TemplatesListResponse(**response.json())
        )

    def get_template(self, request: TemplateGetRequest) -> APIResponse:
        """
        Retrieve information about a single template.
        
        Args:
            request: TemplateGetRequest with template ID
            
        Returns:
            APIResponse with TemplateResponse data
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        logger.debug("Starting get_template operation")
        
        # Validate request
        if not request:
            logger.error("TemplateGetRequest is required")
            raise ValidationError("TemplateGetRequest must be provided")
        
        if not isinstance(request, TemplateGetRequest):
            logger.error(f"Expected TemplateGetRequest, got {type(request).__name__}")
            raise ValidationError("request must be a TemplateGetRequest instance")
        
        logger.debug(f"Template get request: {request}")
        
        # Prepare API call
        url = f"templates/{request.template_id}"
        logger.info(f"Fetching template: {url}")
        
        # Make API call
        response = self.client.request("GET", url)
        
        # Create standardized response
        return self._create_response(
            response,
            TemplateResponse(**response.json())
        )

    def delete_template(self, request: TemplateDeleteRequest) -> APIResponse:
        """
        Delete a template.
        
        Args:
            request: TemplateDeleteRequest with template ID to delete
            
        Returns:
            APIResponse with empty data
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        logger.debug("Starting delete_template operation")
        
        # Validate request
        if not request:
            logger.error("TemplateDeleteRequest is required")
            raise ValidationError("TemplateDeleteRequest must be provided")
        
        if not isinstance(request, TemplateDeleteRequest):
            logger.error(f"Expected TemplateDeleteRequest, got {type(request).__name__}")
            raise ValidationError("request must be a TemplateDeleteRequest instance")
        
        logger.debug(f"Template delete request: {request}")
        
        # Prepare API call
        url = f"templates/{request.template_id}"
        logger.info(f"Deleting template: {url}")
        
        # Make API call
        response = self.client.request("DELETE", url)
        
        # Create standardized response
        return self._create_response(response) 