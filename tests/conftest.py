# tests/conftest.py
import os
import pytest
from vcr import VCR
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get test API key from environment variables
TEST_API_KEY = os.environ.get("MAILERSEND_API_KEY", "test-api-key")

# Configure VCR globally
vcr = VCR(
    cassette_library_dir="tests/fixtures/cassettes",
    record_mode="once",
    match_on=["method", "scheme", "host", "port", "path", "query", "body"],
    filter_headers=["authorization"],
    filter_post_data_parameters=["api_key", "token"],
    serializer="json"
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