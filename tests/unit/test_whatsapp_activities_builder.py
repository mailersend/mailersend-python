"""Tests for WhatsApp Activities builder."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from mailersend.builders.whatsapp_activities import WhatsAppActivitiesBuilder
from mailersend.models.whatsapp_activities import (
    WhatsAppActivitiesListRequest,
    WhatsAppActivityType,
)


class TestWhatsAppActivitiesBuilder:
    """Test WhatsAppActivitiesBuilder."""

    def test_build_list_request_defaults(self):
        request = WhatsAppActivitiesBuilder().build_list_request()

        assert isinstance(request, WhatsAppActivitiesListRequest)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.to_query_params() == {}

    def test_build_list_request_with_all_params(self):
        request = (
            WhatsAppActivitiesBuilder()
            .whatsapp_item_id("item-id")
            .whatsapp_message_id("message-id")
            .recipient("48600000002")
            .type(["delivered", WhatsAppActivityType.READ])
            .date_from(1790000000)
            .date_to(1790086400)
            .page(2)
            .limit(50)
            .build_list_request()
        )

        assert request.to_query_params() == {
            "whatsapp_item_id": "item-id",
            "whatsapp_message_id": "message-id",
            "recipient": "48600000002",
            "type[]": ["delivered", "read"],
            "date_from": 1790000000,
            "date_to": 1790086400,
            "page": 2,
            "limit": 50,
        }

    @pytest.mark.parametrize("activity_type", list(WhatsAppActivityType))
    def test_build_list_request_with_each_type(self, activity_type):
        request = WhatsAppActivitiesBuilder().type([activity_type]).build_list_request()

        assert request.to_query_params() == {"type[]": [activity_type.value]}

    def test_date_accepts_datetime(self):
        request = (
            WhatsAppActivitiesBuilder()
            .date_from(datetime(2026, 10, 1, tzinfo=timezone.utc))
            .date_to(datetime(2026, 10, 2, tzinfo=timezone.utc))
            .build_list_request()
        )

        params = request.to_query_params()
        assert params["date_from"] == 1790812800
        assert params["date_to"] == 1790899200

    def test_build_list_request_rejects_date_to_before_date_from(self):
        with pytest.raises(ValidationError, match="date_to must be greater"):
            (
                WhatsAppActivitiesBuilder()
                .date_from(1790086400)
                .date_to(1790000000)
                .build_list_request()
            )

    @pytest.mark.parametrize("activity_type", ["failed", WhatsAppActivityType.FAILED])
    def test_type_accepts_a_single_value(self, activity_type):
        request = WhatsAppActivitiesBuilder().type(activity_type).build_list_request()

        assert request.to_query_params() == {"type[]": ["failed"]}

    def test_build_list_request_rejects_unknown_type(self):
        with pytest.raises(ValidationError):
            WhatsAppActivitiesBuilder().type(["clicked"]).build_list_request()

    @pytest.mark.parametrize("limit", [1, 100])
    def test_build_list_request_accepts_limit_bounds(self, limit):
        request = WhatsAppActivitiesBuilder().limit(limit).build_list_request()

        assert request.query_params.limit == limit

    @pytest.mark.parametrize("limit", [0, 101])
    def test_build_list_request_rejects_invalid_limit(self, limit):
        with pytest.raises(ValidationError):
            WhatsAppActivitiesBuilder().limit(limit).build_list_request()

    @pytest.mark.parametrize("page", [0, 101])
    def test_build_list_request_rejects_invalid_page(self, page):
        with pytest.raises(ValidationError):
            WhatsAppActivitiesBuilder().page(page).build_list_request()
