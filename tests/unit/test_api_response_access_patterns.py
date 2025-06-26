import pytest
from mailersend.models.base import APIResponse


def test_all_access_patterns_work():
    """Test that all access patterns work correctly"""
    data = {
        "id": "123",
        "name": "Test Item",
        "nested": {
            "value": "nested_value"
        }
    }
    headers = {
        "x-request-id": "req-123",
        "content-type": "application/json"
    }
    
    response = APIResponse(data=data, headers=headers, status_code=200)
    
    # Dict-style access
    assert response["id"] == "123"
    assert response["name"] == "Test Item"
    assert response["nested"]["value"] == "nested_value"
    
    # Attribute-style access
    assert response.id == "123"
    assert response.name == "Test Item"
    
    # Headers access
    assert response.headers["x-request-id"] == "req-123"
    assert response.headers.x_request_id == "req-123"  # dash to underscore conversion
    assert response["headers"]["x-request-id"] == "req-123"


def test_header_dict_functionality():
    """Test HeaderDict specific functionality"""
    headers = {
        "x-request-id": "req-123",
        "content-type": "application/json",
        "X-Rate-Limit": "100"
    }
    
    response = APIResponse(data={}, headers=headers, status_code=200)
    
    # Test dash-to-underscore conversion
    assert response.headers.x_request_id == "req-123"
    assert response.headers.content_type == "application/json"
    assert response.headers.X_Rate_Limit == "100"
    
    # Test original access still works
    assert response.headers["x-request-id"] == "req-123"
    assert response.headers["content-type"] == "application/json"


def test_priority_order():
    """Test that access priority works correctly"""
    # If a field exists in both data and as an attribute, data should win for __getattr__
    data = {"status_code": 999}  # This conflicts with the actual status_code attribute
    response = APIResponse(data=data, headers={}, status_code=200)
    
    # Dict access should get from data
    assert response["status_code"] == 999
    
    # Direct attribute access should get the actual attribute
    assert response.status_code == 200
    
    # __getattr__ should get from data (when attribute doesn't exist directly)
    # But status_code exists directly, so this won't trigger __getattr__


def test_error_cases():
    """Test error handling for invalid access"""
    response = APIResponse(data={"valid_field": "value"}, headers={}, status_code=200)
    
    # Non-existent field should raise KeyError for dict access
    with pytest.raises(KeyError):
        _ = response["nonexistent"]
    
    # Non-existent field should raise AttributeError for attribute access
    with pytest.raises(AttributeError):
        _ = response.nonexistent


def test_method_name_conflicts():
    """Test handling of method name conflicts with data fields"""
    data = {
        "items": [{"id": 1, "name": "Item 1"}],
        "keys": ["key1", "key2"],
        "values": [1, 2, 3],
        "get": "some_value"
    }
    
    response = APIResponse(data=data, headers={}, status_code=200)
    
    # Dict access should work for conflicting names
    assert response["items"][0]["name"] == "Item 1"
    assert response["keys"] == ["key1", "key2"]
    assert response["values"] == [1, 2, 3]
    assert response["get"] == "some_value"
    
    # data_ prefix should work for conflicting names
    assert response.data_items[0]["name"] == "Item 1"
    assert response.data_keys == ["key1", "key2"]
    assert response.data_values == [1, 2, 3]
    assert response.data_get == "some_value"
    
    # Method access should still work (not return data)
    assert callable(response.items)  # Should be the method, not the data
    assert callable(response.keys)   # Should be the method, not the data
    assert callable(response.values) # Should be the method, not the data
    
    # Test that data_ prefix fails for non-existent fields
    with pytest.raises(AttributeError, match="Data field 'nonexistent' not found"):
        _ = response.data_nonexistent 