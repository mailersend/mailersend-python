import pytest
from datetime import datetime

from mailersend.builders.email import EmailsBuilder
from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.email import EmailsListRequest, EmailGetRequest
from pydantic import ValidationError


def _base_builder():
    """Builder with only the required list parameters set."""
    return (
        EmailsBuilder()
        .domain_id("test-domain")
        .date_from(1672574400)
        .date_to(1672660800)
    )


class TestEmailsBuilder:
    """Test cases for EmailsBuilder list requests."""

    def test_basic_builder_creation(self):
        """Test basic builder instantiation."""
        builder = EmailsBuilder()
        assert builder is not None

    def test_domain_id_setting(self):
        """Test setting domain ID."""
        builder = EmailsBuilder()
        result = builder.domain_id("test-domain")

        assert result is builder  # Should return self for chaining
        request = builder.date_from(1672574400).date_to(1672660800).build_list_request()
        assert request.query_params.domain_id == "test-domain"

    def test_date_from_timestamp(self):
        """Test setting date_from with a timestamp."""
        builder = EmailsBuilder()
        result = builder.date_from(1672574400)

        assert result is builder
        request = builder.domain_id("test").date_to(1672660800).build_list_request()
        assert request.query_params.date_from == 1672574400

    def test_date_from_datetime(self):
        """Test setting date_from with datetime."""
        builder = EmailsBuilder()
        test_date = datetime(2023, 1, 1, 12, 0, 0)
        result = builder.date_from(test_date)

        assert result is builder
        request = builder.domain_id("test").date_to(1972660800).build_list_request()
        assert request.query_params.date_from == int(test_date.timestamp())

    def test_date_to_timestamp(self):
        """Test setting date_to with a timestamp."""
        builder = EmailsBuilder()
        result = builder.date_to(1672660800)

        assert result is builder
        request = builder.domain_id("test").date_from(1672574400).build_list_request()
        assert request.query_params.date_to == 1672660800

    def test_date_to_datetime(self):
        """Test setting date_to with datetime."""
        builder = EmailsBuilder()
        test_date = datetime(2023, 1, 2, 12, 0, 0)
        result = builder.date_to(test_date)

        assert result is builder
        request = builder.domain_id("test").date_from(1000000000).build_list_request()
        assert request.query_params.date_to == int(test_date.timestamp())

    def test_date_strings_are_passed_through(self):
        """Test that datetime strings are forwarded unchanged."""
        request = (
            EmailsBuilder()
            .domain_id("test")
            .date_from("2026-08-01 00:00:00")
            .date_to("2026-08-27 00:00:00")
            .build_list_request()
        )

        assert request.query_params.date_from == "2026-08-01 00:00:00"
        assert request.query_params.date_to == "2026-08-27 00:00:00"

    def test_page_setting(self):
        """Test setting page number."""
        builder = EmailsBuilder()
        result = builder.page(2)

        assert result is builder
        request = _base_builder_with(builder).build_list_request()
        assert request.query_params.page == 2

    def test_limit_setting(self):
        """Test setting limit."""
        builder = EmailsBuilder()
        result = builder.limit(50)

        assert result is builder
        request = _base_builder_with(builder).build_list_request()
        assert request.query_params.limit == 50

    def test_required_params_are_emitted(self):
        """Test that the required parameters end up in the query params."""
        params = (
            _base_builder().page(3).limit(50).build_list_request().to_query_params()
        )

        assert params["domain_id"] == "test-domain"
        assert params["date_from"] == 1672574400
        assert params["date_to"] == 1672660800
        assert params["page"] == 3
        assert params["limit"] == 50

    def test_unset_page_and_limit_are_omitted(self):
        """Test that page and limit are omitted when never set on the builder."""
        params = _base_builder().build_list_request().to_query_params()

        assert "page" not in params
        assert "limit" not in params
        assert params == {
            "domain_id": "test-domain",
            "date_from": 1672574400,
            "date_to": 1672660800,
        }

    def test_single_status_string(self):
        """Test setting a single status as a string."""
        builder = EmailsBuilder()
        result = builder.status("sent")

        assert result is builder
        request = _base_builder_with(builder).build_list_request()
        assert request.query_params.status == ["sent"]

    def test_status_list(self):
        """Test setting multiple statuses as a list."""
        request = _base_builder().status(["sent", "delivered"]).build_list_request()
        assert request.query_params.status == ["sent", "delivered"]

    def test_status_replaces_previous_values(self):
        """Test that status() replaces any previously set values."""
        request = (
            _base_builder()
            .status(["sent", "delivered"])
            .status("queued")
            .build_list_request()
        )
        assert request.query_params.status == ["queued"]

    def test_add_status_appends(self):
        """Test that add_status appends to the status filter."""
        request = (
            _base_builder()
            .status("sent")
            .add_status("delivered")
            .add_status("queued")
            .build_list_request()
        )
        assert request.query_params.status == ["sent", "delivered", "queued"]

    def test_add_status_ignores_duplicates(self):
        """Test that duplicate statuses are ignored."""
        request = (
            _base_builder()
            .add_status("sent")
            .add_status("sent")
            .add_status("delivered")
            .build_list_request()
        )
        assert request.query_params.status == ["sent", "delivered"]

    def test_add_status_without_status_call(self):
        """Test that add_status works as the only status setter."""
        request = _base_builder().add_status("rejected").build_list_request()
        assert request.query_params.status == ["rejected"]

    def test_empty_status_becomes_none(self):
        """Test that an unset status filter becomes None."""
        request = _base_builder().build_list_request()
        assert request.query_params.status is None

    def test_single_interaction_string(self):
        """Test setting a single interaction as a string."""
        builder = EmailsBuilder()
        result = builder.interaction("opened")

        assert result is builder
        request = _base_builder_with(builder).build_list_request()
        assert request.query_params.interaction == ["opened"]

    def test_interaction_list(self):
        """Test setting multiple interactions as a list."""
        request = (
            _base_builder().interaction(["opened", "clicked"]).build_list_request()
        )
        assert request.query_params.interaction == ["opened", "clicked"]

    def test_interaction_replaces_previous_values(self):
        """Test that interaction() replaces any previously set values."""
        request = (
            _base_builder()
            .interaction(["opened", "clicked"])
            .interaction("no_interaction")
            .build_list_request()
        )
        assert request.query_params.interaction == ["no_interaction"]

    def test_add_interaction_appends(self):
        """Test that add_interaction appends to the interaction filter."""
        request = (
            _base_builder()
            .interaction("opened")
            .add_interaction("clicked")
            .add_interaction("complained")
            .build_list_request()
        )
        assert request.query_params.interaction == [
            "opened",
            "clicked",
            "complained",
        ]

    def test_add_interaction_ignores_duplicates(self):
        """Test that duplicate interactions are ignored."""
        request = (
            _base_builder()
            .add_interaction("opened")
            .add_interaction("opened")
            .add_interaction("clicked")
            .build_list_request()
        )
        assert request.query_params.interaction == ["opened", "clicked"]

    def test_empty_interaction_becomes_none(self):
        """Test that an unset interaction filter becomes None."""
        request = _base_builder().build_list_request()
        assert request.query_params.interaction is None

    def test_status_serialized_as_indexed_array_params(self):
        """Test that status is serialized as status[0], status[1], not comma-joined."""
        params = (
            _base_builder()
            .status(["sent", "delivered"])
            .build_list_request()
            .to_query_params()
        )

        assert params["status[0]"] == "sent"
        assert params["status[1]"] == "delivered"
        # A scalar `status` is rejected by the API with a 422
        assert "status" not in params
        assert "sent,delivered" not in params.values()

    def test_interaction_serialized_as_indexed_array_params(self):
        """Test that interaction is serialized as interaction[0], interaction[1]."""
        params = (
            _base_builder()
            .interaction(["opened", "clicked"])
            .build_list_request()
            .to_query_params()
        )

        assert params["interaction[0]"] == "opened"
        assert params["interaction[1]"] == "clicked"
        assert "interaction" not in params
        assert "opened,clicked" not in params.values()

    def test_single_status_is_still_an_indexed_array_param(self):
        """Test that even a single status value is sent as an indexed array param."""
        params = _base_builder().status("sent").build_list_request().to_query_params()

        assert params["status[0]"] == "sent"
        assert "status" not in params

    def test_single_interaction_is_still_an_indexed_array_param(self):
        """Test that even a single interaction value is sent as an indexed array."""
        params = (
            _base_builder().interaction("opened").build_list_request().to_query_params()
        )

        assert params["interaction[0]"] == "opened"
        assert "interaction" not in params

    def test_all_statuses_serialized_in_order(self):
        """Test that every documented status is serialized in order."""
        params = (
            _base_builder()
            .status(["queued", "sent", "rejected", "delivered"])
            .build_list_request()
            .to_query_params()
        )

        assert params["status[0]"] == "queued"
        assert params["status[1]"] == "sent"
        assert params["status[2]"] == "rejected"
        assert params["status[3]"] == "delivered"

    def test_all_interactions_serialized_in_order(self):
        """Test that every documented interaction is serialized in order."""
        params = (
            _base_builder()
            .interaction(
                [
                    "opened",
                    "clicked",
                    "unsubscribed",
                    "complained",
                    "no_interaction",
                ]
            )
            .build_list_request()
            .to_query_params()
        )

        assert params["interaction[0]"] == "opened"
        assert params["interaction[1]"] == "clicked"
        assert params["interaction[2]"] == "unsubscribed"
        assert params["interaction[3]"] == "complained"
        assert params["interaction[4]"] == "no_interaction"

    def test_recipient_email_setting(self):
        """Test setting the recipient email filter."""
        builder = EmailsBuilder()
        result = builder.recipient_email("rcpt@example.org")

        assert result is builder
        params = _base_builder_with(builder).build_list_request().to_query_params()
        assert params["recipient_email"] == "rcpt@example.org"

    def test_message_id_setting(self):
        """Test setting the message ID filter."""
        builder = EmailsBuilder()
        result = builder.message_id("6a8fa9b1902fab56e0ce50aa")

        assert result is builder
        params = _base_builder_with(builder).build_list_request().to_query_params()
        assert params["message_id"] == "6a8fa9b1902fab56e0ce50aa"

    def test_template_id_setting(self):
        """Test setting the template ID filter."""
        builder = EmailsBuilder()
        result = builder.template_id("7nxe3yjmeq28vp0k")

        assert result is builder
        params = _base_builder_with(builder).build_list_request().to_query_params()
        assert params["template_id"] == "7nxe3yjmeq28vp0k"

    def test_subject_setting(self):
        """Test setting the subject filter."""
        builder = EmailsBuilder()
        result = builder.subject("Welcome")

        assert result is builder
        params = _base_builder_with(builder).build_list_request().to_query_params()
        assert params["subject"] == "Welcome"

    def test_tag_setting(self):
        """Test setting the tag filter."""
        builder = EmailsBuilder()
        result = builder.tag("newsletter")

        assert result is builder
        params = _base_builder_with(builder).build_list_request().to_query_params()
        assert params["tag"] == "newsletter"

    def test_unset_filters_are_omitted(self):
        """Test that unset optional filters are not sent."""
        params = _base_builder().build_list_request().to_query_params()

        for key in (
            "recipient_email",
            "message_id",
            "template_id",
            "subject",
            "tag",
        ):
            assert key not in params

    def test_method_chaining(self):
        """Test method chaining works correctly."""
        builder = EmailsBuilder()
        result = (
            builder.domain_id("test-domain")
            .date_from(1672574400)
            .date_to(1672660800)
            .page(2)
            .limit(50)
            .status("sent")
            .add_status("delivered")
            .interaction("opened")
            .recipient_email("rcpt@example.org")
            .message_id("6a8fa9b1902fab56e0ce50aa")
            .template_id("7nxe3yjmeq28vp0k")
            .subject("Welcome")
            .tag("newsletter")
        )

        assert result is builder
        params = builder.build_list_request().to_query_params()
        assert params == {
            "domain_id": "test-domain",
            "date_from": 1672574400,
            "date_to": 1672660800,
            "page": 2,
            "limit": 50,
            "status[0]": "sent",
            "status[1]": "delivered",
            "interaction[0]": "opened",
            "recipient_email": "rcpt@example.org",
            "message_id": "6a8fa9b1902fab56e0ce50aa",
            "template_id": "7nxe3yjmeq28vp0k",
            "subject": "Welcome",
            "tag": "newsletter",
        }

    def test_copy_builder(self):
        """Test copying a builder."""
        original = _base_builder().page(2).status("sent").interaction("opened")

        copy = original.copy()

        copy_params = copy.build_list_request().to_query_params()
        original_params = original.build_list_request().to_query_params()
        assert copy_params == original_params

        # Verify they are independent
        copy.domain_id("different-domain")
        assert original.build_list_request().query_params.domain_id == "test-domain"
        assert copy.build_list_request().query_params.domain_id == "different-domain"

    def test_copy_builder_does_not_share_lists(self):
        """Test that copies get their own status and interaction lists."""
        original = _base_builder().status("sent").interaction("opened")

        copy = original.copy()
        copy.add_status("delivered").add_interaction("clicked")

        assert original.build_list_request().query_params.status == ["sent"]
        assert original.build_list_request().query_params.interaction == ["opened"]
        assert copy.build_list_request().query_params.status == [
            "sent",
            "delivered",
        ]
        assert copy.build_list_request().query_params.interaction == [
            "opened",
            "clicked",
        ]

    def test_copy_builder_carries_email_id(self):
        """Test that copy also carries the single email ID."""
        original = EmailsBuilder().email_id("email-id")
        copy = original.copy()

        assert copy.build_get_request().email_id == "email-id"

    def test_reset_builder(self):
        """Test resetting a builder."""
        builder = (
            _base_builder()
            .page(2)
            .limit(50)
            .status("sent")
            .interaction("opened")
            .recipient_email("rcpt@example.org")
            .message_id("6a8fa9b1902fab56e0ce50aa")
            .template_id("7nxe3yjmeq28vp0k")
            .subject("Welcome")
            .tag("newsletter")
            .email_id("email-id")
        )

        # Verify builder has values
        assert builder.build_list_request().query_params.page == 2

        result = builder.reset()
        assert result is builder

        # After reset we cannot build without the required fields,
        # so check the internal state
        assert builder._domain_id is None
        assert builder._date_from is None
        assert builder._date_to is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._status == []
        assert builder._interaction == []
        assert builder._recipient_email is None
        assert builder._message_id is None
        assert builder._template_id is None
        assert builder._subject is None
        assert builder._tag is None
        assert builder._email_id is None

    def test_reset_allows_rebuilding(self):
        """Test that a reset builder can be reused."""
        builder = _base_builder().status("sent")
        builder.reset()

        params = (
            builder.domain_id("other-domain")
            .date_from(1672574400)
            .date_to(1672660800)
            .build_list_request()
            .to_query_params()
        )

        assert params == {
            "domain_id": "other-domain",
            "date_from": 1672574400,
            "date_to": 1672660800,
        }

    def test_build_list_request_returns_emails_list_request(self):
        """Test that build_list_request returns an EmailsListRequest instance."""
        request = _base_builder().build_list_request()
        assert isinstance(request, EmailsListRequest)


