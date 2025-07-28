"""Unit tests for Recipients resource."""
import pytest
from unittest.mock import Mock, patch
from requests import Response

from mailersend.resources.recipients import Recipients
from mailersend.models.base import APIResponse
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

    def _create_mock_response(self, json_data=None):
        """Create a properly configured mock response."""
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = json_data or {}
        mock_response.headers = {
            "content-type": "application/json",
            "x-request-id": "test-request-id",
            "x-apiquota-remaining": "100"
        }
        mock_response.status_code = 200
        mock_response.content = b'{"data": []}'
        return mock_response

    def test_list_recipients_default(self, recipients_resource, mock_client):
        """Test listing recipients with default parameters."""
        # Setup mock response
        mock_response = self._create_mock_response({
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
        })
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_recipients()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/recipients", params={"page": 1, "limit": 25})
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, RecipientsListResponse)
        assert len(response.data.data) == 1
        assert response.data.data[0].id == "recipient123"

    def test_list_recipients_with_request(self, recipients_resource, mock_client):
        """Test listing recipients with request parameters."""
        # Setup
        from mailersend.models.recipients import RecipientsListQueryParams
        query_params = RecipientsListQueryParams(
            domain_id="domain123",
            page=2,
            limit=50,
        )
        request = RecipientsListRequest(query_params=query_params)
        
        mock_response = self._create_mock_response({
            "data": [],
            "links": {},
            "meta": {},
        })
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
        
        mock_response = self._create_mock_response({
            "data": {
                "id": "recipient123",
                "email": "test@example.com",
                "created_at": "2020-06-10T10:09:56Z",
                "updated_at": "2020-06-10T10:09:56Z",
                "deleted_at": "",
            }
        })
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.get_recipient(request)

        # Assertions
        mock_client.get.assert_called_once_with("/v1/recipients/recipient123")
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, RecipientResponse)
        assert response.data.data.id == "recipient123"

    def test_get_recipient_no_request(self, recipients_resource):
        """Test getting recipient without request raises error."""
        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.get_recipient(None)
        assert "Request is required for get_recipient" in str(exc_info.value)

    def test_delete_recipient(self, recipients_resource, mock_client):
        """Test deleting a recipient."""
        # Setup
        request = RecipientDeleteRequest(recipient_id="recipient123")
        mock_response = self._create_mock_response({})
        mock_client.delete.return_value = mock_response

        # Test
        response = recipients_resource.delete_recipient(request)

        # Assertions
        mock_client.delete.assert_called_once_with("/v1/recipients/recipient123")
        assert isinstance(response, APIResponse)

    def test_delete_recipient_no_request(self, recipients_resource):
        """Test deleting recipient without request raises error."""
        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.delete_recipient(None)
        assert "Request is required for delete_recipient" in str(exc_info.value)

    def test_list_blocklist(self, recipients_resource, mock_client):
        """Test listing blocklist entries."""
        # Setup
        from mailersend.models.recipients import SuppressionListQueryParams
        query_params = SuppressionListQueryParams(
            domain_id="domain123",
            page=1,
            limit=25,
        )
        request = SuppressionListRequest(query_params=query_params)
        
        mock_response = self._create_mock_response({
            "data": [
                {
                    "id": "entry123",
                    "type": "pattern",
                    "pattern": ".*@example.com",
                    "created_at": "2020-06-10T10:09:56Z",
                    "updated_at": "2020-06-10T10:09:56Z",
                }
            ]
        })
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
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, BlocklistResponse)

    def test_list_hard_bounces(self, recipients_resource, mock_client):
        """Test listing hard bounces."""
        # Setup
        mock_response = self._create_mock_response({"data": []})
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_hard_bounces()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/suppressions/hard-bounces", params={"page": 1, "limit": 25})
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, HardBouncesResponse)

    def test_list_spam_complaints(self, recipients_resource, mock_client):
        """Test listing spam complaints."""
        # Setup
        mock_response = self._create_mock_response({"data": []})
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_spam_complaints()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/suppressions/spam-complaints", params={"page": 1, "limit": 25})
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, SpamComplaintsResponse)

    def test_list_unsubscribes(self, recipients_resource, mock_client):
        """Test listing unsubscribes."""
        # Setup
        mock_response = self._create_mock_response({"data": []})
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_unsubscribes()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/suppressions/unsubscribes", params={"page": 1, "limit": 25})
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, UnsubscribesResponse)

    def test_list_on_hold(self, recipients_resource, mock_client):
        """Test listing on-hold entries."""
        # Setup
        mock_response = self._create_mock_response({"data": []})
        mock_client.get.return_value = mock_response

        # Test
        response = recipients_resource.list_on_hold()

        # Assertions
        mock_client.get.assert_called_once_with("/v1/suppressions/on-hold-list", params={"page": 1, "limit": 25})
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, OnHoldResponse)

    def test_add_to_blocklist(self, recipients_resource, mock_client):
        """Test adding to blocklist."""
        # Setup
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
            patterns=[".*@example.com"],
        )

        mock_response = self._create_mock_response({"data": []})
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
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, SuppressionAddResponse)

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

        mock_response = self._create_mock_response({"data": []})
        mock_client.post.return_value = mock_response

        # Test
        response = recipients_resource.add_hard_bounces(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
        }
        mock_client.post.assert_called_once_with("/v1/suppressions/hard-bounces", json=expected_body)
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, SuppressionAddResponse)

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

        mock_response = self._create_mock_response({"data": []})
        mock_client.post.return_value = mock_response

        # Test
        response = recipients_resource.add_spam_complaints(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
        }
        mock_client.post.assert_called_once_with("/v1/suppressions/spam-complaints", json=expected_body)
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, SuppressionAddResponse)

    def test_add_unsubscribes(self, recipients_resource, mock_client):
        """Test adding unsubscribes."""
        # Setup
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
        )

        mock_response = self._create_mock_response({"data": []})
        mock_client.post.return_value = mock_response

        # Test
        response = recipients_resource.add_unsubscribes(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
        }
        mock_client.post.assert_called_once_with("/v1/suppressions/unsubscribes", json=expected_body)
        assert isinstance(response, APIResponse)
        assert isinstance(response.data, SuppressionAddResponse)

    def test_delete_from_blocklist(self, recipients_resource, mock_client):
        """Test deleting from blocklist."""
        # Setup
        request = SuppressionDeleteRequest(
            domain_id="domain123",
            ids=["id1", "id2"],
        )

        mock_response = self._create_mock_response({})
        mock_client.delete.return_value = mock_response

        # Test
        response = recipients_resource.delete_from_blocklist(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "ids": ["id1", "id2"],
        }
        mock_client.delete.assert_called_once_with("/v1/suppressions/blocklist", json=expected_body)
        assert isinstance(response, APIResponse)

    def test_delete_from_blocklist_all(self, recipients_resource, mock_client):
        """Test deleting all from blocklist."""
        # Setup
        request = SuppressionDeleteRequest(
            domain_id="domain123",
            all=True,
        )

        mock_response = self._create_mock_response({})
        mock_client.delete.return_value = mock_response

        # Test
        response = recipients_resource.delete_from_blocklist(request)

        # Assertions
        expected_body = {
            "domain_id": "domain123",
            "all": True,
        }
        mock_client.delete.assert_called_once_with("/v1/suppressions/blocklist", json=expected_body)
        assert isinstance(response, APIResponse)

    def test_delete_hard_bounces(self, recipients_resource, mock_client):
        """Test deleting hard bounces."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        mock_response = self._create_mock_response({})
        mock_client.delete.return_value = mock_response

        # Test
        response = recipients_resource.delete_hard_bounces(request)

        # Assertions
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/hard-bounces", json=expected_body)
        assert isinstance(response, APIResponse)

    def test_delete_spam_complaints(self, recipients_resource, mock_client):
        """Test deleting spam complaints."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        mock_response = self._create_mock_response({})
        mock_client.delete.return_value = mock_response

        # Test
        response = recipients_resource.delete_spam_complaints(request)

        # Assertions
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/spam-complaints", json=expected_body)
        assert isinstance(response, APIResponse)

    def test_delete_unsubscribes(self, recipients_resource, mock_client):
        """Test deleting unsubscribes."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        mock_response = self._create_mock_response({})
        mock_client.delete.return_value = mock_response

        # Test
        response = recipients_resource.delete_unsubscribes(request)

        # Assertions
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/unsubscribes", json=expected_body)
        assert isinstance(response, APIResponse)

    def test_delete_from_on_hold(self, recipients_resource, mock_client):
        """Test deleting from on-hold list."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        mock_response = self._create_mock_response({})
        mock_client.delete.return_value = mock_response

        # Test
        response = recipients_resource.delete_from_on_hold(request)

        # Assertions
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_once_with("/v1/suppressions/on-hold-list", json=expected_body)
        assert isinstance(response, APIResponse)

    def test_delete_requests_no_request(self, recipients_resource):
        """Test delete operations without request raise error."""
        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.delete_from_blocklist(None)
        assert "Request is required for delete_from_blocklist" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.delete_hard_bounces(None)
        assert "Request is required for delete_hard_bounces" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.delete_spam_complaints(None)
        assert "Request is required for delete_spam_complaints" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.delete_unsubscribes(None)
        assert "Request is required for delete_unsubscribes" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            recipients_resource.delete_from_on_hold(None)
        assert "Request is required for delete_from_on_hold" in str(exc_info.value)

    @patch('mailersend.resources.recipients.logger')
    def test_logging(self, mock_logger, recipients_resource, mock_client):
        """Test that appropriate logging occurs."""
        # Setup
        mock_response = self._create_mock_response({"data": []})
        mock_client.get.return_value = mock_response

        # Test
        recipients_resource.list_recipients()

        # Verify logging calls
        mock_logger.debug.assert_called()
        mock_logger.info.assert_called()

    def test_query_params_building(self, recipients_resource, mock_client):
        """Test query parameters are built correctly."""
        # Setup
        from mailersend.models.recipients import RecipientsListQueryParams
        query_params = RecipientsListQueryParams(domain_id="domain123")
        request = RecipientsListRequest(query_params=query_params)
        mock_response = self._create_mock_response({"data": []})
        mock_client.get.return_value = mock_response

        # Test with only domain_id
        recipients_resource.list_recipients(request)

        # Should include domain_id and defaults
        expected_params = {"domain_id": "domain123", "page": 1, "limit": 25}
        mock_client.get.assert_called_with("/v1/recipients", params=expected_params)

        # Reset mock
        mock_client.reset_mock()

        # Test with full params
        query_params = RecipientsListQueryParams(domain_id="domain123", page=2, limit=50)
        request = RecipientsListRequest(query_params=query_params)
        recipients_resource.list_recipients(request)

        expected_params = {"domain_id": "domain123", "page": 2, "limit": 50}
        mock_client.get.assert_called_with("/v1/recipients", params=expected_params)

    def test_request_body_building(self, recipients_resource, mock_client):
        """Test request bodies are built correctly."""
        # Setup
        mock_response = self._create_mock_response({"data": []})
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

        # Test with both recipients and patterns
        request = SuppressionAddRequest(
            domain_id="domain123",
            recipients=["test@example.com"],
            patterns=[".*@example.com"],
        )
        recipients_resource.add_to_blocklist(request)

        expected_body = {
            "domain_id": "domain123",
            "recipients": ["test@example.com"],
            "patterns": [".*@example.com"],
        }
        mock_client.post.assert_called_with("/v1/suppressions/blocklist", json=expected_body)

    def test_delete_body_without_domain_id(self, recipients_resource, mock_client):
        """Test delete request body without domain_id (for on-hold)."""
        # Setup
        request = SuppressionDeleteRequest(ids=["id1", "id2"])

        mock_response = self._create_mock_response({})
        mock_client.delete.return_value = mock_response

        # Test
        recipients_resource.delete_from_on_hold(request)

        # Should not include domain_id for on-hold
        expected_body = {"ids": ["id1", "id2"]}
        mock_client.delete.assert_called_with("/v1/suppressions/on-hold-list", json=expected_body) 