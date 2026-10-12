"""Tests for WhatsApp Messages builder."""

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

    @pytest.mark.parametrize("limit", [9, 101])
    def test_build_list_request_rejects_invalid_limit(self, limit):
        with pytest.raises(ValidationError):
            WhatsAppMessagesBuilder().limit(limit).build_list_request()

    def test_build_list_request_rejects_invalid_page(self):
        with pytest.raises(ValidationError):
            WhatsAppMessagesBuilder().page(0).build_list_request()

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
