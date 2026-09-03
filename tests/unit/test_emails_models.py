import pytest
from pydantic import ValidationError

from mailersend.models.email import (
    EmailActivityEvent,
    EmailHeader,
    EmailListItem,
    EmailsListQueryParams,
    EmailsListRequest,
    EmailGetRequest,
)


# Measured response for a populated page of GET /v1/emails
EMAILS_LIST_RESPONSE = {
    "data": [
        {
            "id": "6a8fa9b1902fab56e0ce50dd",
            "from": "sender@example.com",
            "to": "rcpt@example.org",
            "subject": "Welcome",
            "text": None,
            "html": None,
            "template_id": "7nxe3yjmeq28vp0k",
            "domain_id": "7nxe3yjmeq28vp0k",
            "message_id": "6a8fa9b1902fab56e0ce50aa",
            "status": "sent",
            "tags": ["newsletter"],
            "interaction": ["opened"],
            "suppression_reason": None,
            "created_at": "2026-08-27T16:48:42.000000Z",
            "updated_at": "2026-08-27T16:48:42.000000Z",
            "headers": [{"name": "X-Custom", "value": "foo"}],
        }
    ],
    "links": {
        "first": "https://api.mailersend.com/v1/emails?page=1",
        "last": None,
        "prev": None,
        "next": None,
    },
    "meta": {
        "current_page": 1,
        "current_page_url": "https://api.mailersend.com/v1/emails?page=1",
        "from": 1,
        "path": "https://api.mailersend.com/v1/emails",
        "per_page": 10,
        "to": 3,
    },
}

# Measured response for an empty page of GET /v1/emails
EMAILS_LIST_EMPTY_RESPONSE = {
    "data": [],
    "links": {
        "first": "https://api.mailersend.com/v1/emails?page=1",
        "last": None,
        "prev": "https://api.mailersend.com/v1/emails?page=1",
        "next": None,
    },
    "meta": {
        "current_page": 2,
        "current_page_url": "https://api.mailersend.com/v1/emails?page=2",
        "from": None,
        "path": "https://api.mailersend.com/v1/emails",
        "per_page": 10,
        "to": None,
    },
}

# Measured response for GET /v1/email/{email_id}: the list row plus
# a `recipient` object and an `activity` array
EMAIL_GET_RESPONSE = {
    "data": {
        **EMAILS_LIST_RESPONSE["data"][0],
        "recipient": {
            "id": "6a8fa9b1902fab56e0ce50cc",
            "email": "rcpt@example.org",
            "created_at": "2026-08-27T16:48:42.000000Z",
            "updated_at": "2026-08-27T16:48:42.000000Z",
        },
        "activity": [
            {
                "id": "6a8fa9b1902fab56e0ce50e1",
                "type": "queued",
                "created_at": "2026-08-27T16:48:42.000000Z",
            },
            {
                "id": "6a8fa9b1902fab56e0ce50e2",
                "type": "sent",
                "created_at": "2026-08-27T16:48:43.000000Z",
            },
            {
                "id": "6a8fa9b1902fab56e0ce50e3",
                "type": "opened",
                "created_at": "2026-08-27T16:49:17.000000Z",
            },
        ],
    }
}


class TestEmailActivityEvent:
    def test_valid_event(self):
        event = EmailActivityEvent(
            id="6a8fa9b1902fab56e0ce50e1",
            type="opened",
            created_at="2026-08-27T16:48:42.000000Z",
        )

        assert event.id == "6a8fa9b1902fab56e0ce50e1"
        assert event.type == "opened"
        assert event.created_at == "2026-08-27T16:48:42.000000Z"
        assert event.suppression_reason is None

    def test_event_with_suppression_reason(self):
        event = EmailActivityEvent(
            id="6a8fa9b1902fab56e0ce50e1",
            type="suppressed",
            created_at="2026-08-27T16:48:42.000000Z",
            suppression_reason="hard_bounced",
        )

        assert event.type == "suppressed"
        assert event.suppression_reason == "hard_bounced"

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            EmailActivityEvent()

        errors = exc_info.value.errors()
        required_fields = {"id", "type", "created_at"}
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)

    def test_parses_measured_activity_array(self):
        """Test that the measured activity array parses into events."""
        events = [
            EmailActivityEvent(**event)
            for event in EMAIL_GET_RESPONSE["data"]["activity"]
        ]

        assert len(events) == 3
        assert [event.type for event in events] == ["queued", "sent", "opened"]
        assert all(event.suppression_reason is None for event in events)


