"""Unit tests for Recipients resource."""
import pytest
from unittest.mock import Mock, patch
from requests import Response

from mailersend.resources.recipients import Recipients
from mailersend.models.recipients import (
    RecipientsListRequest,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
    RecipientsListResponse,
    RecipientResponse,
    BlocklistResponse,
    HardBouncesResponse,
    SpamComplaintsResponse,
    UnsubscribesResponse,
    OnHoldResponse,
    SuppressionAddResponse,
)
from mailersend.exceptions import ValidationError


class TestRecipientsResource:
    """Test Recipients resource."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()

    @pytest.fixture
    def recipients_resource(self, mock_client):
        """Create Recipients resource with mock client."""
        return Recipients(mock_client)

    def test_list_recipients_default(self, recipients_resource, mock_client):
        """Test listing recipients with default parameters."""
        # Setup mock response
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "recipient123",
                    "email": "test@example.com",
                    "created_at": "2020-06-10T10:09:56Z",
                    "updated_at": "2020-06-10T10:09:56Z",
                    "deleted_at": "",
                }
            ],
            "links": {"first": "https://api.mailersend.com/v1/recipients?page=1"},
            "meta": {"current_page": 1, "per_page": 25, "total": 1},
        }
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_recipients()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/recipients", params={"limit": 25})
        assert isinstance(response, RecipientsListResponse)
        assert len(response.data) == 1
        assert response.data[0].id == "recipient123"

    def test_list_recipients_with_request(self, recipients_resource, mock_client):
        """Test listing recipients with request parameters."""
        # Setup
        request = RecipientsListRequest(
            domain_id="domain123",
            page=2,
            limit=50,
        )
        
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {
            "data": [],
            "links": {},
            "meta": {},
        }
        mock_client.get.return_value = mock_response

        # Test
        recipients_resource.list_recipients(request)

        # Assertions
        expected_params = {
            "domain_id": "domain123",
            "page": 2,
            "limit": 50,
        }
        mock_client.get.assert_called_once_with("/v1/recipients", params=expected_params)

    def test_get_recipient(self, recipients_resource, mock_client):
        """Test getting a single recipient."""
        # Setup
        request = RecipientGetRequest(recipient_id="recipient123")
        
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {
            "data": {
                "id": "recipient123",
                "email": "test@example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
                "deleted_at": "",
            }
        }
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.get_recipient(request)

        # Assertions
        mock_client.get.assert_called_once_with("/v1/recipients/recipient123")
        assert isinstance(response, RecipientResponse)
        assert response.data.id == "recipient123"

    def test_get_recipient_no_request(self, recipients_resource):
        """Test getting recipient without request raises error."""
        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.get_recipient(None)
        assert "Request is required for get_recipient" in str(exc_info.value)

    def test_delete_recipient(self, recipients_resource, mock_client):
        """Test deleting a recipient."""
        # Setup
        request = RecipientDeleteRequest(recipient_id="recipient123")

        # Test
        recipients_resource.delete_recipient(request)

        # Assertions
        mock_client.delete.assert_called_once_with("/v1/recipients/recipient123")

    def test_delete_recipient_no_request(self, recipients_resource):
        """Test deleting recipient without request raises error."""
        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.delete_recipient(None)
        assert "Request is required for delete_recipient" in str(exc_info.value)

    def test_list_blocklist(self, recipients_resource, mock_client):
        """Test listing blocklist entries."""
        # Setup
        request = SuppressionListRequest(
            domain_id="domain123",
            page=1,
            limit=25,
        )
        
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "entry123",
                    "type": "pattern",
                    "pattern": ".*@example.com",
                    "created_at": "2020-06-10T10:09:56Z",
                    "updated_at": "2020-06-10T10:09:56Z",
                }
            ]
        }
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_blocklist(request)

        # Assertions
        expected_params = {
            "domain_id": "domain123",
            "page": 1,
            "limit": 25,
        }
        mock_client.get.assert_called_once_with("/v1/suppressions/blocklist", params=expected_params)
        assert isinstance(response, BlocklistResponse)

    def test_list_hard_bounces(self, recipients_resource, mock_client):
        """Test listing hard bounces."""
        # Setup
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_hard_bounces()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/suppressions/hard-bounces", params={"limit": 25})
        assert isinstance(response, HardBouncesResponse)

    def test_list_spam_complaints(self, recipients_resource, mock_client):
        """Test listing spam complaints."""
        # Setup
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_spam_complaints()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/suppressions/spam-complaints", params={"limit": 25})
        assert isinstance(response, SpamComplaintsResponse)

    def test_list_unsubscribes(self, recipients_resource, mock_client):
        """Test listing unsubscribes."""
        # Setup
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_unsubscribes()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/suppressions/unsubscribes", params={"limit": 25})
        assert isinstance(response, UnsubscribesResponse)

    def test_list_on_hold(self, recipients_resource, mock_client):
        """Test listing on-hold entries."""
        # Setup
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_on_hold()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/suppressions/on-hold-list", params={"limit": 25})
        assert isinstance(response, OnHoldResponse)

    def test_add_to_blocklist(self, recipients_resource, mock_client):
        """Test adding to blocklist."""
        # Setup
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
            patterns=[".*@example.com"],
        )
        
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.post.return_value = mock_response

        # Test
        response = recipients_resource.add_to_blocklist(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
            "patterns": [".*@example.com"],
        }
        mock_client.post.assert_called_once_with("/v1/suppressions/blocklist", json=expected_body)
        assert isinstance(response, SuppressionAddResponse)

    def test_add_to_blocklist_no_request(self, recipients_resource):
        """Test adding to blocklist without request raises error."""
        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.add_to_blocklist(None)
        assert "Request is required for add_to_blocklist" in str(exc_info.value)

    def test_add_hard_bounces(self, recipients_resource, mock_client):
        """Test adding hard bounces."""
        # Setup
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
        )
        
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.post.return_value = mock_response

        # Test
        response = recipients_resource.add_hard_bounces(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
        }
        mock_client.post.assert_called_once_with("/v1/suppressions/hard-bounces", json=expected_body)
        assert isinstance(response, SuppressionAddResponse)

    def test_add_hard_bounces_no_recipients(self, recipients_resource):
        """Test adding hard bounces without recipients raises error."""
        request = SuppressionAddRequest(domain_id="domain123")
        
        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.add_hard_bounces(request)
        assert "Recipients are required for add_hard_bounces" in str(exc_info.value)

    def test_add_spam_complaints(self, recipients_resource, mock_client):
        """Test adding spam complaints."""
        # Setup
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
        )
        
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.post.return_value = mock_response

        # Test
        response = recipients_resource.add_spam_complaints(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
        }
        mock_client.post.assert_called_once_with("/v1/suppressions/spam-complaints", json=expected_body)
        assert isinstance(response, SuppressionAddResponse)

    def test_add_unsubscribes(self, recipients_resource, mock_client):
        """Test adding unsubscribes."""
        # Setup
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
        )
        
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.post.return_value = mock_response

        # Test
        response = recipients_resource.add_unsubscribes(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
        }
        mock_client.post.assert_called_once_with("/v1/suppressions/unsubscribes", json=expected_body)
        assert isinstance(response, SuppressionAddResponse)

    def test_delete_from_blocklist(self, recipients_resource, mock_client):
        """Test deleting from blocklist."""
        # Setup
        request = SuppressionDeleteRequest(
            domain_id="domain123",
            ids=["id1", "id2"],
        )

        # Test
        recipients_resource.delete_from_blocklist(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "ids": ["id1", "id2"],
        }
        mock_client.delete.assert_called_once_with("/v1/suppressions/blocklist", json=expected_body)

    def test_delete_from_blocklist_all(self, recipients_resource, mock_client):
        """Test deleting all from blocklist."""
        # Setup
        request = SuppressionDeleteRequest(
            domain_id="domain123",
            all=True,
        )

        # Test
        recipients_resource.delete_from_blocklist(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "all": True,
        }
        mock_client.delete.assert_called_once_with("/v1/suppressions/blocklist", json=expected_body)

    def test_delete_hard_bounces(self, recipients_resource, mock_client):
        """Test deleting hard bounces."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        # Test
        recipients_resource.delete_hard_bounces(request)

        # Assertions
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/hard-bounces", json=expected_body)

    def test_delete_spam_complaints(self, recipients_resource, mock_client):
        """Test deleting spam complaints."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        # Test
        recipients_resource.delete_spam_complaints(request)

        # Assertions
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/spam-complaints", json=expected_body)

    def test_delete_unsubscribes(self, recipients_resource, mock_client):
        """Test deleting unsubscribes."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        # Test
        recipients_resource.delete_unsubscribes(request)

        # Assertions
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/unsubscribes", json=expected_body)

    def test_delete_from_on_hold(self, recipients_resource, mock_client):
        """Test deleting from on-hold list."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        # Test
        recipients_resource.delete_from_on_hold(request)

        # Assertions
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/on-hold-list", json=expected_body)

    def test_delete_requests_no_request(self, recipients_resource):
        """Test delete methods without request raise errors."""
        methods = [
            recipients_resource.delete_from_blocklist,
            recipients_resource.delete_hard_bounces,
            recipients_resource.delete_spam_complaints,
            recipients_resource.delete_unsubscribes,
            recipients_resource.delete_from_on_hold,
        ]
        
        for method in methods:
            with pytest.raises(ValidationError) as exc_info:
                method(None)
            assert "Request is required" in str(exc_info.value)

    @patch('mailersend.resources.recipients.logger')
    def test_logging(self, mock_logger, recipients_resource, mock_client):
        """Test that appropriate logging occurs."""
        # Setup
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.get.return_value = mock_response

        # Test
        recipients_resource.list_recipients()

        # Check logging calls
        mock_logger.debug.assert_called()
        mock_logger.info.assert_called()

    def test_query_params_building(self, recipients_resource, mock_client):
        """Test query parameters are built correctly."""
        # Setup
        request = RecipientsListRequest(domain_id="domain123")
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.get.return_value = mock_response

        # Test with only domain_id
        recipients_resource.list_recipients(request)
        
        expected_params = {"domain_id": "domain123", "limit": 25}
        mock_client.get.assert_called_with("/v1/recipients", params=expected_params)

        # Reset mock
        mock_client.reset_mock()

        # Test with all parameters
        request = RecipientsListRequest(domain_id="domain123", page=2, limit=50)
        recipients_resource.list_recipients(request)
        
        expected_params = {"domain_id": "domain123", "page": 2, "limit": 50}
        mock_client.get.assert_called_with("/v1/recipients", params=expected_params)

    def test_request_body_building(self, recipients_resource, mock_client):
        """Test request bodies are built correctly."""
        # Setup
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = {"data": []}
        mock_client.post.return_value = mock_response

        # Test with recipients only
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
        )
        recipients_resource.add_to_blocklist(request)

        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
        }
        mock_client.post.assert_called_with("/v1/suppressions/blocklist", json=expected_body)

        # Reset mock
        mock_client.reset_mock()

        # Test with patterns only
        request = SuppressionAddRequest(
            domain_id="domain123",
            patterns=[".*@example.com"],
        )
        recipients_resource.add_to_blocklist(request)

        expected_body = {
            "domain_id": "domain123",
            "patterns": [".*@example.com"],
        }
        mock_client.post.assert_called_with("/v1/suppressions/blocklist", json=expected_body)

    def test_delete_body_without_domain_id(self, recipients_resource, mock_client):
        """Test delete request body without domain_id (for on-hold)."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        # Test
        recipients_resource.delete_from_on_hold(request)

        # Assertions - domain_id should not be in body
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/on-hold-list", json=expected_body) 