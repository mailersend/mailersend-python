import requests
from mailersend.base import base


class NewEmail(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewEmail, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def set_mail_from(self, mail_from, message):
        message["from"] = mail_from

    def set_mail_to(self, mail_to, message):
        message["to"] = mail_to

    def set_subject(self, subject, message):
        message["subject"] = subject

    def set_html_content(self, content, message):
        message["html"] = content

    def set_plaintext_content(self, text, message):
        message["text"] = text

    def set_template(self, template_id, message):
        message["template_id"] = template_id

    def set_simple_personalization(self, personalization, message):
        message["variables"] = personalization

    def set_advanced_personalization(self, personalization, message):
        message["personalization"] = personalization

    def set_cc_recipients(self, cc, message):
        message["cc"] = cc

    def set_bcc_recipients(self, bcc, message):
        message["bcc"] = bcc

    def set_tags(self, tags, message):
        message["tags"] = tags

    def set_attachments(self, attachments, message):
        message["attachments"] = attachments

    def send(self, message):
        request = requests.post(
            f"{self.api_base}/email", headers=self.headers_default, json=message
        )
        return f"{request.status_code}\n{request.text}"
