import json
import pytest
from mailersend.models.base import APIResponse


def test_to_json_method():
    """Test the to_json() method with various options."""
    
    data = {"id": "msg-12345", "status": "sent"}
    headers = {"x-request-id": "req-456", "content-type": "application/json"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=202,
        request_id="req-456",
        rate_limit_remaining=1000
    )
    
    # Test compact JSON
    json_str = response.to_json()
    assert isinstance(json_str, str)
    parsed = json.loads(json_str)
    assert parsed["data"] == data
    assert parsed["headers"] == headers
    assert parsed["status_code"] == 202
    assert parsed["success"] is True
    
    # Test pretty-printed JSON
    pretty_json = response.to_json(indent=2)
    assert "\n" in pretty_json
    assert "  " in pretty_json  # Check for indentation
    
    # Verify pretty JSON content is the same
    parsed_pretty = json.loads(pretty_json)
    assert parsed_pretty == parsed


def test_json_dumps_direct():
    """Test that json.dumps() works directly on APIResponse."""
    
    data = {"id": "msg-12345", "status": "sent"}
    headers = {"x-request-id": "req-456"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=200
    )
    
    # This should work thanks to the dict-like interface
    json_str = json.dumps(dict(response))
    parsed = json.loads(json_str)
    
    assert parsed["data"] == data
    assert parsed["headers"] == headers
    assert parsed["status_code"] == 200
    assert parsed["success"] is True


def test_dict_like_interface_for_json():
    """Test that APIResponse behaves like a dict for JSON serialization."""
    
    data = {"id": "msg-12345"}
    headers = {"x-request-id": "req-456"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=201
    )
    
    # Test dict-like methods
    keys = list(response.keys())
    values = list(response.values())
    items = list(response.items())
    
    assert "data" in keys
    assert "headers" in keys
    assert "status_code" in keys
    assert "success" in keys
    
    assert data in values
    assert 201 in values
    assert True in values  # success
    
    # Test that items() returns key-value pairs
    items_dict = dict(items)
    assert items_dict["data"] == data
    assert items_dict["status_code"] == 201


def test_json_serialization_with_complex_data():
    """Test JSON serialization with nested/complex data structures."""
    
    complex_data = {
        "emails": [
            {"id": "email-1", "to": "user1@example.com"},
            {"id": "email-2", "to": "user2@example.com"}
        ],
        "meta": {
            "total": 2,
            "processed": 2
        }
    }
    
    headers = {
        "x-request-id": "req-789",
        "x-total-count": "2"
    }
    
    response = APIResponse(
        data=complex_data,
        headers=headers,
        status_code=200
    )
    
    # Test JSON conversion
    json_str = response.to_json(indent=2)
    parsed = json.loads(json_str)
    
    # Verify nested structure is preserved
    assert len(parsed["data"]["emails"]) == 2
    assert parsed["data"]["emails"][0]["id"] == "email-1"
    assert parsed["data"]["meta"]["total"] == 2
    assert parsed["headers"]["x-total-count"] == "2"


def test_json_with_none_values():
    """Test JSON serialization handles None values correctly."""
    
    data = {"id": "msg-12345", "error": None}
    headers = {"x-request-id": "req-456"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=200,
        request_id=None,  # None value
        rate_limit_remaining=None  # None value
    )
    
    json_str = response.to_json()
    parsed = json.loads(json_str)
    
    # Verify None values are preserved in JSON
    assert parsed["data"]["error"] is None
    assert parsed["request_id"] is None
    assert parsed["rate_limit_remaining"] is None


def test_json_comparison():
    """Test that to_json() and json.dumps(dict(response)) produce equivalent results."""
    
    data = {"id": "msg-12345", "status": "sent"}
    headers = {"x-request-id": "req-456"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=202,
        request_id="req-456",
        rate_limit_remaining=500
    )
    
    # Get JSON via both methods
    method1 = response.to_json()
    method2 = json.dumps(dict(response))
    
    # Parse both and compare
    parsed1 = json.loads(method1)
    parsed2 = json.loads(method2)
    
    assert parsed1 == parsed2


def test_json_custom_encoder_args():
    """Test that custom json.dumps arguments work with to_json()."""
    
    data = {"message": "Hello, 世界!"}  # Unicode content
    headers = {"x-request-id": "req-456"}
    
    response = APIResponse(
        data=data,
        headers=headers,
        status_code=200
    )
    
    # Test with ensure_ascii=False
    json_unicode = response.to_json(ensure_ascii=False)
    assert "世界" in json_unicode  # Unicode should be preserved
    
    # Test with ensure_ascii=True (default)
    json_ascii = response.to_json(ensure_ascii=True)
    assert "\\u" in json_ascii  # Unicode should be escaped 