"""
Handles /recipients endpoint
Doc: https://developers.mailersend.com/api/v1/recipients.html
"""

import requests
from mailersend.base import base


class NewRecipient(base.NewAPIClient):
    """
    Instantiates the /recipients endpoint object
    """

    pass

    def get_recipients(self):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.get(
            f"{self.api_base}/recipients", headers=self.headers_default
        )
        return request.text

    def get_recipient_by_id(self, recipient_id):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.get(
            f"{self.api_base}/recipients/{recipient_id}", headers=self.headers_default
        )
        return request.text

    def delete_recipient(self, recipient_id):
        """
        Returns a HTTP status code from the MailerSend API
        """

        request = requests.delete(
            f"{self.api_base}/recipients/{recipient_id}", headers=self.headers_default
        )
        return request.status_code

    def get_recipients_from_blocklist(self, domain_id=None, limit=None, page=None):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}
        message["domain_id"] = domain_id
        message["limit"] = limit
        message["page"] = page

        request = requests.get(
            f"{self.api_base}/suppressions/blocklist",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def get_hard_bounces(self, domain_id=None, limit=None, page=None):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}
        message["domain_id"] = domain_id
        message["limit"] = limit
        message["page"] = page

        request = requests.get(
            f"{self.api_base}/suppressions/hard_bounces",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def get_spam_complaints(self, domain_id=None, limit=None, page=None):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}
        message["domain_id"] = domain_id
        message["limit"] = limit
        message["page"] = page

        request = requests.get(
            f"{self.api_base}/suppressions/spam-complaints",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def get_unsubscribes(self, domain_id=None, limit=None, page=None):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}
        message["domain_id"] = domain_id
        message["limit"] = limit
        message["page"] = page

        request = requests.get(
            f"{self.api_base}/suppressions/unsubscribes",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def add_to_blocklist(self, domain_id, recipients=None, patterns=None):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}
        message["domain_id"] = domain_id

        if recipients is not None:
            message["recipients"] = recipients
        if patterns is not None:
            message["patterns"] = patterns

        request = requests.post(
            f"{self.api_base}/suppressions/blocklist",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def delete_from_blocklist(self, ids=None, remove_all=False):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}

        if ids is not None:
            message["ids"] = ids
        if remove_all is True:
            message["all"] = "true"

        request = requests.delete(
            f"{self.api_base}/suppressions/blocklist",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def add_hard_bounces(self, domain_id=None, recipients=None):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}
        message["domain_id"] = domain_id

        if recipients is not None:
            message["recipients"] = recipients

        request = requests.post(
            f"{self.api_base}/suppressions/hard-bounces",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def delete_hard_bounces(self, ids=None, remove_all=False):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}

        if ids is not None:
            message["ids"] = ids
        if remove_all is True:
            message["all"] = "true"

        request = requests.delete(
            f"{self.api_base}/suppressions/hard-bounces",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def add_spam_complaints(self, domain_id=None, recipients=None):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}
        message["domain_id"] = domain_id

        if recipients is not None:
            message["recipients"] = recipients

        request = requests.post(
            f"{self.api_base}/suppressions/spam-complaints",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def delete_spam_complaints(self, ids=None, remove_all=False):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}

        if ids is not None:
            message["ids"] = ids
        if remove_all is True:
            message["all"] = "true"

        request = requests.delete(
            f"{self.api_base}/suppressions/spam-complaints",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def add_unsubscribes(self, domain_id=None, recipients=None):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}
        message["domain_id"] = domain_id

        if recipients is not None:
            message["recipients"] = recipients

        request = requests.post(
            f"{self.api_base}/suppressions/unsubscribes",
            headers=self.headers_default,
            json=message,
        )
        return request.text

    def delete_unsubscribes(self, ids=None, remove_all=False):
        """
        Returns a HTTP status code from the MailerSend API
        """
        message = {}

        if ids is not None:
            message["ids"] = ids
        if remove_all is True:
            message["all"] = True

        request = requests.delete(
            f"{self.api_base}/suppressions/unsubscribes",
            headers=self.headers_default,
            json=message,
        )
        return request.text
