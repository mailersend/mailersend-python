from typing import Dict, Any, Optional, Union, List, TypeVar, Type, ClassVar
from ..utils.api_helpers import ApiHelpers
from ..models.base import BaseModel, ModelList

T = TypeVar('T', bound=BaseModel)


class BaseResource:
    """Base class for all API resources."""
    
    BASE_API_URL: ClassVar[str] = ""
    MODEL_CLASS: ClassVar[Type[BaseModel]] = BaseModel
    
    def __init__(self, client):
        """
        Initialize a resource with the API client.
        
        Args:
            client: The MailerSendClient instance
        """
        self.client = client
        
    def _process_response(self, response_data: Dict[str, Any], model_class: Optional[Type[T]] = None) -> Union[T, ModelList[T], Dict[str, Any]]:
        """
        Process the API response data into model instances.
        
        Args:
            response_data: The raw API response data
            model_class: The model class to use for conversion
            
        Returns:
            Processed model instance(s) or raw data
        """
        cls = model_class or self.MODEL_CLASS
        
        if not cls:
            return response_data
            
        # Handle pagination results
        if isinstance(response_data, dict) and "data" in response_data:
            items = [cls(**item) for item in response_data["data"]]
            return ModelList(
                items=items,
                meta=response_data.get("meta", {}),
                links=response_data.get("links", {})
            )
            
        # Handle single item
        if isinstance(response_data, dict):
            return cls(**response_data)
            
        # Handle list of items
        if isinstance(response_data, list):
            return [cls(**item) for item in response_data]
            
        return response_data