from typing import List, Dict, Any, Generic, TypeVar, Optional, Union
from pydantic import BaseModel as PydanticBaseModel, ConfigDict
import json

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


class HeaderDict(dict):
    """
    A dictionary that supports both dict['key'] and dict.key access patterns.
    Converts dashes to underscores for attribute access.
    """
    
    def __getattr__(self, name):
        # Convert underscores back to dashes for header lookup
        header_name = name.replace('_', '-')
        if header_name in self:
            return self[header_name]
        raise AttributeError(f"Header '{header_name}' not found")
    
    def __setattr__(self, name, value):
        # Convert underscores to dashes and store in dict
        header_name = name.replace('_', '-')
        self[header_name] = value


class APIResponse:
    """
    Unified response container for all API responses.
    
    This class provides a consistent interface for accessing response data,
    headers, and metadata while maintaining backward compatibility.
    
    Examples:
        >>> response = client.emails.send(email)
        >>> email_id = response["id"]  # Dict-like access
        >>> email_id = response.id     # Attribute access
        >>> request_id = response.headers["x-request-id"]        # Dict access
        >>> request_id = response.headers.x_request_id           # Attribute access
        >>> request_id = response["headers"]["x-request-id"]     # Nested dict access
        
        # JSON conversion
        >>> json_str = response.to_json()                       # Method call
        >>> json_str = json.dumps(response)                     # Direct serialization
    """
    
    def __init__(
        self,
        data: Any,
        headers: Dict[str, str],
        status_code: int,
        request_id: Optional[str] = None,
        rate_limit_remaining: Optional[int] = None
    ):
        self.data = data
        self.headers = HeaderDict(headers)  # Use HeaderDict instead of regular dict
        self.status_code = status_code
        self.request_id = request_id
        self.rate_limit_remaining = rate_limit_remaining
    
    def __getitem__(self, key):
        """Allow dict-like access to data and object attributes."""
        # First try data dict
        if isinstance(self.data, dict) and key in self.data:
            return self.data[key]
        elif hasattr(self.data, key):
            return getattr(self.data, key)
        # Then try object attributes (like 'headers', 'status_code', etc.)
        elif hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key '{key}' not found in response data or attributes")
    
    def __contains__(self, key):
        """Support 'in' operator."""
        if isinstance(self.data, dict) and key in self.data:
            return True
        elif hasattr(self.data, key):
            return True
        elif hasattr(self, key):
            return True
        return False
    
    def __getattr__(self, name):
        """Allow direct access to data fields for convenience."""
        if isinstance(self.data, dict) and name in self.data:
            return self.data[name]
        elif hasattr(self.data, name):
            return getattr(self.data, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __repr__(self) -> str:
        return f"APIResponse(status_code={self.status_code}, data={self.data})"
    
    def __str__(self) -> str:
        return str(self.data)
    
    def __iter__(self):
        """Make the object iterable for json.dumps() support."""
        return iter(self.to_dict().items())
    
    def default(self, obj):
        """Custom JSON encoder for json.dumps() support."""
        if isinstance(obj, APIResponse):
            return obj.to_dict()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    @property
    def success(self) -> bool:
        """Whether the request was successful."""
        return 200 <= self.status_code < 300
    
    @property
    def retry_after(self) -> Optional[int]:
        """Get the recommended retry time in seconds from headers."""
        retry_after = self.headers.get("Retry-After") or self.headers.get("retry-after")
        if retry_after:
            try:
                return int(retry_after)
            except (ValueError, TypeError):
                pass
        return None
    
    def get(self, key, default=None):
        """Get a value from data with a default fallback (dict-like interface)."""
        try:
            return self[key]
        except KeyError:
            return default
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to a dictionary for debugging or serialization."""
        return {
            "data": self.data,
            "headers": dict(self.headers),
            "status_code": self.status_code,
            "request_id": self.request_id,
            "rate_limit_remaining": self.rate_limit_remaining,
            "success": self.success
        }
    
    def to_json(self, indent: Optional[int] = None, **kwargs) -> str:
        """
        Convert response to JSON string.
        
        Args:
            indent: Number of spaces for indentation (None for compact JSON)
            **kwargs: Additional arguments passed to json.dumps()
            
        Returns:
            JSON string representation of the response
            
        Examples:
            >>> response.to_json()                    # Compact JSON
            >>> response.to_json(indent=2)            # Pretty-printed JSON
            >>> response.to_json(ensure_ascii=False)  # Custom json.dumps args
        """
        return json.dumps(self.to_dict(), indent=indent, **kwargs)
    
    def keys(self):
        """Support dict-like interface for json.dumps()."""
        return self.to_dict().keys()
    
    def values(self):
        """Support dict-like interface for json.dumps()."""
        return self.to_dict().values()
    
    def items(self):
        """Support dict-like interface for json.dumps()."""
        return self.to_dict().items()


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