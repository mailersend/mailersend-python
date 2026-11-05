"""Models for Account API."""

from typing import Optional

from .base import BaseModel


class AccountEmails(BaseModel):
    """Email usage of the account."""

    sent: int
    received: int
    limit: int


class AccountRateLimits(BaseModel):
    """Requests per minute allowed for each rate limit group."""

    general: int
    email: int
    bulk_email: int
    activity: int


class AccountResourceUsage(BaseModel):
    """Usage of a single account resource."""

    used: int
    limit: Optional[int] = None


class AccountResources(BaseModel):
    """Usage of the account resources."""

    domains: AccountResourceUsage
    users: AccountResourceUsage
    free_accountant_seat: AccountResourceUsage
    templates: AccountResourceUsage
    smtp_users: AccountResourceUsage
    api_tokens: AccountResourceUsage
    webhooks: AccountResourceUsage


class AccountSmsAddon(BaseModel):
    """SMS add-on usage."""

    sent: int
    received: int
    limit: int


class AccountWhatsAppAddon(BaseModel):
    """WhatsApp add-on usage."""

    sent: int
    limit: int


class AccountAddons(BaseModel):
    """Add-ons of the account."""

    sms: AccountSmsAddon
    whatsapp: Optional[AccountWhatsAppAddon] = None
    phone_numbers: int
    domain_spaces: int
    data_retention_days: int
    dedicated_ips: int


class Account(BaseModel):
    """Account behind the API token."""

    name: str
    status: str
    plan_type: str
    data_retention_days: int
    emails: AccountEmails
    rate_limits: AccountRateLimits
    resources: AccountResources
    addons: AccountAddons