class TestEmailListItem:
    def test_parses_measured_row(self):
        """Test that the measured list row parses in full."""
        row = EMAILS_LIST_RESPONSE["data"][0]
        item = EmailListItem(**row)

        assert item.id == "6a8fa9b1902fab56e0ce50dd"
        assert item.from_email == "sender@example.com"
        assert item.to == "rcpt@example.org"
        assert item.subject == "Welcome"
        assert item.text is None
        assert item.html is None
        assert item.template_id == "7nxe3yjmeq28vp0k"
        assert item.domain_id == "7nxe3yjmeq28vp0k"
        assert item.message_id == "6a8fa9b1902fab56e0ce50aa"
        assert item.status == "sent"
        assert item.tags == ["newsletter"]
        assert item.interaction == ["opened"]
        assert item.suppression_reason is None
        assert item.created_at == "2026-08-27T16:48:42.000000Z"
        assert item.updated_at == "2026-08-27T16:48:42.000000Z"

    def test_from_field_is_aliased_to_from_email(self):
        """Test that the response's 'from' key populates from_email."""
        item = EmailListItem(**EMAILS_LIST_RESPONSE["data"][0])

        assert item.from_email == "sender@example.com"

    def test_from_email_can_also_be_populated_by_field_name(self):
        """Test that from_email is accepted by its field name too."""
        row = dict(EMAILS_LIST_RESPONSE["data"][0])
        row.pop("from")
        row["from_email"] = "sender@example.com"

        item = EmailListItem(**row)

        assert item.from_email == "sender@example.com"

    def test_headers_are_parsed_as_objects(self):
        """Test that headers become EmailHeader objects with name and value."""
        item = EmailListItem(**EMAILS_LIST_RESPONSE["data"][0])

        assert len(item.headers) == 1
        assert isinstance(item.headers[0], EmailHeader)
        assert item.headers[0].name == "X-Custom"
        assert item.headers[0].value == "foo"

    def test_missing_headers_defaults_to_none(self):
        """Test that an absent headers key leaves headers as None."""
        row = dict(EMAILS_LIST_RESPONSE["data"][0])
        row.pop("headers")

        item = EmailListItem(**row)

        assert item.headers is None

    def test_empty_interaction_list(self):
        """Test that an email with no interactions parses to an empty list."""
        row = dict(EMAILS_LIST_RESPONSE["data"][0])
        row["interaction"] = []

        item = EmailListItem(**row)

        assert item.interaction == []

    def test_missing_interaction_defaults_to_empty_list(self):
        """Test that an absent interaction key defaults to an empty list."""
        row = dict(EMAILS_LIST_RESPONSE["data"][0])
        row.pop("interaction")

        item = EmailListItem(**row)

        assert item.interaction == []

    def test_rejected_email_with_suppression_reason(self):
        """Test that suppression_reason is retained for rejected emails."""
        row = dict(EMAILS_LIST_RESPONSE["data"][0])
        row["status"] = "rejected"
        row["suppression_reason"] = "hard_bounced"

        item = EmailListItem(**row)

        assert item.status == "rejected"
        assert item.suppression_reason == "hard_bounced"

    def test_optional_fields_default_to_none(self):
        """Test that the optional fields default to None when absent."""
        item = EmailListItem(
            id="6a8fa9b1902fab56e0ce50dd",
            **{"from": "sender@example.com"},
            to="rcpt@example.org",
            subject="Welcome",
            domain_id="7nxe3yjmeq28vp0k",
            message_id="6a8fa9b1902fab56e0ce50aa",
            status="sent",
            created_at="2026-08-27T16:48:42.000000Z",
            updated_at="2026-08-27T16:48:42.000000Z",
        )

        assert item.text is None
        assert item.html is None
        assert item.template_id is None
        assert item.tags is None
        assert item.suppression_reason is None
        assert item.headers is None
        assert item.interaction == []

    def test_content_is_returned_for_a_single_email(self):
        """Test that text and html are parsed when the API returns them."""
        row = dict(EMAILS_LIST_RESPONSE["data"][0])
        row["text"] = "Hello"
        row["html"] = "<p>Hello</p>"

        item = EmailListItem(**row)

        assert item.text == "Hello"
        assert item.html == "<p>Hello</p>"

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            EmailListItem()

        errors = exc_info.value.errors()
        required_fields = {
            "id",
            "from",
            "to",
            "subject",
            "domain_id",
            "message_id",
            "status",
            "created_at",
            "updated_at",
        }
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)

    def test_invalid_from_email(self):
        row = dict(EMAILS_LIST_RESPONSE["data"][0])
        row["from"] = "invalid-email"

        with pytest.raises(ValidationError) as exc_info:
            EmailListItem(**row)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("from",) for error in errors)

    def test_single_email_extra_keys_are_ignored(self):
        """The single email row carries recipient and activity, which have no
        fields on EmailListItem and are dropped rather than rejected."""
        item = EmailListItem(**EMAIL_GET_RESPONSE["data"])

        assert item.id == "6a8fa9b1902fab56e0ce50dd"
        assert not hasattr(item, "recipient")
        assert not hasattr(item, "activity")

    def test_parses_every_row_of_a_measured_page(self):
        items = [EmailListItem(**row) for row in EMAILS_LIST_RESPONSE["data"]]

        assert len(items) == 1
        assert items[0].from_email == "sender@example.com"

    def test_parses_an_empty_measured_page(self):
        items = [EmailListItem(**row) for row in EMAILS_LIST_EMPTY_RESPONSE["data"]]

        assert items == []


