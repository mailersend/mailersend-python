import os
import requests
import json

API_BASE = "https://api.mailersend.com/v1"
class NewApiClient():

    def __init__(
        self,
        api_base = API_BASE,
        headers_default = None,
        headers_auth = None,
        mailersend_api_key = None):

        self.mailersend_api_key = os.environ.get("MAILERSEND_API_KEY")
        self.headers_auth = 'Bearer {}'.format(self.mailersend_api_key)
        self.headers_default = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "MailerSend-Client-python-v1",
            "Authorization": self.headers_auth
        }

        super(NewApiClient, self).__init__()
    
    def getMessageById(self, messageId):
        self.messageId = messageId

        request = requests.get(API_BASE + "/messages/" + messageId, headers = self.headers_default)
        return request.text

    def getMessages(self):
        request = requests.get(API_BASE+ "/messages", headers = self.headers_default)
        return request.text

    def getRecipients(self):
        request = requests.get(API_BASE+ "/recipients", headers = self.headers_default)
        return request.text

    def getRecipientById(self, recipientId):
        request = requests.get(API_BASE + "/recipients/" + recipientId, headers = self.headers_default)
        return request.text

    def deleteRecipient(self, recipientId):
        request = requests.delete(API_BASE + "/recipients/" + recipientId, headers = self.headers_default)
        return request.status_code

    def send(self, mail_from, mail_to, mail_subject, mail_content, mail_text=None):
        
        self.mail_from = {
            "from": {
                "email": mail_from
            }
        }
        
        mail_data = [ { "email": receiver } for receiver in mail_to ]
        self.mail_to = {
            "to": mail_data
        }
        
    
        self.mail_subject = {
            "subject": mail_subject
        }

        self.mail_content = {
                "html": mail_content
            }
        
        self.mail_text = {
            "text": mail_text or "foo"
        }

        message = { **self.mail_from, **self.mail_to, **self.mail_subject, **self.mail_content, **self.mail_text } 

        # print(json.dumps(self.headers_default))
        # print(json.dumps(message))
        
        request = requests.post(API_BASE + "/email", headers = self.headers_default, json=message)
        return request.text

        