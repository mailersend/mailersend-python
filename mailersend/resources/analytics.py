from typing import Dict, Any, Optional

from .base import BaseResource
from ..models.analytics import AnalyticsRequest
from ..models.base import APIResponse
from ..exceptions import ValidationError


class Analytics(BaseResource):
    """
    Client for interacting with the MailerSend Analytics API.
    
    Provides methods for retrieving analytics data grouped by date, country,
    user agent, and reading environment.
    """

    def get_activity_by_date(self, request: AnalyticsRequest) -> APIResponse:
        """
        Retrieve analytics data grouped by date.
        
        Args:
            request: AnalyticsRequest with date range and filtering options
            
        Returns:
            APIResponse with activity data grouped by date
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Retrieving analytics data by date")
        
        if not request:
            self.logger.error("No AnalyticsRequest object provided")
            raise ValidationError("AnalyticsRequest must be provided")
        
        if not request.event:
            self.logger.error("No events specified for date analytics")
            raise ValidationError("At least one event must be specified for date analytics")
        
        # Convert to query parameters
        params = self._build_query_params(request)
        
        self.logger.info("Requesting analytics data by date")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", "analytics/date", params=params)
        
        return self._create_response(response)
    
    def get_opens_by_country(self, request: AnalyticsRequest) -> APIResponse:
        """
        Retrieve analytics data grouped by country.
        
        Args:
            request: AnalyticsRequest with date range and filtering options
            
        Returns:
            APIResponse with opens data grouped by country
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Retrieving analytics data by country")
        
        if not request:
            self.logger.error("No AnalyticsRequest object provided")
            raise ValidationError("AnalyticsRequest must be provided")
        
        # Convert to query parameters (exclude event and group_by for country endpoint)
        params = self._build_query_params(request, exclude_fields=["event", "group_by"])
        
        self.logger.info("Requesting analytics data by country")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", "analytics/country", params=params)
        
        return self._create_response(response)
    
    def get_opens_by_user_agent(self, request: AnalyticsRequest) -> APIResponse:
        """
        Retrieve analytics data grouped by user agent name.
        
        Args:
            request: AnalyticsRequest with date range and filtering options
            
        Returns:
            APIResponse with opens data grouped by user agent
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Retrieving analytics data by user agent")
        
        if not request:
            self.logger.error("No AnalyticsRequest object provided")
            raise ValidationError("AnalyticsRequest must be provided")
        
        # Convert to query parameters (exclude event and group_by for user agent endpoint)
        params = self._build_query_params(request, exclude_fields=["event", "group_by"])
        
        self.logger.info("Requesting analytics data by user agent")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", "analytics/ua-name", params=params)
        
        return self._create_response(response)
    
    def get_opens_by_reading_environment(self, request: AnalyticsRequest) -> APIResponse:
        """
        Retrieve analytics data grouped by reading environment.
        
        Args:
            request: AnalyticsRequest with date range and filtering options
            
        Returns:
            APIResponse with opens data grouped by reading environment
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Retrieving analytics data by reading environment")
        
        if not request:
            self.logger.error("No AnalyticsRequest object provided")
            raise ValidationError("AnalyticsRequest must be provided")
        
        # Convert to query parameters (exclude event and group_by for reading environment endpoint)
        params = self._build_query_params(request, exclude_fields=["event", "group_by"])
        
        self.logger.info("Requesting analytics data by reading environment")
        self.logger.debug(f"Query params: {params}")
        
        response = self.client.request("GET", "analytics/ua-type", params=params)
        
        return self._create_response(response)
    
    def _build_query_params(self, request: AnalyticsRequest, exclude_fields: Optional[list] = None) -> Dict[str, Any]:
        """
        Build query parameters from AnalyticsRequest.
        
        Args:
            request: The AnalyticsRequest object
            exclude_fields: List of fields to exclude from the params
            
        Returns:
            Dictionary of query parameters
        """
        exclude_fields = exclude_fields or []
        
        # Convert model to dict with aliases
        params = request.model_dump(by_alias=True, exclude_none=True)
        
        # Remove excluded fields (including their array versions)
        for field in exclude_fields:
            params.pop(field, None)
            params.pop(f"{field}[]", None)
        
        return params 