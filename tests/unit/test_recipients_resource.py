"""Unit tests for Recipients resource."""
import pytest
from unittest.mock import Mock, MagicMock
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
)
from mailersend.exceptions import ValidationError


class TestRecipients:
    """Test Recipients resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = Recipients(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_recipients_returns_api_response(self):
        """Test list_recipients method returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_recipients()

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_recipients_with_request(self):
        """Test list_recipients with custom request."""
        from mailersend.models.recipients import RecipientsListQueryParams

        query_params = RecipientsListQueryParams(
            domain_id="test-domain", page=2, limit=50
        )
        request = RecipientsListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_recipients(request)

        # Verify client was called with correct params
        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="recipients",
            params={"domain_id": "test-domain", "page": 2, "limit": 50},
        )

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_recipients_with_defaults(self):
        """Test list_recipients with default request."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_recipients()

        # Verify client was called with defaults
        self.mock_client.request.assert_called_once_with(
            method="GET", path="recipients", params={"page": 1, "limit": 25}
        )

        assert result == self.mock_api_response

    def test_get_recipient_returns_api_response(self):
        """Test get_recipient method returns APIResponse."""
        request = RecipientGetRequest(recipient_id="test-recipient")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_recipient(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_recipient_with_valid_request(self):
        """Test get_recipient with valid request."""
        request = RecipientGetRequest(recipient_id="test-recipient")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_recipient(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="GET", path="recipients/test-recipient"
        )

    def test_delete_recipient_returns_api_response(self):
        """Test delete_recipient method returns APIResponse."""
        request = RecipientDeleteRequest(recipient_id="test-recipient")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_recipient(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_recipient_with_valid_request(self):
        """Test delete_recipient with valid request."""
        request = RecipientDeleteRequest(recipient_id="test-recipient")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_recipient(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="recipients/test-recipient"
        )

    def test_list_blocklist_returns_api_response(self):
        """Test list_blocklist method returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_blocklist()

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_hard_bounces_returns_api_response(self):
        """Test list_hard_bounces method returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_hard_bounces()

        assert result == self.mock_api_response

    def test_list_spam_complaints_returns_api_response(self):
        """Test list_spam_complaints method returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_spam_complaints()

        assert result == self.mock_api_response

    def test_list_unsubscribes_returns_api_response(self):
        """Test list_unsubscribes method returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_unsubscribes()

        assert result == self.mock_api_response

    def test_list_on_hold_returns_api_response(self):
        """Test list_on_hold method returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_on_hold()

        assert result == self.mock_api_response

    def test_add_to_blocklist_returns_api_response(self):
        """Test add_to_blocklist method returns APIResponse."""
        request = SuppressionAddRequest(
            domain_id="test-domain", recipients=["test@example.com"]
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.add_to_blocklist(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_add_to_blocklist_with_request_body(self):
        """Test add_to_blocklist with request body serialization."""
        request = SuppressionAddRequest(
            domain_id="test-domain",
            recipients=["test@example.com", "test2@example.com"],
            patterns=["@spam.com"],
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.add_to_blocklist(request)

        # Verify client was called with correct data
        call_args = self.mock_client.request.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["path"] == "suppressions/blocklist"

        body = call_args[1]["body"]
        assert "domain_id" in body
        assert "recipients" in body
        assert "patterns" in body

    def test_add_hard_bounces_returns_api_response(self):
        """Test add_hard_bounces method returns APIResponse."""
        request = SuppressionAddRequest(
            domain_id="test-domain", recipients=["test@example.com"]
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.add_hard_bounces(request)

        assert result == self.mock_api_response

    def test_add_spam_complaints_returns_api_response(self):
        """Test add_spam_complaints method returns APIResponse."""
        request = SuppressionAddRequest(
            domain_id="test-domain", recipients=["test@example.com"]
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.add_spam_complaints(request)

        assert result == self.mock_api_response

    def test_add_unsubscribes_returns_api_response(self):
        """Test add_unsubscribes method returns APIResponse."""
        request = SuppressionAddRequest(
            domain_id="test-domain", recipients=["test@example.com"]
        )

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.add_unsubscribes(request)

        assert result == self.mock_api_response

    def test_delete_from_blocklist_returns_api_response(self):
        """Test delete_from_blocklist method returns APIResponse."""
        request = SuppressionDeleteRequest(domain_id="test-domain", ids=["id1", "id2"])

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_from_blocklist(request)

        assert result == self.mock_api_response

    def test_delete_from_blocklist_with_request_body(self):
        """Test delete_from_blocklist with request body serialization."""
        request = SuppressionDeleteRequest(domain_id="test-domain", ids=["id1", "id2"])

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_from_blocklist(request)

        # Verify client was called with correct data
        call_args = self.mock_client.request.call_args
        assert call_args[1]["method"] == "DELETE"
        assert call_args[1]["path"] == "suppressions/blocklist"

        body = call_args[1]["body"]
        assert "domain_id" in body
        assert "ids" in body

    def test_delete_hard_bounces_excludes_domain_id(self):
        """Test delete_hard_bounces excludes domain_id from body."""
        request = SuppressionDeleteRequest(domain_id="test-domain", ids=["id1", "id2"])

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_hard_bounces(request)

        # Verify domain_id is excluded from request body
        call_args = self.mock_client.request.call_args
        body = call_args[1]["body"]
        assert "domain_id" not in body
        assert "ids" in body

    def test_delete_spam_complaints_excludes_domain_id(self):
        """Test delete_spam_complaints excludes domain_id from body."""
        request = SuppressionDeleteRequest(domain_id="test-domain", ids=["id1", "id2"])

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_spam_complaints(request)

        # Verify domain_id is excluded from request body
        call_args = self.mock_client.request.call_args
        body = call_args[1]["body"]
        assert "domain_id" not in body
        assert "ids" in body

    def test_delete_unsubscribes_excludes_domain_id(self):
        """Test delete_unsubscribes excludes domain_id from body."""
        request = SuppressionDeleteRequest(domain_id="test-domain", ids=["id1", "id2"])

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_unsubscribes(request)

        # Verify domain_id is excluded from request body
        call_args = self.mock_client.request.call_args
        body = call_args[1]["body"]
        assert "domain_id" not in body
        assert "ids" in body

    def test_delete_from_on_hold_excludes_domain_id(self):
        """Test delete_from_on_hold excludes domain_id from body."""
        request = SuppressionDeleteRequest(domain_id="test-domain", ids=["id1", "id2"])

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_from_on_hold(request)

        # Verify domain_id is excluded from request body
        call_args = self.mock_client.request.call_args
        body = call_args[1]["body"]
        assert "domain_id" not in body
        assert "ids" in body

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        from mailersend.models.recipients import RecipientsListQueryParams

        query_params = RecipientsListQueryParams()
        request_list = RecipientsListRequest(query_params=query_params)
        request_get = RecipientGetRequest(recipient_id="test-recipient")
        request_delete = RecipientDeleteRequest(recipient_id="test-recipient")
        request_add = SuppressionAddRequest(
            domain_id="test-domain", recipients=["test@example.com"]
        )
        request_del = SuppressionDeleteRequest(domain_id="test-domain", ids=["id1"])

        # Test that each method returns the expected APIResponse type
        assert isinstance(
            self.resource.list_recipients(request_list), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.get_recipient(request_get), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.delete_recipient(request_delete), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.add_to_blocklist(request_add), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.delete_from_blocklist(request_del),
            type(self.mock_api_response),
        )
