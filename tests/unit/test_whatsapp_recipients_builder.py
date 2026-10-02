"""Tests for WhatsApp Recipients builder."""

import pytest
from pydantic import ValidationError

from mailersend.builders.whatsapp_recipients import WhatsAppRecipientsBuilder
from mailersend.models.whatsapp_recipients import (
    WhatsAppRecipientsListRequest,
    WhatsAppRecipientGetRequest,
    WhatsAppRecipientStatus,
)


class TestWhatsAppRecipientsBuilder:
    """Test WhatsAppRecipientsBuilder."""

    def test_build_list_request_defaults(self):
        request = WhatsAppRecipientsBuilder().build_list_request()

        assert isinstance(request, WhatsAppRecipientsListRequest)
        assert request.query_params.status is None
        assert request.to_query_params() == {}

    @pytest.mark.parametrize("status", list(WhatsAppRecipientStatus))
    def test_build_list_request_with_status(self, status):
        request = WhatsAppRecipientsBuilder().status(status).build_list_request()

        assert request.to_query_params() == {"status": status.value}

    def test_build_list_request_with_all_params(self):
        request = (
            WhatsAppRecipientsBuilder()
            .status(WhatsAppRecipientStatus.BLOCKED)
            .page(3)
            .limit(10)
            .build_list_request()
        )

        assert request.to_query_params() == {
            "status": "blocked",
            "page": 3,
            "limit": 10,
        }

    def test_build_list_request_rejects_invalid_limit(self):
        with pytest.raises(ValidationError):
            WhatsAppRecipientsBuilder().limit(200).build_list_request()

    def test_build_list_request_rejects_invalid_status(self):
        with pytest.raises(ValidationError):
            WhatsAppRecipientsBuilder().status("opt_out").build_list_request()

    def test_build_get_request(self):
        request = (
            WhatsAppRecipientsBuilder()
            .whatsapp_recipient_id("recipient-id")
            .build_get_request()
        )

        assert isinstance(request, WhatsAppRecipientGetRequest)
        assert request.whatsapp_recipient_id == "recipient-id"

    def test_build_get_request_requires_id(self):
        with pytest.raises(ValueError, match="WhatsApp recipient ID is required"):
            WhatsAppRecipientsBuilder().build_get_request()
