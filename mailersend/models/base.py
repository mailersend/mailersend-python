from typing import List, Dict, Any, Generic, TypeVar, Optional
from pydantic import BaseModel as PydanticBaseModel, ConfigDict

T = TypeVar('T')

class BaseModel(PydanticBaseModel):
    """
    Base model for all MailerSend data models.
    
    Extends Pydantic's BaseModel with common functionality for all models
    in the MailerSend SDK.
    """

    # Allow extra fields that might be sent by the API but not defined in models
    # Allow field population by alias to support API responses with different naming
    model_config = ConfigDict(validate_by_name=True, extra="ignore")
        
    @classmethod
    def from_api(cls, data: Dict[str, Any]):
        """
        Create a model instance from API response data.
        
        Args:
            data: API response data dictionary
            
        Returns:
            Initialized model instance
        """
        return cls(**data)


class ModelList(Generic[T]):
    """
    Container for paginated lists of models returned by the API.
    
    Provides access to the items along with pagination metadata.
    """
    
    def __init__(
        self, 
        items: List[T], 
        meta: Optional[Dict[str, Any]] = None,
        links: Optional[Dict[str, Any]] = None
    ):
        self.items = items
        self.meta = meta or {}
        self.links = links or {}
        
    def __iter__(self):
        return iter(self.items)
        
    def __getitem__(self, index):
        return self.items[index]
    
    def __len__(self):
        return len(self.items)
    
    @property
    def total(self) -> int:
        """Total number of items across all pages."""
        return self.meta.get("total", len(self.items))
    
    @property
    def count(self) -> int:
        """Number of items in the current page."""
        return self.meta.get("count", len(self.items))
    
    @property
    def per_page(self) -> int:
        """Number of items per page."""
        return self.meta.get("per_page", len(self.items))
    
    @property
    def current_page(self) -> int:
        """Current page number."""
        return self.meta.get("current_page", 1)
    
    @property
    def last_page(self) -> int:
        """Last page number."""
        return self.meta.get("last_page", 1)
    
    @property
    def has_more_pages(self) -> bool:
        """Whether there are more pages available."""
        return self.current_page < self.last_page