class TestEmailsBuilderGetRequest:
    """Test cases for EmailsBuilder single email requests."""

    def test_email_id_setting(self):
        """Test setting the email ID."""
        builder = EmailsBuilder()
        result = builder.email_id("6a8fa9b1902fab56e0ce50dd")

        assert result is builder  # Should return self for chaining
        request = builder.build_get_request()
        assert request.email_id == "6a8fa9b1902fab56e0ce50dd"

    def test_build_get_request_returns_email_get_request(self):
        """Test that build_get_request returns an EmailGetRequest instance."""
        request = EmailsBuilder().email_id("email-id").build_get_request()
        assert isinstance(request, EmailGetRequest)

    def test_build_get_request_without_email_id_raises_error(self):
        """Test that building without email_id raises ValidationError."""
        builder = EmailsBuilder()

        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_get_request()

        assert "email_id is required" in str(exc_info.value)

    def test_build_get_request_with_empty_email_id_raises_error(self):
        """Test that an empty email_id raises ValidationError."""
        builder = EmailsBuilder().email_id("")

        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_get_request()

        assert "email_id is required" in str(exc_info.value)

    def test_get_request_ignores_list_params(self):
        """Test that a get request only needs the email ID."""
        request = (
            EmailsBuilder().email_id("email-id").status("sent").build_get_request()
        )
        assert request.email_id == "email-id"