class TestEmailsListQueryParams:
    def test_valid_params(self):
        params = EmailsListQueryParams(
            domain_id="7nxe3yjmeq28vp0k",
            date_from=1672574400,
            date_to=1672660800,
            page=2,
            limit=50,
            status=["sent", "delivered"],
            interaction=["opened"],
            recipient_email="rcpt@example.org",
            message_id="6a8fa9b1902fab56e0ce50aa",
            template_id="7nxe3yjmeq28vp0k",
            subject="Welcome",
            tag="newsletter",
        )

        assert params.domain_id == "7nxe3yjmeq28vp0k"
        assert params.date_from == 1672574400
        assert params.date_to == 1672660800
        assert params.page == 2
        assert params.limit == 50
        assert params.status == ["sent", "delivered"]
        assert params.interaction == ["opened"]
        assert params.recipient_email == "rcpt@example.org"
        assert params.message_id == "6a8fa9b1902fab56e0ce50aa"
        assert params.template_id == "7nxe3yjmeq28vp0k"
        assert params.subject == "Welcome"
        assert params.tag == "newsletter"

    def test_default_values(self):
        params = EmailsListQueryParams(
            domain_id="7nxe3yjmeq28vp0k",
            date_from=1672574400,
            date_to=1672660800,
        )

        assert params.page == 1
        assert params.limit == 25
        assert params.status is None
        assert params.interaction is None
        assert params.recipient_email is None
        assert params.message_id is None
        assert params.template_id is None
        assert params.subject is None
        assert params.tag is None

    def test_domain_id_is_stripped(self):
        params = EmailsListQueryParams(
            domain_id="  7nxe3yjmeq28vp0k  ",
            date_from=1672574400,
            date_to=1672660800,
        )

        assert params.domain_id == "7nxe3yjmeq28vp0k"

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            EmailsListQueryParams()

        errors = exc_info.value.errors()
        required_fields = {"domain_id", "date_from", "date_to"}
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)

    @pytest.mark.parametrize("domain_id", ["", "   "])
    def test_empty_domain_id_raises(self, domain_id):
        with pytest.raises(ValidationError, match="domain_id is required"):
            EmailsListQueryParams(
                domain_id=domain_id, date_from=1672574400, date_to=1672660800
            )

    @pytest.mark.parametrize("page", [0, 101])
    def test_page_validation(self, page):
        with pytest.raises(ValidationError):
            EmailsListQueryParams(
                domain_id="domain",
                date_from=1672574400,
                date_to=1672660800,
                page=page,
            )

    @pytest.mark.parametrize("limit", [9, 1001])
    def test_limit_validation(self, limit):
        with pytest.raises(ValidationError):
            EmailsListQueryParams(
                domain_id="domain",
                date_from=1672574400,
                date_to=1672660800,
                limit=limit,
            )

    def test_subject_min_length_validation(self):
        with pytest.raises(ValidationError):
            EmailsListQueryParams(
                domain_id="domain",
                date_from=1672574400,
                date_to=1672660800,
                subject="ab",
            )

    def test_message_id_must_be_alphanumeric(self):
        with pytest.raises(ValidationError, match="message_id must be alphanumeric"):
            EmailsListQueryParams(
                domain_id="domain",
                date_from=1672574400,
                date_to=1672660800,
                message_id="6a8fa9b1-902f",
            )

    def test_status_validation(self):
        params = EmailsListQueryParams(
            domain_id="domain",
            date_from=1672574400,
            date_to=1672660800,
            status=["queued", "sent", "rejected", "delivered"],
        )
        assert params.status == ["queued", "sent", "rejected", "delivered"]

        with pytest.raises(ValidationError, match="Invalid status values"):
            EmailsListQueryParams(
                domain_id="domain",
                date_from=1672574400,
                date_to=1672660800,
                status=["sent", "opened"],
            )

    def test_interaction_validation(self):
        all_interactions = [
            "opened",
            "clicked",
            "unsubscribed",
            "complained",
            "no_interaction",
        ]
        params = EmailsListQueryParams(
            domain_id="domain",
            date_from=1672574400,
            date_to=1672660800,
            interaction=all_interactions,
        )
        assert params.interaction == all_interactions

        with pytest.raises(ValidationError, match="Invalid interaction values"):
            EmailsListQueryParams(
                domain_id="domain",
                date_from=1672574400,
                date_to=1672660800,
                interaction=["opened", "sent"],
            )

    def test_invalid_recipient_email_raises(self):
        with pytest.raises(ValidationError):
            EmailsListQueryParams(
                domain_id="domain",
                date_from=1672574400,
                date_to=1672660800,
                recipient_email="not-an-email",
            )

    def test_date_range_validation(self):
        with pytest.raises(
            ValidationError, match="date_to must be greater than date_from"
        ):
            EmailsListQueryParams(
                domain_id="domain", date_from=1672660800, date_to=1672574400
            )

        with pytest.raises(
            ValidationError, match="date_to must be greater than date_from"
        ):
            EmailsListQueryParams(
                domain_id="domain", date_from=1672574400, date_to=1672574400
            )

    def test_date_range_validation_skipped_for_string_dates(self):
        """Dates given as strings are not comparable and are left to the API."""
        params = EmailsListQueryParams(
            domain_id="domain",
            date_from="2026-08-27 00:00:00",
            date_to="2026-08-01 00:00:00",
        )

        assert params.date_from == "2026-08-27 00:00:00"
        assert params.date_to == "2026-08-01 00:00:00"

    def test_to_query_params(self):
        params = EmailsListQueryParams(
            domain_id="7nxe3yjmeq28vp0k",
            date_from=1672574400,
            date_to=1672660800,
            page=2,
            limit=50,
            status=["sent", "delivered"],
            interaction=["opened", "clicked"],
            recipient_email="rcpt@example.org",
            message_id="6a8fa9b1902fab56e0ce50aa",
            template_id="7nxe3yjmeq28vp0k",
            subject="Welcome",
            tag="newsletter",
        )

        assert params.to_query_params() == {
            "domain_id": "7nxe3yjmeq28vp0k",
            "date_from": 1672574400,
            "date_to": 1672660800,
            "page": 2,
            "limit": 50,
            "status[0]": "sent",
            "status[1]": "delivered",
            "interaction[0]": "opened",
            "interaction[1]": "clicked",
            "recipient_email": "rcpt@example.org",
            "message_id": "6a8fa9b1902fab56e0ce50aa",
            "template_id": "7nxe3yjmeq28vp0k",
            "subject": "Welcome",
            "tag": "newsletter",
        }

    def test_to_query_params_minimal(self):
        params = EmailsListQueryParams(
            domain_id="7nxe3yjmeq28vp0k",
            date_from=1672574400,
            date_to=1672660800,
        )

        assert params.to_query_params() == {
            "domain_id": "7nxe3yjmeq28vp0k",
            "date_from": 1672574400,
            "date_to": 1672660800,
            "page": 1,
            "limit": 25,
        }

    def test_to_query_params_omits_none_values(self):
        params = EmailsListQueryParams(
            domain_id="7nxe3yjmeq28vp0k",
            date_from=1672574400,
            date_to=1672660800,
            page=None,
            limit=None,
        )

        assert params.to_query_params() == {
            "domain_id": "7nxe3yjmeq28vp0k",
            "date_from": 1672574400,
            "date_to": 1672660800,
        }

    def test_status_is_serialized_as_indexed_array_params(self):
        """status must be sent as status[0], status[1] — never comma-joined,
        which the API rejects with a 422."""
        params = EmailsListQueryParams(
            domain_id="domain",
            date_from=1672574400,
            date_to=1672660800,
            status=["queued", "sent", "rejected", "delivered"],
        )

        query_params = params.to_query_params()

        assert query_params["status[0]"] == "queued"
        assert query_params["status[1]"] == "sent"
        assert query_params["status[2]"] == "rejected"
        assert query_params["status[3]"] == "delivered"
        assert "status" not in query_params
        assert not any(
            isinstance(value, str) and "," in value for value in query_params.values()
        )

    def test_interaction_is_serialized_as_indexed_array_params(self):
        """interaction must be sent as interaction[0], interaction[1], ..."""
        params = EmailsListQueryParams(
            domain_id="domain",
            date_from=1672574400,
            date_to=1672660800,
            interaction=["opened", "clicked", "no_interaction"],
        )

        query_params = params.to_query_params()

        assert query_params["interaction[0]"] == "opened"
        assert query_params["interaction[1]"] == "clicked"
        assert query_params["interaction[2]"] == "no_interaction"
        assert "interaction" not in query_params

    def test_empty_status_and_interaction_lists_are_omitted(self):
        params = EmailsListQueryParams(
            domain_id="domain",
            date_from=1672574400,
            date_to=1672660800,
            status=[],
            interaction=[],
        )

        query_params = params.to_query_params()

        assert "status" not in query_params
        assert "status[0]" not in query_params
        assert "interaction" not in query_params
        assert "interaction[0]" not in query_params


