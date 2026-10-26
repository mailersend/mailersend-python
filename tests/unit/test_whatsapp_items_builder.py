"""Tests for WhatsApp Items builder."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from mailersend.builders.whatsapp_items import WhatsAppItemsBuilder
from mailersend.models.whatsapp_items import (
    WhatsAppItemsListRequest,
    WhatsAppItemGetRequest,
    WhatsAppItemStatus,
)


class TestWhatsAppItemsBuilder:
    """Test WhatsAppItemsBuilder."""

    def test_build_list_request_defaults(self):
        request = WhatsAppItemsBuilder().build_list_request()

        assert isinstance(request, WhatsAppItemsListRequest)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.to_query_params() == {}

    def test_build_list_request_with_all_params(self):
        request = (
            WhatsAppItemsBuilder()
            .recipient("48600000002")
            .whatsapp_message_id("message-id")
            .status(["failed", WhatsAppItemStatus.READ])
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
            "recipient": "48600000002",
            "whatsapp_message_id": "message-id",
            "status[]": ["failed", "read"],
            "whatsapp_account_id": "whatsapp-account-id",
            "from": "48600000001",
            "template_id": "template-id",
            "date_from": 1790000000,
            "date_to": 1790086400,
            "page": 2,
            "limit": 50,
        }

    @pytest.mark.parametrize("status", list(WhatsAppItemStatus))
    def test_build_list_request_with_each_status(self, status):
        request = WhatsAppItemsBuilder().status([status]).build_list_request()

        assert request.to_query_params() == {"status[]": [status.value]}

    def test_date_accepts_datetime(self):
        request = (
            WhatsAppItemsBuilder()
            .date_from(datetime(2026, 10, 1, tzinfo=timezone.utc))
            .date_to(datetime(2026, 10, 2, tzinfo=timezone.utc))
            .build_list_request()
        )

        params = request.to_query_params()
        assert params["date_from"] == 1790812800
        assert params["date_to"] == 1790899200

    def test_date_accepts_iso_string(self):
        request = (
            WhatsAppItemsBuilder()
            .date_from("2026-10-14T00:00:00Z")
            .date_to("2026-10-15 00:00:00")
            .build_list_request()
        )

        params = request.to_query_params()
        assert params["date_from"] == "2026-10-14T00:00:00Z"
        assert params["date_to"] == "2026-10-15 00:00:00"

    def test_build_list_request_rejects_date_to_before_date_from(self):
        with pytest.raises(ValidationError, match="date_to must be greater"):
            (
                WhatsAppItemsBuilder()
                .date_from(1790086400)
                .date_to(1790000000)
                .build_list_request()
            )

    @pytest.mark.parametrize("status", ["failed", WhatsAppItemStatus.FAILED])
    def test_status_accepts_a_single_value(self, status):
        request = WhatsAppItemsBuilder().status(status).build_list_request()

        assert request.to_query_params() == {"status[]": ["failed"]}

    def test_build_list_request_rejects_unknown_status(self):
        with pytest.raises(ValidationError):
            WhatsAppItemsBuilder().status(["bounced"]).build_list_request()

    @pytest.mark.parametrize("limit", [1, 100])
    def test_build_list_request_accepts_limit_bounds(self, limit):
        request = WhatsAppItemsBuilder().limit(limit).build_list_request()

        assert request.query_params.limit == limit

    @pytest.mark.parametrize("limit", [0, 101])
    def test_build_list_request_rejects_invalid_limit(self, limit):
        with pytest.raises(ValidationError):
            WhatsAppItemsBuilder().limit(limit).build_list_request()

    @pytest.mark.parametrize("page", [0, 101])
    def test_build_list_request_rejects_invalid_page(self, page):
        with pytest.raises(ValidationError):
            WhatsAppItemsBuilder().page(page).build_list_request()

    def test_build_get_request(self):
        request = (
            WhatsAppItemsBuilder().whatsapp_item_id(" item-id ").build_get_request()
        )

        assert isinstance(request, WhatsAppItemGetRequest)
        assert request.whatsapp_item_id == "item-id"

    def test_build_get_request_requires_id(self):
        with pytest.raises(ValueError, match="WhatsApp item ID is required"):
            WhatsAppItemsBuilder().build_get_request()

    def test_build_get_request_rejects_blank_id(self):
        with pytest.raises(ValidationError):
            WhatsAppItemsBuilder().whatsapp_item_id("   ").build_get_request()
