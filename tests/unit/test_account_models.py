"""Tests for Account models."""

import copy

import pytest
from pydantic import ValidationError

from mailersend.models.account import (
    Account,
    AccountAddons,
    AccountResourceUsage,
    AccountWhatsAppAddon,
)

ACCOUNT_RESPONSE = {
    "data": {
        "name": "Acme Inc",
        "status": "approved",
        "plan_type": "starter",
        "data_retention_days": 7,
        "emails": {"sent": 12000, "received": 430, "limit": -1},
        "rate_limits": {"general": 60, "email": 120, "bulk_email": 10, "activity": 10},
        "resources": {
            "domains": {"used": 3, "limit": 10},
            "users": {"used": 2, "limit": 5},
            "free_accountant_seat": {"used": 0, "limit": 0},
            "templates": {"used": 41, "limit": 250},
            "smtp_users": {"used": 1, "limit": 50},
            "api_tokens": {"used": 4, "limit": 50},
            "webhooks": {"used": 2, "limit": 50},
        },
        "addons": {
            "sms": {"sent": 120, "received": 30, "limit": -1},
            "whatsapp": {"sent": 800, "limit": 1000},
            "phone_numbers": 1,
            "domain_spaces": 2,
            "data_retention_days": 30,
            "dedicated_ips": 0,
        },
    }
}


def account_data():
    return copy.deepcopy(ACCOUNT_RESPONSE["data"])


class TestAccount:
    def test_parses_full_response(self):
        account = Account(**account_data())

        assert account.name == "Acme Inc"
        assert account.status == "approved"
        assert account.plan_type == "starter"
        assert account.data_retention_days == 7
        assert account.emails.sent == 12000
        assert account.emails.received == 430
        assert account.emails.limit == -1
        assert account.rate_limits.general == 60
        assert account.rate_limits.email == 120
        assert account.rate_limits.bulk_email == 10
        assert account.rate_limits.activity == 10
        assert account.resources.domains == AccountResourceUsage(used=3, limit=10)
        assert account.resources.users == AccountResourceUsage(used=2, limit=5)
        assert account.resources.templates == AccountResourceUsage(used=41, limit=250)
        assert account.resources.smtp_users == AccountResourceUsage(used=1, limit=50)
        assert account.resources.api_tokens == AccountResourceUsage(used=4, limit=50)
        assert account.resources.webhooks == AccountResourceUsage(used=2, limit=50)
        assert account.addons.sms.sent == 120
        assert account.addons.sms.received == 30
        assert account.addons.sms.limit == -1
        assert account.addons.whatsapp == AccountWhatsAppAddon(sent=800, limit=1000)
        assert account.addons.phone_numbers == 1
        assert account.addons.domain_spaces == 2
        assert account.addons.data_retention_days == 30
        assert account.addons.dedicated_ips == 0

    def test_parses_free_accountant_seat(self):
        data = account_data()
        data["resources"]["free_accountant_seat"] = {"used": 1, "limit": 1}

        account = Account(**data)

        assert account.resources.free_accountant_seat == AccountResourceUsage(
            used=1, limit=1
        )

    def test_free_accountant_seat_is_required(self):
        data = account_data()
        del data["resources"]["free_accountant_seat"]

        with pytest.raises(ValidationError):
            Account(**data)

    def test_whatsapp_addon_can_be_none(self):
        data = account_data()
        data["addons"]["whatsapp"] = None

        account = Account(**data)

        assert account.addons.whatsapp is None

    def test_webhooks_limit_can_be_none(self):
        data = account_data()
        data["resources"]["webhooks"]["limit"] = None

        account = Account(**data)

        assert account.resources.webhooks.limit is None
        assert account.resources.webhooks.used == 2

    def test_from_api(self):
        account = Account.from_api(account_data())

        assert isinstance(account.addons, AccountAddons)
        assert account.addons.sms.limit == -1
