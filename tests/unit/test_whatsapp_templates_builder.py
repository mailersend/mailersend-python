"""Tests for WhatsApp Templates builder."""

import pytest
from pydantic import ValidationError

from mailersend.builders.whatsapp_templates import WhatsAppTemplatesBuilder
from mailersend.models.whatsapp_templates import (
    WhatsAppTemplatesListRequest,
    WhatsAppTemplateGetRequest,
    WhatsAppTemplateStatus,
    WhatsAppTemplateCategory,
)


class TestWhatsAppTemplatesBuilder:
    """Test WhatsAppTemplatesBuilder."""

    def test_build_list_request_defaults(self):
        request = WhatsAppTemplatesBuilder().build_list_request()

        assert isinstance(request, WhatsAppTemplatesListRequest)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.to_query_params() == {}

    def test_build_list_request_with_all_params(self):
        request = (
            WhatsAppTemplatesBuilder()
            .whatsapp_account_id("whatsapp-account-id")
            .status(WhatsAppTemplateStatus.APPROVED)
            .category(WhatsAppTemplateCategory.UTILITY)
            .language("en_US")
            .page(2)
            .limit(50)
            .build_list_request()
        )

        assert request.to_query_params() == {
            "whatsapp_account_id": "whatsapp-account-id",
            "status": "approved",
            "category": "UTILITY",
            "language": "en_US",
            "page": 2,
            "limit": 50,
        }

    @pytest.mark.parametrize("status", list(WhatsAppTemplateStatus))
    def test_build_list_request_with_each_status(self, status):
        request = WhatsAppTemplatesBuilder().status(status).build_list_request()

        assert request.to_query_params() == {"status": status.value}

    @pytest.mark.parametrize("category", list(WhatsAppTemplateCategory))
    def test_build_list_request_with_each_category(self, category):
        request = WhatsAppTemplatesBuilder().category(category).build_list_request()

        assert request.to_query_params() == {"category": category.value}

    def test_build_list_request_accepts_string_values(self):
        request = (
            WhatsAppTemplatesBuilder()
            .status("in_appeal")
            .category("MARKETING")
            .build_list_request()
        )

        assert request.to_query_params() == {
            "status": "in_appeal",
            "category": "MARKETING",
        }

    def test_build_list_request_rejects_unknown_status(self):
        with pytest.raises(ValidationError):
            WhatsAppTemplatesBuilder().status("live").build_list_request()

    def test_build_list_request_rejects_lowercase_category(self):
        with pytest.raises(ValidationError):
            WhatsAppTemplatesBuilder().category("utility").build_list_request()

    def test_build_list_request_rejects_long_language(self):
        with pytest.raises(ValidationError):
            WhatsAppTemplatesBuilder().language("x" * 21).build_list_request()

    @pytest.mark.parametrize("limit", [1, 100])
    def test_build_list_request_accepts_limit_bounds(self, limit):
        request = WhatsAppTemplatesBuilder().limit(limit).build_list_request()

        assert request.query_params.limit == limit

    @pytest.mark.parametrize("limit", [0, 101])
    def test_build_list_request_rejects_invalid_limit(self, limit):
        with pytest.raises(ValidationError):
            WhatsAppTemplatesBuilder().limit(limit).build_list_request()

    @pytest.mark.parametrize("page", [0, 101])
    def test_build_list_request_rejects_invalid_page(self, page):
        with pytest.raises(ValidationError):
            WhatsAppTemplatesBuilder().page(page).build_list_request()

    def test_build_get_request(self):
        request = (
            WhatsAppTemplatesBuilder()
            .whatsapp_template_id(" template-id ")
            .build_get_request()
        )

        assert isinstance(request, WhatsAppTemplateGetRequest)
        assert request.whatsapp_template_id == "template-id"

    def test_build_get_request_requires_id(self):
        with pytest.raises(ValueError, match="WhatsApp template ID is required"):
            WhatsAppTemplatesBuilder().build_get_request()

    def test_build_get_request_rejects_blank_id(self):
        with pytest.raises(ValidationError):
            WhatsAppTemplatesBuilder().whatsapp_template_id("   ").build_get_request()