class TestEmailsBuilderValidation:
    """Validation test cases for EmailsBuilder list requests."""

    def test_build_list_request_without_domain_id_raises_error(self):
        """Test that a missing domain_id raises ValidationError."""
        builder = EmailsBuilder().date_from(1672574400).date_to(1672660800)

        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_list_request()

        assert "domain_id is required" in str(exc_info.value)

    def test_build_list_request_without_date_from_raises_error(self):
        """Test that a missing date_from raises ValidationError."""
        builder = EmailsBuilder().domain_id("test").date_to(1672660800)

        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_list_request()

        assert "date_from is required" in str(exc_info.value)

    def test_build_list_request_without_date_to_raises_error(self):
        """Test that a missing date_to raises ValidationError."""
        builder = EmailsBuilder().domain_id("test").date_from(1672574400)

        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_list_request()

        assert "date_to is required" in str(exc_info.value)

    def test_empty_domain_id_raises_error(self):
        """Test that an empty domain_id raises ValidationError."""
        builder = EmailsBuilder().domain_id("").date_from(1).date_to(2)

        with pytest.raises(MailerSendValidationError) as exc_info:
            builder.build_list_request()

        assert "domain_id is required" in str(exc_info.value)

    @pytest.mark.parametrize("page", [0, 101])
    def test_invalid_page_raises_error(self, page):
        """Test that a page outside 1..100 raises an error."""
        with pytest.raises(ValidationError):
            _base_builder().page(page).build_list_request()

    @pytest.mark.parametrize("page", [1, 100])
    def test_valid_page_boundaries(self, page):
        """Test that the page boundaries are accepted."""
        request = _base_builder().page(page).build_list_request()
        assert request.query_params.page == page

    @pytest.mark.parametrize("limit", [9, 1001])
    def test_invalid_limit_raises_error(self, limit):
        """Test that a limit outside 10..1000 raises an error."""
        with pytest.raises(ValidationError):
            _base_builder().limit(limit).build_list_request()

    @pytest.mark.parametrize("limit", [10, 1000])
    def test_valid_limit_boundaries(self, limit):
        """Test that the limit boundaries are accepted."""
        request = _base_builder().limit(limit).build_list_request()
        assert request.query_params.limit == limit

    def test_short_subject_raises_error(self):
        """Test that a subject under 3 characters raises an error."""
        with pytest.raises(ValidationError):
            _base_builder().subject("ab").build_list_request()

    def test_three_character_subject_is_valid(self):
        """Test that a 3-character subject is accepted."""
        request = _base_builder().subject("abc").build_list_request()
        assert request.query_params.subject == "abc"

    def test_non_alphanumeric_message_id_raises_error(self):
        """Test that a non-alphanumeric message_id raises an error."""
        with pytest.raises(ValidationError, match="message_id must be alphanumeric"):
            _base_builder().message_id("6a8fa9b1-902f").build_list_request()

    def test_invalid_recipient_email_raises_error(self):
        """Test that an invalid recipient email raises an error."""
        with pytest.raises(ValidationError):
            _base_builder().recipient_email("not-an-email").build_list_request()

    def test_invalid_status_raises_error(self):
        """Test that an unknown status value raises an error."""
        with pytest.raises(ValidationError, match="Invalid status values"):
            _base_builder().status(["sent", "bounced"]).build_list_request()

    def test_invalid_added_status_raises_error(self):
        """Test that an unknown status added via add_status raises an error."""
        with pytest.raises(ValidationError, match="Invalid status values"):
            _base_builder().add_status("opened").build_list_request()

    def test_invalid_interaction_raises_error(self):
        """Test that an unknown interaction value raises an error."""
        with pytest.raises(ValidationError, match="Invalid interaction values"):
            _base_builder().interaction(["opened", "bounced"]).build_list_request()

    def test_invalid_added_interaction_raises_error(self):
        """Test that an unknown interaction via add_interaction raises an error."""
        with pytest.raises(ValidationError, match="Invalid interaction values"):
            _base_builder().add_interaction("sent").build_list_request()

    def test_date_to_equal_to_date_from_raises_error(self):
        """Test that date_to equal to date_from raises an error."""
        with pytest.raises(
            ValidationError, match="date_to must be greater than date_from"
        ):
            EmailsBuilder().domain_id("test").date_from(1672574400).date_to(
                1672574400
            ).build_list_request()

    def test_date_to_before_date_from_raises_error(self):
        """Test that date_to earlier than date_from raises an error."""
        with pytest.raises(
            ValidationError, match="date_to must be greater than date_from"
        ):
            EmailsBuilder().domain_id("test").date_from(1672660800).date_to(
                1672574400
            ).build_list_request()


def _base_builder_with(builder: EmailsBuilder) -> EmailsBuilder:
    """Add the required list parameters to an existing builder."""
    return builder.domain_id("test").date_from(1672574400).date_to(1672660800)
