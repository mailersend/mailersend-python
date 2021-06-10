"""
MailerSend Official Python DSK
@maintainer: Alexandros Orfanos (alexandros at remotecompany dot com)
"""
import json
import os

import requests

API_BASE = "https://api.mailersend.com/v1"

# initiate empty dict - this will fill up with e-mail info
message = {}


class NewApiClient:
    def __init__(
        self,
        api_base=API_BASE,
        headers_default=None,
        headers_auth=None,
        mailersend_api_key=None,
    ):

        self.mailersend_api_key = os.environ.get("MAILERSEND_API_KEY")
        self.headers_auth = f"Bearer {self.mailersend_api_key}"
        self.headers_default = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "MailerSend-Client-python-v1",
            "Authorization": f"{self.headers_auth}",
        }

        super(NewApiClient, self).__init__()

    def _generateConfigChangeBody(self, key, value):
        self.key = key
        self.value = value

        data = {key: value}

        return data

    def createToken(self, tokenName, tokenScopes):
        self.tokenName = tokenName
        self.tokenScopes = tokenScopes

        _data = {"name": tokenName, "scopes": tokenScopes}

        request = requests.post(
            f"{API_BASE}/token", headers=self.headers_default, json=_data
        )
        return request.text

    def freezeToken(self, tokenId, pause=True):
        self.tokenId = tokenId
        self.pause = pause

        if pause == True:
            _data = self._generateConfigChangeBody("status", "pause")
        else:
            _data = self._generateConfigChangeBody("status", "unpause")

        request = requests.put(
            f"{API_BASE}/token/{tokenId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def deleteToken(self, tokenId):
        self.tokenId = tokenId

        request = requests.delete(
            f"{API_BASE}/token/{token_id}/", headers=self.headers_default
        )
        return request.status_code

    def getActivityByDate(self, domainId, dateFrom, dateTo, groupBy, event):
        self.domainId = domainId
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.groupBy = groupBy
        self.event = event

        _data = {
            "date_from": dateFrom,
            "date_to": dateTo,
            "event": event,
        }

        if domainId is not None:
            _data["domain_id"] = domainId

        if groupBy is not None:
            _data["group_by"] = groupBy

        request = requests.get(
            f"{API_BASE}/analytics/date", headers=self.headers_default, json=_data
        )

        return print(request.text)

    def getDomainActivity(
        self, domainId, page=None, limit=None, dateFrom=None, dateTo=None, event=None
    ):
        self.domainId = domainId
        self.page = page
        self.limit = limit
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.event = event

        _data = {
            "page": page or None,
            "limit": limit or None,
            "dateFrom": dateFrom or None,
            "dateTo": dateTo or None,
            "event": event or None,
        }

        request = requests.get(
            f"{API_BASE}/activity/{domainId}", headers=self.headers_default, json=_data
        )
        return request.text

    def getDomains(self):
        request = requests.get(f"{API_BASE}/domains", headers=self.headers_default)
        return request.text

    def deleteDomain(self, domainId):
        self.domainId = domainId

        request = requests.delete(
            f"{API_BASE}/domains/{domainId}", headers=self.headers_default
        )
        return request.status_code

    def getDomainById(self, domainId):
        self.domainId = domainId

        request = requests.get(
            f"{API_BASE}/domains/{domainId}", headers=self.headers_default
        )
        return request.text

    def getIdByName(self, category, name):
        self.category = category
        self.name = name

        request = requests.get(f"{API_BASE}/{category}", headers=self.headers_default)

        _json_req = request.json()

        category_search_asset = {"recipients": "email", "domains": "name"}

        _data_block = _json_req["data"]

        for data in _data_block:
            if data[category_search_asset.get(category)] == name:
                return data["id"]
            else:
                raise ValueError("Not found")

        return request.text

    def getMessageById(self, messageId):
        self.messageId = messageId

        request = requests.get(
            f"{API_BASE}/messages/{messageId}", headers=self.headers_default
        )
        return request.text

    def getMessages(self):
        request = requests.get(f"{API_BASE}/messages", headers=self.headers_default)
        return request.text

    def getRecipients(self):
        request = requests.get(f"{API_BASE}/recipients", headers=self.headers_default)
        return request.text

    def getRecipientById(self, recipientId):
        self.recipientId = recipientId
        request = requests.get(
            f"{API_BASE}/recipients/{recipientId}", headers=self.headers_default
        )
        return request.text

    def getRecipientsForDomain(self, domainId):
        self.domainId = domainId

        request = requests.get(
            f"{API_BASE}/domains/{domainId}/recipients",
            headers=self.headers_default,
        )
        return print(request.text)

    def deleteRecipient(self, recipientId):
        self.recipientId = recipientId
        request = requests.delete(
            f"{API_BASE}/recipients/{recipientId}", headers=self.headers_default
        )
        return request.status_code

    def sendPaused(self, domainId, enable=True):
        self.domainId = domainId
        self.enable = enable
        _data = self._generateConfigChangeBody("send_paused", enable)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def trackClicks(self, domainId, enable=True):
        self.domainId = domainId
        self.enable = enable
        _data = self._generateConfigChangeBody("track_clicks", enable)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def trackOpens(self, domainId, enable=True):
        self.domainId = domainId
        self.enable = enable
        _data = self._generateConfigChangeBody("track_opens", enable)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def trackUnsubscribe(self, domainId, enable=True):
        self.domainId = domainId
        self.enable = enable
        _data = self._generateConfigChangeBody("track_unsubscribe", enable)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def trackUnsubscribeHtml(self, domainId, html):
        self.domainId = domainId
        self.html = html
        _data = self._generateConfigChangeBody("track_unsubscribe_html", html)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def trackUnsubscribePlain(self, domainId, plaintext):
        self.domainId = domainId
        self.plaintext = plaintext
        _data = self._generateConfigChangeBody("track_unsubscribe_plain", plaintext)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def trackContent(self, domainId, enable=True):
        self.domainId = domainId
        self.enable = enable
        _data = self._generateConfigChangeBody("track_content", enable)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def customTracking(self, domainId, enable=True):
        self.domainId = domainId
        self.enable = enable
        _data = self._generateConfigChangeBody("custom_tracking_enabled", enable)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def setCustomTrackingSubdomain(self, domainId, subdomain):
        self.domainId = domainId
        self.subdomain = subdomain
        _data = self._generateConfigChangeBody("custom_tracking_subdomain", subdomain)
        request = requests.put(
            f"{API_BASE}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def send(
        self,
        mail_from,
        mail_to,
        mail_subject,
        mail_content,
        mail_text=None,
        template_id=None,
        variables=None,
    ):

        self.mail_from = {"from": {"email": mail_from}}

        mail_data = [{"email": receiver} for receiver in mail_to]
        self.mail_to = {"to": mail_data}

        self.mail_subject = {"subject": mail_subject}

        self.mail_content = {"html": mail_content}

        self.mail_text = {"text": mail_text or None}

        self.template_id = {"template_id": template_id}

        message["from"] = {"email": mail_from}
        message["to"] = mail_data
        message["subject"] = mail_subject

        if template_id is None:
            message["html"] = mail_content or None
            message["text"] = mail_text or None
        else:
            message["template_id"] = template_id

        if variables is None:
            pass
        else:
            message["variables"] = variables

        request = requests.post(
            f"{API_BASE}/email", headers=self.headers_default, json=message
        )
        return print(request.status_code)
