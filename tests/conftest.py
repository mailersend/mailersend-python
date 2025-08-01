# tests/conftest.py
import os
import pytest
import re
from vcr import VCR
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get test API key from environment variables
TEST_API_KEY = os.environ.get("MAILERSEND_API_KEY", "test-api-key")


def sanitize_response_body(response):
    """Sanitize response body to remove sensitive data like accessToken."""
    try:
        # Get the response body - handle different VCR formats
        body = None
        if response.get('body'):
            if isinstance(response['body'], dict):
                body = response['body'].get('string')
            else:
                body = response['body']
        
        if not body:
            return response
            
        # Convert bytes to string if needed
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
        # Only process if it looks like JSON (contains accessToken)
        if 'accessToken' in body or 'mlsn.' in body:
            # Replace accessToken values
            body = re.sub(
                r'"accessToken":"mlsn\.[a-f0-9]+"',
                '"accessToken":"***FILTERED***"',
                body
            )
            
            # Replace any other mlsn tokens
            body = re.sub(
                r'"mlsn\.[a-f0-9]{60,}"',
                '"***FILTERED***"',
                body
            )
            
            # Replace preview tokens
            body = re.sub(
                r'"preview":"mlsn\.[a-f0-9]+"',
                '"preview":"***FILTERED***"',
                body
            )
            
            # Update the response body (convert back to bytes for VCR)
            if isinstance(response['body'], dict):
                response['body']['string'] = body.encode('utf-8')
            else:
                response['body'] = body.encode('utf-8')
        
    except Exception as e:
        print(f"[VCR FILTER] Error sanitizing response: {e}")
        # Don't fail tests if filtering fails
        pass
    
    return response


# Configure VCR globally
vcr = VCR(
    cassette_library_dir="tests/fixtures/cassettes",
    record_mode="once",
    match_on=["method", "scheme", "host", "port", "path", "query", "body"],
    filter_headers=["authorization"],
    filter_post_data_parameters=["api_key", "token", "accessToken"],
    serializer="yaml",
    before_record_response=sanitize_response_body,
)

# Create a pytest fixture for the API key
@pytest.fixture
def api_key():
    """Return the test API key."""
    return TEST_API_KEY


# Create a fixture for the client
@pytest.fixture
def email_client(api_key):
    """Create and return an Email client instance."""
    from mailersend.client import MailerSendClient

    client = MailerSendClient(api_key=api_key)

    return client
