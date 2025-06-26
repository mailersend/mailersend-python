import pytest
from mailersend.models.base import APIResponse


def test_all_access_patterns_work():
    """Test that all desired access patterns now work."""
    
    # Create a sample response
    data = {"id": "msg-12345", "status": "sent"}
    headers = {"x-request-id": "req-456", "x-apiquota-remaining": "1000"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=202,
        request_id="req-456",
        rate_limit_remaining=1000
    )
    
    # Test data access patterns
    assert response["id"] == "msg-12345"          # Dict-like access
    assert response.id == "msg-12345"             # Attribute access
    
    # Test header access patterns - ALL should work now
    assert response.headers["x-request-id"] == "req-456"        # Direct dict access
    assert response.headers.x_request_id == "req-456"          # Attribute access with underscore
    assert response["headers"]["x-request-id"] == "req-456"    # Nested dict access
    
    # Test other object attributes
    assert response["status_code"] == 202         # Object attribute via dict access
    assert response.status_code == 202            # Object attribute via attribute access
    
    # Test 'in' operator
    assert "id" in response                       # Data field
    assert "headers" in response                  # Object attribute
    assert "status_code" in response              # Object attribute


def test_header_dict_functionality():
    """Test HeaderDict specific functionality."""
    
    data = {"id": "msg-12345"}
    headers = {"x-request-id": "req-456", "content-type": "application/json"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=202
    )
    
    # Test HeaderDict attribute access with dash-to-underscore conversion
    assert response.headers.x_request_id == "req-456"          # x-request-id → x_request_id
    assert response.headers.content_type == "application/json" # content-type → content_type
    
    # Original dict access still works
    assert response.headers["x-request-id"] == "req-456"
    assert response.headers["content-type"] == "application/json"


def test_priority_order():
    """Test that data fields take priority over object attributes."""
    
    # Create response where data has a field that conflicts with object attribute
    data = {"headers": "this-is-data-not-headers"}
    headers = {"x-request-id": "req-456"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=202
    )
    
    # Data field should take priority
    assert response["headers"] == "this-is-data-not-headers"
    assert response.headers["x-request-id"] == "req-456"  # But actual headers still accessible


def test_error_cases():
    """Test appropriate errors for non-existent keys/attributes."""
    
    data = {"id": "msg-12345"}
    headers = {"x-request-id": "req-456"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=202
    )
    
    # Non-existent data field
    with pytest.raises(KeyError):
        _ = response["nonexistent"]
    
    # Non-existent header
    with pytest.raises(AttributeError):
        _ = response.headers.nonexistent_header 