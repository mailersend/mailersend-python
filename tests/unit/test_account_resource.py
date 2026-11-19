"""Tests for Account resource."""

import inspect
import json

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from mailersend.models.account import Account
from mailersend.models.base import APIResponse
from mailersend.resources.account import AccountResource

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


async def resolve(result):
    if inspect.iscoroutine(result):
        return await result
    return result


class TestAccountResource:
    @pytest.fixture(autouse=True, params=["sync", "async"])
    def setup(self, request):
        http_response = MagicMock(
            status_code=200,
            headers={"x-request-id": "test-req-id"},
            json=MagicMock(return_value=ACCOUNT_RESPONSE),
            content=json.dumps(ACCOUNT_RESPONSE).encode(),
        )
        self.mock_client = MagicMock()
        if request.param == "async":
            self.mock_client.request = AsyncMock(return_value=http_response)
        else:
            self.mock_client.request = Mock(return_value=http_response)
        self.resource = AccountResource(self.mock_client)

    async def test_get_account_calls_correct_endpoint(self):
        await resolve(self.resource.get_account())

        self.mock_client.request.assert_called_once_with(method="GET", path="account")

    async def test_get_account_returns_api_response(self):
        result = await resolve(self.resource.get_account())

        assert isinstance(result, APIResponse)
        assert result.status_code == 200
        assert result.request_id == "test-req-id"
        assert result.data == ACCOUNT_RESPONSE

    async def test_get_account_response_parses_into_account_model(self):
        result = await resolve(self.resource.get_account())

        account = Account(**result.data["data"])

        assert account.name == "Acme Inc"
        assert account.emails.limit == -1
        assert account.resources.free_accountant_seat.used == 0
        assert account.resources.free_accountant_seat.limit == 0
        assert account.addons.whatsapp.sent == 800