class TestEmailsListRequest:
    def test_valid_request(self):
        query_params = EmailsListQueryParams(
            domain_id="7nxe3yjmeq28vp0k",
            date_from=1672574400,
            date_to=1672660800,
        )

        request = EmailsListRequest(query_params=query_params)

        assert request.query_params == query_params

    def test_to_query_params_delegates_to_query_params(self):
        query_params = EmailsListQueryParams(
            domain_id="7nxe3yjmeq28vp0k",
            date_from=1672574400,
            date_to=1672660800,
            status=["sent"],
        )

        request = EmailsListRequest(query_params=query_params)

        assert request.to_query_params() == query_params.to_query_params()
        assert request.to_query_params()["status[0]"] == "sent"

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            EmailsListRequest()

        errors = exc_info.value.errors()
        error_fields = {error["loc"][0] for error in errors}
        assert {"query_params"}.issubset(error_fields)


class TestEmailGetRequest:
    def test_valid_email_id(self):
        request = EmailGetRequest(email_id="6a8fa9b1902fab56e0ce50dd")

        assert request.email_id == "6a8fa9b1902fab56e0ce50dd"

    def test_email_id_with_whitespace(self):
        request = EmailGetRequest(email_id="  6a8fa9b1902fab56e0ce50dd  ")

        assert request.email_id == "6a8fa9b1902fab56e0ce50dd"

    def test_empty_email_id(self):
        with pytest.raises(ValueError) as exc_info:
            EmailGetRequest(email_id="")

        assert "email_id is required" in str(exc_info.value)

    def test_whitespace_only_email_id(self):
        with pytest.raises(ValueError) as exc_info:
            EmailGetRequest(email_id="   ")

        assert "email_id is required" in str(exc_info.value)

    def test_none_email_id(self):
        with pytest.raises(ValueError):
            EmailGetRequest(email_id=None)

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            EmailGetRequest()

        errors = exc_info.value.errors()
        error_fields = {error["loc"][0] for error in errors}
        assert {"email_id"}.issubset(error_fields)
