import requests
from mailersend.base import base

message = {}


class NewEmail(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewEmail, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def setMailFrom(self, mail_from, message):
        message["from"] = mail_from

    def setMailTo(self, mail_to, message):
        message["to"] = mail_to

    def setSubject(self, subject, message):
        message["subject"] = subject

    def setHTMLContent(self, content, message):
        message["html"] = content

    def setPlaintextContent(self, text, message):
        message["text"] = text

    def setTemplate(self, template_id, message):
        message["template_id"] = template_id

    def setSimplePersonalization(self, personalization, message):
        message["variables"] = personalization

    def setAdvancedPersonalization(self, personalization, message):
        message["personalization"] = personalization

    def setCCRecipients(self, cc, message):
        message["cc"] = cc

    def setBCCRecipients(self, bcc, message):
        message["bcc"] = bcc

    def setTags(self, tags, message):
        message["tags"] = tags

    def setAttachments(self, attachments, message):
        message["attachments"] = attachments

    def send(self, message):
        request = requests.post(
            f"{self.api_base}/email", headers=self.headers_default, json=message
        )
        return f"{request.status_code}\n{request.text}"
