import pytest
from mailersend.models.base import APIResponse


class TestAPIResponse:
    """Test suite for the unified APIResponse class."""
    
    def test_basic_response_creation(self):
        """Test basic APIResponse creation and properties."""
        data = {"id": "12345", "status": "sent"}
        headers = {"x-request-id": "req-123", "x-apiquota-remaining": "1000"}
        
        response = APIResponse(
            data=data,
            headers=headers,
            status_code=200,
            request_id="req-123",
            rate_limit_remaining=1000
        )
        
        assert response.data == data
        assert response.headers == headers
        assert response.status_code == 200
        assert response.request_id == "req-123"
        assert response.rate_limit_remaining == 1000
        assert response.success is True
    
    def test_dict_like_access(self):
        """Test dict-like access to response data."""
        data = {"id": "12345", "status": "sent"}
        response = APIResponse(
            data=data,
            headers={},
            status_code=200
        )
        
        # Test __getitem__
        assert response["id"] == "12345"
        assert response["status"] == "sent"
        
        # Test __contains__
        assert "id" in response
        assert "status" in response
        assert "nonexistent" not in response
        
        # Test get method with default
        assert response.get("id") == "12345"
        assert response.get("nonexistent", "default") == "default"
    
    def test_attribute_access(self):
        """Test direct attribute access to response data."""
        data = {"id": "12345", "status": "sent"}
        response = APIResponse(
            data=data,
            headers={},
            status_code=200
        )
        
        # Test __getattr__
        assert response.id == "12345"
        assert response.status == "sent"
        
        # Test AttributeError for non-existent attributes
        with pytest.raises(AttributeError):
            _ = response.nonexistent
    
    def test_success_property(self):
        """Test success property for different status codes."""
        # Test successful responses
        for status_code in [200, 201, 204, 299]:
            response = APIResponse(
                data={},
                headers={},
                status_code=status_code
            )
            assert response.success is True
        
        # Test error responses
        for status_code in [400, 401, 404, 500]:
            response = APIResponse(
                data={},
                headers={},
                status_code=status_code
            )
            assert response.success is False
    
    def test_retry_after_property(self):
        """Test retry_after property extraction from headers."""
        # Test with Retry-After header
        response = APIResponse(
            data={},
            headers={"Retry-After": "60"},
            status_code=429
        )
        assert response.retry_after == 60
        
        # Test with lowercase header
        response = APIResponse(
            data={},
            headers={"retry-after": "120"},
            status_code=429
        )
        assert response.retry_after == 120
        
        # Test without header
        response = APIResponse(
            data={},
            headers={},
            status_code=200
        )
        assert response.retry_after is None
        
        # Test with invalid value
        response = APIResponse(
            data={},
            headers={"Retry-After": "invalid"},
            status_code=429
        )
        assert response.retry_after is None
    
    def test_to_dict_method(self):
        """Test conversion to dictionary."""
        data = {"id": "12345"}
        headers = {"x-request-id": "req-123"}
        response = APIResponse(
            data=data,
            headers=headers,
            status_code=200,
            request_id="req-123",
            rate_limit_remaining=1000
        )
        
        result = response.to_dict()
        expected = {
            "data": data,
            "headers": headers,
            "status_code": 200,
            "request_id": "req-123",
            "rate_limit_remaining": 1000,
            "success": True
        }
        
        assert result == expected
    
    def test_string_representations(self):
        """Test __repr__ and __str__ methods."""
        data = {"id": "12345"}
        response = APIResponse(
            data=data,
            headers={},
            status_code=200
        )
        
        assert "APIResponse" in repr(response)
        assert "200" in repr(response)
        assert str(response) == str(data)
    
    def test_complex_data_structures(self):
        """Test with complex nested data structures."""
        data = {
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ],
            "meta": {
                "total": 2,
                "page": 1
            }
        }
        
        response = APIResponse(
            data=data,
            headers={},
            status_code=200
        )
        
        # Test nested access
        assert response["items"][0]["name"] == "Item 1"
        assert response["meta"]["total"] == 2
        
        # Test attribute-style access
        assert response.items[0]["name"] == "Item 1"
        assert response.meta["total"] == 2 