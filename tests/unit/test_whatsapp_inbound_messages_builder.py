"""Tests for WhatsApp Inbound Messages builder."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from mailersend.builders.whatsapp_inbound_messages import (
    WhatsAppInboundMessagesBuilder,
)
from mailersend.models.whatsapp_inbound_messages import (
    WhatsAppInboundMessagesListRequest,
    WhatsAppInboundMessageGetRequest,
    WhatsAppInboundMessageType,
)


class TestWhatsAppInboundMessagesBuilder:
    """Test WhatsAppInboundMessagesBuilder."""

    def test_build_list_request_defaults(self):
        request = WhatsAppInboundMessagesBuilder().build_list_request()

        assert isinstance(request, WhatsAppInboundMessagesListRequest)
        assert request.to_query_params() == {}

    def test_build_list_request_with_all_params(self):
        request = (
            WhatsAppInboundMessagesBuilder()
            .whatsapp_account_id("whatsapp-account-id")
            .type(["text", WhatsAppInboundMessageType.IMAGE])
            .date_from(1790000000)
            .date_to(1790086400)
            .page(2)
            .limit(50)
            .build_list_request()
        )

        assert request.to_query_params() == {
            "whatsapp_account_id": "whatsapp-account-id",
            "type[]": ["text", "image"],
            "date_from": 1790000000,
            "date_to": 1790086400,
            "page": 2,
            "limit": 50,
        }

    def test_date_accepts_datetime(self):
        request = (
            WhatsAppInboundMessagesBuilder()
            .date_from(datetime(2026, 10, 1, tzinfo=timezone.utc))
            .date_to(datetime(2026, 10, 2, tzinfo=timezone.utc))
            .build_list_request()
        )

        params = request.to_query_params()
        assert params["date_from"] == 1790812800
        assert params["date_to"] == 1790899200

    def test_date_accepts_iso_string(self):
        request = (
            WhatsAppInboundMessagesBuilder()
            .date_from("2026-10-01T00:00:00Z")
            .date_to("2026-10-02T00:00:00Z")
            .build_list_request()
        )

        params = request.to_query_params()
        assert params["date_from"] == "2026-10-01T00:00:00Z"
        assert params["date_to"] == "2026-10-02T00:00:00Z"

    def test_build_list_request_rejects_date_to_before_date_from(self):
        with pytest.raises(ValidationError, match="date_to must be greater"):
            (
                WhatsAppInboundMessagesBuilder()
                .date_from(1790086400)
                .date_to(1790000000)
                .build_list_request()
            )

    def test_build_list_request_rejects_unknown_type(self):
        with pytest.raises(ValidationError):
            WhatsAppInboundMessagesBuilder().type(["fax"]).build_list_request()

    def test_build_get_request(self):
        request = (
            WhatsAppInboundMessagesBuilder()
            .whatsapp_inbound_message_id("inbound-message-id")
            .build_get_request()
        )

        assert isinstance(request, WhatsAppInboundMessageGetRequest)
        assert request.whatsapp_inbound_message_id == "inbound-message-id"

    def test_build_get_request_requires_id(self):
        with pytest.raises(ValueError, match="WhatsApp inbound message ID is required"):
            WhatsAppInboundMessagesBuilder().build_get_request()
