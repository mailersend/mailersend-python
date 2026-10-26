"""Tests for WhatsApp Messages builder."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from mailersend.builders.whatsapp_messages import WhatsAppMessagesBuilder
from mailersend.models.whatsapp_messages import (
    WhatsAppMessagesListRequest,
    WhatsAppMessageGetRequest,
)


class TestWhatsAppMessagesBuilder:
    """Test WhatsAppMessagesBuilder."""

    def test_build_list_request_defaults(self):
        request = WhatsAppMessagesBuilder().build_list_request()

        assert isinstance(request, WhatsAppMessagesListRequest)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.to_query_params() == {}

    def test_build_list_request_with_pagination(self):
        request = WhatsAppMessagesBuilder().page(2).limit(50).build_list_request()

        assert request.to_query_params() == {"page": 2, "limit": 50}

    def test_build_list_request_with_all_params(self):
        request = (
            WhatsAppMessagesBuilder()
            .whatsapp_account_id("whatsapp-account-id")
            .from_number("48600000001")
            .template_id("template-id")
            .date_from(1790000000)
            .date_to(1790086400)
            .page(2)
            .limit(50)
            .build_list_request()
        )

        assert request.to_query_params() == {
            "whatsapp_account_id": "whatsapp-account-id",
            "from": "48600000001",
            "template_id": "template-id",
            "date_from": 1790000000,
            "date_to": 1790086400,
            "page": 2,
            "limit": 50,
        }

    def test_date_accepts_datetime(self):
        request = (
            WhatsAppMessagesBuilder()
            .date_from(datetime(2026, 10, 1, tzinfo=timezone.utc))
            .date_to(datetime(2026, 10, 2, tzinfo=timezone.utc))
            .build_list_request()
        )

        params = request.to_query_params()
        assert params["date_from"] == 1790812800
        assert params["date_to"] == 1790899200

    def test_date_accepts_iso_string(self):
        request = (
            WhatsAppMessagesBuilder()
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
                WhatsAppMessagesBuilder()
                .date_from(1790086400)
                .date_to(1790000000)
                .build_list_request()
            )

    @pytest.mark.parametrize("limit", [1, 100])
    def test_build_list_request_accepts_limit_bounds(self, limit):
        request = WhatsAppMessagesBuilder().limit(limit).build_list_request()

        assert request.query_params.limit == limit

    @pytest.mark.parametrize("limit", [0, 101])
    def test_build_list_request_rejects_invalid_limit(self, limit):
        with pytest.raises(ValidationError):
            WhatsAppMessagesBuilder().limit(limit).build_list_request()

    @pytest.mark.parametrize("page", [0, 101])
    def test_build_list_request_rejects_invalid_page(self, page):
        with pytest.raises(ValidationError):
            WhatsAppMessagesBuilder().page(page).build_list_request()

    def test_build_get_request(self):
        request = (
            WhatsAppMessagesBuilder()
            .whatsapp_message_id(" message-id ")
            .build_get_request()
        )

        assert isinstance(request, WhatsAppMessageGetRequest)
        assert request.whatsapp_message_id == "message-id"

    def test_build_get_request_requires_id(self):
        with pytest.raises(ValueError, match="WhatsApp message ID is required"):
            WhatsAppMessagesBuilder().build_get_request()

    def test_build_get_request_rejects_blank_id(self):
        with pytest.raises(ValidationError):
            WhatsAppMessagesBuilder().whatsapp_message_id("   ").build_get_request()
