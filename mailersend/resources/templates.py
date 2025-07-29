"""Templates resource for MailerSend SDK."""

from typing import Optional

from .base import BaseResource
from ..models.base import APIResponse
from ..models.templates import (
    TemplatesListRequest,
    TemplateGetRequest,
    TemplateDeleteRequest,
)

class Templates(BaseResource):
    """
    Client for interacting with the MailerSend Templates API.

    Provides methods for managing templates including listing,
    retrieving single templates, and deleting templates.
    """

    def list_templates(
        self, request: Optional[TemplatesListRequest] = None
    ) -> APIResponse:
        """
        Retrieve a list of templates.

        Args:
            request: Optional TemplatesListRequest with filtering and pagination options

        Returns:
            APIResponse with TemplatesListResponse data
        """
        self.logger.debug("Starting list_templates operation")

        # Validate and prepare request
        if request is None:
            request = TemplatesListRequest()

        self.logger.debug(f"Templates list request: {request}")

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(f"Fetching templates with params: {params}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint="templates", params=params
        )

        # Create standardized response
        return self._create_response(response)

    def get_template(self, request: TemplateGetRequest) -> APIResponse:
        """
        Retrieve information about a single template.

        Args:
            request: TemplateGetRequest with template ID

        Returns:
            APIResponse with TemplateResponse data
        """
        self.logger.debug(f"Template get request: {request}")

        # Make API call
        response = self.client.request(
            method="GET", endpoint=f"templates/{request.template_id}"
        )

        # Create standardized response
        return self._create_response(response)

    def delete_template(self, request: TemplateDeleteRequest) -> APIResponse:
        """
        Delete a template.

        Args:
            request: TemplateDeleteRequest with template ID to delete

        Returns:
            APIResponse with empty data
        """
        self.logger.debug("Starting delete_template operation")
        self.logger.debug(f"Deleting template: {request.template_id}")

        # Make API call
        response = self.client.request(
            method="DELETE", endpoint=f"templates/{request.template_id}"
        )

        # Create standardized response
        return self._create_response(response)
