"""
Handles /email endpoint
Doc: https://developers.mailersend.com/api/v1/email.html
"""

import requests
from mailersend.base import base


class NewEmail(base.NewAPIClient):
    """
    Send an e-mail
    """

    pass

    def set_mail_from(self, mail_from, message):
        """
        Appends the 'from' part on an e-mail
        """
        message["from"] = mail_from

    def set_mail_to(self, mail_to, message):
        """
        Appends the 'to' part on an e-mail
        """
        message["to"] = mail_to

    def set_subject(self, subject, message):
        """
        Appends the 'subject' part on an e-mail
        """
        message["subject"] = subject

    def set_html_content(self, content, message):
        """
        Appends the HTML content of an e-mail
        """
        message["html"] = content

    def set_plaintext_content(self, text, message):
        """
        Appends the plaintext content of an e-mail
        """
        message["text"] = text

    def set_template(self, template_id, message):
        """
        Appends the 'template_id' part on an e-mail
        """
        message["template_id"] = template_id

    def set_simple_personalization(self, personalization, message):
        """
        Handles simple personalization
        """
        message["variables"] = personalization

    def set_advanced_personalization(self, personalization, message):
        """
        Handles advanced personalization
        """
        message["personalization"] = personalization

    def set_cc_recipients(self, cc_recipient, message):
        """
        Appends the 'cc' part on an e-mail
        """
        message["cc"] = cc_recipient

    def set_bcc_recipients(self, bcc_recipient, message):
        """
        Appends the 'bcc' part on an e-mail
        """
        message["bcc"] = bcc_recipient

    def set_tags(self, tags, message):
        """
        Handles e-mail tags
        """
        message["tags"] = tags

    def set_attachments(self, attachments, message):
        """
        Appends an attachment on an e-mail
        """
        message["attachments"] = attachments

    def set_reply_to(self, reply_to, message):
        """
        Appends 'reply to' on an e-mail
        """
        message["reply_to"] = reply_to

    def send(self, message):
        """
        Handles e-mail sending

        @params:
          message (dict): A dict containing required parameters for mail sending
        """

        request = requests.post(
            f"{self.api_base}/email", headers=self.headers_default, json=message
        )
        return f"{request.status_code}\n{request.text}"
